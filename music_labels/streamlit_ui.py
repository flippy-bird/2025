import streamlit as st
import librosa
import numpy as np
import os
import tempfile
from interface import AudioDectector

audio_dector = AudioDectector()


st.title("🎵 音乐风格&情感识别系统")

uploaded_file = st.file_uploader("请上传音乐文件（支持 mp3/wav）", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    if st.button("开始识别"):
        with st.spinner("正在分析，请稍候..."):
            # 临时保存文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # 调用分析函数
            result = audio_dector.detect(tmp_path)

            # 显示结果
            st.success("识别完成！")
            st.subheader("🎵 风格（Genre）")
            st.json(result["genre"])

            st.subheader("🎶 情感（Emotion）")
            st.json(result["emotion"])

            st.subheader("🥁 乐器（Instrument）")
            st.json(result["instruments"])

            st.subheader("🧑‍🎤 性别")
            st.markdown(f"{result['gender']}")

            # 删除临时文件
            os.remove(tmp_path)
