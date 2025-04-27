from typing import List, Dict, Any, Union, Generator
from openai import OpenAI
from .model_interface import ModelInterface

class HunyuanVisionClient(ModelInterface):
    def __init__(self, api_key: str, base_url: str, default_model: str):
        if not api_key:
            raise ValueError("Missing API key for HunyuanVisionClient")
        
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

        if stream:
            def generate_stream():
                for chunk in completion:
                    if chunk.choices[0].delta and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            return generate_stream()
        else:
            return completion.choices[0].message.content
