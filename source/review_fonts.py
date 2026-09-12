"""Portable fonts for generated diagnostic labels (not building signage)."""
from pathlib import Path
from PIL import ImageFont
import os


def review_font(size=20):
    candidates = [os.environ.get('REVIEW_FONT'), 'DejaVuSans.ttf',
                  '/System/Library/Fonts/Supplemental/Arial.ttf',
                  str(Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/arial.ttf')]
    for path in candidates:
        if path:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default(size=size)
