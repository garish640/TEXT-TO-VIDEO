import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import importlib
from config import PROMPT_MODEL

def load_prompt_generator():
    module_name = f"Models.Image.Img_Prompts.{PROMPT_MODEL}"
    try:
        module = importlib.import_module(module_name)
        print(f"📝 Loading Prompt Generator: {PROMPT_MODEL}")
        return module.PromptGenerator()
    except ImportError:
        raise ImportError(f"❌ Error: {PROMPT_MODEL}.py not found in Models/Image/Img_Prompts") 
    
if __name__ == "__main__":
    prompt_generator = load_prompt_generator()
    print(prompt_generator)
