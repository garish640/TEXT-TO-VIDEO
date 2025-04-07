from moviepy.video.fx.all import fadein, fadeout

class FadeInFadeOutAnimation:
    def __init__(self):
        pass

    def apply(self, clip, fade_in=True, fade_out=True):
        if fade_in:
            clip = fadein(clip, duration=0.5)
        if fade_out:
            clip = fadeout(clip, duration=0.5)
        return clip
    
class Animation:
    def __init__(self):
        pass
    
    def apply(self, clip, **kwargs):
        fade_in = kwargs.get('fade_in', True)
        fade_out = kwargs.get('fade_out', True)
        return FadeInFadeOutAnimation().apply(clip, fade_in=fade_in, fade_out=fade_out)