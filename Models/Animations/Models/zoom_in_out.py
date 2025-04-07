from moviepy.video.fx.all import crop

def zoom_in_out(clip, zoom_in=True):
        """Apply a smooth zoom-in or zoom-out effect while keeping it centered."""
        w, h = clip.size

        def zoom_effect(get_frame, t):
            zoom_factor = 1 + (0.2 * (t / clip.duration)) if zoom_in else 1.2 - (0.2 * (t / clip.duration))
            zoomed_clip = clip.resize(zoom_factor)

            new_w, new_h = zoomed_clip.size
            x_center, y_center = new_w // 2, new_h // 2
            return crop(zoomed_clip, width=w, height=h, x_center=x_center, y_center=y_center).get_frame(t)

        return clip.fl(zoom_effect)
        
class Animation:
    def __init__(self):
        pass
        
    def apply(self, clip, **kwargs):
        """Apply the zoom effect to the clip based on index in sequence"""
        zoom_in = kwargs.get('zoom_in', True)
        return zoom_in_out(clip, zoom_in=zoom_in)