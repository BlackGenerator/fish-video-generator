#!/usr/bin/env python3
"""
Fish Video Generator - 模型一键下载脚本

功能：
- 下载 Fish-Speech、Kandinsky 2.2、Zeroscope 所需全部模型
- 自动创建标准目录结构
- 支持断点续传与高速传输（hf_transfer）
- 兼容本地运行与 GitHub Actions CI

目录结构输出：
.
├── checkpoints/
│   └── openaudio-s1-mini/          ← Fish-Speech
└── models/
    ├── kandinsky-community/
    │   ├── kandinsky-2-2-prior/
    │   └── kandinsky-2-2-decoder/
    └── cerspense/
        └── zeroscope_v2_576w/      ← Text2Video-Zero
"""

import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download

# ==================== 配置区 ====================
# 基准目录（默认为脚本所在目录的父目录）
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

CHECKPOINTS_DIR = PROJECT_ROOT / "checkpoints"
MODELS_DIR = PROJECT_ROOT / "models"

# Fish-Speech
FISH_SPEECH_REPO = "fishaudio/openaudio-s1-mini"
FISH_SPEECH_PATH = CHECKPOINTS_DIR / "openaudio-s1-mini"

# Kandinsky 2.2
KANDINSKY_PRIOR_REPO = "kandinsky-community/kandinsky-2-2-prior"
KANDINSKY_DECODER_REPO = "kandinsky-community/kandinsky-2-2-decoder"
KANDINSKY_BASE = MODELS_DIR / "kandinsky-community"

# Zeroscope (Text2Video-Zero)
ZEROSCOPE_REPO = "cerspense/zeroscope_v2_576w"
ZEROSCOPE_PATH = MODELS_DIR / "cerspense" / "zeroscope_v2_576w"

# 是否启用 hf_transfer 加速（需 pip install hf_transfer）
ENABLE_HF_TRANSFER = os.environ.get("HF_HUB_ENABLE_HF_TRANSFER", "1") == "1"
# =================================================


def setup_directories():
    """创建必要的目录"""
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ 目录已准备就绪：")
    print(f"   Checkpoints: {CHECKPOINTS_DIR}")
    print(f"   Models:      {MODELS_DIR}\n")


def download_repo(repo_id: str, local_dir: Path, name: str):
    """通用模型下载函数"""
    print(f"📥 正在下载 {name} ({repo_id}) ...")
    try:
        local_dir.parent.mkdir(parents=True, exist_ok=True)
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            resume_download=True,
            token=os.getenv("HF_TOKEN"),  # 支持私有模型
        )
        print(f"✅ {name} 已保存至: {local_dir}\n")
    except Exception as e:
        print(f"❌ {name} 下载失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    print("🚀 Fish Video Generator - 模型下载器\n")

    if ENABLE_HF_TRANSFER:
        # 启用 hf_transfer（如果已安装）
        try:
            import hf_transfer  # noqa: F401
            os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
            print("⚡ 已启用 hf_transfer 高速下载\n")
        except ImportError:
            pass  # 无影响，降级为普通下载

    setup_directories()

    # 1. 下载 Fish-Speech
    download_repo(
        repo_id=FISH_SPEECH_REPO,
        local_dir=FISH_SPEECH_PATH,
        name="Fish-Speech (TTS)"
    )

    # 2. 下载 Kandinsky 2.2 Prior
    download_repo(
        repo_id=KANDINSKY_PRIOR_REPO,
        local_dir=KANDINSKY_BASE / "kandinsky-2-2-prior",
        name="Kandinsky 2.2 Prior"
    )

    # 3. 下载 Kandinsky 2.2 Decoder
    download_repo(
        repo_id=KANDINSKY_DECODER_REPO,
        local_dir=KANDINSKY_BASE / "kandinsky-2-2-decoder",
        name="Kandinsky 2.2 Decoder"
    )

    # 4. 下载 Zeroscope 视频模型
    download_repo(
        repo_id=ZEROSCOPE_REPO,
        local_dir=ZEROSCOPE_PATH,
        name="Zeroscope (Text2Video-Zero)"
    )

    print("🎉 所有模型下载完成！")
    print("\n📌 使用说明：")
    print(f"  • 在 docker-compose.yml 中挂载：")
    print(f"      ./checkpoints:/app/checkpoints")
    print(f"      ./models:/app/models")
    print(f"  • 首次运行 docker-compose up --build")


if __name__ == "__main__":
    main()