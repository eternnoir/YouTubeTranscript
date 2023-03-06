import streamlit as st
import yt_transcript
import uuid
import os

st.title('WhisperSubs')
st.write('Automatic Subtitle Generation for YouTube using OpenAI Whisper API')
st.write('利用 OpenAI Whisper API 轉換 YouTube 影片為自動生成字幕')
youtubeUrl = st.text_input('Youtube URL', '')
col1, col2 = st.columns(2)

with col1:
    openai_api = st.text_input('openAI API Key', '')

with col2:
    ext_name = st.selectbox(
        'Format',
        ('text', 'json', 'srt', 'verbose_json', 'vtt'))
    lang = st.text_input('Language', '')
    st.write(
        ' Supplying the input language in [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) format ')

if st.button('Start to transcript'):
    with st.spinner('Please wait...'):
        # try:
        uuid_file_name = str(uuid.uuid4())+".mp3"
        yt_transcript.download_yt_to_mp3(youtubeUrl, uuid_file_name)
        st.success(f"Download successful! File name: {uuid_file_name}")
        language = None
        if lang:
            language = lang

        st.info(
            f'Calling Whisper API... Language: {language}, Format: {ext_name}')
        resp = yt_transcript.whisper(
            openai_api, uuid_file_name, ext_name, language)
        print(resp)
        st.info("Received response from Whisper API")
        os.remove(uuid_file_name)
        st.info(f"Clean up {uuid_file_name}")
        st.download_button(
            'Download', resp, file_name=f'result.{ext_name}')
        # except Exception as e:
        #     st.error(e)

    st.success("Transcription completed successfully!")
