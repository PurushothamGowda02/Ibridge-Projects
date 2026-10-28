"""
Configuration Manager for Virtual Brain Assistant.

This module handles loading, validating, and providing access to configuration
settings from YAML files and environment variables.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing required fields."""
    pass


class ConfigurationManager:
    """
    Manages configuration loading and validation for the Virtual Brain Assistant.
    
    Loads configuration from:
    1. config.yaml file for general settings
    2. Environment variables for sensitive data (API keys)
    
    Validates required fields and provides typed access to configuration values.
    """
    
    def __init__(self, config_path: str = "config.yaml", env_path: Optional[str] = ".env"):
        """
        Initialize the Configuration Manager.
        
        Args:
            config_path: Path to the YAML configuration file
            env_path: Path to the .env file (optional)
        
        Raises:
            ConfigurationError: If configuration file is missing or invalid
        """
        self.config_path = Path(config_path)
        self.env_path = Path(env_path) if env_path else None
        self._config: Dict[str, Any] = {}
        
        # Load environment variables
        self._load_environment()
        
        # Load YAML configuration
        self._load_config_file()
        
        # Validate configuration
        self._validate_config()
    
    def _load_environment(self) -> None:
        """Load environment variables from .env file if it exists."""
        if self.env_path and self.env_path.exists():
            load_dotenv(self.env_path)
    
    def _load_config_file(self) -> None:
        """
        Load configuration from YAML file.
        
        Raises:
            ConfigurationError: If config file doesn't exist or is invalid YAML
        """
        if not self.config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error reading configuration file: {e}")
        
        if not isinstance(self._config, dict):
            raise ConfigurationError("Configuration file must contain a YAML dictionary")
    
    def _validate_config(self) -> None:
        """
        Validate that all required configuration sections and fields are present.
        
        Raises:
            ConfigurationError: If required fields are missing or invalid
        """
        # Required top-level sections
        required_sections = ['llm', 'memory', 'voice']
        for section in required_sections:
            if section not in self._config:
                raise ConfigurationError(f"Missing required configuration section: {section}")
        
        # Validate LLM configuration
        self._validate_llm_config()
        
        # Validate memory configuration
        self._validate_memory_config()
        
        # Validate voice configuration
        self._validate_voice_config()
    
    def _validate_llm_config(self) -> None:
        """Validate LLM configuration section."""
        llm_config = self._config.get('llm', {})
        
        # Check required fields
        if 'provider' not in llm_config:
            raise ConfigurationError("LLM configuration missing 'provider' field")
        
        provider = llm_config['provider']
        valid_providers = ['openai', 'huggingface', 'groq', 'local']
        if provider not in valid_providers:
            raise ConfigurationError(
                f"Invalid LLM provider '{provider}'. Must be one of: {valid_providers}"
            )
        
        # Check for API key based on provider
        if provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ConfigurationError(
                    "OPENAI_API_KEY environment variable is required when using OpenAI provider"
                )
        elif provider == 'groq':
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                raise ConfigurationError(
                    "GROQ_API_KEY environment variable is required when using Groq provider"
                )
        elif provider == 'huggingface':
            # HuggingFace API key is optional for public models
            pass
        elif provider == 'local':
            # Local models don't require API keys
            pass
        
        # Check model field
        if 'model' not in llm_config:
            raise ConfigurationError("LLM configuration missing 'model' field")
    
    def _validate_memory_config(self) -> None:
        """Validate memory configuration section."""
        memory_config = self._config.get('memory', {})
        
        if 'vector_store' not in memory_config:
            raise ConfigurationError("Memory configuration missing 'vector_store' field")
        
        vector_store = memory_config['vector_store']
        valid_stores = ['faiss', 'chromadb']
        if vector_store not in valid_stores:
            raise ConfigurationError(
                f"Invalid vector store '{vector_store}'. Must be one of: {valid_stores}"
            )
        
        if 'embedding_model' not in memory_config:
            raise ConfigurationError("Memory configuration missing 'embedding_model' field")
    
    def _validate_voice_config(self) -> None:
        """Validate voice configuration section."""
        voice_config = self._config.get('voice', {})
        
        required_fields = ['input_enabled', 'output_enabled', 'language']
        for field in required_fields:
            if field not in voice_config:
                raise ConfigurationError(f"Voice configuration missing '{field}' field")
    
    def get_llm_settings(self) -> Dict[str, Any]:
        """
        Get LLM configuration settings.
        
        Returns:
            Dictionary containing LLM settings including provider, model, and parameters.
            API keys are loaded from environment variables.
        """
        llm_config = self._config['llm'].copy()
        
        # Add API key from environment if applicable
        provider = llm_config['provider']
        if provider == 'openai':
            llm_config['api_key'] = os.getenv('OPENAI_API_KEY')
        elif provider == 'groq':
            llm_config['api_key'] = os.getenv('GROQ_API_KEY')
        elif provider == 'huggingface':
            llm_config['api_key'] = os.getenv('HUGGINGFACE_API_KEY')
        elif provider == 'local':
            llm_config['model_path'] = os.getenv('LOCAL_MODEL_PATH', llm_config.get('model_path'))
        
        return llm_config
    
    def get_memory_settings(self) -> Dict[str, Any]:
        """
        Get memory system configuration settings.
        
        Returns:
            Dictionary containing memory settings including vector store type,
            embedding model, and persistence configuration.
        """
        return self._config['memory'].copy()
    
    def get_voice_settings(self) -> Dict[str, Any]:
        """
        Get voice input/output configuration settings.
        
        Returns:
            Dictionary containing voice settings including input/output enabled flags,
            language, and TTS parameters.
        """
        return self._config['voice'].copy()
    
    def get_task_settings(self) -> Dict[str, Any]:
        """
        Get task executor configuration settings.
        
        Returns:
            Dictionary containing task execution settings.
        """
        return self._config.get('tasks', {}).copy()
    
    def get_ui_settings(self) -> Dict[str, Any]:
        """
        Get UI configuration settings.
        
        Returns:
            Dictionary containing UI settings.
        """
        return self._config.get('ui', {}).copy()
    
    def get_system_settings(self) -> Dict[str, Any]:
        """
        Get system configuration settings.
        
        Returns:
            Dictionary containing system-level settings.
        """
        return self._config.get('system', {}).copy()
    
    def get_logging_settings(self) -> Dict[str, Any]:
        """
        Get logging configuration settings.
        
        Returns:
            Dictionary containing logging settings.
        """
        return self._config.get('logging', {}).copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key path.
        
        Args:
            key: Dot-separated key path (e.g., 'llm.provider')
            default: Default value if key is not found
        
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def reload(self) -> None:
        """
        Reload configuration from files.
        
        Useful for picking up configuration changes without restarting.
        
        Raises:
            ConfigurationError: If reloaded configuration is invalid
        """
        self._load_environment()
        self._load_config_file()
        self._validate_config()
