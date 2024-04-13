import logging
import os

import streamlit as st
import yt_dlp


@st.cache_resource
def build_logger():
    class StreamlitLogger(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            st.write(log_entry)

    logger = logging.getLogger("yt_dlp_streamlit_logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(StreamlitLogger())
    return logger


def download(url, directory):
    options = {
        'no_color': True,
        'format': 'best',
        'outtmpl': f'{directory}/%(title)s.%(ext)s',
        'logger': build_logger()
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])


def show_inputs() -> (str, str):
    url = st.text_input('URL:', value='https://youtu.be/Pbkn21NNduc', key='url')
    home_directory = os.path.expanduser("~")
    output_directory = st.text_input('Output directory:', value=f'{home_directory}/Downloads', key='directory')

    return url, output_directory


def main():
    st.title('🍿 Downloader')

    url, directory = show_inputs()

    if st.button('Download', disabled=not url):
        download(url, directory)
        st.balloons()


if __name__ == "__main__":
    main()
