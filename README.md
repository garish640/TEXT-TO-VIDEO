ai lucky l# Text to Video Generator

A comprehensive pipeline that converts text prompts into engaging short-form videos with voiceovers and captions.

## 🌟 Features

- **Script Generation**: Create engaging scripts using AI models (DDC or Gemini)
- **Voiceover Synthesis**: Generate natural-sounding voiceovers
- **Image Generation**: Create images from script segments
- **Video Creation**: Assemble images into a video with animations
- **Caption Generation**: Add automatically generated captions in different styles
- **Progress Tracking**: Monitor the generation process with a visual progress indicator

## 📋 Requirements

```
python-dotenv==1.0.1
requests==2.32.3
openai==1.0.0
google-generativeai==0.8.4
whisperx==3.3.1
moviepy==1.0.3
ffmpeg-python==0.2.0
python-json-logger>=2.0.7
tqdm>=4.66.1
pillow>=10.0.0
numpy>=1.24.0
torch>=2.0.0
edge-tts>=6.1.9
```

## 🚀 Quick Start

1. Clone the repository
2. Create and activate a virtual environment:
   ```
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your API keys in `.env`:
   ```
   DDC_API_KEY=your_ddc_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```
4. Run the generator:
   ```
   python main.py --topic "Your topic here"
   ```

## 🛠️ Command Line Arguments

- `--topic`, `-t`: Topic for video generation
- `--output`, `-o`: Output filename (default: "output_video.mp4")
- `--no-captions`: Skip caption generation
- `--debug`: Enable debug logging
- `--skip-cleanup`: Skip cleanup of temporary files

## 📁 Project Structure

```
├── main.py                # Main entry point
├── config.py              # Configuration settings
├── progress_tracker.py    # Progress tracking utilities
├── .env                   # Environment variables (API keys)
├── requirements.txt       # Project dependencies
├── Models/                # Model implementations
│   ├── Script/            # Script generation models
│   ├── Voiceover/         # Voiceover generation models
│   ├── Image/             # Image generation models
│   ├── Video/             # Video creation models
│   ├── Captions/          # Caption generation models
│   └── Animations/        # Animation effect models
└── Data/                  # Data storage
    └── Temp/              # Temporary files during generation
```

## ⚙️ Configuration

You can customize the generation pipeline by modifying `config.py`:

- `SCRIPT_MODEL`: Model for script generation (e.g., "ddc")
- `IMG_MODEL`: Model for image generation (e.g., "pixelmuse")
- `AUDIO_MODEL`: Model for voiceover generation (e.g., "openfm")
- `AUDIO_MODEL_VOICE`: Voice to use for voiceover (e.g., "shimmer")
- `ANIMATION`: Animation style (e.g., "zoom_fade_mix")
- `VIDEO_MODEL`: Video creation model (e.g., "moviepy")
- `CAPTION_MODEL`: Caption generation model (e.g., "whisperx")
- `CAPTION_STYLE`: Caption style (e.g., "comic_style")

## 🔄 Pipeline Flow

1. **Script Generation**: Create an engaging script based on the input topic
2. **Voiceover Generation**: Convert the script to audio using text-to-speech
3. **Image Preparation**: Format the script for image generation
4. **Image Generation**: Create visuals for each script segment
5. **Video Creation**: Assemble images with animations and audio
6. **Caption Generation**: Add captions to the video
7. **Cleanup**: Remove temporary files

## 🧩 Extending the Project

You can extend the project by:

1. Adding new script generation models in `Models/Script/Models/`
2. Adding new voiceover models in `Models/Voiceover/Models/`
3. Adding new image generation models in `Models/Image/Models/`
4. Adding new video creation models in `Models/Video/Models/`
5. Adding new caption models in `Models/Captions/Models/`
6. Adding new animation styles in `Models/Animations/Models/`

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Feel free to submit pull requests or open issues to improve the project.

## 🧑‍💻 Developer

Developed with 💘 by Krish.
