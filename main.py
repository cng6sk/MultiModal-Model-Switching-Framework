import base64
import sys
from model_registry import get_model, list_available_models
from typing import List, Dict, Any
from pprint import pprint
import imghdr 
import copy

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
    # 自动检测
    with open(image_path, "rb") as image_file:
        image_type = imghdr.what(image_file)
    # 若检测失败，根据文件扩展名
    if not image_type:
        if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
            image_type = 'jpeg'
        elif image_path.lower().endswith('.png'):
            image_type = 'png'
        elif image_path.lower().endswith('.webp'):
            image_type = 'webp'
        else:
            image_type = 'png'
    # 使用正确的MIME类型
    image_url = f"data:image/{image_type};base64,{base64_image}"
    
    return {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {"url": image_url}
            },
            {
                "type": "text",
                "text": prompt
            }
        ]
    }

def handle_stream_response(stream_generator, chat_history, model_name):
    """处理流式响应，并添加到 messages"""
    full_response = ""
    print(f"{model_name}: ", end="", flush=True)
    
    for chunk in stream_generator:
        full_response += chunk
        print(chunk, end="", flush=True)  
    print()
    # 添加到 messages
    chat_history.append(create_text_message(full_response, role="assistant"))
    return full_response

def main():
    available_models = list_available_models()
    
    print("可用模型:")
    for i, i_model_name in enumerate(available_models):
        print(f"{i+1}. {i_model_name}")
    
    print(f"请选择模型 (1-{len(available_models)}, 默认: 1): ", end="")
    model_choice = input().strip()
    
    # 处理输入(默认选第一个)
    if model_choice == "":
        model_index = 0  
    else:
        try:
            model_index = int(model_choice) - 1
            if model_index < 0 or model_index >= len(available_models):
                print(f"无效选择。使用默认模型: {available_models[0]}")
                model_index = 0
        except ValueError:
            print(f"无效输入。使用默认模型: {available_models[0]}")
            model_index = 0
    
    model_name = available_models[model_index]
    model = get_model(model_name)
    print(f"已选择模型: {model_name}")
    
    # 创建对话历史
    chat_history = [
        create_text_message("你是一个有用的AI助手，可以理解图像并回答问题。", role="system")
    ]
    
    print("是否启用流式输出模式? (y/n, 默认: y)")
    stream_mode_input = input().lower()
    stream_mode = stream_mode_input != 'n'
    
    # 循环对话
    while True:
        print("\n选项: 1-发送文本, 2-发送图片, 3-切换流式模式, 4-切换模型, 5-删除一轮对话, 6-输出messages, q-退出")
        choice = input("请选择: ")
        
        if choice.lower() == 'q':
            break
            
        elif choice == '1':
            # 加入文本消息
            user_input = input("请输入问题: ")
            chat_history.append(create_text_message(user_input))
            
        elif choice == '2':
            # 加入图片消息
            image_path = input("请输入图片路径: ")
            prompt = input("请输入关于图片的问题: ")
            a = create_image_message(image_path, prompt)
            # print(a)
            chat_history.append(a)
            
        elif choice == '3':
            # 切换流式模式
            stream_mode = not stream_mode
            print(f"流式输出模式已{'启用' if stream_mode else '禁用'}")
            continue
            
        elif choice == '4':
            # 切换模型
            print("可用模型:")
            for i, i_model_name in enumerate(available_models):
                print(f"{i+1}. {i_model_name}")
                
            new_model_choice = input(f"请选择新模型 (1-{len(available_models)}): ")
            
            try:
                new_model_index = int(new_model_choice) - 1
                if new_model_index < 0 or new_model_index >= len(available_models):
                    print(f"无效选择。继续使用当前模型: {model_name}")
                    continue
                    
                new_model_name = available_models[new_model_index]
                
                if new_model_name != model_name:
                    try:
                        model = get_model(new_model_name)
                        model_name = new_model_name
                        print(f"已切换到模型: {model_name}")
                        
                        # 询问是否重置对话历史
                        reset_choice = input("是否重置对话历史? (y/n, 默认: n): ").lower()
                        if reset_choice == 'y':
                            # 重置对话历史
                            chat_history = [
                                create_text_message("你是一个有用的AI助手，可以理解图像并回答问题。", role="system")
                            ]
                            print("已重置对话历史")
                        else:
                            print("保留当前对话历史")
                    except Exception as e:
                        print(f"切换模型失败: {e}")
            except ValueError:
                print(f"无效输入。继续使用当前模型: {model_name}")
            continue
        elif choice == '5':
            # 删除对话历史中的最后一条消息（debug）
            # pprint(chat_history)
            if len(chat_history) > 1:
                removed_message = chat_history.pop()
                # 检查是否需要同时删除对话的另一半（用户问题或AI回复）
                if len(chat_history) > 1 and removed_message["role"] == "assistant":
                    delete_user_msg = input("是否同时删除相关的用户问题? (y/n, 默认: n): ").lower()
                    if delete_user_msg == 'y':
                        chat_history.pop()
                        print("已删除最后一轮完整对话")
                    else:
                        print("已删除最后一条AI回复")
                else:
                    role = "用户" if removed_message["role"] == "user" else "AI助手"
                    print(f"已删除最后一条{role}消息")
            else:
                print("对话历史为空或仅包含系统消息，无法删除")
            continue
        
        elif choice == '6':
            pprint(chat_history)
            continue


        print(f"\n正在使用 {model_name} 处理请求...\n")
        
        try:
            # 流式模式选择
            chat_history_copy = copy.deepcopy(chat_history)
            if stream_mode:
                stream_generator = model.chat(chat_history_copy, stream=True)
                handle_stream_response(stream_generator, chat_history, model_name)
            else:
                response = model.chat(chat_history_copy, stream=False)
                print(f"{model_name}: {response}")
                # 回复添加到对话历史
                chat_history.append(create_text_message(response, role="assistant"))
        except Exception as e:
            print(f"模型调用出错: {e}")

if __name__ == "__main__":
    main()


# src\p925678.png
# 请你分步骤解答这道题，输出对这道题的思考判断过程。
# src\p925260.png
# 提取图中的：['发票代码','发票号码','到站','燃油费','票价','乘车日期','开车时间','车次','座号']，请你以JSON格式输出，不要输出```json```代码段”。
# 请总结一下上面的所有图片。
# src\dog_and_girl.jpeg
# 请问图中有什么东西，简要回答
# 请总结一下上面的所有内容。 
# 根据图像写一首诗。
# src\Sprite-0002.png
# 据上面的所有图像写一首词，念奴娇。不要给出解析。