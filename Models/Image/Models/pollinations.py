import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import requests
import time
from Models.config import SAVE_IMAGES_TO
from Models.Image.utils import ensure_save_directory

class ImageGenerator():
    def __init__(self):
        self.prompt_generator = None
        
    def set_prompt_generator(self, prompt_generator):
        """Sets the prompt generator instance to use for generating image prompts."""
        self.prompt_generator = prompt_generator
        
    def generate_image_prompt(self, text):
        """Generates an image prompt from text using the assigned prompt generator."""
        if self.prompt_generator:
            return self.prompt_generator.generate_prompt(text)
        else:
            return text
        
    def download_image(self, prompt, img_number):
        """Downloads AI-generated images from Pollinations API using Flux model."""
        width, height, seed, model = 720, 1280, 42, "flux"
        image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}&nologo=True"

        try:
            response = requests.get(image_url, timeout=35)
            if response.status_code == 200:
                filename = f"{SAVE_IMAGES_TO}/image_{img_number}.jpg"
                
                ensure_save_directory(filename)
                
                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"✅ Image {img_number} saved: {filename}")
                time.sleep(1)
            else:
                print(f"❌ Failed to fetch image {img_number}. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error downloading image {img_number}: {e}")

    def generate_images_from_script(self, script_lines):
        """Processes script lines, generates image prompts, and downloads images."""
        for i, line in enumerate(script_lines, start=1):
            print(f"🎨 Generating prompt for line {i}/{len(script_lines)}...")
            image_prompt = self.generate_image_prompt(line)
            print(f"📜 Prompt {i}: {image_prompt}")
            
            self.download_image(image_prompt, i)
            time.sleep(1)