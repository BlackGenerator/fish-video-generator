# DALL·E Mini CPU 版本
from fastapi import FastAPI
from dalle_mini import DalleMini
import io
from PIL import Image

app = FastAPI()
model = DalleMini.from_pretrained("dalle-mini/dalle-mini")

@app.post("/generate")
async def generate(request: dict):
    images = model.generate(request["text"], num_images=1)
    img = Image.fromarray(images[0])
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return Response(content=buf.getvalue(), media_type="image/png")