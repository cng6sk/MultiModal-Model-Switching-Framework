import os
from typing import Dict, Optional
from dotenv import load_dotenv
from models.qwen_vl_client import QwenVLClient
from models.glm4v_client import GLM4VClient
from models.doubao_client import DoubaoClient
from models.hunyuan_vision_client import HunyuanVisionClient
from models.moonshot_v1_vision_client import MoonshotVisionClient

load_dotenv()

# 模型配置
MODEL_CONFIGS = {
    "qwen-vl": {
        "class": QwenVLClient,
        "api_key": os.getenv("ALIYUN_BAILIAN_API_KEY"),
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-vl-max-latest"
    },
    "glm-4v": {
        "class": GLM4VClient,
        "api_key": os.getenv("ZHIPUAI_API_KEY"),
        "base_url": None,
        "default_model": "glm-4v-plus"
    },
    "doubao-vision": {
        "class": DoubaoClient,
        "api_key": os.getenv("ARK_API_KEY"),
        "base_url": None,
        "default_model": "doubao-1-5-vision-pro-32k-250115"
    },
    "hunyuan-vision": {
        "class": HunyuanVisionClient,
        "api_key": os.getenv("HUNYUAN_API_KEY"),
        "base_url": "https://api.hunyuan.cloud.tencent.com/v1",
        "default_model": "hunyuan-turbo-vision"
    },
    "moonshot-vision": {
        "class": MoonshotVisionClient,
        "api_key": os.getenv("MOONSHOT_API_KEY"),
        "base_url": "https://api.moonshot.cn/v1",
        "default_model": "moonshot-v1-32k-vision-preview"
    }
}

# 单例模型实例存储
_MODEL_INSTANCES = {}

def get_model(name: str):
    """获取指定名称的模型实例，使用单例模式"""
    # 模型实例已经存在
    if name in _MODEL_INSTANCES:
        return _MODEL_INSTANCES[name]
    
    # 检查模型配置
    config = MODEL_CONFIGS.get(name)
    if not config:
        raise ValueError(f"Model '{name}' not found in registry. Available models: {list(MODEL_CONFIGS.keys())}")
    
    # 检查API密钥
    if not config["api_key"]:
        raise ValueError(f"Missing API key for {name}! Please check your .env file.")
    
    # 创建模型实例
    model_instance = config["class"](
        api_key=config["api_key"],
        base_url=config["base_url"],
        default_model=config["default_model"]
    )
    
    # 存储实例以便下次使用
    _MODEL_INSTANCES[name] = model_instance
    
    return model_instance

def list_available_models():
    """列出所有可用的模型名称"""
    return list(MODEL_CONFIGS.keys())
