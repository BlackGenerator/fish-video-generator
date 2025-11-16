import requests
import base64

def clone_voice(text: str, audio_path: str) -> bytes:
    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()
    
    payload = {
        "text": text,
        "reference_audio": audio_b64,
        "format": "wav"
    }
    
    response = requests.post(
        "http://fish-speech:8000/v1/tts",
        json=payload,
        timeout=600  # 10分钟超时
    )
    response.raise_for_status()
    return response.content