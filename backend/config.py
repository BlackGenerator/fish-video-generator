# backend/config.py
import os

IMAGE_GEN_URL = os.getenv("IMAGE_GEN_URL", "http://image-gen:8000/generate")
VOICE_GEN_URL = os.getenv("VOICE_GEN_URL", "http://voice-gen:8000/generate")
VIDEO_GEN_URL = os.getenv("VIDEO_GEN_URL", "http://video-gen:8000/generate")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/static/outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)