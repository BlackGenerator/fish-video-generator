from fastapi import FastAPI, HTTPException, Response
from diffusers import KandinskyV22Pipeline, KandinskyV22PriorPipeline
import torch
from PIL import Image
import io

app = FastAPI(title="Kandinsky 2.2 Image Generator")

# 全局加载模型（首次启动慢，后续快）
print("Loading Kandinsky 2.2 models...")

# Prior pipeline (text → image embedding)
prior_pipe = KandinskyV22PriorPipeline.from_pretrained(
    "kandinsky-community/kandinsky-2-2-prior",
    torch_dtype=torch.float32,
    use_safetensors=True
).to("cpu")

# Decoder pipeline (embedding → image)
decoder_pipe = KandinskyV22Pipeline.from_pretrained(
    "kandinsky-community/kandinsky-2-2-decoder",
    torch_dtype=torch.float32,
    use_safetensors=True
).to("cpu")

@app.post("/generate")
async def generate(payload: dict):
    prompt = payload.get("text", "").strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Text prompt is required")

    try:
        # Step 1: Generate image embedding from text
        image_emb = prior_pipe(prompt).image_embeds

        # Step 2: Decode embedding to image
        image = decoder_pipe(
            image_embeds=image_emb,
            num_inference_steps=20,
            height=768,
            width=768,
        ).images[0]

        # Return as PNG
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)
        return Response(content=buf.getvalue(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")