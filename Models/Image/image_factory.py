import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.dont_write_bytecode = True
import importlib
from config import IMG_MODEL
from Models.Image.Img_Prompts.img_prompt_factory import load_prompt_generator

def load_image_model():
    module_name = f"Models.Image.Models.{IMG_MODEL}"
    try:
        module = importlib.import_module(module_name)
        print(f"📝 Loading Image Model: {IMG_MODEL}")
        image_generator = module.ImageGenerator()
        prompt_generator = load_prompt_generator()
        image_generator.set_prompt_generator(prompt_generator)
        return image_generator
    except ImportError:
        raise ImportError(f"❌ Error: {IMG_MODEL}.py not found in Models/Image/Models")

if __name__ == "__main__":
    generator = load_image_model()