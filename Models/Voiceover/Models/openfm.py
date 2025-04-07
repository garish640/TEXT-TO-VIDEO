import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import requests
import os
from dotenv import dotenv_values
from Models.config import SAVE_VOICEOVER_TO
from config import AUDIO_MODEL_VOICE
from Models.utils import ensure_save_directory

class VoiceOverGenerator:
    def __init__(self):
        ensure_save_directory(SAVE_VOICEOVER_TO)

    def text_to_audio(self, text):
        url = "https://openfm.onrender.com/api/generate"

        data = {
            "input": text,
            "voice": AUDIO_MODEL_VOICE,
            "vibe": "storytelling",
            "customPrompt": ""
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            with open(SAVE_VOICEOVER_TO, "wb") as f:
                f.write(response.content)
            print(f"✅ Audio file saved at {SAVE_VOICEOVER_TO}")
        else:
            print(f"❌ Error: Request failed with status code {response.status_code}")

    def generate_voiceover(self, text):
        self.text_to_audio(text)