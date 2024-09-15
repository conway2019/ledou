import  requests
import streamlit as st
import yaml
from openai import OpenAI

def llm_response(prompt):
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
        # Get the system prompt for the chatbot
        system_prompt = conversation_setting.get('system_prompt', "我是乐豆小助手，逗乐不停，欢乐满荧！")

    llm = OpenAI(api_key=api_key, base_url=base_url)
    messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt}
    ]

    # Generate a response from the chatbot
    response = llm.chat.completions.create(
            model=llm.models.list().data[0].id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
    return response.choices[0].message.content

def tts_api(text:str):
    headers = {'Content-Type': 'application/json'}
    print(text)
    data = {"text": text}
    url = "http://127.0.0.1:7863/"
    response = requests.post(url+"tts", headers=headers, json=data)
    print(response)
    response = response.json()
    print(response)
    if response['code'] == 0:
        res = response['res']
        return res
    else:
        return response['msg']

def main():
    # Set the title of the app
    st.title("乐豆：逗乐不停，欢乐满荧")
    st.caption("你喜欢什么样的笑话？冷笑话、幽默笑话、职场笑话、儿童笑话？说出你的想法吧！")
 
    # st.header("列-1")
    if "voice" not in st.session_state.keys():
        st.session_state.voice = []   

    for voice in st.session_state.voice:
        with st.chat_message(voice["role"]):
            if voice["role"] == "user":
                 st.markdown(voice["content"])
            else:
                path=voice["content"]
                audio_file = open(path, 'rb')
                audio_bytes = audio_file.read()
                    # 使用st.audio函数播放音频
                st.audio(audio_bytes, format='audio/wav')
    if prompt := st.chat_input("请输入你的问题?"):
    # Display user message in chat message container
        with st.chat_message("user"):
             st.markdown(prompt)
    # Add user message to chat history
        st.session_state.voice.append({"role": "user", "content": prompt})

        if st.session_state.voice[-1]["role"] != "assistant":
            with st.spinner("Thinking..."):
                with st.chat_message("assistant"):
                    stream = llm_response(prompt)
                    #显示llm返回结果
                    with st.chat_message("user"):
                        st.markdown(stream)

                    #调用 tts接口生成音频
                    path=tts_api(stream)
                    audio_file = open(path, 'rb')
                    audio_bytes = audio_file.read()
                    # 使用st.audio函数播放音频
                    st.audio(audio_bytes, format='audio/wav')
                    st.session_state.voice.append({"role": "assistant", "content": path})
       
        print(st.session_state.voice)
        
if __name__ == "__main__":
    main()

