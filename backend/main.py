from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from redis import Redis
from rq import Queue
import uuid
import shutil
from pathlib import Path
from models import TaskResponse, TaskStatus
from tasks import async_generate_image, async_clone_voice, async_generate_video

app = FastAPI(title="Text-to-Video API")
app.mount("/outputs", StaticFiles(directory="static/outputs"), name="outputs")

redis_conn = Redis(host="redis", port=6379)
queue = Queue("default", connection=redis_conn)

@app.post("/api/image/generate", response_model=TaskResponse)
async def generate_image_api(text: str = Form(...)):
    task_id = f"img_{uuid.uuid4().hex}"
    queue.enqueue(async_generate_image, task_id, text, job_timeout='600')
    return {"task_id": task_id}

@app.post("/api/voice/clone", response_model=TaskResponse)
async def clone_voice_api(
    text: str = Form(...),
    audio: UploadFile = File(...)
):
    if not audio.filename.endswith(('.wav', '.mp3')):
        raise HTTPException(400, "Only WAV/MP3 allowed")
    
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    audio_path = upload_dir / f"{uuid.uuid4()}_{audio.filename}"
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)
    
    task_id = f"voice_{uuid.uuid4().hex}"
    queue.enqueue(
        async_clone_voice,
        task_id,
        text,
        str(audio_path),
        job_timeout='1800'  # 30分钟
    )
    return {"task_id": task_id}

@app.post("/api/video/generate", response_model=TaskResponse)
async def generate_video_api(
    image_url: str = Form(...),
    audio_url: str = Form(...),
    duration: int = Form(600)  # 默认10分钟
):
    task_id = f"video_{uuid.uuid4().hex}"
    queue.enqueue(
        async_generate_video,
        task_id,
        image_url,
        audio_url,
        duration,
        job_timeout='7200'  # 2小时
    )
    return {"task_id": task_id}

@app.get("/api/task/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    job = queue.fetch_job(task_id)
    if not job:
        raise HTTPException(404, "Task not found")
    
    meta = job.meta or {}
    return TaskStatus(
        status=meta.get("status", job.get_status()),
        result_url=meta.get("result_url"),
        error=meta.get("error")
    )