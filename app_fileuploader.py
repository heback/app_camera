import streamlit as st
import os

img_path = os.path.join(os.path.dirname(__file__), 'images')
if not os.path.exists(img_path):
    os.mkdir(img_path)

uploaded_file = st.file_uploader('이미지 선택', type=['jpg','png'])

if uploaded_file is not None:
    with open(os.path.join(img_path, uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())