import streamlit as st
from google import genai
from google.genai.errors import APIError

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="우리 아파트 분리수거 관리 시스템",
    page_icon="♻️",
    layout="wide"
)

# 커스텀 CSS (이미지 스타일 반영)
st.markdown("""
<style>
    /* 사이드바 하단 강조 버튼 스타일 */
    .active-btn {
        background-color: #FF4B4B !important;
        color: white !important;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .footer-text {
        color: #888888;
        font-size: 13px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 2. 세션 상태 초기화 (페이지 이동 관리)
if "current_page" not in st.session_state:
    st.session_state.current_page = "의식개선 공영방송"

# 3. Gemini API 클라이언트 초기화
api_key = st.secrets.get("GEMINI_API_KEY")

# 4. 사이드바 구성 (이미지 왼쪽 메뉴 레이아웃 반영)
with st.sidebar:
    st.caption("아파트 분리수거 관리")
    
    # 메뉴 선택 라디오 버튼
    selected_menu = st.radio(
        "메뉴 선택",
        ["메인 페이지", "Trash Alarm", "분리수거 점수제", "의식개선 공영방송"],
        index=["메인 페이지", "Trash Alarm", "분리수거 점수제", "의식개선 공영방송"].index(st.session_state.current_page),
        label_visibility="collapsed"
    )
    
    # 세션 상태 업데이트
    st.session_state.current_page = selected_menu

    st.markdown("---")
    st.markdown("### ♻️ 그린 아파트")
    st.caption("분리수거 관리 시스템")
    st.write("")

    # 하단 내비게이션 버튼 그룹 (이미지 하단 버튼 UI 모방)
    pages = ["메인 페이지", "Trash Alarm", "분리수거 점수제", "의식개선 공영방송"]
    for p in pages:
        if p == st.session_state.current_page:
            st.button(p, key=f"btn_{p}", type="primary", use_container_width=True)
        else:
            if st.button(p, key=f"btn_{p}", use_container_width=True):
                st.session_state.current_page = p
                st.rerun()

# -------------------------------------------------------------------
# 페이지 1: 의식개선 공영방송 (이미지 메인 화면 구현)
# -------------------------------------------------------------------
if st.session_state.current_page == "의식개선 공영방송":
    st.title("📢 의식개선 공영방송")
    st.write("주민에게 올바른 분리배출 방법을 알리는 공영방송 문구 예시입니다.")
    st.write("")

    # 방송 문구 선택 옵션
    preset_options = [
        "기본 안내",
        "주말/배달 용기 배출 안내",
        "음식물 및 악취 방지 안내",
        "🤖 AI 맞춤형 원고 생성"
    ]
    
    selected_option = st.selectbox("방송 문구 선택", preset_options)

    # 기본 프리셋 문구
    default_scripts = {
        "기본 안내": "주민 여러분, 깨끗한 아
streamlit
google-genai
