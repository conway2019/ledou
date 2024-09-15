import torch
import torchaudio
from fastapi import FastAPI
# chat = ChatTTS.Chat()
import uvicorn
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav
import os, sys
sys.path.insert(0, os.path.abspath('../../CosyVoice/third_party/Matcha-TTS'))

def torch_gc():
    if torch.cuda.is_available():
        # with torch.cuda.device(DEVICE):
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
import configparser
import os
# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前文件的目录路径（上一级）
parent_dir_path = os.path.dirname(current_file_path)
# 获取上两级目录的路径
grandparent_dir_path = os.path.dirname(parent_dir_path)

config = configparser.ConfigParser()
conf_path=grandparent_dir_path+'/configs/config.ini'
config.read(conf_path)

CosyVoice_model_path = config['paths']['CosyVoice_model_path']
audio_folder_path = config['paths']['audio_folder_path']

def count_files_in_folder():
    assert audio_folder_path!= None
    count = 0
    # 遍历文件夹中所有文件和子文件夹
    for root, dirs, files in os.walk(audio_folder_path):
        count += len(files)  # 累计文件数量
    return count

from pydub import AudioSegment
def combined_audio(path, count):
    for i in range(count):
        audio = AudioSegment.from_file(path.format(i))
        if i == 0:
            combined_audio = audio
        else:
            combined_audio = combined_audio + audio 
    combined_audio.export(path, format="wav")

import random
from pydantic import BaseModel
app = FastAPI()
# 定义asr数据模型，用于接收POST请求中的数据
class TTSItem(BaseModel):
    text : str # 输入
@app.post("/tts")
def tts(item: TTSItem):
    assert CosyVoice_model_path != None
    cosyvoice = CosyVoice(CosyVoice_model_path)

    # sft usage
    print(cosyvoice.list_avaliable_spks())
    
    num = str(count_files_in_folder()+1)
    path = audio_folder_path + num +".wav"
    output = cosyvoice.inference_sft(item.text, '中文女', stream=False)
    print('音频片段个数', len(output))
    if len(output) == 1:
        torchaudio.save(path, j['tts_speech'], 22050)
    else:
        for i, j in enumerate(output):
            torchaudio.save(path.format(i), j['tts_speech'], 22050)
        #合并音频片段
        combined_audio(path, i)
    torch_gc()
   
    result_dict = {"code": 0, "msg": "ok", "res": path}

    return result_dict
if __name__ == '__main__':
    uvicorn.run("tts_server:app", host='127.0.0.1', port=7863)