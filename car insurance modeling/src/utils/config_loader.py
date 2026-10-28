"""Configuration loader utility."""
import yaml
import os
from pathlib import Path

def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    project_root = Path(__file__).parent.parent.parent
    full_path = project_root / config_path
    
    with open(full_path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config

def get_data_paths(config: dict) -> tuple:
    """Get data paths from configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Tuple of (raw_data_path, processed_data_path)
    """
    project_root = Path(__file__).parent.parent.parent
    raw_path = project_root / config['data']['raw_data_path']
    processed_path = project_root / config['data']['processed_data_path']
    
    return str(raw_path), str(processed_path)