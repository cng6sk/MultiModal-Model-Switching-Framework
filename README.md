# MultiModal-Model-Switching-Framework

一个支持多种视觉语言模型动态切换的统一调用框架，让您可以轻松比较和使用不同的多模态大语言模型。

## 目前支持的模型

当前支持以下多模态大语言模型:

- qwen-vl (通义千问VL-阿里巴巴)
- glm-4v (智谱AI)
- doubao-vision (豆包-抖音)
- hunyuan-vision (腾讯混元)
- moonshot-vision (月之暗面-Moonshot AI)

## 快速开始

### 环境准备

1. 克隆本仓库:
```bash
git clone https://github.com/yourusername/multimodal-model-switching-framework.git
cd multimodal-model-switching-framework
```
2. 创建环境变量文件 `.env`，添加各模型API密钥:
```
ALIYUN_BAILIAN_API_KEY=your_qwen_api_key
ZHIPUAI_API_KEY=your_glm_api_key
ARK_API_KEY=your_doubao_api_key
HUNYUAN_API_KEY=your_hunyuan_api_key
MOONSHOT_API_KEY=your_moonshot_api_key
```

### 运行程序
```
python main.py
```

## 项目结构
```
multimodal_inference/
├── models/
│   ├── __init__.py
│   ├── model_interface.py       # 定义模型统一接口
│   ├── qwen_vl_client.py        # 通义千问VL调用实现
│   ├── glm4v_client.py          # 智谱GLM-4V调用实现
│   ├── doubao_client.py         # 豆包视觉模型调用实现
│   ├── hunyuan_vision_client.py # 混元视觉模型调用实现
│   ├── moonshot_v1_vision_client.py # 月之暗面视觉模型调用实现
├── model_registry.py            # 模型注册表
├── main.py                      # 主程序入口
├── .env                         # 环境变量配置
├── requirements.txt             # 依赖项
└── README.md                    # 项目说明
```

## 如何扩展新模型

要添加新的多模态模型支持，只需执行以下步骤:

1. 在`models/`目录下创建新的客户端实现，继承`ModelInterface`抽象类
2. 在`model_registry.py`中添加新模型的配置信息
3. 在`.env`文件中添加相应的API密钥配置

新客户端示例:

```python
from typing import List, Dict, Any, Union, Generator
from openai import OpenAI
from .model_interface import ModelInterface

class NewModelClient(ModelInterface):
    def __init__(self, api_key: str, base_url: str, default_model: str):
        if not api_key:
            raise ValueError("Missing API key for NewModelClient")
        
        self.api_key = api_key
        self.base_url = base_url
        self.model = default_model
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
    
    def chat(self, messages: List[Dict[str, Any]], stream: bool = False) -> Union[str, Generator[str, None, None]]:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
        )
```

## 许可证
MIT License