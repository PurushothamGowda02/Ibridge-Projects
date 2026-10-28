"""AI Core - LangChain-based processing engine for command interpretation and response generation"""

from typing import Dict, Any, Optional, List
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
try:
    from langchain_huggingface import HuggingFacePipeline
    HUGGINGFACE_PIPELINE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_PIPELINE_AVAILABLE = False
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
import re


class AICore:
    """
    AI Core processing engine that uses LangChain to interpret commands,
    manage conversation context, and generate intelligent responses.
    """
    
    def __init__(
        self,
        llm_config: Dict[str, Any],
        memory_system: Any,
        task_executor: Any
    ):
        """
        Initialize the AI Core with LLM configuration and component references.
        
        Args:
            llm_config: Dictionary containing LLM provider, model, and settings
            memory_system: MemorySystem instance for conversation and fact storage
            task_executor: TaskExecutor instance for executing system tasks
        """
        self.llm_config = llm_config
        self.memory_system = memory_system
        self.task_executor = task_executor
        self.llm = None
        self.conversation_history: List[Any] = []
        
        # Initialize LLM
        self.initialize_llm()
        
        # Create prompt template
        self.create_agent_chain()
    
    def initialize_llm(self) -> None:
        """
        Initialize the LLM based on the configured provider.
        
        Supports:
        - OpenAI (GPT models)
        - HuggingFace (various models)
        - Local models (LLaMA via llama-cpp-python)
        
        Raises:
            ValueError: If provider is unsupported or configuration is invalid
            RuntimeError: If LLM initialization fails
        """
        provider = self.llm_config.get('provider')
        model = self.llm_config.get('model')
        
        if not provider:
            raise ValueError("LLM provider not specified in configuration")
        
        if not model:
            raise ValueError("LLM model not specified in configuration")
        
        try:
            if provider == 'openai':
                self._initialize_openai()
            elif provider == 'huggingface':
                self._initialize_huggingface()
            elif provider == 'groq':
                self._initialize_groq()
            elif provider == 'local':
                self._initialize_local()
            else:
                raise ValueError(f"Unsupported LLM provider: {provider}")
        
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {str(e)}")
    
    def _initialize_openai(self) -> None:
        """Initialize OpenAI LLM."""
        api_key = self.llm_config.get('api_key')
        model = self.llm_config.get('model', 'gpt-3.5-turbo')
        temperature = self.llm_config.get('temperature', 0.7)
        
        if not api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=api_key
        )
    
    def _initialize_huggingface(self) -> None:
        """Initialize HuggingFace LLM using Inference API."""
        import os
        
        # Use a capable instruction-following model via HuggingFace Inference API
        api_key = self.llm_config.get('api_key') or os.getenv('HUGGINGFACE_API_KEY')
        temperature = self.llm_config.get('temperature', 0.7)
        max_tokens = self.llm_config.get('max_tokens', 512)
        
        # Use HuggingFace Inference API with a strong free model
        # mistralai/Mistral-7B-Instruct-v0.3 gives GPT-3.5 quality answers for free
        inference_model = "mistralai/Mistral-7B-Instruct-v0.3"
        
        try:
            from langchain_huggingface import HuggingFaceEndpoint
            
            print(f"Connecting to HuggingFace Inference API: {inference_model}")
            
            self.llm = HuggingFaceEndpoint(
                repo_id=inference_model,
                huggingfacehub_api_token=api_key,
                max_new_tokens=max_tokens,
                temperature=temperature,
                task="text-generation",
            )
            
            # Store that we're using the inference API
            self.llm_config['_inference_api'] = True
            self.llm_config['_inference_model'] = inference_model
            
            print(f"✅ HuggingFace Inference API ready! Model: {inference_model}")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR connecting to HuggingFace Inference API:\n{error_details}")
            raise RuntimeError(f"Failed to connect to HuggingFace Inference API: {str(e)}")
    
    def _initialize_groq(self) -> None:
        """Initialize Groq LLM."""
        api_key = self.llm_config.get('api_key')
        model = self.llm_config.get('model', 'llama-3.3-70b-versatile')
        temperature = self.llm_config.get('temperature', 0.7)

        if not api_key:
            raise ValueError("Groq API key not provided")

        if not GROQ_AVAILABLE:
            raise RuntimeError(
                "langchain-groq is not installed. Run: pip install langchain-groq"
            )

        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            groq_api_key=api_key
        )

    def _initialize_local(self) -> None:
        """Initialize local LLM (Ollama or LLaMA)."""
        model = self.llm_config.get('model', 'llama3.2:3b')
        temperature = self.llm_config.get('temperature', 0.7)
        max_tokens = self.llm_config.get('max_tokens', 512)
        
        # Try Ollama first (recommended for local models)
        try:
            from langchain_community.llms import Ollama
            
            self.llm = Ollama(
                model=model,
                temperature=temperature,
                num_predict=max_tokens,
            )
            return
        except ImportError:
            pass  # Try LlamaCpp next
        except Exception as e:
            # Ollama might not be installed or running
            pass
        
        # Fallback to LlamaCpp
        try:
            from langchain_community.llms import LlamaCpp
        except ImportError:
            raise RuntimeError(
                "No local LLM backend available. "
                "Install Ollama (https://ollama.com) or llama-cpp-python"
            )
        
        model_path = self.llm_config.get('model_path')
        if not model_path:
            raise ValueError("Local model path not specified for LlamaCpp")
        
        self.llm = LlamaCpp(
            model_path=model_path,
            temperature=temperature,
            max_tokens=max_tokens,
            n_ctx=2048
        )
    
    def create_agent_chain(self) -> None:
        """
        Create prompt template for the LLM.
        
        Sets up system prompt that describes available tools and capabilities.
        """
        self.system_prompt = """You are RAJIV, an intelligent virtual assistant. You are helpful, intelligent, and professional.

You can help users with:
- Answering any questions about any topic (science, technology, history, etc.)
- Explaining concepts and providing detailed information
- Having natural conversations
- Telling the current time and date
- Performing calculations
- Opening applications
- System administration tasks

When users ask questions:
- Provide clear, accurate, and helpful answers
- Be conversational and engaging
- Use your knowledge to explain topics thoroughly
- If you don't know something, say so honestly
- Maintain a professional but friendly personality

For system tasks (time, calculations, apps), use the appropriate tools.
For general questions, provide comprehensive answers using your knowledge.

Always be helpful, accurate, and maintain a professional, intelligent personality."""
    
    def _detect_and_execute_tool(self, user_input: str) -> Optional[str]:
        """
        Detect if user input requires a tool and execute it.
        
        Args:
            user_input: The user's command
        
        Returns:
            Tool result if a tool was executed, None otherwise
        """
        user_input_lower = user_input.lower()
        
        # Check for time request
        if any(phrase in user_input_lower for phrase in ['what time', 'current time', 'time is it']):
            try:
                time = self.task_executor.get_current_time()
                return f"The current time is {time}."
            except Exception as e:
                return f"I couldn't get the time: {str(e)}"
        
        # Check for date request
        if any(phrase in user_input_lower for phrase in ['what date', 'current date', 'date today', "today's date"]):
            try:
                date = self.task_executor.get_current_date()
                return f"Today's date is {date}."
            except Exception as e:
                return f"I couldn't get the date: {str(e)}"
        
        # Check for calculation request
        calc_patterns = [
            r'calculate\s+(.+)',
            r'what is\s+(\d+[\+\-\*/]\d+.*)',
            r'compute\s+(.+)',
            r'solve\s+(.+)'
        ]
        for pattern in calc_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                expression = match.group(1).strip()
                try:
                    result = self.task_executor.calculate(expression)
                    return f"The result is {result}."
                except Exception as e:
                    return f"I couldn't calculate that: {str(e)}"
        
        # Check for app opening request - improved patterns
        open_patterns = [
            r'open\s+(\w+)',
            r'launch\s+(\w+)',
            r'start\s+(\w+)',
            r'run\s+(\w+)',
            r'execute\s+(\w+)',
            r'can you open\s+(\w+)',
            r'please open\s+(\w+)',
            r'i want to open\s+(\w+)',
        ]
        for pattern in open_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                app_name = match.group(1)
                try:
                    result = self.task_executor.open_application(app_name)
                    return result['message']
                except Exception as e:
                    return f"I couldn't open the application: {str(e)}"
        
        return None
    
    def process_command(self, user_input: str) -> str:
        """
        Process a user command and generate a response.
        
        This method:
        1. Checks if a tool needs to be executed
        2. Retrieves relevant context from memory
        3. Passes the command to the LLM
        4. Stores the conversation in memory
        5. Returns the generated response
        
        Args:
            user_input: The user's command or question
        
        Returns:
            The assistant's response string
        
        Raises:
            ValueError: If user_input is empty
            RuntimeError: If LLM processing fails
        """
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty")
        
        user_input = user_input.strip()
        
        try:
            # First, check if this requires a tool execution
            tool_result = self._detect_and_execute_tool(user_input)
            if tool_result:
                # Store conversation in memory if available
                if self.memory_system:
                    try:
                        self.memory_system.store_conversation(
                            user_input=user_input,
                            assistant_response=tool_result,
                            metadata={}
                        )
                    except Exception as e:
                        print(f"Warning: Failed to store in memory: {e}")
                return tool_result
            
            # Retrieve relevant memories for context
            relevant_memories = []
            if self.memory_system:
                try:
                    relevant_memories = self.memory_system.retrieve_relevant_memories(
                        query=user_input,
                        k=3
                    )
                except Exception as e:
                    print(f"Warning: Failed to retrieve memories: {e}")
            
            # Build context from memories
            context_parts = []
            for memory, score in relevant_memories:
                if hasattr(memory, 'user_input'):
                    # It's a conversation entry
                    context_parts.append(
                        f"Previous: User said '{memory.user_input}', "
                        f"Assistant replied '{memory.assistant_response}'"
                    )
                elif hasattr(memory, 'content'):
                    # It's a fact
                    context_parts.append(f"Known fact: {memory.content}")
            
            # Build messages for the LLM
            messages = [SystemMessage(content=self.system_prompt)]
            
            # Add context if available
            if context_parts:
                context_str = "\n".join(context_parts)
                messages.append(SystemMessage(content=f"Relevant context:\n{context_str}"))
            
            # Add conversation history (last 5 exchanges)
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # Add current user input
            messages.append(HumanMessage(content=user_input))
            
            # Get response from LLM
            # Check if LLM supports chat format (OpenAI) or needs plain text (HuggingFace)
            if hasattr(self.llm, 'invoke') and self.llm_config.get('provider') in ('openai', 'groq'):
                response = self.llm.invoke(messages)
                # Extract content from response
                if hasattr(response, 'content'):
                    response_text = response.content
                else:
                    response_text = str(response)
            else:
                # For HuggingFace Inference API (Mistral), use proper chat format
                # Build conversation history
                history_parts = []
                for msg in self.conversation_history[-6:]:
                    if isinstance(msg, HumanMessage):
                        history_parts.append(f"[INST] {msg.content} [/INST]")
                    elif isinstance(msg, AIMessage):
                        history_parts.append(msg.content)
                
                # Build Mistral instruction prompt
                history_str = "\n".join(history_parts)
                if history_str:
                    prompt = f"<s>{history_str}\n[INST] {user_input} [/INST]"
                else:
                    prompt = f"<s>[INST] {self.system_prompt}\n\n{user_input} [/INST]"
                
                response = self.llm.invoke(prompt)
                response_text = str(response).strip()
                
                # Clean up any repeated prompt text in response
                if "[/INST]" in response_text:
                    response_text = response_text.split("[/INST]")[-1].strip()
                
                if not response_text or len(response_text) < 3:
                    response_text = "I understand your question, but I need more context to provide a helpful answer. Could you please rephrase or provide more details?"
            
            if not response_text or not response_text.strip():
                response_text = "I'm sorry, I couldn't generate a response. Could you rephrase your question?"
            
            # Update conversation history
            self.conversation_history.append(HumanMessage(content=user_input))
            self.conversation_history.append(AIMessage(content=response_text))
            
            # Store conversation in memory if available
            if self.memory_system:
                try:
                    self.memory_system.store_conversation(
                        user_input=user_input,
                        assistant_response=response_text,
                        metadata={}
                    )
                except Exception as e:
                    print(f"Warning: Failed to store in memory: {e}")
            
            return response_text
        
        except Exception as e:
            # Log error and return user-friendly message
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR in process_command: {error_details}")
            error_msg = f"Error processing command: {str(e)}"
            raise RuntimeError(error_msg)
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        Get recent conversation history.
        
        Args:
            limit: Maximum number of conversations to return
        
        Returns:
            List of conversation dictionaries with 'user' and 'assistant' keys
        """
        if not self.memory_system:
            return []
        
        try:
            history = self.memory_system.get_conversation_history(limit=limit)
            
            return [
                {
                    'user': entry.user_input,
                    'assistant': entry.assistant_response,
                    'timestamp': entry.timestamp.isoformat()
                }
                for entry in history
            ]
        except Exception as e:
            print(f"Warning: Failed to get conversation history: {e}")
            return []
    
    def clear_conversation_memory(self) -> None:
        """Clear the conversation buffer memory."""
        self.conversation_history.clear()
    
    def reset(self) -> None:
        """Reset the AI Core state, clearing all memory."""
        self.conversation_history.clear()
        if self.memory_system:
            try:
                self.memory_system.clear_all()
            except Exception as e:
                print(f"Warning: Failed to clear memory: {e}")
