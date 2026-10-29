import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="K-공영방송 | 경비원 아저씨의 분리배출 고충 센터",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS (모바일 앱 스타일 디자인 적용)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #EAEAEA;
    }

    /* 메인 헤더 카드 */
    .app-header {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8811 100%);
        color: white;
        padding: 24px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0px 8px 20px rgba(255, 107, 53, 0.15);
        margin-bottom: 12px;
    }
    .app-header h2 {
        color: #FFFFFF;
        margin: 0;
        font-size: 24px;
        font-weight: 800;
    }
    
    /* 긴급 자막/알림 바 */
    .news-ticker {
        background-color: #FFF3EB;
        color: #D9381E;
        padding: 12px 18px;
        font-weight: 700;
        font-size: 14px;
        border-radius: 14px;
        border: 1px solid #FFE2D1;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
    }

    /* 콘텐츠 카드 스타일 */
    .content-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #EFEFEF;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 16px;
    }
    
    /* 고충 및 지침 카드 (레드 & 블루/오렌지 포인트) */
    .danger-card {
        background-color: #FFF5F5;
        border: 1px solid #FFE3E3;
        border-left: 6px solid #FF4D4D;
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 15px;
    }
    .danger-card h4 {
        color: #E03131;
        margin-top: 0;
        margin-bottom: 8px;
        font-size: 16px;
    }

    .info-card {
        background-color: #F0F9FF;
        border: 1px solid #E0F2FE;
        border-left: 6px solid #0EA5E9;
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 15px;
    }
    .info-card h4 {
        color: #0284C7;
        margin-top: 0;
        margin-bottom: 8px;
        font-size: 16px;
    }

    /* 커스텀 버튼 디자인 */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8811 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 700;
        font-size: 16px;
        width: 100%;
        box-shadow: 0px 4px 12px rgba(255, 107, 53, 0.2);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 16px rgba(255, 107, 53, 0.3);
    }

    /* 응원 메시지 리스트 카운터/카드 */
    .cheer-card {
        background-color: #FFFFFF;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #EAEAEA;
        margin-bottom: 12px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.02);
    }
    .cheer-name {
        color: #FF6B35;
        font-weight: bold;
        font-size: 15px;
        margin-bottom: 4px;
    }
    .cheer-msg {
        color: #495057;
        font-size: 14px;
        line-height: 1.5;
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
st.markdown("""
    <div class='app-header'>
        <h2>📺 K-공영방송 [특별기획]</h2>
        <p style='margin: 5px 0 0 0; opacity: 0.9; font-size: 15px;'>아파트 경비원 아저씨의 분리배출 고충 센터</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='news-ticker'>
        🚨 <b>[긴급 보도]</b> &nbsp; 혼합 배출로 지자체 수거 거부 속출... 경비원 80% 이상이 재분류 작업으로 심각한 고충 호소
    </div>
""", unsafe_allow_html=True)

# 5. 사이드바 메뉴
st.sidebar.title("📺 방송 프로그램")
menu = st.sidebar.radio(
    "시청할 코너를 선택하세요:",
    [
        "1. [현장 보도] 경비원 고충 실태",
        "2. [밀착 취재] 경비원을 괴롭히는 5대 배출 실수",
        "3. [주민 참여] 나의 분리배출 양심 지수",
        "4. [공익 캠페인] 경비원 아저씨 응원 게시판"
    ]
)

# ----------------------------------------------------
# 1. 현장 보도
# ----------------------------------------------------
if menu == "1. [현장 보도] 경비원 고충 실태":
    st.subheader("📰 [보도] 무심코 버린 쓰레기, 누군가에겐 과중한 노동입니다")
    st.write("아파트 주민들이 잘못 버린 쓰레기로 인해 발생하는 경비원분들의 실제 작업 부담 수치입니다.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="⏱️ 경비원 일평균 분리수거 재작업", value="2.8 시간", delta="순찰/방범 업무 차질", delta_color="inverse")
    with col2:
        st.metric(label="⚠️ 잘못 배출되어 버려지는 비율", value="42.1%", delta="오염으로 인한 재활용 불가", delta_color="inverse")
    with col3:
        st.metric(label="🩹 베임/다침 등 부상 경험", value="67.3%", delta="깨진 유리/날카로운 자재", delta_color="inverse")

    st.markdown("---")
    st.markdown("### 🎙️ 현장 인터뷰")
    st.info("""
    **"수거업체에서 안 가져가니까 저희가 일일이 칼로 박스 테이프 뜯고, 페트병 라벨 떼고, 양념 묻은 건 수세미로 다시 닦습니다. 새벽부터 쓰레기 정리하다 보면 온몸이 안 아픈 곳이 없습니다."**  
    — *OO아파트 경비원 K씨*
    """)

# ----------------------------------------------------
# 2. 밀착 취재
# ----------------------------------------------------
elif menu == "2. [밀착 취재] 경비원을 괴롭히는 5대 배출 실수":
    st.subheader("🔍 [기획] 경비원 아저씨의 손을 두 번 가시게 만드는 주요 사례")
    st.write("확인할 품목을 선택하면 경비원의 고충과 주민 올바른 수칙을 비교해 보여드립니다.")
    
    selected = st.selectbox(
        "배출 품목을 선택하세요:",
        [
            "선택하세요",
            "1. 테이프·송장이 붙은 택배 박스",
            "2. 양념이 묻은 배달 플라스틱 용기",
            "3. 라벨이 붙어있는 투명 페트병",
            "4. 신문지 없이 버린 깨진 유리병",
            "5. 종량제 봉투에 넣은 폐건전지"
        ]
    )
    
    if selected == "1. 테이프·송장이 붙은 택배 박스":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='danger-card'><h4>❌ 경비원 아저씨의 고충</h4><p>수거 업체에서 테이프 부착 건은 전량 수거를 거부합니다. 결국 경비원분이 칼을 들고 일일이 테이프를 뜯어내야 합니다.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='info-card'><h4>✅ 주민 올바른 수칙</h4><p><b>테이프와 운송장은 완전히 제거</b>한 후, 박스를 납작하게 접어서 종이류 수거함에 배출해주세요.</p></div>", unsafe_allow_html=True)

    elif selected == "2. 양념이 묻은 배달 플라스틱 용기":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='danger-card'><h4>❌ 경비원 아저씨의 고충</h4><p>악취와 벌레를 유발하고 주변 깨끗한 재활용품까지 오염시킵니다. 경비원분이 직접 수세미로 닦거나 일반 쓰레기로 옮겨 담습니다.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='info-card'><h4>✅ 주민 올바른 수칙</h4><p>물로 깨끗이 헹궈서 배출하고, <b>착색되어 지워지지 않는 용기는 일반쓰레기(종량제 봉투)</b>로 버려주세요.</p></div>", unsafe_allow_html=True)

    elif selected == "3. 라벨이 붙어있는 투명 페트병":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='danger-card'><h4>❌ 경비원 아저씨의 고충</h4><p>투명 페트병 별도 배출제로 인해 라벨이 붙어있으면 아파트 전체에 과태료가 부과될 수 있어 일일이 손으로 제거합니다.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='info-card'><h4>✅ 주민 올바른 수칙</h4><p><b>비닐 라벨을 뜯어 비닐류에 버리고</b>, 페트병은 찌그러뜨린 후 뚜껑을 닫아 전용 수거함에 넣어주세요.</p></div>", unsafe_allow_html=True)

    elif selected == "4. 신문지 없이 버린 깨진 유리병":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='danger-card'><h4>❌ 경비원 아저씨의 고충</h4><p>마대 자루를 정돈하거나 수거하는 과정에서 날카로운 유리에 손이나 다리를 베이는 인명 사고가 자주 발생합니다.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='info-card'><h4>✅ 주민
