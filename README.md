当然！以下是根据您项目最新架构（含 Vue 前端、Kandinsky 2.2 图像生成、Fish-Speech 语音合成、Text2Video-Zero 视频生成、Docker Compose 部署、GitHub Actions CI/CD）全面更新的 **README.md**：

---

# 🐟 Fish Video Generator

> **Generate narrated videos from text — all open-source, CPU-only, and self-hostable**

Type a sentence → Get a video with voiceover.  
No GPU. No cloud APIs. No paywalls.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![CI/CD](https://github.com/BlackGenerator/fish-video-generator/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/BlackGenerator/fish-video-generator/actions)
[![Docker Image Size (tag)](https://img.shields.io/docker/image-size/ghcr.io/blackgenerator/fish-video-generator/frontend/latest?label=frontend)](https://github.com/orgs/blackgenerator/packages)

---

## 🌟 Features

- ✅ **Text-to-Video + Voiceover** in one pipeline  
- ✅ **Runs on CPU only** – works on laptops, cloud VMs (8GB+ RAM)  
- ✅ **Modern Vue 3 frontend** with real-time preview & download  
- ✅ **Modular microservices**: swap any component (image/voice/video)  
- ✅ **Fully containerized** with Docker Compose  
- ✅ **Automated CI/CD** – images published to GHCR on every push  
- ✅ **Open weights & permissive licenses** (Apache 2.0 / MIT)

---

## 🧠 Tech Stack

| Component | Technology |
|----------|------------|
| **Frontend** | Vue 3 + Vite + Tailwind-like CSS |
| **Backend** | FastAPI + RQ (task queue) |
| **Image Gen** | Kandinsky 2.2 (`kandinsky-community/kandinsky-2-2`) |
| **Voice Synth** | Fish-Speech v1.4 (`fishaudio/fish-speech`) |
| **Video Gen** | Text2Video-Zero (`cerspense/zeroscope_v2_576w`) |
| **Orchestration** | Docker Compose |
| **CI/CD** | GitHub Actions → GHCR |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose v2+
- At least **8 GB RAM** (16 GB recommended)
- ~12 GB free disk space (for model weights)

### Run Locally

```bash
git clone https://github.com/BlackGenerator/fish-video-generator.git
cd fish-video-generator

# Start all services (first run downloads models ~5GB)
docker-compose up --build
```

> ⏱️ **First launch takes 5–10 minutes** (models are cached afterward).

### Use the Web UI

Open your browser:  
👉 **http://localhost**

Enter a prompt like:  
> “A cyberpunk cat riding a neon scooter through Tokyo at night”

Click **“Create Video”** → Wait 30–90 seconds → Watch & download!

---

## 📂 Project Structure

```
fish-video-generator/
├── backend/               # API orchestration & task queue
├── services/
│   ├── image-gen/         # Kandinsky 2.2 (text → image)
│   └── video-gen/         # Text2Video-Zero (image + audio → video)
├── frontend/              # Vue 3 web UI (replaces old index.html)
├── static/outputs/        # Generated videos stored here
├── docker-compose.yml     # Main deployment manifest
└── .github/workflows/ci-cd.yml  # Auto-builds Docker images
```

> 💡 **Note**: `fish-speech` runs as an external service (see `docker-compose.yml`).

---

## 🛠️ Configuration

Edit `docker-compose.yml` to customize:

| Environment Variable | Default | Description |
|----------------------|--------|-------------|
| `VIDEO_DURATION` | `30` | Max video length (seconds) |
| `AUDIO_LANG` | `en` | Voice language (`en`, `zh`, `ja`, etc.) |
| `IMAGE_SIZE` | `768` | Output resolution (Kandinsky) |

Example:
```yaml
backend:
  environment:
    - VIDEO_DURATION=60
    - AUDIO_LANG=zh
```

---

## 📦 Model Licenses

| Model | License | Commercial Use |
|-------|--------|----------------|
| Kandinsky 2.2 | Apache 2.0 | ✅ Yes |
| Fish-Speech | MIT | ✅ Yes |
| Zeroscope (Text2Video-Zero) | CC BY-NC-SA 4.0 | ❌ No |

> ⚠️ For commercial deployments, replace `video-gen` with a commercial-friendly video model.

---

## 🔄 CI/CD Pipeline

On every push to `main`:
1. Lints code
2. Builds multi-arch Docker images (`linux/amd64`, `linux/arm64`)
3. Pushes to **GitHub Container Registry (GHCR)**:
   - `ghcr.io/blackgenerator/fish-video-generator/frontend:latest`
   - `ghcr.io/blackgenerator/fish-video-generator/backend:latest`
   - `.../image-gen`, `.../video-gen`

You can pull and run production images directly:
```bash
docker run -p 80:80 ghcr.io/blackgenerator/fish-video-generator/frontend:latest
```

---

## 🤝 Contributing

We welcome contributions! Ideas:
- Add **Stable Diffusion Video** or **Kandinsky 3.0** support
- Implement **ONNX quantization** for faster CPU inference
- Build a **mobile app** using the same backend
- Add **user accounts & history**

Please open an issue or PR!

---

## 📜 License

This project is licensed under **Apache License 2.0**.

> Note: While the *code* is Apache 2.0, some *models* have different licenses. Review model licenses before commercial use.

---

## 🙏 Acknowledgements

- [Kandinsky 2.2](https://github.com/ai-forever/Kandinsky-2) – AI Forever  
- [Fish-Speech](https://github.com/fishaudio/fish-speech) – Fish Audio  
- [Text2Video-Zero](https://github.com/Picsart-AI-Research/Text2Video-Zero) – Picsart AI Research  
- [Vue 3](https://vuejs.org/) – Evan You et al.  
- [FastAPI](https://fastapi.tiangolo.com/) – Sebastián Ramírez  

---

> 🐟 **Empowering creators with open, local, and private AI video generation.**  
> Made with ❤️ — no tracking, no telemetry, no nonsense.