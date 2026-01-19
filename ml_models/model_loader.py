"""
ML Model Loader Utility
Handles loading and caching of machine learning models for dyslexia detection
"""

import os
from pathlib import Path
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Model paths
MODELS_DIR = Path(settings.BASE_DIR) / 'ml_models'

MODEL_PATHS = {
    'eye_movement': MODELS_DIR / 'dyslexia_eye_movement_model.keras',
    'audio_lstm': MODELS_DIR / 'dyslexia_audio_lstm_model_v2.keras',
    'dysgraphia': MODELS_DIR / 'dysgraphia_model.h5',
}

# Cache for loaded models
_model_cache = {}


def load_model(model_name):
    """
    Load a machine learning model by name.
    
    Args:
        model_name (str): Name of the model ('eye_movement', 'audio_lstm', or 'dysgraphia')
    
    Returns:
        model: Loaded Keras/TensorFlow model or None if not available
    """
    # Return cached model if already loaded
    if model_name in _model_cache:
        logger.info(f"Using cached model: {model_name}")
        return _model_cache[model_name]
    
    # Check if model name is valid
    if model_name not in MODEL_PATHS:
        logger.error(f"Unknown model name: {model_name}")
        return None
    
    model_path = MODEL_PATHS[model_name]
    
    # Check if model file exists
    if not model_path.exists():
        logger.warning(f"Model file not found: {model_path}")
        logger.warning(f"Please place the model file in: {MODELS_DIR}")
        return None
    
    try:
        # Import TensorFlow/Keras only when needed
        from tensorflow import keras
        
        logger.info(f"Loading model: {model_name} from {model_path}")
        
        # Load the model
        if model_path.suffix == '.h5':
            model = keras.models.load_model(str(model_path))
        elif model_path.suffix == '.keras':
            model = keras.models.load_model(str(model_path))
        else:
            logger.error(f"Unsupported model format: {model_path.suffix}")
            return None
        
        # Cache the model
        _model_cache[model_name] = model
        logger.info(f"Successfully loaded model: {model_name}")
        
        return model
        
    except ImportError:
        logger.error("TensorFlow/Keras not installed. Install with: pip install tensorflow")
        return None
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {str(e)}")
        return None


def is_model_available(model_name):
    """
    Check if a model file exists.
    
    Args:
        model_name (str): Name of the model
    
    Returns:
        bool: True if model file exists, False otherwise
    """
    if model_name not in MODEL_PATHS:
        return False
    return MODEL_PATHS[model_name].exists()


def get_available_models():
    """
    Get list of available models.
    
    Returns:
        list: Names of models that have files present
    """
    return [name for name in MODEL_PATHS.keys() if is_model_available(name)]


def clear_model_cache():
    """Clear the model cache to free memory."""
    global _model_cache
    _model_cache.clear()
    logger.info("Model cache cleared")


def get_model_info():
    """
    Get information about all models.
    
    Returns:
        dict: Dictionary with model information
    """
    info = {}
    for name, path in MODEL_PATHS.items():
        info[name] = {
            'path': str(path),
            'exists': path.exists(),
            'size_mb': round(path.stat().st_size / (1024 * 1024), 2) if path.exists() else 0,
            'loaded': name in _model_cache
        }
    return info
