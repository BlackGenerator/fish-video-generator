#!/usr/bin/env python3
"""
Fish Video Generator - 模型一键下载脚本 (Hugging Face Hub 0.32+)

✅ 兼容最新 hf_xet 加速后端（无需手动配置）
✅ 自动处理门控模型（需 HF_TOKEN）
✅ 标准目录输出，适配 docker-compose

输出结构：
.
├── checkpoints/
│   └── openaudio-s1-mini/          ← Fish-Speech TTS
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

# ==================== 配置 ====================
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

CHECKPOINTS_DIR = PROJECT_ROOT / "checkpoints"
MODELS_DIR = PROJECT_ROOT / "models"

# Fish-Speech (门控模型)
# FISH_SPEECH_REPO = "fishaudio/openaudio-s1-mini"
# FISH_SPEECH_PATH = CHECKPOINTS_DIR / "openaudio-s1-mini"

# Kandinsky 2.2
KANDINSKY_PRIOR_REPO = "kandinsky-community/kandinsky-2-2-prior"
KANDINSKY_DECODER_REPO = "kandinsky-community/kandinsky-2-2-decoder"
KANDINSKY_BASE = MODELS_DIR / "kandinsky-community"

# Zeroscope (Text2Video-Zero)
ZEROSCOPE_REPO = "cerspense/zeroscope_v2_576w"
ZEROSCOPE_PATH = MODELS_DIR / "cerspense" / "zeroscope_v2_576w"
# ==============================================


def ensure_directories():
    """创建输出目录"""
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 目录准备就绪:")
    print(f"   Checkpoints: {CHECKPOINTS_DIR}")
    print(f"   Models:      {MODELS_DIR}\n")


def download_model(repo_id: str, local_dir: Path, name: str):
    """下载单个模型仓库"""
    print(f"📥 正在下载 {name} ({repo_id}) ...")
    try:
        local_dir.parent.mkdir(parents=True, exist_ok=True)
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            resume_download=True,
            token=os.getenv("HF_TOKEN"),  # 必须用于门控模型
        )
        print(f"✅ {name} 已保存至: {local_dir}\n")
    except Exception as e:
        print(f"❌ 下载失败 [{name}]: {e}", file=sys.stderr)
        if "403 Client Error" in str(e) or "access" in str(e).lower():
            print("\n💡 提示：此模型为门控模型，请确保：")
            print("  1. 已在 https://huggingface.co/fishaudio/openaudio-s1-mini 点击 'Agree and access'")
            print("  2. 设置了 HF_TOKEN 环境变量")
        sys.exit(1)


def main():
    print("🚀 Fish Video Generator - 模型下载器 (Hugging Face Hub 0.32+)\n")

    # 自动检测 huggingface_hub 版本
    import huggingface_hub
    print(f"📦 huggingface_hub 版本: {huggingface_hub.__version__}")
    if tuple(map(int, huggingface_hub.__version__.split(".")[:2])) < (0, 32):
        print("⚠️  警告：建议升级到 huggingface_hub>=0.32.0 以获得最佳性能\n")
    else:
        print("⚡ 已启用 hf_xet 加速（如仓库支持）\n")

    ensure_directories()

    # 1. Fish-Speech (门控)
    # download_model(
    #     repo_id=FISH_SPEECH_REPO,
    #     local_dir=FISH_SPEECH_PATH,
    #     name="Fish-Speech (TTS)"
    # )

    # 2. Kandinsky Prior
    download_model(
        repo_id=KANDINSKY_PRIOR_REPO,
        local_dir=KANDINSKY_BASE / "kandinsky-2-2-prior",
        name="Kandinsky 2.2 Prior"
    )

    # 3. Kandinsky Decoder
    download_model(
        repo_id=KANDINSKY_DECODER_REPO,
        local_dir=KANDINSKY_BASE / "kandinsky-2-2-decoder",
        name="Kandinsky 2.2 Decoder"
    )

    # 4. Zeroscope Video Model
    download_model(
        repo_id=ZEROSCOPE_REPO,
        local_dir=ZEROSCOPE_PATH,
        name="Zeroscope (Text2Video-Zero)"
    )

    print("🎉 所有模型下载完成！")
    print("\n📌 使用说明：")
    print("  在 docker-compose.yml 中挂载：")
    print("    ./checkpoints:/app/checkpoints")
    print("    ./models:/app/models")


if __name__ == "__main__":
    main()
