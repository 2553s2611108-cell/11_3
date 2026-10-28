import os
import streamlit as st
import google.generativeai as genai

# 1. 페이지 기본 설정 (가장 위에 배치)
st.set_page_config(
    page_title="우리아파트 분리배출 공영방송",
    page_icon="📢",
    layout="wide"
)

# 2. 커스텀 CSS (이미지 기반 오렌지/크림 모바일 UI 테마 적용)
st.markdown("""
    <style>
    /* 전체 배경 및 기본 폰트 */
    .stApp {
        background-color: #F9F7F2;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 헤더 및 메인 타이틀 */
    h1 {
        color: #FF5E36 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    /* 지표 카드 (Metrics) 디자인 */
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

    /* 버튼 모바일 커스텀 (둥근 주황색 버튼) */
    div.stButton > button {
        background-color: #FF5E36 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
       streamlit>=1.30.0
google-generativeai>=0.4.0
 

