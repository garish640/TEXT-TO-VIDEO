import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Models.config import SAVE_TIMESTAMPS_TO, SAVE_VIDEO_TO, SAVE_VOICEOVER_TO, SAVE_IMAGES_TO, SAVE_SCRIPT_TO
import whisper
from moviepy.video.fx.all import crop
from Models.config import VIDEO_RATIO

def ensure_directories():
    """Ensures all necessary directories exist."""
    dirs = [
        os.path.dirname(SAVE_TIMESTAMPS_TO),
        os.path.dirname(SAVE_VIDEO_TO),
        os.path.dirname(SAVE_IMAGES_TO),
        os.path.dirname(SAVE_VOICEOVER_TO),
        os.path.dirname(SAVE_TIMESTAMPS_TO)
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

def crop_to_portrait(clip):
        """Ensure the image is in portrait ratio by cropping."""
        w, h = clip.size
        target_ratio = VIDEO_RATIO
        current_ratio = w / h

        if current_ratio > target_ratio:
            new_width = int(h * target_ratio)
            x_center = w // 2
            clip = crop(clip, width=new_width, height=h, x_center=x_center, y_center=h // 2)
        elif current_ratio < target_ratio:
            new_height = int(w / target_ratio)
            y_center = h // 2
            clip = crop(clip, width=w, height=new_height, x_center=w // 2, y_center=y_center)
        
        return clip
        
def load_timestamps(timestamps_file=SAVE_TIMESTAMPS_TO):
    """Load timestamps from a JSON file."""
    if not os.path.exists(timestamps_file):
        print(f"❌ Timestamps file not found: {timestamps_file}")
        return []
    
    with open(timestamps_file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_script_lines(script_file=SAVE_SCRIPT_TO):
    """Load the script from the file and return a list of lines."""
    with open(script_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def transcribe_audio_with_script(audio_file=SAVE_VOICEOVER_TO, script_file=SAVE_SCRIPT_TO, output_file=SAVE_TIMESTAMPS_TO):
    """
    Transcribes the audio to get the total duration and then distributes timestamps
    to the script lines proportionally so that they exactly cover the audio duration.
    
    This function can be used by any video generation model to create timestamps.
    
    Args:
        audio_file: Path to the audio file to transcribe
        script_file: Path to the script file containing the text lines
        output_file: Path where the timestamp JSON will be saved
        
    Returns:
        List of segments with start, end, and text information
    """
    print("⏳ Transcribing audio and generating timestamps...")
    
    if os.path.exists(output_file):
        print(f"✅ Using existing timestamps from {output_file}")
        return load_timestamps(output_file)
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return []
        
    model = whisper.load_model("small")
    result = model.transcribe(audio_file)

    total_audio_duration = result["segments"][-1]["end"] if result["segments"] else 52.0
    script_lines = load_script_lines(script_file)

    estimated_durations = [max(1.0, 0.25 * len(line.split())) for line in script_lines]
    total_estimated = sum(estimated_durations)

    scale_factor = total_audio_duration / total_estimated
    scaled_durations = [d * scale_factor for d in estimated_durations]

    matched_segments = []
    last_end = 0.0
    for line, duration in zip(script_lines, scaled_durations):
        segment = {"start": last_end, "end": last_end + duration, "text": line}
        matched_segments.append(segment)
        last_end += duration

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(matched_segments, f, indent=4)

    print(f"✅ Timestamps saved to {output_file}")
    return matched_segments

def verify_assets(timestamps=None, audio_file=SAVE_VOICEOVER_TO):
    """Verify that all necessary assets exist for video generation."""
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    if timestamps is None:
        timestamps = load_timestamps()
    
    if not timestamps:
        print("❌ No timestamp data available")
        return False
    
    missing_images = []
    for i in range(1, len(timestamps) + 1):
        image_path = f"{SAVE_IMAGES_TO.rstrip('/')}/image_{i}.jpg"
        if not os.path.exists(image_path):
            missing_images.append(i)
    
    if missing_images:
        print(f"⚠️ Warning: {len(missing_images)} images missing: {missing_images}")
        return len(missing_images) < len(timestamps)
        
    return True 