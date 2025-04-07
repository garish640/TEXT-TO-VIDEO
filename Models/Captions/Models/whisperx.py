import whisperx
import torch
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
sys.dont_write_bytecode = True
from Models.config import SAVE_TIMESTAMPS_TO, SAVE_VOICEOVER_TO

from Models.Captions.caption_processor import process_video as process_with_captions
from Models.Captions.utils import get_available_caption_styles, get_available_fonts
from config import CAPTION_STYLE, CAPTION_MODEL_TYPE

class CaptionGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float32"
        self.whisper_model = whisperx.load_model(CAPTION_MODEL_TYPE, device=self.device, compute_type=self.compute_type)
        fonts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Fonts')
        os.makedirs(fonts_dir, exist_ok=True)

    def generate_word_timestamps(self, audio_path, output_json=SAVE_TIMESTAMPS_TO):
        """Generate word-level timestamps using WhisperX."""
        if not os.path.exists(audio_path):
            print(f"❌ Audio file not found: {audio_path}")
            return None

        audio = whisperx.load_audio(audio_path)
        transcription = self.whisper_model.transcribe(audio, batch_size=16)

        model_a, metadata = whisperx.load_align_model(language_code="en", device=self.device)
        aligned_result = whisperx.align(transcription["segments"], model_a, metadata, audio, self.device)
        
        print(f"⏳ Processing aligned result to extract word timestamps...")
        
        if "word_segments" not in aligned_result or not aligned_result["word_segments"]:
            print("⚠️ No word segments found in alignment result. Using segment-level timestamps instead.")
            words_data = []
            for segment in aligned_result.get("segments", []):
                if "start" in segment and "end" in segment and "text" in segment:
                    words_data.append({
                        "start": segment["start"],
                        "end": segment["end"],
                        "text": segment["text"]
                    })
        else:
            words_data = []
            for w in aligned_result["word_segments"]:
                if "start" not in w or "end" not in w:
                    print(f"⚠️ Missing start/end time for word: {w.get('word', 'unknown')}")
                    continue
                    
                words_data.append({
                    "start": w["start"],
                    "end": w["end"],
                    "text": w.get("word", "")
                })

        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(words_data, f, indent=4)

        print(f"✅ Word timestamps saved to {output_json} ({len(words_data)} words)")
        return output_json

    def process_video(self, video_path, style_name=None, output_path=None):
        """Process video with captions using the centralized processor."""
        if style_name is None:
            style_name = CAPTION_STYLE
            
        return process_with_captions(self, video_path, style_name, output_path)

    def get_available_styles(self):
        """Lists all available caption styles"""
        styles = get_available_caption_styles()
        print(f"\n📚 Available caption styles:")
        for style in styles:
            marker = "✓" if style == CAPTION_STYLE else " "
            print(f" [{marker}] {style}")
        return styles
        
    def get_available_fonts(self):
        """Lists all available fonts"""
        fonts = get_available_fonts()
        print(f"\n🔠 Available fonts:")
        for font in fonts:
            print(f" - {font}")
        return fonts

if __name__ == "__main__":
    caption_generator = CaptionGenerator()
    
    available_styles = caption_generator.get_available_styles()
    available_fonts = caption_generator.get_available_fonts()
    
    video_path = input("\nEnter video path: ")
    print(f"Using caption style: {CAPTION_STYLE}")
    
    use_different_style = input(f"Would you like to use a different style? (y/n): ").lower() == 'y'
    
    if use_different_style and available_styles:
        style_name = input(f"Enter style name ({', '.join(available_styles)}): ") or CAPTION_STYLE
    else:
        style_name = CAPTION_STYLE
        
    caption_generator.process_video(video_path, style_name)
