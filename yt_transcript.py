from pytube import YouTube
import openai
import requests


def download_yt_to_mp3(url, filepath):
    yt = YouTube(url)
    print('download...')
    yt.streams.filter().get_audio_only().download(filename=filepath)
    print(f'download {url} to mp3 {filepath} done.')


def whisper(openai_key, file_path, response_f='text', language=None):
    openai.api_key = openai_key
    api_url = 'https://api.openai.com/v1/audio/transcriptions'
    headers = {'Authorization': 'Bearer '+openai_key}
    audio_file = open(file_path, "rb")
    req_data = {
        'model': 'whisper-1',
        'response_format': response_f,
    }
    if language:
        req_data['language'] = language

    # transcript = openai.Audio.transcribe(
    #     "whisper-1", audio_file, response_format=response_f)
    # return transcript
    response = requests.post(api_url, files={'file': audio_file},
                             headers=headers, data=req_data)
    response.raise_for_status()
    return response.text
