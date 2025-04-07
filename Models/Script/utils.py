from Models.config import SAVE_SCRIPT_TO
import re
import os

SYSTEM_PROMPT = (
    "You are a professional script writer. You are given a topic "
    "and must generate a professional script on that topic for a YouTube short about 45 seconds long. "
    "Make the script engaging, start with a hook, make it curiosity-driven, and provide only the script in plain text. "
    "Do not include stage directions or sound effects like (0-3 seconds), (Sound of wind howling), (Beat), (Pause), etc. "
    "Give only the script text. Make it 30 seconds long, and finish the topic completely. "
    "Don't refer to a second part, and use simple, easy-to-understand English without complex vocabulary."
    "And do not enter or add a new line, full script in single line only"
)

def format_script(text):
    """Formats the script for better readability."""
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\(.*?\)', '', text)
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    formatted_script = "\n".join(sentence.strip() for sentence in sentences if sentence.strip())
    return formatted_script

def save_formatted_script(script_text, file_path=None):
    """Saves the formatted script to a file."""
    if file_path is None:
        file_path = SAVE_SCRIPT_TO
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    formatted_text = format_script(script_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return formatted_text
