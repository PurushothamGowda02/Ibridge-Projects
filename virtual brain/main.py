#!/usr/bin/env python3
"""
Virtual Brain Assistant - Main Entry Point

This is the main entry point for the Virtual Brain Assistant application.
It initializes all components, validates the configuration, and launches
the Streamlit UI.

Usage:
    python main.py
    
    Or with streamlit directly:
    streamlit run main.py
"""

import sys
import os
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.config_manager import ConfigurationManager, ConfigurationError
from src.memory.memory_system import MemorySystem
from src.tasks.task_executor import TaskExecutor
from src.ai_core.ai_core import AICore
from src.input.input_module import InputModule
from src.output.output_module import OutputModule


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('virtual_brain_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def validate_environment():
    """
    Validate the environment and dependencies before starting.
    
    Raises:
        RuntimeError: If critical dependencies are missing or environment is invalid
    """
    logger.info("Validating environment...")
    
    # Check if config file exists
    if not Path('config.yaml').exists():
        raise RuntimeError(
            "Configuration file 'config.yaml' not found. "
            "Please create it based on the example configuration."
        )
    
    # Check if .env file exists (optional but recommended)
    if not Path('.env').exists():
        logger.warning(
            ".env file not found. API keys should be set as environment variables."
        )
    
    logger.info("Environment validation passed")


def initialize_components():
    """
    Initialize all system components with proper error handling.
    
    Returns:
        tuple: (config_manager, memory_system, task_executor, ai_core, 
                input_module, output_module)
    
    Raises:
        RuntimeError: If component initialization fails
    """
    logger.info("Initializing Virtual Brain Assistant components...")
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        config_manager = ConfigurationManager()
        logger.info("[OK] Configuration loaded successfully")
        
        # Initialize Memory System
        logger.info("Initializing Memory System...")
        memory_settings = config_manager.get_memory_settings()
        memory_system = MemorySystem(
            vector_store_type=memory_settings.get('vector_store', 'faiss'),
            embedding_model=memory_settings.get('embedding_model'),
            dimension=384,  # Default dimension for all-MiniLM-L6-v2
            persist_directory=memory_settings.get('persist_directory')
        )
        logger.info(f"[OK] Memory System initialized with {memory_settings.get('vector_store', 'faiss')} backend")
        
        # Initialize Task Executor
        logger.info("Initializing Task Executor...")
        task_executor = TaskExecutor()
        logger.info("[OK] Task Executor initialized")
        
        # Initialize AI Core
        logger.info("Initializing AI Core...")
        llm_settings = config_manager.get_llm_settings()
        ai_core = AICore(
            llm_config=llm_settings,
            memory_system=memory_system,
            task_executor=task_executor
        )
        logger.info("[OK] AI Core initialized")
        
        # Initialize Input Module
        logger.info("Initializing Input Module...")
        input_module = InputModule()
        if input_module.microphone_available:
            logger.info("[OK] Input Module initialized (microphone available)")
        else:
            logger.warning("[OK] Input Module initialized (microphone NOT available)")
        
        # Initialize Output Module
        logger.info("Initializing Output Module...")
        voice_settings = config_manager.get_voice_settings()
        output_module = OutputModule(
            voice_enabled=voice_settings.get('output_enabled', True)
        )
        logger.info("[OK] Output Module initialized")
        
        logger.info("All components initialized successfully!")
        
        return (
            config_manager,
            memory_system,
            task_executor,
            ai_core,
            input_module,
            output_module
        )
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        raise RuntimeError(f"Failed to load configuration: {e}")
    
    except Exception as e:
        logger.error(f"Component initialization failed: {e}", exc_info=True)
        raise RuntimeError(f"Failed to initialize components: {e}")


def print_startup_banner(config_manager):
    """
    Print a startup banner with system information.
    
    Args:
        config_manager: ConfigurationManager instance
    """
    banner = """
    ==============================================================
                                                           
              VIRTUAL BRAIN ASSISTANT                  
                                                           
              Your AI-Powered Assistant                    
                                                           
    ==============================================================
    """
    print(banner)
    
    # Display configuration info
    llm_provider = config_manager.get('llm.provider', 'Unknown')
    llm_model = config_manager.get('llm.model', 'Unknown')
    vector_store = config_manager.get('memory.vector_store', 'Unknown')
    
    print(f"    LLM Provider: {llm_provider}")
    print(f"    LLM Model: {llm_model}")
    print(f"    Vector Store: {vector_store}")
    print()
    print("    Starting Streamlit UI...")
    print()


def launch_streamlit_ui():
    """
    Launch the Streamlit UI application.
    
    This function uses os.system to run streamlit, which will start
    the web interface for the Virtual Brain Assistant.
    """
    logger.info("Launching Streamlit UI...")
    
    # Get the path to the Streamlit app
    app_path = Path(__file__).parent / "src" / "ui" / "app.py"
    
    if not app_path.exists():
        raise RuntimeError(f"Streamlit app not found at {app_path}")
    
    # Launch Streamlit
    # Note: This will block until the Streamlit app is closed
    import subprocess
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(app_path),
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        logger.info("Streamlit UI closed by user")
    except Exception as e:
        logger.error(f"Failed to launch Streamlit: {e}")
        raise RuntimeError(f"Failed to launch Streamlit UI: {e}")


def main():
    """
    Main entry point for the Virtual Brain Assistant.
    
    This function:
    1. Validates the environment
    2. Initializes all components
    3. Launches the Streamlit UI
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    try:
        # Validate environment
        validate_environment()
        
        # Initialize components (this validates configuration)
        config_manager, memory_system, task_executor, ai_core, input_module, output_module = initialize_components()
        
        # Print startup banner
        print_startup_banner(config_manager)
        
        # Launch Streamlit UI
        launch_streamlit_ui()
        
        return 0
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease check your config.yaml and .env files.")
        print("See .env.example for required environment variables.")
        return 1
    
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        print(f"\n❌ Error: {e}")
        return 1
    
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n\n👋 Virtual Brain Assistant shutting down...")
        return 0
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}")
        print("\nPlease check the log file for details: virtual_brain_assistant.log")
        return 1


if __name__ == "__main__":
    sys.exit(main())
