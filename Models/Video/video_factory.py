import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.dont_write_bytecode = True
import importlib
from config import VIDEO_MODEL

def load_video_model():
    module_name = f"Models.Video.Models.{VIDEO_MODEL}"
    try:
        module = importlib.import_module(module_name)
        print(f"📝 Loading Video Model: {VIDEO_MODEL}")
        video_generator = module.VideoGenerator()
        return video_generator
    except ImportError:
        raise ImportError(f"❌ Error: {VIDEO_MODEL}.py not found in Models/Video/Models")

if __name__ == "__main__":
    generator = load_video_model()
