from recbole.quick_start import run_recbole
from recbole.config import Config
import os

def train_recommender(config_file):
    """
    Train a recommender system using RecBole.
    
    Args:
        config_file (str): Path to the configuration YAML file.
    
    Returns:
        dict: Result of the training process, as returned by RecBole.
    
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        RuntimeError: If an error occurs during training.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"The configuration file '{config_file}' does not exist.")
    
    try:
        # Load the configuration file explicitly
        config = Config(config_file_list=[config_file])
        
        # Pass the configuration to run_recbole using unpacking
        result = run_recbole(
            model=config['model'],
            dataset=config['dataset'],
            config_file_list=[config_file]
        )
        return result
    except Exception as e:
        raise RuntimeError(f"Error during training: {e}")

def evaluate_recommender(config_file):
    """
    Evaluate a trained recommender system using RecBole.
    
    Args:
        config_file (str): Path to the configuration YAML file.
    
    Returns:
        dict: Result of the evaluation process, as returned by RecBole.
    
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        RuntimeError: If an error occurs during evaluation.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"The configuration file '{config_file}' does not exist.")
    
    try:
        # Load the configuration file explicitly
        config = Config(config_file_list=[config_file])
        
        # Run evaluation using RecBole with the saved model
        result = run_recbole(
            model=config['model'],
            dataset=config['dataset'],
            config_file_list=[config_file],
            saved=True
        )
        return result
    except Exception as e:
        raise RuntimeError(f"Error during evaluation: {e}")