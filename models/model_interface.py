from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union, Generator

class ModelInterface(ABC):
    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], stream: bool = False) -> Union[str, Generator[str, None, None]]:
        """
        进行对话，支持文本和图像输入
        
        Args:
            messages: 对话历史，格式符合OpenAI Chat API规范
            stream: 是否流式输出
            
        Returns:
            如果stream=False，返回完整回复字符串
            如果stream=True，返回生成回复内容的生成器
        """
        pass
