import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="K-공영방송 | 경비원 아저씨의 분리배출 고충 센터",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS (공영방송 뉴스 스타일 적용)
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .sub-header {
        background-color: #cc0000;
        color: white;
        padding: 8px 15px;
        font-weight: bold;
        font-size: 15px;
        border-radius: 5px;
        margin-bottom: 25px;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 18px;
        border-radius: 8px;
        border-left: 5px solid #203a43;
        margin-bottom: 15px;
    }
    .danger-box {
        background-color: #fff3cd;
        padding: 18px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화 (응원 메시지 저장)
if "cheer_messages" not in st.session_state:
    st.session_state["cheer_messages"] = [
        {"name": "101동 주민", "msg": "상자 테이프 항상 떼고 버릴게요. 매번 고생 많으십니다!"},
        {"name": "502호 주민", "msg": "배달 용기 깨끗이 씻어서 버리는 습관 만들었습니다. 감사합니다."}
    ]

# 4. 상단 타이틀 & 속보 자막
st.markdown("<div class='main-header'>📺 K-공영방송 [특별기획] 아파트 경비원 아저씨의 분리배출 고충 센터</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>🚨 [긴급 보도] 혼합 배출로 지자체 수거 거부 속출... 경비원 80% 이상이 재분류 작업으로 심각한 고충 호소</div>", unsafe_allow_html=True)

# 
streamlit
