import wave
import os

def get_wav_info(file_path):
    # 打开WAV文件
    with wave.open(file_path, 'rb') as wav_file:
        # 获取WAV文件的帧率（每秒采样数）
        frame_rate = wav_file.getframerate()
        # 获取WAV文件的帧数
        frames = wav_file.getnframes()
        # 计算WAV文件的时长（秒）
        duration = frames / float(frame_rate)
    return int(duration)

def get_file_size(file_path):
    # 获取文件大小（字节）
    size = os.path.getsize(file_path)
    # 将字节转换为更易读的单位（KB、MB等）
    if size < 1024:
        return f"{size} bytes"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size / (1024 * 1024):.2f}"