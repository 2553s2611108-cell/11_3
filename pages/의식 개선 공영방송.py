import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="K-공영방송 | 경비원 아저씨의 분리배출 잔혹사",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS (공영방송 뉴스 자막 & 방송국 스타일)
st.markdown("""
    <style>
    .broadcast-title {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .news-ticker {
        background-color: #cc0000;
        color: white;
        padding: 10px 15px;
        font-weight: bold;
        font-size: 16px;
        border-radius: 5px;
        margin-top: 15px;
        margin-bottom: 25px;
    }
    .card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border-left: 6px solid #1e3c72;
        margin-bottom: 15px;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 18px;
        border-radius: 8px;
        border-left: 6px solid #ffc107;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화 (응원 메시지 저장용)
if "cheer_messages" not in st.session_state:
    st.session_state.cheer_messages = [
        {"name": "101동 주민", "msg": "상자 테이프 항상 떼고 버릴게요. 매번 고생 많으십니다!"},
        {"name": "502호 주민", "msg": "배달 용기 씻어서 버리는 습관 만들었습니다. 경비원 아저씨 감사합니다."}
    ]

# 4. 방송국 헤더 & 속보 전광판
st.markdown("<div class='broadcast-title'>📺 K-공영방송 [기획취재] 아파트 경비원 아저씨의 분리배출 잔혹사</div>", unsafe_allow_html=True)
st.markdown("<div class='news-ticker'>🚨 [긴급 보도] 분리수거 미비로 지자체 수거 거부 속출... 경비원 80% 이상이 '재분류 작업으로 심각한 고충' 호소</div>", unsafe_allow_html=True)

# 5. 사이드바 방송 편성표
st.sidebar.title("📺 방송 프로그램")
menu = st.sidebar.radio(
    "시청할 코너를 선택하세요:",
    [
        "1. [현장 취재] 경비원 고충 실태",
        "2. [밀착 취재] 경비원을 괴롭히는 5대 배출 실수",
        "3. [주민 참여] 나의 분리배출 양심 지수",
        "4. [공익 캠페인] 경비원 아저씨 응원 전광판"
    ]
)

# ----------------
streamlit
