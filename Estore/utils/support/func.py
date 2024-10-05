from typing import Optional
from pathlib import Path

from PIL import Image


def resize_image(img_path: str | bytes | Path, w: int, h: Optional[int] = None):
    """resize the given image.
    if the given w or h is bigger than the original value the minimum size will
    be used.

    Args:
        img_path (Any): image source
        w (int): width
        h (int, optional): height. Defaults to None.
    """
    img = Image.open(img_path)
    original_w, original_h = img.size


    if h is None:
        h = round(w * original_h / original_w)
    
    if original_h <= h and original_w <= w:
        return
    
    w, h = min(w, original_w), min(h, original_h)

    resized = img.resize((w, h), Image.Resampling.NEAREST)
    resized.save(img_path, optimize=True, quality=70)

    resized.close()
    img.close()
