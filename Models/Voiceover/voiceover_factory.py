import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.dont_write_bytecode = True
import importlib
from config import AUDIO_MODEL

def load_voiceover_model():
    module_name = f"Models.Voiceover.Models.{AUDIO_MODEL}"
    try:
        module = importlib.import_module(module_name)
        print(f"🎙️ Loading Voiceover Model: {AUDIO_MODEL}")
        return module.VoiceOverGenerator()
    except ImportError:
        raise ImportError(f"❌ Error: {AUDIO_MODEL}.py not found in Models/Voiceover/Models")

if __name__ == "__main__":
    generator = load_voiceover_model()
    text = input("Enter text for voiceover: ")
    generator.generate_voiceover(text)
