import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader, X, Minimize2, Maximize2 } from 'lucide-react';
import axios from 'axios';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const Chatbot = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hi! I'm your AI Learning Assistant powered by Groq AI. I can help you with:\n\n• Course recommendations\n• Learning tips and strategies\n• Answering questions about any topic\n• Study guidance and motivation\n• Platform navigation\n\nAsk me anything - I'm here to help you succeed! 🚀",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateBotResponse = async (userMessage: string): Promise<string> => {
    try {
      // Call backend AI chat endpoint
      const token = localStorage.getItem('token');
      
      // Build conversation history for context
      const conversationHistory = messages.slice(-5).map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      }));
      
      const response = await axios.post(
        '/api/v1/ai/chat',
        {
          message: userMessage,
          conversation_history: conversationHistory
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      return response.data.response;
    } catch (error) {
      console.error('AI chat error:', error);
      
      // Fallback to keyword-based responses if API fails
      const lowerMessage = userMessage.toLowerCase();

      if (lowerMessage.includes('course') || lowerMessage.includes('recommend')) {
        return "I recommend starting with our beginner-friendly courses! Based on your interests, you might enjoy:\n\n• Web Development Fundamentals\n• Data Science Basics\n• Python Programming\n\nWould you like me to help you enroll in any of these?";
      }

      if (lowerMessage.includes('help') || lowerMessage.includes('how')) {
        return "I'm here to help! You can:\n\n1. Browse courses in the Library\n2. Track your progress in My Learning\n3. Use AI Tutor Lab for personalized learning\n4. Take quizzes to test your knowledge\n\nWhat would you like to know more about?";
      }

      return "I'm having trouble connecting to my AI brain right now. Please try asking your question again! 🤖";
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Simulate thinking delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const botResponseText = await generateBotResponse(inputMessage);
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: botResponseText,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error generating response:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, I'm having trouble responding right now. Please try again in a moment.",
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: '1',
        text: "Chat cleared! I'm ready to help you with anything. What would you like to know? 🤖",
        sender: 'bot',
        timestamp: new Date()
      }
    ]);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-2rem)] max-w-5xl mx-auto">
      {/* Header */}
      <div className="glass-card mb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center">
            <Bot className="text-primary" size={24} />
          </div>
          <div>
            <h2 className="text-2xl font-bold">AI Learning Assistant</h2>
            <p className="text-white/60 text-sm">Ask me anything about your learning journey</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setIsMinimized(!isMinimized)}
            className="p-2 rounded-lg hover:bg-white/5 transition-colors"
            title={isMinimized ? "Maximize" : "Minimize"}
          >
            {isMinimized ? <Maximize2 size={20} /> : <Minimize2 size={20} />}
          </button>
          <button
            onClick={clearChat}
            className="p-2 rounded-lg hover:bg-white/5 transition-colors text-red-400"
            title="Clear chat"
          >
            <X size={20} />
          </button>
        </div>
      </div>

      {!isMinimized && (
        <>
          {/* Messages Area */}
          <div className="flex-1 glass-card overflow-y-auto mb-4 p-6 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
              >
                {/* Avatar */}
                <div className={`flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center ${
                  message.sender === 'bot' 
                    ? 'bg-primary/20 text-primary' 
                    : 'bg-white/10 text-white'
                }`}>
                  {message.sender === 'bot' ? <Bot size={20} /> : <User size={20} />}
                </div>

                {/* Message Bubble */}
                <div className={`flex-1 max-w-[70%] ${message.sender === 'user' ? 'text-right' : 'text-left'}`}>
                  <div className={`inline-block p-4 rounded-2xl ${
                    message.sender === 'bot'
                      ? 'bg-white/5 text-white'
                      : 'bg-primary/20 text-white'
                  }`}>
                    <p className="whitespace-pre-wrap break-words">{message.text}</p>
                  </div>
                  <p className="text-xs text-white/40 mt-1 px-2">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            ))}

            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
                  <Bot className="text-primary" size={20} />
                </div>
                <div className="bg-white/5 p-4 rounded-2xl">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="glass-card p-4">
            <div className="flex gap-3">
              <input
                ref={inputRef}
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/40 focus:outline-none focus:border-primary/50 transition-colors"
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isLoading}
                className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isLoading ? (
                  <Loader className="animate-spin" size={20} />
                ) : (
                  <>
                    <Send size={20} />
                    <span className="hidden sm:inline">Send</span>
                  </>
                )}
              </button>
            </div>
            <p className="text-xs text-white/40 mt-2 text-center">
              Press Enter to send • Shift + Enter for new line
            </p>
          </div>
        </>
      )}

      {isMinimized && (
        <div className="glass-card p-8 text-center">
          <Bot className="text-primary mx-auto mb-4" size={48} />
          <p className="text-white/60">Chat minimized. Click maximize to continue.</p>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
