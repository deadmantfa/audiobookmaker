import io

import streamlit as st
from PIL import Image
from gtts import gTTS
from poppler import load_from_data, PageRenderer

st.set_page_config(page_title='AudioBook Maker', page_icon='https://i.postimg.cc/mk0CgTnh/logo-transparent-200.png',
                   layout='wide', initial_sidebar_state='expanded')

st.title('Audio Book Maker')
st.header(
    "[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E226KBO)&nbsp;[![GitHub release ("
    "latest by date)](https://img.shields.io/github/v/release/deadmantfa/audiobookmaker?style=for-the-badge)]("
    "https://github.com/deadmantfa/audiobookmaker)")
st.header('Preview Uploaded PDF')
st.warning('Before switching pages be sure to download any converted pages or you will need to reconvert')


def convert(pdf_document, start, end):
    try:
        text = ''
        for x in range(start - 1, end):
            page_current = pdf_document.create_page(x)
            text += page_current.text()
        # initialize tts, create mp3 and play
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang='en', slow=False, lang_check=False)
        tts.write_to_fp(mp3_fp)
        return mp3_fp
    except AssertionError:
        st.error('The PDF does not seem to have text and maybe its a scanned')


@st.cache
def render_page(file, page):
    renderer = PageRenderer()
    page_1 = file.create_page(page - 1)
    image = renderer.render_page(page_1)

    pil_image = Image.frombytes(
        "RGBA",
        (image.width, image.height),
        image.data,
        "raw",
        str(image.format),
    )
    return pil_image


def preview(pdf_document):
    input_page = st.number_input('Page number', 1, step=2)
    col1, col2 = st.beta_columns(2)
    col1.header(f"Page {input_page}")
    col2.header(f"Page {input_page + 1}")
    left_page = render_page(pdf_document, input_page)
    right_page = render_page(pdf_document, input_page + 1)
    col1.image(left_page, use_column_width=True)
    col2.image(right_page, use_column_width=True)


def main():
    with st.sidebar:
        st.title('Audio Book Maker')
        uploaded_file = st.file_uploader("Upload a PDF", type=['pdf'])
        start_page = st.number_input("Start Page", 1)
        end_page = st.number_input("End Page", 1)
        st.info('Conversion takes time, so please be patient')
        convert_to_audio = st.button('Convert')
        if uploaded_file is not None:
            pdf_document = load_from_data(uploaded_file.read())
        if start_page > end_page:
            st.error('Start Page cannot be greater than end page')
        elif start_page <= end_page:
            if convert_to_audio and uploaded_file is not None:
                audio_file = convert(pdf_document, start_page, end_page)
                st.audio(audio_file, format='audio/mp3')

    if uploaded_file is not None:
        preview(pdf_document)
    else:
        st.info('Upload a PDF, check the sidebar on the left')


if __name__ == "__main__":
    main()
