import wave
import os
import re
import random

def get_wav_info(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        frame_rate = wav_file.getframerate()
        frames = wav_file.getnframes()
        duration = frames / float(frame_rate)
    return int(duration)

def get_file_size(file_path):
    size = os.path.getsize(file_path)
    if size < 1024:
        return f"{size} bytes"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size / (1024 * 1024):.2f}"
    
    
def check_words(text, words:list):
    pattern = "|".join(words)
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False


def generate_uid(length=8):
    uid = ''.join(str(random.randint(0, 9)) for _ in range(length))
    return uid