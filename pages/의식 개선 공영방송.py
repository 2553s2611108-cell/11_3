import streamlit as st

# 1. 페이지 설정 (최상단 배치)
st.set_page_config(
    page_title="K-공영방송 | 경비원 아저씨의 분리배출 고충 센터",
    page_icon="📺",
    layout="wide"
)

# 2. 세션 상태 안전 초기화 (NameError 완벽 차단)
if "cheer_messages" not in st.session_state:
    st.session_state["cheer_messages"] = [
        {"name": "101동 주민", "msg": "상자 테이프 항상 떼고 버릴게요. 고생 많으십니다!"},
        {"name": "502호 주민", "msg": "배달 용기 깨끗이 씻어서 버리는 습관 만들었습니다."}
    ]

# 3. CSS 스타일링
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .sub-header {
        background-color: #cc0000;
        color: white;
        padding: 8px 15px;
        font-weight: bold;
        font-size: 14px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .box-info {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #203a43;
        margin-bottom: 10px;
    }
    .box-danger {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. 헤더
st.markdown("<div class='main-header'>📺 K-공영방송 [특별기획] 아파트 경비원 아저씨의 분리배출 고충 센터</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>🚨 [긴급 보도] 무분별한 혼합 배출로 수거 거부 속출... 경비원 재분류 노동 고충 심각</div>", unsafe_allow_html=True)

# 5. 사이드바
st.sidebar.title("📺 방송 프로그램")
menu = st.sidebar.radio(
    "코너 선택:",
    [
        "1. [현장 보도] 경비원 고충 실태",
        "2. [밀착 취재] 5대 배출 실수",
        "3. [주민 참여] 나의 양심 지수",
        "4. [공익 캠페인] 응원 전광판"
    ]
)

# ----------------------------------------------------
# 코너 1
# ----------------------------------------------------
if menu == "1. [현장 보도] 경비원 고충 실태":
    st.subheader("📰 [보도] 잘못 버린 쓰레기, 누군가에겐 과중한 노동입니다")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("⏱️ 일평균 재작업 시간", "2.8 시간", "순찰 업무 차질")
    col2.metric("⚠️ 오염/재활용 불가 비율", "42.1%", "전량 폐기 처분")
    col3.metric("🩹 베임 등 부상 경험", "6
streamlit
