from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import DiffusionPipeline
import torch
import numpy as np
from moviepy.editor import ImageSequenceClip
import os
from pathlib import Path
from typing import List
import tempfile

app = FastAPI(title="Text2Video-Zero Service")

# 初始化模型（CPU 版本）
print("Loading Text2Video-Zero model...")
model_id = "cerspense/zeroscope_v2_576w"
pipe = DiffusionPipeline.from_pretrained(model_id)
pipe.to("cpu")  # 强制使用 CPU 推理

class VideoRequest(BaseModel):
    prompt: str
    duration: float = 10.0  # 默认持续时间为 10 秒
    fps: int = 8  # 帧率，默认为 8 FPS

@app.post("/generate")
async def generate_video(req: VideoRequest):
    """
    Generate a video from text prompt.
    
    Parameters:
    - prompt: The text description of the video.
    - duration: Duration of the video in seconds (default 10).
    - fps: Frames per second (default 8).
    """
    try:
        # 计算需要生成的帧数
        num_frames = int(req.duration * req.fps)

        # 使用 Text2Video-Zero 生成帧序列
        frames = pipe(
            prompt=req.prompt,
            num_inference_steps=20,  # 调整步数以平衡速度和质量
            num_frames=num_frames,
            guidance_scale=9.0
        ).frames[0]

        # 将帧转换为 PIL 图像列表
        pil_images = [torch_to_pil(frame) for frame in frames]

        # 使用 MoviePy 创建视频剪辑
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / f"video_{hash(req.prompt)}{req.duration}.mp4"
            clip = ImageSequenceClip(pil_images, fps=req.fps)
            clip.write_videofile(str(output_path), codec="libx264", audio=False)

            # 返回视频文件路径
            return {"video_url": str(output_path)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

def torch_to_pil(tensor_image):
    """Converts a PyTorch tensor image to a PIL Image."""
    image_np = (tensor_image.cpu().numpy() * 255).astype(np.uint8)
    if image_np.shape[0] == 1:
        image_np = np.squeeze(image_np, axis=0)
    elif image_np.shape[0] == 3:
        image_np = np.moveaxis(image_np, 0, -1)
    return Image.fromarray(image_np)