# scripts/download_models.py
import os
from huggingface_hub import hf_hub_download
import urllib.request

REPO_ID = "fishaudio/fish-speech-1.5"
OUTPUT_DIR = "models"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📥 Downloading model weights from Hugging Face...")

# Main model and vocoder
for filename in [
    "model.pth",
    "firefly-gan-vq-fsq-8x1024-21hz-generator.pth",
    "tokenizer.tiktoken"
]:
    hf_hub_download(
        repo_id=REPO_ID,
        filename=filename,
        local_dir=OUTPUT_DIR,
        local_dir_use_symlinks=False,
    )

print("✅ All models downloaded successfully.")
