from typing import List, Dict, Any, Union, Generator
from zhipuai import ZhipuAI
from .model_interface import ModelInterface

class GLM4VClient(ModelInterface):
    def __init__(self, api_key: str, base_url: str = None, default_model: str = None):
        if not api_key:
            raise ValueError("Missing API key for GLM4VClient")
        
        self.api_key = api_key
        self.model = default_model or "glm-4v-plus"
        
        
        
        self.client = ZhipuAI(
            api_key=self.api_key
        )
    
    def chat(self, messages: List[Dict[str, Any]], stream: bool = False) -> Union[str, Generator[str, None, None]]:
        """
        进行对话，支持文本和图像输入
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
        )

        if stream:
            def generate_stream():
                for chunk in completion:
                    if hasattr(chunk.choices[0], 'delta') and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            return generate_stream()
        else:
            return completion.choices[0].message.content
