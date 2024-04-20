from pydub import AudioSegment
from pydub.playback import play
import requests
import random
import string
import os
import datetime
import uuid
from models.files import query_all_by_id as query_all_by_id_files
from models.record import query_insert_recoed
from models.utils import get_wav_info
from models.utils import get_file_size
from models.utils import check_words
from models.words import query_all as query_all_words

cache_gpt_path = "data/gpt/"
cache_combined_path = "data/combined/"
file_format = ".wav"
ori_sound_path = "data/"
api_url = 'http://myserver.oxoooo.com:9880'

def generate_random_name():
    length = random.randint(1, 20)
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

def api_process_return(text, select_id, uid):
    words_list = query_all_words()[0][0]
    words = words_list.split(",")
    check_result = check_words(text, words)
    formatted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(check_result)
    if not check_result:
        data = {}
        data['msg'] = 'ok'
        data['data'] = ''
        data['time'] = formatted_time

        voice_file_path = query_all_by_id_files(select_id)[0][7]
        voice_file_name = query_all_by_id_files(select_id)[0][0]
        voice_full_path = os.path.join(voice_file_path, voice_file_name)
        gpt_sund_name = get_gpt_sovits(text)
        sound1 = cache_gpt_path + gpt_sund_name + file_format
        sound2 = voice_full_path
        sync_sound_name = sync_sound(sound1, sound2)
        data['data'] = sync_sound_name
        
        length = get_wav_info(cache_combined_path + sync_sound_name)
        size = get_file_size(cache_combined_path + sync_sound_name)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id = str(uuid.uuid4())
        full_text = text + query_all_by_id_files(select_id)[0][3]
        query_insert_recoed(sync_sound_name, length, size, full_text, uid, time, cache_combined_path, cache_gpt_path, gpt_sund_name, id)
        if query_insert_recoed:
            return data
    else:
        data = {}
        data['msg'] = '含有违禁词'
        data['data'] = ''
        data['time'] = formatted_time
        return data

def api_server_play(filename):
    try:
        file = f'data/combined/{filename}'
        audio = AudioSegment.from_wav(file)
        play(audio)
        data = {'msg': 'ok'}
    except:
        data = {'msg': 'filed'}
    return data