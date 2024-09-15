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
        config = yaml.safe_load(file)
        conversation_setting = config['conversation_setting']
        
        # Get the max token length for the chatbot
        max_tokens = conversation_setting.get('max_tokens', 2048)
        # Get the temperature for the chatbot
        temperature = conversation_setting.get('temperature', 0.0)
        # Get the api key for the OpenAI API
        api_key = conversation_setting.get('api_key', "internlm2")
        # Get the base url for the OpenAI API
        base_url = conversation_setting.get('base_url', "http://0.0.0.0:23333/v1")
        model_name = conversation_setting.get('model_name', "internlm2_5-7b-chat")
        # Get the system prompt for the chatbot
        system_prompt = conversation_setting.get('system_prompt', "我是乐豆小助手，逗乐不停，欢乐满荧！")

    state = st.session_state
    if "message_history" not in state:
        state.message_history = []
    
    if system_prompt != "":
        state.message_history.append({"role": "system", "content": system_prompt})
    
    llm = OpenAI(api_key=api_key, base_url=base_url)
        
    if st.sidebar.button("开启新对话"):
        if not os.path.exists("chat_history"):
            os.mkdir("chat_history")
            pass
        with open(f"chat_history/{time.time()}.json", "w") as f:
            json.dump(state.message_history, f, ensure_ascii=False)
            pass
        state.message_history = []
                    
    # Set the title of the app
    st.title("乐豆：逗乐不停，欢乐满荧")
    st.caption("你喜欢什么样的笑话？冷笑话、幽默笑话、职场笑话、儿童笑话？说出你的想法吧！")

    user_input = st.chat_input("输入消息")
    if user_input:
        state.message_history.append({"role": "user", "content": user_input})
        # Generate a response from the chatbot
        print(model_name)
        response = llm.chat.completions.create(
            #model=llm.models.list().data[0].id,
            model=model_name,
            messages=state.message_history,
            max_tokens=max_tokens,
            temperature=temperature
        )

        state.message_history.append({"role": "assistant", "content": response.choices[0].message.content})
        pass
    for message in state.message_history:
        if message["role"] == "system":
            continue
        else:
            st.chat_message(message["role"]).write(message["content"])

    # Create a text input for the user to type their message

    pass

if __name__ == "__main__":
    chat_ui()
    pass

    