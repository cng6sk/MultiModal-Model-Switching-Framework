import base64
import sys
from model_registry import get_model
from typing import List, Dict, Any

def encode_image(image_path: str) -> str:
    """将图像文件编码为base64字符串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def create_text_message(text: str, role: str = "user") -> Dict[str, Any]:
    """创建纯文本消息"""
    return {
        "role": role,
        "content": [{"type": "text", "text": text}]
    }

def create_image_message(image_path: str, prompt: str) -> Dict[str, Any]:
    """创建包含图像的消息"""
    base64_image = encode_image(image_path)
    return {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
            },
            {
                "type": "text",
                "text": prompt
            }
        ]
    }

def handle_stream_response(stream_generator, chat_history):
    """处理流式响应，并将完整回复添加到对话历史中"""
    full_response = ""
    print("AI助手: ", end="", flush=True)
    
    for chunk in stream_generator:
        full_response += chunk
        print(chunk, end="", flush=True)
    
    print()  # 打印换行
    
    # 将完整回复添加到对话历史
    chat_history.append(create_text_message(full_response, role="assistant"))
    return full_response

def main():
    model_name = "qwen-vl"
    model = get_model(model_name)
    
    # 创建对话历史
    chat_history = [
        create_text_message("你是一个有用的AI助手，可以理解图像并回答问题。", role="system")
    ]
    
    print("是否启用流式输出模式? (y/n)")
    stream_mode = input().lower() == 'y'
    
    # 循环进行对话
    while True:
        print("\n选项: 1-发送文本, 2-发送图片, 3-切换流式模式, q-退出")
        choice = input("请选择: ")
        
        if choice.lower() == 'q':
            break
            
        elif choice == '1':
            # 发送文本消息
            user_input = input("请输入问题: ")
            chat_history.append(create_text_message(user_input))
            
        elif choice == '2':
            # 发送图片消息
            image_path = input("请输入图片路径: ")
            prompt = input("请输入关于图片的问题: ")
            chat_history.append(create_image_message(image_path, prompt))
            
        elif choice == '3':
            # 切换流式模式
            stream_mode = not stream_mode
            print(f"流式输出模式已{'启用' if stream_mode else '禁用'}")
            continue
            
        else:
            print("无效选项，请重新选择")
            continue
        
        # 获取模型回复
        print("\n正在等待AI回复...\n")
        
        if stream_mode:
            # 流式模式
            stream_generator = model.chat(chat_history, stream=True)
            handle_stream_response(stream_generator, chat_history)
        else:
            # 非流式模式
            response = model.chat(chat_history, stream=False)
            print(f"AI助手: {response}")
            # 将AI回复添加到对话历史
            chat_history.append(create_text_message(response, role="assistant"))

if __name__ == "__main__":
    main()


# src\p925678.png
# 请你分步骤解答这道题，输出对这道题的思考判断过程。
# src\p925260.png
# 提取图中的：['发票代码','发票号码','到站','燃油费','票价','乘车日期','开车时间','车次','座号']，请你以JSON格式输出，不要输出```json```代码段”。
# 请总结一下上面的所有图片。
# src\dog_and_girl.jpeg