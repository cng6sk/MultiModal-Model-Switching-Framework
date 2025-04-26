import os
from typing import Dict, Optional
from dotenv import load_dotenv
from models.qwen_vl_client import QwenVLClient
from models.glm4v_client import GLM4VClient

# 加载.env文件
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
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "glm-4v-plus"
    }
}

# 单例模型实例存储
_MODEL_INSTANCES = {}

def get_model(name: str):
    """获取指定名称的模型实例，使用单例模式"""
    # 如果模型实例已经存在，直接返回
    if name in _MODEL_INSTANCES:
        return _MODEL_INSTANCES[name]
    
    # 检查模型配置是否存在
    config = MODEL_CONFIGS.get(name)
    if not config:
        raise ValueError(f"Model '{name}' not found in registry. Available models: {list(MODEL_CONFIGS.keys())}")
    
    # 检查API密钥是否存在
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
