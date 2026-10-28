import os
import datetime
import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(
    page_title="아파트 분리배출 공영방송 시스템",
    page_icon="📢",
    layout="wide"
)

# 2. 커스텀 CSS (방송국 대시보드 테마)
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F6F9;
        font-family: 'Pretendard', sans-serif;
    }
    h1 {
        color: #1E3A8A !important;
        font-weight: 800 !important;
    }
    .broadcast-box {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        border-left: 8px solid #2563EB;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    div.stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 브라우저 음성 합성(TTS) 재생용 JavaScript 함수
def speak_text(text_content):
    # HTML/JS를 이용한 안전한 브라우저 음성 출력
    clean_text = text_content.replace("\n", " ").replace("'", "\\'")
    tts_script = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{clean_text}');
            msg.lang = 'ko-KR';
            msg.rate = 0.9; // 아나운서처럼 안정적인 속도
            window.speechSynthesis.cancel(); // 이전 음성 중지
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(tts_script, height=0)

# 4. 헤더
st.title("📢 우리아파트 아침 공영방송 시스템")
st.caption("매일 아침 입주민의 분리배출 의식을 바꾸는 올바른 환경 안내 방송국")

# 세션 상태 초기화
if "broadcast_log" not in st.session_state:
    st.session_state.broadcast_log = []

# 사이드바
st.sidebar.header("🎙️ 방송국 제어판")
menu =
