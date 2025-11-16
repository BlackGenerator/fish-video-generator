import os
from pathlib import Path
from rq import get_current_job
from services.image_client import generate_image
from services.voice_client import clone_voice
from services.video_client import generate_video

OUTPUT_DIR = Path("/app/static/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def async_generate_image(task_id: str, text: str):
    job = get_current_job()
    try:
        job.meta.update({"status": "processing", "stage": "image"})
        job.save_meta()
        
        image_data = generate_image(text)
        output_path = OUTPUT_DIR / f"{task_id}.png"
        with open(output_path, "wb") as f:
            f.write(image_data)
            
        job.meta.update({
            "status": "completed",
            "result_url": f"/outputs/{task_id}.png"
        })
        job.save_meta()
    except Exception as e:
        job.meta.update({"status": "failed", "error": str(e)})
        job.save_meta()

def async_clone_voice(task_id: str, text: str, audio_path: str):
    job = get_current_job()
    try:
        job.meta.update({"status": "processing", "stage": "voice"})
        job.save_meta()
        
        audio_data = clone_voice(text, audio_path)
        output_path = OUTPUT_DIR / f"{task_id}.wav"
        with open(output_path, "wb") as f:
            f.write(audio_data)
            
        job.meta.update({
            "status": "completed",
            "result_url": f"/outputs/{task_id}.wav"
        })
        job.save_meta()
    except Exception as e:
        job.meta.update({"status": "failed", "error": str(e)})
        job.save_meta()

def async_generate_video(task_id: str, image_url: str, audio_url: str, duration: int):
    job = get_current_job()
    try:
        job.meta.update({"status": "processing", "stage": "video"})
        job.save_meta()
        
        video_data = generate_video(image_url, audio_url, duration)
        output_path = OUTPUT_DIR / f"{task_id}.mp4"
        with open(output_path, "wb") as f:
            f.write(video_data)
            
        job.meta.update({
            "status": "completed",
            "result_url": f"/outputs/{task_id}.mp4"
        })
        job.save_meta()
    except Exception as e:
        job.meta.update({"status": "failed", "error": str(e)})
        job.save_meta()