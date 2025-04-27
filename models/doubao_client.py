from typing import List, Dict, Any, Union, Generator
from volcenginesdkarkruntime import Ark
from .model_interface import ModelInterface

class DoubaoClient(ModelInterface):
    def __init__(self, api_key: str, base_url: str, default_model: str):
        if not api_key:
            raise ValueError("Missing API key for DoubaoClient")
        
        self.api_key = api_key
        self.model = default_model
    


        self.client = Ark(
            api_key=self.api_key,
        )
    
    def chat(self, messages: List[Dict[str, Any]], stream: bool = False) -> Union[str, Generator[str, None, None]]:
        messages = self._convert_message_format(messages)
        
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

    def _convert_message_format(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            """
            转换消息格式以适应豆包模型的要求
            
            转换规则:
            如果content是列表且只有一个纯文本项，转换为字符串
            """
            for message in messages:
                if 'content' in message and isinstance(message['content'], list):
                    if len(message['content']) == 1 and message['content'][0].get('type') == 'text':
                        message['content'] = message['content'][0]['text']
                    elif len(message['content']) > 1:
                        # 多模态内容跳过
                        pass
            
            return messages