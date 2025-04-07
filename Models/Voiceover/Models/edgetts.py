import sys
import os
import asyncio
import edge_tts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from Models.config import SAVE_VOICEOVER_TO
from config import AUDIO_MODEL_VOICE
from Models.utils import ensure_save_directory

class VoiceOverGenerator:
    def __init__(self):
        ensure_save_directory(SAVE_VOICEOVER_TO)

    async def text_to_audio(self, text):
        communicate = edge_tts.Communicate(text, AUDIO_MODEL_VOICE)
        await communicate.save(SAVE_VOICEOVER_TO)
        print(f"✅ Audio file saved at {SAVE_VOICEOVER_TO}")

    def generate_voiceover(self, text):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(self.text_to_audio(text))
        else:
            loop.run_until_complete(self.text_to_audio(text))


if __name__ == "__main__":
    generator = VoiceOverGenerator()
    text = input("Enter text for voiceover: ")
    generator.generate_voiceover(text)
