# -*- coding: utf-8
import streamlit as st
from openai import OpenAI
import os
import json
import time
import yaml

# Create a chatbot UI with Streamlit and OpenAI
def chat_ui():
   # 打开并读取 YAML 文件
    with open('../configs/config.yaml', 'r', encoding='UTF-8') as file:
        # Get the max token length for the chatbot
        max_tokens = config.get(['conversation_setting']['max_tokens'], 2048)
        # Get the temperature for the chatbot
        temperature = config.get(['conversation_setting']['temperature'], 0.0)
        # Get the api key for the OpenAI API
        api_key = config.get(['conversation_setting']['api_key'], "internlm2")
        # Get the base url for the OpenAI API
        base_url = config.get(['conversation_setting']['base_url'], "http://0.0.0.0:23333/v1")
        # Get the system prompt for the chatbot
        system_prompt = config.get(['conversation_setting']['system_prompt'], "我是乐豆小助手，逗乐不停，欢乐满荧！")

    message_history = []
    if system_prompt != "":
        message_history.append({"role": "system", "content": system_prompt})
    
    llm = OpenAI(api_key=api_key, base_url=base_url)
        
    if st.sidebar.button("开启新对话"):
        if not os.path.exists("chat_history"):
            os.mkdir("chat_history")
            pass
        with open(f"chat_history/{time.time()}.json", "w") as f:
            json.dump(message_history, f, ensure_ascii=False)
            pass
        message_history = []
                    
    # Set the title of the app
    st.title("乐豆：逗乐不停，欢乐满荧")
    st.caption("你喜欢什么样的笑话？冷笑话、幽默笑话、职场笑话、儿童笑话？说出你的想法吧！")

    user_input = st.chat_input("输入消息")
    if user_input:
        message_history.append({"role": "user", "content": user_input})
        # Generate a response from the chatbot
        response = llm.chat.completions.create(
            model=llm.models.list().data[0].id,
            messages=message_history,
            max_tokens=max_tokens,
            temperature=temperature
        )

        message_history.append({"role": "assistant", "content": response.choices[0].message.content})
        pass
    for message in message_history:
        if message["role"] == "system":
            continue
        else:
            st.chat_message(message["role"]).write(message["content"])

    # Create a text input for the user to type their message

    pass

if __name__ == "__main__":
    chat_ui()
    pass

    