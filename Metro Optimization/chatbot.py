import os
import sys
import random
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Workaround for Python 3.14 venv blocking global packages
user_site = os.path.join(os.getenv('APPDATA', ''), 'Python', 'Python314', 'site-packages')
if user_site not in sys.path:
    sys.path.append(user_site)

from database import db, ChatMessage

try:
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    LANGCHAIN_GROQ_AVAILABLE = True
except ImportError:
    LANGCHAIN_GROQ_AVAILABLE = False

class MetroChatbot:
    """AI-powered chatbot for metro passenger assistance using Groq and LangChain"""
    
    def __init__(self):
        # Initialize Groq LLM chain if package and API key are available
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.chain = None
        
        if LANGCHAIN_GROQ_AVAILABLE and self.api_key:
            try:
                llm = ChatGroq(
                    temperature=0.5, 
                    model_name="llama-3.1-8b-instant",  # Updated to current supported model
                    groq_api_key=self.api_key
                )
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are the official customer AI Assistant for 'Metro Optimized', the Bangalore Metro service. "
                               "You help passengers with route, fare, schedule, KYC, and general queries. "
                               "The lines are Green, Purple, Yellow, Red, and Blue. Operating hours are 5:30 AM to 11:30 PM. "
                               "Contact: +91-80-2363-2363. email: support@metrooptimized.com. "
                               "Provide brief, polite, and exact answers. Keep responses primarily raw text or lightly formatted "
                               "so they look good in a generic chat window."),
                    ("human", "{user_input}")
                ])
                self.chain = prompt | llm | StrOutputParser()
                logging.info("Groq LangChain initialized successfully!")
            except Exception as e:
                logging.error(f"Error initializing Groq: {e}")
                
        # Fallback rule-based responses
        self.responses = {
            'greeting': [
                "Hello! 👋 Welcome to Bangalore Metro Assistant. How can I help you today?",
                "Hi there! I'm here to help with your metro journey. What do you need?",
                "Welcome to Metro Optimized! Ask me about routes, fares, or schedules.",
            ],
            'fare': [
                "To check fares, please select your starting and destination stations. I can provide the exact fare.",
                "Our fares depend on the distance traveled. Select your journey route for pricing.",
            ],
            'schedule': [
                "Metro trains run from 5:30 AM to 11:30 PM with trains every 3-5 minutes during peak hours.",
                "Schedules vary by line. Which metro line are you interested in?",
            ],
            'contact': [
                "You can reach us at: +91-80-2363-2363 or email: support@metrooptimized.com",
                "Visit our website at metrooptimized.com for more information.",
            ],
            'kyc': [
                "KYC (Know Your Customer) verification is required for certain card types. Upload your ID through your account settings.",
                "Complete your KYC process in Settings → Card Management → KYC Verification.",
            ],
            'recharge': [
                "You can recharge your metro card through: 1) Mobile App 2) Website 3) Ticket counters at major stations",
                "Visit Card Management section to recharge online instantly!",
            ],
            'lines': [
                "We have 5 metro lines: Green Line, Purple Line, Yellow Line, Red Line, and Blue Line. Each serves different areas of Bangalore.",
                "Which line would you like to know more about?",
            ],
            'help': [
                "I can help with: 1) Fare calculations 2) Route suggestions 3) Schedule info 4) KYC verification 5) Card recharge",
                "Feel free to ask about any metro services!",
            ],
        }
    
    def get_response(self, user_message, user_id=None):
        """Generate chatbot response based on user input"""
        
        # 1. Try using Groq AI first
        if self.chain:
            try:
                ai_response = self.chain.invoke({"user_input": user_message})
                return ai_response
            except Exception as e:
                logging.error(f"Groq API Error: {e}")
                # If AI fails, proceed to rule-based fallback
                pass
                
        # 2. Inform the user if the AI is not configured but they want it
        if not self.api_key and "ai" in user_message.lower():
            return "Note: For advanced AI responses, please set the GROQ_API_KEY environment variable. I am currently running in rule-based mode."

        # 3. Rule-based fallback keyword matching
        message_lower = user_message.lower()
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'greet']):
            return random.choice(self.responses['greeting'])
        elif any(word in message_lower for word in ['fare', 'price', 'cost', 'ticket']):
            return random.choice(self.responses['fare'])
        elif any(word in message_lower for word in ['schedule', 'time', 'train', 'frequency']):
            return random.choice(self.responses['schedule'])
        elif any(word in message_lower for word in ['contact', 'call', 'email', 'support']):
            return random.choice(self.responses['contact'])
        elif any(word in message_lower for word in ['kyc', 'verification', 'document']):
            return random.choice(self.responses['kyc'])
        elif any(word in message_lower for word in ['recharge', 'balance', 'add money']):
            return random.choice(self.responses['recharge'])
        elif any(word in message_lower for word in ['line', 'route', 'green', 'purple', 'yellow', 'red', 'blue']):
            return random.choice(self.responses['lines'])
        elif any(word in message_lower for word in ['help', 'assist', 'what can you']):
            return random.choice(self.responses['help'])
        else:
            return "I'm here to help with metro-related queries. Try asking about routes, fares, schedules, or KYC verification!"
    
    def save_message(self, user_id, message_type, content):
        """Save chat message to database"""
        message = ChatMessage(
            user_id=user_id,
            message_type=message_type,
            content=content
        )
        db.session.add(message)
        db.session.commit()
        return message
    
    def get_chat_history(self, user_id, limit=20):
        """Retrieve chat history for user"""
        return ChatMessage.query.filter_by(user_id=user_id).order_by(
            ChatMessage.timestamp.desc()
        ).limit(limit).all()[::-1]
