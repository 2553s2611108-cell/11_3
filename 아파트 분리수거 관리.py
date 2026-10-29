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
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 16px;
    letter-spacing: -0.02em;
    color: #FFFFFF;
}
.hero-desc {
    font-size: 14px;
    line-height: 1.7;
    color: #E2E8F0;
    max-width: 480px;
    font-weight: 300;
}

/* Environment Banner */
.env-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: row;
    margin-bottom: 40px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}
.env-text {
    flex: 1;
    padding: 36px 40px;
    background: linear-gradient(135deg, #103B32 0%, #174C41 100%);
    color: white;
}
.env-text .tag {
    font-size: 11px;
    letter-spacing: 2px;
    color: #A3E635;
    font-weight: 600;
    margin-bottom: 8px;
}
.env-text h2 {
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 12px 0;
    color: #FFFFFF;
}
.env-text p {
    font-size: 13px;
    line-height: 1.6;
    color: #CBD5E1;
    margin: 0;
}
.env-image {
    flex: 1;
    background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1000&q=80') center/cover;
    min-height: 180px;
}

/* Section Header */
.section-header {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 28px;
}
.section-eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: #2D6A4F;
    margin-bottom: 6px;
    text-transform: uppercase;
}
.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.01em;
    margin-bottom: 6px;
}
.section-subtitle {
    font-size: 13px;
    color: #64748B;
}

/* Stat Box */
.stat-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    transition: all 0.2s ease;
}
.stat-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
}
.stat-label { font-size: 12px; font-weight: 500; color: #64748B; }
.stat-value { font-size: 28px; font-weight: 700; color: #103B32; margin: 6px 0; }
.stat-note { font-size: 11px; color: #2563EB; font-weight: 500; }

/* Service & News Cards */
.custom-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 24px;
    height: 100%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    transition: all 0.25s ease;
}
.custom-card:hover {
    border-color: #CBD5E1;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}
.card-icon { font-size: 26px; margin-bottom: 12px; }
.card-title { font-size: 16px; font-weight: 700; color: #0F172A; margin-bottom: 8px; }
.card-desc { font-size: 12.5px; color: #64748B; line-height: 1.6; margin: 0; }

.news-tag {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #15803D;
    background: #F0FDF4;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom:
