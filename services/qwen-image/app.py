from modelscope import DiffusionPipeline
import torch
from flask import Flask, request, jsonify, send_file
import os
import io
from PIL import Image
import logging
import time

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 从环境变量获取配置
MODEL_PATH = os.getenv("MODEL_PATH", "/app/model")  # 可以是模型ID或本地路径
DEVICE = os.getenv("DEVICE", "cpu")
DEFAULT_WIDTH = int(os.getenv("DEFAULT_WIDTH", 1664))
DEFAULT_HEIGHT = int(os.getenv("DEFAULT_HEIGHT", 928))
DEFAULT_STEPS = int(os.getenv("DEFAULT_STEPS", 50))
DEFAULT_CFG_SCALE = float(os.getenv("DEFAULT_CFG_SCALE", 4.0))
DEFAULT_SEED = int(os.getenv("DEFAULT_SEED", 42))

# 正向提示增强
POSITIVE_MAGIC = {
    "en": ", Ultra HD, 4K, cinematic composition.",
    "zh": ", 超清，4K，电影级构图."
}

# 支持的宽高比
ASPECT_RATIOS = {
    "1:1": (1328, 1328),
    "16:9": (1664, 928),
    "9:16": (928, 1664),
    "4:3": (1472, 1140),
    "3:4": (1140, 1472),
    "3:2": (1584, 1056),
    "2:3": (1056, 1584),
    "21:9": (2048, 896),
    "custom": None  # 自定义尺寸
}

# 确定设备和数据类型
if DEVICE == "cpu" or not torch.cuda.is_available():
    TORCH_DTYPE = torch.float32
    DEVICE = "cpu"
    logger.info("Using CPU for inference with float32 precision")
else:
    # 检查设备是否支持bfloat16
    if torch.cuda.is_bf16_supported():
        TORCH_DTYPE = torch.bfloat16
        logger.info("Using GPU with bfloat16 precision")
    else:
        TORCH_DTYPE = torch.float16
        logger.info("Using GPU with float16 precision")
    
    # 设置设备索引（如果指定）
    if DEVICE != "cuda" and DEVICE.startswith("cuda:"):
        device_idx = DEVICE.split(":")[1]
        torch.cuda.set_device(int(device_idx))
    DEVICE = "cuda"

# 加载模型
logger.info(f"Loading Qwen-Image model from '{MODEL_PATH}' with dtype={TORCH_DTYPE} on device={DEVICE}")

try:
    # 使用modelscope的DiffusionPipeline
    pipe = DiffusionPipeline.from_pretrained(
        MODEL_PATH,
        torch_dtype=TORCH_DTYPE,
        custom_pipeline="qwen_image"  # 指定Qwen-Image专用pipeline
    )
    
    # 移动到指定设备
    pipe = pipe.to(DEVICE)
    
    # CPU优化
    if DEVICE == "cpu":
        logger.info("Applying CPU optimizations")
        pipe.unet.to(memory_format=torch.channels_last)
    
    # 启用xformers内存高效注意力（如果可用）
    try:
        pipe.enable_xformers_memory_efficient_attention()
        logger.info("Enabled xformers memory efficient attention")
    except Exception as e:
        logger.info(f"xformers not available: {str(e)}")
    
    # 启用注意力切片，减少内存使用
    pipe.enable_attention_slicing()
    logger.info("Enabled attention slicing for memory optimization")
    
    logger.info("Qwen-Image model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load Qwen-Image model: {str(e)}")
    logger.exception("Full traceback:")
    raise

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "device": DEVICE,
        "model_path": MODEL_PATH,
        "dtype": str(TORCH_DTYPE),
        "supported_aspect_ratios": list(ASPECT_RATIOS.keys()),
        "memory_allocated": f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB" if DEVICE != "cpu" else "N/A"
    })

@app.route('/generate', methods=['POST'])
def generate_image():
    start_time = time.time()
    data = request.get_json()
    
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing prompt in request"}), 400
    
    # 获取请求参数
    prompt = data.get('prompt', '')
    aspect_ratio = data.get('aspect_ratio', '16:9')
    negative_prompt = data.get('negative_prompt', " ")
    steps = int(data.get('steps', DEFAULT_STEPS))
    cfg_scale = float(data.get('cfg_scale', DEFAULT_CFG_SCALE))
    seed = int(data.get('seed', DEFAULT_SEED))
    
    # 确定语言以应用相应的正向增强
    language = "zh" if any('\u4e00' <= char <= '\u9fff' for char in prompt) else "en"
    prompt += POSITIVE_MAGIC[language]
    
    # 处理分辨率
    if aspect_ratio in ASPECT_RATIOS and ASPECT_RATIOS[aspect_ratio] is not None:
        width, height = ASPECT_RATIOS[aspect_ratio]
    else:
        # 自定义分辨率
        width = int(data.get('width', DEFAULT_WIDTH))
        height = int(data.get('height', DEFAULT_HEIGHT))
        
        # 验证分辨率
        min_dim, max_dim = 512, 2048
        width = max(min_dim, min(width, max_dim))
        height = max(min_dim, min(height, max_dim))
        
        # 确保尺寸是64的倍数（Qwen-Image要求）
        width = round(width / 64) * 64
        height = round(height / 64) * 64
    
    # 验证步数
    steps = max(20, min(steps, 100))
    
    logger.info(f"Generating image with prompt: '{prompt}' at {width}x{height}, steps={steps}, cfg_scale={cfg_scale}, seed={seed}")
    
    try:
        # 创建生成器
        generator = torch.Generator(device=DEVICE).manual_seed(seed)
        
        # 生成图像 - 包含Qwen-Image特有的参数
        result = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
            true_cfg_scale=cfg_scale,  # Qwen-Image特有的参数
            generator=generator
        )
        
        image = result.images[0]
        
        # 保存到内存
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        
        elapsed = time.time() - start_time
        logger.info(f"Image generated successfully in {elapsed:.2f} seconds")
        
        # 添加性能指标到响应头
        response = send_file(img_io, mimetype='image/png')
        response.headers['X-Generation-Time'] = f"{elapsed:.2f}"
        response.headers['X-Resolution'] = f"{width}x{height}"
        response.headers['X-Steps'] = str(steps)
        return response
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({
            "error": str(e),
            "hint": "Check model loading and ensure you have sufficient memory"
        }), 500

@app.route('/aspect_ratios', methods=['GET'])
def get_aspect_ratios():
    """返回支持的宽高比列表及其对应分辨率"""
    result = {}
    for ratio, size in ASPECT_RATIOS.items():
        if size is not None:
            result[ratio] = {"width": size[0], "height": size[1]}
        else:
            result[ratio] = "custom"
    return jsonify(result)

if __name__ == '__main__':
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    # 启用多线程处理
    app.run(host=host, port=port, threaded=True, debug=debug)