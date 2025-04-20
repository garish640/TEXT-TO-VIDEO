import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from Models.config import SAVE_VOICEOVER_TO
from config import AUDIO_MODEL_VOICE
from Models.utils import ensure_save_directory

class VoiceOverGenerator:
    def __init__(self):
        ensure_save_directory(SAVE_VOICEOVER_TO)

    def generate_voiceover(self, text):
        url = "https://www.openai.fm/api/generate"
        payload = {
            "input": text,
            "voice": AUDIO_MODEL_VOICE,
            "vibe": "null"
        }
        files = {key: (None, value) for key, value in payload.items()}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            with open(SAVE_VOICEOVER_TO, "wb") as f:
                f.write(response.content)
            print(f"✅ Audio file saved at {SAVE_VOICEOVER_TO}")
        else:
            print("❌ Error:", response.status_code, response.text)


if __name__ == "__main__":
    generator = VoiceOverGenerator()
    text = input("Enter text for voiceover: ")
    generator.generate_voiceover(text)
