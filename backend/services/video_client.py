import requests

def generate_video(image_url: str, audio_url: str, duration: int) -> bytes:
    payload = {
        "image_url": image_url,
        "audio_url": audio_url,
        "duration": duration  # 秒
    }
    
    response = requests.post(
        "http://video-gen:8002/generate",
        json=payload,
        timeout=3600  # 1小时超时（10分钟视频需较长时间）
    )
    response.raise_for_status()
    return response.content