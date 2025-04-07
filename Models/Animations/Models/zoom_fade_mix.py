from moviepy.video.fx.all import fadein, fadeout, crop
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.dont_write_bytecode = True
from Models.Animations.Models.zoom_in_out import zoom_in_out
from Models.Animations.Models.fadein_fadeout import FadeInFadeOutAnimation

class ZoomFadeMixAnimation:
    def __init__(self):
        pass
        
    def apply(self, clip, zoom_in=True, fade_in=True, fade_out=True):
        """Apply both zoom and fade effects to a clip."""
        clip = zoom_in_out(clip, zoom_in=zoom_in)
        
        clip = FadeInFadeOutAnimation().apply(clip, fade_in=fade_in, fade_out=fade_out)
            
        return clip

class Animation:
    def __init__(self):
        pass
        
    def apply(self, clip, **kwargs):
        """Apply the combined zoom and fade effects to the clip."""
        zoom_in = kwargs.get('zoom_in', True)
        fade_in = kwargs.get('fade_in', True)
        fade_out = kwargs.get('fade_out', True)
        
        return ZoomFadeMixAnimation().apply(
            clip, 
            zoom_in=zoom_in,
            fade_in=fade_in,
            fade_out=fade_out
        )
