import requests
from config import IMAGE_GEN_URL

def generate_image(text: str) -> bytes:
    response = requests.post(
        f"{IMAGE_GEN_URL}/generate",
        json={"text": text},
        timeout=300  # 5分钟超时
    )
    response.raise_for_status()
    return response.content