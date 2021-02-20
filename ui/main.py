import base64

import streamlit as st
import os
import pdfminer

with st.sidebar:
    st.title('Audio Book Maker')
    uploaded_file = st.file_uploader("Upload Files", type=['pdf'])
    start_page = st.number_input("Start Page", 1)
    end_page = st.number_input("End Page", 10)
    chapter_name = st.text_input("Chapter name", 'Chapter 1')

'''
# Preview PDF
'''
if uploaded_file is not None:
    base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)
