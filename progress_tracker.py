"""
Progress Tracker Module for Text-to-Video Pipeline

This module provides a consistent way to track and display progress
throughout the generation pipeline.
"""

import time
from tqdm import tqdm
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class Stage(Enum):
    INIT = 0
    SCRIPT = 1
    VOICEOVER = 2
    IMAGE_PREP = 3
    IMAGE_GEN = 4
    VIDEO = 5
    CAPTIONS = 6
    CLEANUP = 7
    COMPLETE = 8

class ProgressTracker:
    """Tracks and displays progress throughout the generation pipeline."""
    
    def __init__(self, topic):
        """Initialize a new progress tracker."""
        self.topic = topic
        self.start_time = time.time()
        self.stage_times = {}
        self.current_stage = Stage.INIT
        self.total_steps = len(Stage) - 1
        self.progress_bar = tqdm(total=100, desc="Overall Progress", unit="%")
        self.progress_bar.update(0)
        logger.info(f"Starting video generation for topic: '{topic}'")
        
    def update_stage(self, stage):
        """Update the current generation stage."""
        prev_stage = self.current_stage
        self.current_stage = stage
        
        if prev_stage != Stage.INIT:
            stage_duration = time.time() - self.stage_start_time
            self.stage_times[prev_stage.name] = stage_duration
            logger.info(f"Completed stage {prev_stage.name} in {stage_duration:.2f} seconds")
        
        self.stage_start_time = time.time()
        
        if stage != Stage.INIT:
            progress_percent = (stage.value / self.total_steps) * 100
            self.progress_bar.update(progress_percent - self.progress_bar.n)
            logger.info(f"Starting stage: {stage.name}")
            print(f"\n{self._get_stage_emoji(stage)} Stage: {stage.name}")
    
    def complete(self, output_path=None):
        """Mark the generation as complete."""
        self.update_stage(Stage.COMPLETE)
        total_time = time.time() - self.start_time
        self.progress_bar.update(100 - self.progress_bar.n)
        self.progress_bar.close()
        
        print("\n✅ Generation Complete!")
        print(f"Total time: {self._format_time(total_time)}")
        
        if output_path:
            print(f"Output saved to: {output_path}")
        
        print("\nTiming Summary:")
        for stage, duration in self.stage_times.items():
            print(f"  {stage}: {self._format_time(duration)}")
        
        logger.info(f"Generation complete. Total time: {total_time:.2f} seconds")
        if output_path:
            logger.info(f"Output saved to: {output_path}")
    
    def log_substep(self, message, current=None, total=None):
        """Log a substep within the current stage."""
        if current is not None and total is not None:
            logger.info(f"Progress: {current}/{total} - {message}")
            print(f"  [{current}/{total}] {message}")
        else:
            logger.info(message)
            print(f"  {message}")
    
    def error(self, message, exception=None):
        """Log an error in the current stage."""
        logger.error(message)
        if exception:
            logger.error(f"Exception: {str(exception)}")
        print(f"\n❌ Error: {message}")
    
    def warning(self, message):
        """Log a warning in the current stage."""
        logger.warning(message)
        print(f"\n⚠️ Warning: {message}")
    
    def _format_time(self, seconds):
        """Format time in seconds to a human-readable string."""
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            seconds = seconds % 60
            return f"{minutes}m {seconds:.2f}s"
        else:
            hours = int(seconds // 3600)
            seconds = seconds % 3600
            minutes = int(seconds // 60)
            seconds = seconds % 60
            return f"{hours}h {minutes}m {seconds:.2f}s"
    
    def _get_stage_emoji(self, stage):
        """Get an emoji representing the current stage."""
        emojis = {
            Stage.SCRIPT: "📝",
            Stage.VOICEOVER: "🎙️",
            Stage.IMAGE_PREP: "📋",
            Stage.IMAGE_GEN: "🎨",
            Stage.VIDEO: "🎬",
            Stage.CAPTIONS: "💬",
            Stage.CLEANUP: "🧹",
            Stage.COMPLETE: "✅",
        }
        return emojis.get(stage, "🔄") 