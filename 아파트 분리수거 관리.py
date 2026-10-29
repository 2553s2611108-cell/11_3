import streamlit as st
from datetime import datetime
import uuid

# 1. 페이지 설정
st.set_page_config(
    page_title="그린 아파트 | 리사이클링 케어",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "메인 페이지"
if "reports" not in st.session_state:
    st.session_state.reports = []

def go(page):
    st.session_state.page = page

# 3. 고급 모던 CSS 스타일링
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');

html, body, [class*="css"] {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
    background-color: #FAFAFA;
    color: #1A202C;
}

.block-container {
    max-width: 1140px !important;
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

/* Hero Section */
.hero-wrapper {
    background: linear-gradient(135deg, rgba(15, 42, 36, 0.88) 0%, rgba(26, 60, 52, 0.75) 100%), 
                url('https://images.unsplash.com/photo-1449844908441-8829872d2607?auto=format&fit=crop&w=2000&q=85') center/cover no-repeat;
    border-radius: 16px;
    padding: 56px 48px;
    color: #FFFFFF;
    box-shadow: 0 20px 40px rgba(15, 42, 36, 0.12);
    margin-bottom: 32px;
}
.hero-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #C5A880;
    margin-bottom: 12px;
}
.hero-title {
    font-size: clamp(28px, 4.2vw, 42px);
    font-weight: 7
    
