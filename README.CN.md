# 🐟 Fish 视频生成器

> **输入一段文字，自动生成带语音解说的视频 —— 全开源、仅需 CPU、可完全私有部署**

无需 GPU，无需联网 API，无需付费。  
在您自己的电脑或服务器上，一键运行整套 AI 视频生成系统。

[![许可证](https://img.shields.io/badge/许可证-Apache%202.0-蓝色.svg)](LICENSE)  
[![CI/CD](https://github.com/BlackGenerator/fish-video-generator/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/BlackGenerator/fish-video-generator/actions)  
[![前端镜像大小](https://img.shields.io/docker/image-size/ghcr.io/blackgenerator/fish-video-generator/frontend/latest?label=前端)](https://github.com/orgs/blackgenerator/packages)

---

## 🌟 核心特性

- ✅ **文本 → 带语音的视频** 一站式生成  
- ✅ **纯 CPU 运行**：8GB 内存即可启动（推荐 16GB）  
- ✅ **现代化 Vue 3 前端界面**：支持实时预览、一键下载  
- ✅ **模块化微服务架构**：可自由替换图像/语音/视频组件  
- ✅ **Docker 一键部署**：开发、测试、生产环境一致  
- ✅ **自动化 CI/CD**：每次提交自动构建并发布 Docker 镜像  
- ✅ **全开源 + 宽松许可证**：Apache 2.0 / MIT，支持商用（部分模型除外）

---

## 🧠 技术栈

| 模块 | 技术 |
|------|------|
| **前端界面** | Vue 3 + Vite + 响应式 CSS |
| **后端调度** | FastAPI + RQ（任务队列） |
| **图像生成** | Kandinsky 2.2（`kandinsky-community/kandinsky-2-2`） |
| **语音合成** | Fish-Speech v1.4（`fishaudio/fish-speech`） |
| **视频合成** | Text2Video-Zero（`cerspense/zeroscope_v2_576w`） |
| **部署方式** | Docker Compose |
| **持续集成** | GitHub Actions → GHCR（GitHub 容器注册表） |

---

## 🚀 快速开始

### 前置要求
- 已安装 **Docker 与 Docker Compose v2+**
- 至少 **8 GB 内存**（推荐 16 GB）
- 约 **12 GB 可用磁盘空间**（用于下载模型权重）

### 本地运行

```bash
git clone https://github.com/BlackGenerator/fish-video-generator.git
cd fish-video-generator

# 启动所有服务（首次运行会自动下载约 5GB 模型）
docker-compose up --build
```

> ⏱️ **首次启动需 5–10 分钟**（后续启动秒级，模型已缓存）。

### 使用 Web 界面

打开浏览器访问：  
👉 **http://localhost**

输入提示词，例如：  
> “一只赛博朋克风格的猫骑着霓虹滑板穿梭在东京夜景中”

点击 **“创建视频”** → 等待 30–90 秒 → 即可观看并下载！

---

## 📂 项目结构

```
fish-video-generator/
├── backend/               # 后端 API 与任务调度
├── services/
│   ├── image-gen/         # 图像生成服务（Kandinsky 2.2）
│   └── video-gen/         # 视频合成服务（Text2Video-Zero）
├── frontend/              # Vue 3 前端（替代旧版 index.html）
├── static/outputs/        # 生成的视频文件存储目录
├── docker-compose.yml     # 主部署配置文件
└── .github/workflows/ci-cd.yml  # 自动构建与发布流程
```

> 💡 注：`fish-speech` 作为独立服务在 `docker-compose.yml` 中定义。

---

## 🛠️ 自定义配置

编辑 `docker-compose.yml` 可调整参数：

| 环境变量 | 默认值 | 说明 |
|--------|-------|------|
| `VIDEO_DURATION` | `30` | 视频最大时长（秒） |
| `AUDIO_LANG` | `en` | 语音语言（`en` 英语, `zh` 中文, `ja` 日语等） |
| `IMAGE_SIZE` | `768` | 图像输出分辨率 |

示例：
```yaml
backend:
  environment:
    - VIDEO_DURATION=60
    - AUDIO_LANG=zh
```

---

## 📦 模型许可证说明

| 模型 | 许可证 | 是否可用于商业 |
|------|--------|----------------|
| Kandinsky 2.2 | Apache 2.0 | ✅ 是 |
| Fish-Speech | MIT | ✅ 是 |
| Zeroscope (Text2Video-Zero) | CC BY-NC-SA 4.0 | ❌ 否（非商业） |

> ⚠️ 如需商业用途，请替换 `video-gen` 服务为商用友好的视频生成模型。

---

## 🔄 自动化构建与部署（CI/CD）

每次向 `main` 分支推送代码时，GitHub Actions 会自动：
1. 代码格式检查
2. 构建多平台 Docker 镜像（支持 Intel/AMD 和 Apple Silicon）
3. 推送至 **GitHub 容器注册表（GHCR）**：

- `ghcr.io/blackgenerator/fish-video-generator/frontend:latest`
- `ghcr.io/blackgenerator/fish-video-generator/backend:latest`
- `.../image-gen`, `.../video-gen`

您也可以直接拉取生产镜像运行：
```bash
docker run -p 80:80 ghcr.io/blackgenerator/fish-video-generator/frontend:latest
```

---

## 🤝 贡献指南

欢迎贡献！以下方向尤其需要帮助：
- 集成 **Stable Diffusion Video** 或 **Kandinsky 3.0**
- 为 CPU 推理添加 **ONNX 量化加速**
- 开发配套 **移动端 App**
- 增加 **用户账户系统** 与 **历史记录**

请通过 Issue 或 Pull Request 提交您的想法！

---

## 📜 许可证

本项目代码采用 **Apache License 2.0** 开源协议。

> 注意：虽然项目代码可商用，但部分所用模型有独立许可证。商用前请务必确认各模型授权条款。

---

## 🙏 致谢

- [Kandinsky 2.2](https://github.com/ai-forever/Kandinsky-2) – AI Forever 团队  
- [Fish-Speech](https://github.com/fishaudio/fish-speech) – Fish Audio  
- [Text2Video-Zero](https://github.com/Picsart-AI-Research/Text2Video-Zero) – Picsart AI Research  
- [Vue 3](https://vuejs.org/) – 尤雨溪及社区  
- [FastAPI](https://fastapi.tiangolo.com/) – Sebastián Ramírez  

---

> 🐟 **让每一位创作者都能拥有私有、开源、可控的 AI 视频生成能力。**  
> 无追踪，无遥测，无套路 —— 纯粹的技术共享。