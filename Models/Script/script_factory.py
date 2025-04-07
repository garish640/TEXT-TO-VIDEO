import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.dont_write_bytecode = True
import importlib
from config import SCRIPT_MODEL

def load_script_model():
    module_name = f"Models.Script.Models.{SCRIPT_MODEL}"
    try:
        module = importlib.import_module(module_name)
        print(f"📝 Loading Script Model: {SCRIPT_MODEL}")
        return module.ScriptGenerator()
    except ImportError:
        raise ImportError(f"❌ Error: {SCRIPT_MODEL}.py not found in Models/Script/Models")

if __name__ == "__main__":
    script = load_script_model()
    topic = input("Enter a topic: ")
    script = script.generate_script(topic)
    print("📝 Generated Script Successfully")