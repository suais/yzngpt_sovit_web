from pydub import AudioSegment
from pydub.playback import play
import requests
import random
import string
import shutil
import datetime

cache_gpt_path = "cache/gpt/"
cache_combined_path = "cache/combined/"
file_format = ".wav"
ori_sound_path = "data/"
api_url = 'http://myserver.oxoooo.com:9880'

def generate_random_name():
    length = random.randint(10, 20)
    filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    return filename

def get_gpt_sovits(text):
    url = api_url
    params = {'text': text, 'text_language': 'zh'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        gpt_name = generate_random_name()
        gpt_name_all = f'{cache_gpt_path}{gpt_name}{file_format}'
        with open(gpt_name_all, 'wb') as f:
            f.write(response.content)
            print('文件下载完成')
        return gpt_name
    else:
        print(response.status_code)
        print('文件下载失败')
        return None

def sync_sound(gpt_file, ori_file):
    sound1 = AudioSegment.from_wav(gpt_file)
    sound2 = AudioSegment.from_wav(ori_file)
    combined = sound1 + sound2
    random_name = generate_random_name()
    filename = f"{cache_combined_path}{random_name}.wav"
    combined.export(filename, format="wav")
    return f"{random_name}{file_format}"

def get_sound_path(num):
    data_sound = {
        "0": "0_[GPT生成用户名]你好.wav",
        "1": "1_[GPT生成用户名]问候.wav",
        "2": "2_[AI生成名字]引导提问.wav",
        "3": "3_[AI生成名字]打招呼.wav",
        "4": "4_RTOS和高手C课程进一步介绍.wav",
        "5": "5_RTOS是全网更低门槛课程 有门槛学高手C课程.wav",
        "6": "6_RTOS课程郭天祥经典.wav",
        "7": "7_告诉大家振南一直在线答疑.wav",
        "8": "8_学RTOS之前建议先学高手C.wav",
        "9": "9_学习课程的重要性.wav",
        "10": "10_希望我的知识可以帮到大家.wav",
        "11": "11_引导下单+联系客服.wav",
        "12": "12_引导多来直播间问问题.wav",
        "13": "13_引导领内部资料.wav",
        "14": "14_课程中的经验你在别的课程学不到.wav",
        "15": "15_课程介绍+让大家留问题振南答疑.wav"
    }
    return data_sound[num]

def api_process_return(text, select):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    data = {}
    data['msg'] = 'ok'
    data['data'] = ''
    data['time'] = formatted_time
    if select == "0":
        sound1 = get_gpt_sovits(text)
        data['data'] = f"{sound1}{file_format}"
        source_file = f"{cache_gpt_path}{sound1}.wav"
        shutil.move(source_file, cache_combined_path)
    else:
        sound1 = cache_gpt_path + get_gpt_sovits(text) + {file_format}
        sound2 = ori_sound_path + get_sound_path(select) 
        data['data'] = sync_sound(sound1, sound2)
    return data

def api_server_play(filename):
    try:
        file = f'cache/combined/{filename}'
        audio = AudioSegment.from_wav(file)
        play(audio)
        data = {'msg': 'ok'}
    except:
        data = {'msg': 'filed'}
    return data