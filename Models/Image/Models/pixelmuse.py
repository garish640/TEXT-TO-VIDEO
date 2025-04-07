import sys
import os
import requests
import time
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
sys.dont_write_bytecode = True
from Models.config import SAVE_IMAGES_TO
from config import IMG_MODEL_TYPE
from Models.Image.utils import ensure_save_directory

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

class ImageGenerator():
    def __init__(self):
        self.prompt_generator = None
        
    def set_prompt_generator(self, prompt_generator):
        self.prompt_generator = prompt_generator
        
    def generate_image_prompt(self, text):
        if self.prompt_generator:
            return self.prompt_generator.generate_prompt(text)
        else:
            return text
        
    def download_image(self, prompt, img_number):
        url = "https://www.pixelmuse.studio/api/predictions"
        headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://www.pixelmuse.studio",
            "referer": "https://www.pixelmuse.studio/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        payload = {
            "prompt": prompt,
            "model": IMG_MODEL_TYPE,
            "style": "none",
            "aspect_ratio": "9:16"
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=35)
            
            if response.status_code == 201:
                response_data = response.json()
                image_url_list = response_data.get("output", [])
                if isinstance(image_url_list, list) and image_url_list:
                    image_url = image_url_list[0]
                else:
                    image_url = None
                
                if image_url:
                    print(image_url)
                    
                    image_response = requests.get(image_url, timeout=35)
                    
                    if image_response.status_code == 200:
                        filename = os.path.join(SAVE_IMAGES_TO, f"image_{img_number}.jpg")
                        ensure_save_directory(os.path.dirname(filename))
                        
                        with open(filename, "wb") as file:
                            file.write(image_response.content)
                        
                    else:
                        print(f"❌ Failed to download image {img_number} from {image_url}")
                else:
                    print(f"❌ No image URL found in response for image {img_number}")
            else:
                print(f"❌ Failed to fetch image {img_number}. Status Code: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error downloading image {img_number}: {e}")

    def generate_images_from_script(self, script_lines):
        for i, line in enumerate(script_lines, start=1):
            print(f"🎨 Generating prompt for line {i}/{len(script_lines)}...")
            image_prompt = self.generate_image_prompt(line)
            print(f"📜 Prompt {i}: {image_prompt}")
            
            self.download_image(image_prompt, i)
            time.sleep(1)