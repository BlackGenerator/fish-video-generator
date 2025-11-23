# 使用官方 Python 镜像（轻量级）
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（FFmpeg 用于视频拼接与编码，OpenCV 可选）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libglib2.0-0 \
        libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装 Python 包
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip && \
    pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 安装 Text2Video-Zero 所需的额外依赖（若未包含在 requirements.txt 中）
# 注意：diffusers 和 transformers 已在 requirements.txt 中声明更佳
# RUN pip install accelerate diffusers transformers torch torchvision torchaudio

# 复制应用代码
COPY app.py .

# 暴露服务端口
EXPOSE 8000

# 启动命令（使用 uvicorn 运行 FastAPI）
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]