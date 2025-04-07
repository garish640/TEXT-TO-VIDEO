import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import google.generativeai as genai
from dotenv import dotenv_values
from Models.Image.utils import SYSTEM_PROMPT
from Models.config import SAVE_SCRIPT_TO
from config import PROMPT_MODEL_TYPE

class PromptGenerator:
    def __init__(self):
        env_vars = dotenv_values(".env")
        self.api_key = env_vars.get("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found. Check your .env file.")
        
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name=PROMPT_MODEL_TYPE,
            generation_config={
                "temperature": 0.9,
                "top_p": 0.8,
                "top_k": 40
            }
        )

    def generate_prompt(self, scene_text):
        Generated_Script = open(SAVE_SCRIPT_TO, "r").read()
        print(Generated_Script)
        """Generates an image prompt based on the scene text."""
        full_prompt = f"{SYSTEM_PROMPT}\n\nScript: {Generated_Script}\n\nScene: {scene_text}\n\nGenerate an image prompt:"
        response = self.model.generate_content(full_prompt)
        return response.text if hasattr(response, "text") else response.result
    
if __name__ == "__main__":
    prompt_generator = PromptGenerator()
    prompt = prompt_generator.generate_prompt("Mahatma Gandhi was a great leader.")
    print(prompt)

