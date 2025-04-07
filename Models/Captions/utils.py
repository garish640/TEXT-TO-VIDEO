import os
import json
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import shutil

def get_available_caption_styles():
    """Returns a list of available caption styles in the Caption_Styles folder."""
    styles_dir = os.path.join(os.path.dirname(__file__), 'Caption_Styles')
    if not os.path.exists(styles_dir):
        os.makedirs(styles_dir, exist_ok=True)
        
    styles = []
    for file in os.listdir(styles_dir):
        if file.endswith('.json'):
            style_name = file.replace('.json', '')
            styles.append(style_name)
            
    if not styles:
        default_style = {
            "font_size_ratio": 0.04,
            "padding_x_ratio": 0.02,
            "padding_top_ratio": 0.01,
            "padding_bottom_ratio": 0.02,
            "bg_color": [0, 0, 0, 200],
            "text_color": [255, 255, 255, 255],
            "position": "bottom",
            "vertical_offset": 300,
            "font": "arial.ttf",
            "uppercase": True
        }
        save_caption_style("default", default_style)
        styles = ["default"]
        
    return styles

def get_available_fonts():
    """Returns a list of available fonts in the Fonts folder."""
    fonts_dir = os.path.join(os.path.dirname(__file__), 'Fonts')
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir, exist_ok=True)
        
    fonts = []
    for file in os.listdir(fonts_dir):
        if file.endswith(('.ttf', '.otf')):
            fonts.append(file)
            
    if not fonts and os.path.exists(os.path.join("Data", "Fonts")):
        data_fonts_dir = os.path.join("Data", "Fonts")
        if os.path.exists(data_fonts_dir):
            for file in os.listdir(data_fonts_dir):
                if file.endswith(('.ttf', '.otf')):
                    src_path = os.path.join(data_fonts_dir, file)
                    dst_path = os.path.join(fonts_dir, file)
                    shutil.copy2(src_path, dst_path)
                    fonts.append(file)
                    print(f"Copied font {file} to Captions/Fonts directory")
    
    return fonts

def add_font(font_path):
    """Adds a font file to the Fonts folder."""
    if not os.path.exists(font_path):
        print(f"❌ Font file not found: {font_path}")
        return False
        
    fonts_dir = os.path.join(os.path.dirname(__file__), 'Fonts')
    os.makedirs(fonts_dir, exist_ok=True)
    
    font_name = os.path.basename(font_path)
    dst_path = os.path.join(fonts_dir, font_name)
    
    shutil.copy2(font_path, dst_path)
    print(f"✅ Font {font_name} added to Captions/Fonts directory")
    return True

def load_caption_style(style_name="default"):
    """Loads a caption style from the Caption_Styles folder."""
    style_path = os.path.join(os.path.dirname(__file__), 'Caption_Styles', f"{style_name}.json")
    
    if not os.path.exists(style_path):
        print(f"⚠️ Style '{style_name}' not found. Using default style.")
        return load_caption_style()
        
    with open(style_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_caption_style(style_name, style_config):
    """Saves a caption style to the Caption_Styles folder."""
    styles_dir = os.path.join(os.path.dirname(__file__), 'Caption_Styles')
    os.makedirs(styles_dir, exist_ok=True)
    
    style_path = os.path.join(styles_dir, f"{style_name}.json")
    with open(style_path, "w", encoding="utf-8") as f:
        json.dump(style_config, f, indent=4)
    
    print(f"✅ Caption style '{style_name}' saved.")
    return style_path

def create_text_image(text, video_width, video_height, style=None):
    """Creates an image containing styled text for captions."""
    if style is None:
        style = load_caption_style()
        
    font_size = int(video_height * style.get("font_size_ratio", 0.04))
    padding_x = int(video_width * style.get("padding_x_ratio", 0.02))
    padding_top = int(video_height * style.get("padding_top_ratio", 0.01))
    padding_bottom = int(video_height * style.get("padding_bottom_ratio", 0.02))
    bg_color = tuple(style.get("bg_color", [0, 0, 0, 200]))
    text_color = tuple(style.get("text_color", [255, 255, 255, 255]))
    
    if style.get("uppercase", True):
        text = text.upper()
    
    temp_img = Image.new("RGBA", (video_width, font_size + padding_top + padding_bottom), (0, 0, 0, 0))
    draw = ImageDraw.Draw(temp_img)
    
    font_name = style.get("font", "arial.ttf")
    captions_font_path = os.path.join(os.path.dirname(__file__), 'Fonts', font_name)
    data_font_path = os.path.join("Data", "Fonts", font_name)
    
    try:
        if os.path.exists(captions_font_path):
            font = ImageFont.truetype(captions_font_path, font_size)
        elif os.path.exists(data_font_path):
            font = ImageFont.truetype(data_font_path, font_size)
            add_font(data_font_path)
        else:
            available_fonts = get_available_fonts()
            if available_fonts:
                alternative_font = available_fonts[0]
                print(f"⚠️ Font '{font_name}' not found. Using '{alternative_font}' instead.")
                alt_font_path = os.path.join(os.path.dirname(__file__), 'Fonts', alternative_font)
                font = ImageFont.truetype(alt_font_path, font_size)
            else:
                font = ImageFont.load_default()
                print(f"⚠️ No fonts found. Using default font.")
    except Exception as e:
        print(f"⚠️ Error loading font: {e}. Using default font.")
        font = ImageFont.load_default()
    
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = right - left, bottom - top
    
    bg_width = text_width + 2 * padding_x
    bg_height = text_height + padding_top + padding_bottom
    temp_img = temp_img.resize((bg_width, bg_height))
    draw = ImageDraw.Draw(temp_img)
    
    draw.rectangle([(0, 0), temp_img.size], fill=bg_color)
    
    text_x = (bg_width - text_width) // 2
    text_y = padding_top
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    return np.array(temp_img) 