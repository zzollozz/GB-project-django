import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = BASE_DIR / 'media'