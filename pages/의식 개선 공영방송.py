import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="K-공영방송 | 경비원 아저씨의 분리배출 고충 센터",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS (문법 오류 방지를 위해 f-string 및 따옴표 구조 안전화)
st.markdown("""
    <style>
    /* 전체 배경 및 기본 폰트 설정 */
    .stApp {
        background-color: #FAFAFA;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* 메인 헤더 디자인 */
    .main-header {
        background: linear-gradient(135deg, #FF7E5F 0%, #FEB47B 100%);
        color: white;
        padding: 25px 20px;
        border-radius: 18px;
        text-align: center;
        font-size: 26px;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(255, 126, 95, 0.25);
        margin-bottom: 12px;
    }
    
    /* 속보 자막 바 */
    .sub-header {
        background-color: #FF5252;
        color: white;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 14px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 2px 8px rgba(255, 82, 82, 0.2);
    }
    
    /* 카드 스타일 (안내 및 정보) */
    .info-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        border-left: 6px solid #FF7E5F;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* 주의/위험 카드 스타일 */
    .danger-box {
        background-color: #FFF5F2;
        padding: 20px;
        border-radius: 16px;
        border-left: 6px solid #FF5252;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }
    
    /* 메트릭 스탯 카드 디자인 */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F0;
    }
    
    /* 응원 메시지 카드 커스텀 */
    .cheer-card {
        background-color: #FFFFFF;
        padding: 16px 20px;
        border-radius: 14px;
        margin-bottom: 12px;
        border: 1px solid #EFEFEF;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 안전하게 초기화
if "cheer_messages" not in st.session_state:
    st.session_state["cheer_messages"] = [
        {"name": "101동 주민", "msg": "상자 테이프 항상 떼고 버릴게요. 매번 고생 많으십니다!"},
        {"name": "502호 주민", "msg": "배달 용기 깨끗이 씻어서 버리는 습관 만들었습니다. 감사합니다."}
    ]

# 4. 상단 타이틀 & 속보 자막
st.markdown("<div class='main-header'>📺 K-공영방송 [특별기획] 아파트 경비원 아저씨의 분리배출 고충 센터</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>🚨 [긴급 보도] 혼합 배출로 지자체 수거 거부 속출... 경비원 80% 이상이 재분류 작업으로 심
