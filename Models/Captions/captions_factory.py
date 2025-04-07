import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.dont_write_bytecode = True
import importlib
from config import CAPTION_MODEL

def get_available_caption_models():
    """Returns a list of available caption models."""
    models_dir = os.path.join(os.path.dirname(__file__), 'Models')
    models = []
    
    if os.path.exists(models_dir):
        for file in os.listdir(models_dir):
            if file.endswith('.py') and not file.startswith('__'):
                model_name = file.replace('.py', '')
                models.append(model_name)
    
    return models

def load_caption_model(model_name=None):
    """Loads the specified caption model or uses the one from config."""
    if model_name is None:
        model_name = CAPTION_MODEL
        
    module_name = f"Models.Captions.Models.{model_name}"
    try:
        module = importlib.import_module(module_name)
        print(f"📝 Loading Caption Model: {model_name}")
        return module.CaptionGenerator()
    except ImportError:
        raise ImportError(f"❌ Error: {model_name}.py not found in Models/Captions/Models")

if __name__ == "__main__":
    available_models = get_available_caption_models()
    print(f"Available caption models: {', '.join(available_models)}")
    
    model_name = input(f"Select caption model ({', '.join(available_models)} or press Enter for default): ") or CAPTION_MODEL
    
    generator = load_caption_model(model_name)
    video_path = input("Enter path to video file: ")
    generator.process_video(video_path)
