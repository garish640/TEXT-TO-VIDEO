import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.dont_write_bytecode = True
import importlib
from config import ANIMATION

def load_animation_model():
    module_name = f"Models.Animations.Models.{ANIMATION}"
    try:
        module = importlib.import_module(module_name)
        return module.Animation()
    except ImportError:
        raise ImportError(f"❌ Error: {ANIMATION}.py not found in Models/Animations/Models")
    
if __name__ == "__main__":
    animation = load_animation_model()
    print(animation)
