import os
import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(
    page_title="우리아파트 분리배출 공영방송",
    page_icon="📢",
    layout="wide"
)

# 2. 모바일 UI 테마 CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #F9F7F2;
        font-family: 'Pretendard', -apple-system, sans-serif;
    }
    h1 {
        color: #FF5E36 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0px 4px 15px rgba(255, 94, 54, 0.08);
        border: 1px solid #FFEBE3;
    }
    div[data-testid="stMetricValue"] {
        color: #FF5E36 !important;
        font-weight: 700;
    }
    div.stButton > button {
        background-color: #FF5E36 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 12px rgba(255, 94, 54, 0.25);
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #E04B26 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #EFEFEF;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 앱 타이틀
st.title("📢 우리아파트 Clean-Up 공영방송")
st.caption("주민 모두가 함께 만드는 올바른 분리배출 문화 챌린지")

# 4. 사이드바 메뉴
st.sidebar.header("📺 방송국 채널")
menu = st.sidebar.radio(
    "이동할 메뉴를 선택하세요:",
    [
        "📺 오늘의 방송 (메인)",
        "🔍 분리배출 가이드",
        "🧩 분리배출 O/X 퀴즈",
        "📸 주민 실천 인증 게시판",
        "🤖 AI 분리배출 상담소"
    ]
)

# -------------------------------------------------------------------
# 1. 메인 방송
# -------------------------------------------------------------------
if menu == "📺 오늘의 방송 (메인)":
    st.subheader("📡 오늘의 아파트 환경 방송")
    
    st.info("""
    **[안내 방송]** 
    주민 여러분, 안녕하십니까! 아파트 환경 관리 방송국입니다. 
    오늘도 올바른 분리배출을 통해 깨끗한 우리 아파트와 지구를 만드는데 동참해주세요!
    - **오늘의 강조사항**: 라벨 제거하지 않은 투명 페트병은 재활용이 불가능합니다. 꼭 라벨을 떼서 배출해주세요!
    """)
    
    col1, col2, col3 = st.columns(3)
