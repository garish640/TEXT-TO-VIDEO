import sys
import os
import shutil
import logging
import traceback
import argparse
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("generation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.dont_write_bytecode = True

from Models.Script.script_factory import load_script_model
from Models.Voiceover.voiceover_factory import load_voiceover_model
from Models.Image.image_factory import load_image_model
from Models.Video.video_factory import load_video_model
from Models.Captions.captions_factory import load_caption_model
from Models.Script.utils import save_formatted_script
from Models.Image.utils import format_for_image_prompt
from config import CAPTION_MODEL, CAPTION_STYLE
from progress_tracker import ProgressTracker, Stage
import time


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Text-to-Video Generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--topic", "-t",
        type=str,
        help="Topic for video generation"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output_video.mp4",
        help="Output filename for the generated video"
    )
    
    parser.add_argument(
        "--no-captions",
        action="store_true",
        help="Skip caption generation"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    parser.add_argument(
        "--skip-cleanup",
        action="store_true",
        help="Skip cleanup of temporary files"
    )
    
    return parser.parse_args()


def main():
    """Main function to orchestrate the text-to-video generation pipeline."""
    args = parse_arguments()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    try:
        if not args.skip_cleanup:
            clear_temp_data()
        ensure_temp_folders()

        topic = args.topic
        if not topic:
            topic = input("Enter a topic for your video: ")
            
        tracker = ProgressTracker(topic)
        
        # 1. Generate Script
        tracker.update_stage(Stage.SCRIPT)
        script_generator = load_script_model()
        tracker.log_substep("Generating script...")
        script = script_generator.generate_script(topic)
        print(f"\nGenerated Script:\n{script}\n")
        
        # 2. Generate Voiceover
        tracker.update_stage(Stage.VOICEOVER)
        voiceover_generator = load_voiceover_model()
        tracker.log_substep("Synthesizing voiceover...")
        audio_path = voiceover_generator.generate_voiceover(script)
        tracker.log_substep(f"Voiceover saved to: {audio_path}")

        # 3. Format script for image generation
        tracker.update_stage(Stage.IMAGE_PREP)
        tracker.log_substep("Formatting script for image generation...")
        formatted_script = save_formatted_script(script)
        
        # 4. Format script for image prompts
        tracker.log_substep("Creating image prompts...")
        image_prompts = format_for_image_prompt(formatted_script)
        tracker.log_substep(f"Created {len(image_prompts)} image prompts")
        
        # 5. Generate Images
        tracker.update_stage(Stage.IMAGE_GEN)
        image_generator = load_image_model()
        image_paths = []
        
        for i, prompt in enumerate(image_prompts):
            tracker.log_substep(f"Generating image", i+1, len(image_prompts))
            image_path = f"image_{i+1}.jpg"
            try:
                image_generator.download_image(prompt, i+1)
                image_paths.append(image_path)
            except Exception as e:
                tracker.error(f"Error generating image {i+1}", e)
            time.sleep(1)
        
        # 6. Generate Video
        tracker.update_stage(Stage.VIDEO)
        tracker.log_substep("Assembling video...")
        video_generator = load_video_model()
        video_path = video_generator.generate_video(topic)
        
        if video_path and args.output and args.output != "output_video.mp4":
            try:
                output_dir = os.path.dirname(video_path)
                new_path = os.path.join(output_dir, args.output)
                os.rename(video_path, new_path)
                video_path = new_path
                tracker.log_substep(f"Video renamed to {args.output}")
            except Exception as e:
                tracker.warning(f"Could not rename output file: {str(e)}")
        
        # 7. Add Captions to Video
        if video_path and not args.no_captions:
            tracker.update_stage(Stage.CAPTIONS)
            tracker.log_substep(f"Adding captions using model: {CAPTION_MODEL}, style: {CAPTION_STYLE}")
            
            caption_generator = load_caption_model(CAPTION_MODEL)
            
            try:
                captioned_video_path = caption_generator.process_video(video_path, CAPTION_STYLE)
                
                if captioned_video_path:
                    video_path = captioned_video_path
                else:
                    tracker.warning("Captioning failed, but original video is available")
            except Exception as e:
                tracker.error(f"Error during captioning", e)
        elif video_path and args.no_captions:
            tracker.log_substep("Skipping caption generation (--no-captions flag)")
        else:
            tracker.error("Video generation failed")

        # Clear the Temp data after Generation
        if not args.skip_cleanup:
            tracker.update_stage(Stage.CLEANUP)
            tracker.log_substep("Cleaning up temporary files...")
            clear_temp_data()
        else:
            tracker.log_substep("Skipping cleanup (--skip-cleanup flag)")
        
        # Complete the process
        tracker.complete(video_path if 'video_path' in locals() and video_path else None)
          
        return {
            "script": formatted_script,
            "audio_path": audio_path,
            "image_paths": image_paths,
            "video_path": video_path if 'video_path' in locals() else None
        }
    
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        logger.error(traceback.format_exc())
        if 'tracker' in locals():
            tracker.error("Fatal error in generation process", e)
        return {"error": str(e)}


def clear_temp_data():
    """Clear temporary data from previous generations."""
    logger.info("Clearing temporary data")
    temp_dir = Path("Data/Temp")
    
    if not temp_dir.exists():
        logger.warning("Temp directory does not exist")
        return
        
    for item in temp_dir.iterdir():
        try:
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            elif item.is_file():
                item.unlink()
        except PermissionError:
            logger.warning(f"Could not remove {item} - Permission denied")
        except Exception as e:
            logger.warning(f"Error clearing {item}: {str(e)}")


def ensure_temp_folders():
    """Ensure all required temporary folders exist."""
    logger.info("Ensuring temporary folders exist")
    for folder in ["Script", "Voiceover", "Generated_Images", "Video", "Timestamps"]:
        folder_path = Path("Data/Temp") / folder
        folder_path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()