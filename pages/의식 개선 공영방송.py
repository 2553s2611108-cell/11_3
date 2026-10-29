import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="K-공영방송 | 경비원 아저씨의 분리배출 고충 센터",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS (제시된 이미지 UI 스타일 반영: 오렌지/코랄 톤 모던 레이아웃)
st.markdown("""
    <style>
    /* 전체 배경 및 기본 폰트 설정 */
    .stApp {
        background-color: #FAFAFA;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
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
st.markdown("<div class='sub-header'>🚨 [긴급 보도] 혼합 배출로 지자체 수거 거부 속출... 경비원 80% 이상이 재분류 작업으로 심각한 고충 호소</div>", unsafe_allow_html=True)

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
    st.write("")
    
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
            st.markdown("<div class='danger-box'><h4 style='color:#FF5252; margin-top:0;'>❌ 경비원 아저씨의 고충</h4><p style='color:#424242;'>수거 업체에서 테이프 부착 건은 전량 수거를 거부합니다. 결국 경비원분이 칼을 들고 일일이 테이프를 뜯어내야 합니다.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='info-box'><h4 style='color:#FF7E5F; margin-top:0;'>✅ 주민 올바른 수칙</h4><p style='color:#424242;'><b>테이프와 운송장은 완전히 제거</b>한 후, 박스를 납작하게 접어서 종이류 수거함에 배출해주세요.</p></div>", unsafe_allow_html=True)

    elif selected == "2. 양념이 묻은 배달 플라스틱 용기":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='danger-box'><h4 style='color:#FF5252; margin-top:0;'>❌ 경비원 아저씨의 고충</h4><p style='color:#424242;'>악취와 벌레를 유발하고 주변 깨끗한 재활용품까지 오염시킵니다. 경비원분이 직접 수세미로 닦거나 일반 쓰레기로 옮겨 담습니다.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='info-box'><h4 style='color:#FF7E5F; margin-top:0;'>✅ 주민 올바른 수칙</h4><p style='color:#424242;'>물로 깨끗이 헹궈서 배출하고, <b>착색되어 지워지지 않는 용기는 일반쓰레기(종량제 봉투)</b>로 버려주세요.</p></div>", unsafe_allow_html=True)

    elif selected == "3. 라벨이 붙어있는 투명 페트병":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='danger-box'><h4 style='color:#FF5252; margin-top:0;'>❌ 경비원 아저씨의 고충</h4><p style='color:#424242;'>투명 페트병 별도 배출제로 인해 라벨이 붙어있으면 아파트 전체에 과태료가 부과될 수 있어 일일이 손으로 제거합니다.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='info-box'><h4 style='color:#FF7E5F; margin-top:0;'>✅ 주민 올바른 수칙</h4><p style='color:#424242;'><b>비닐 라벨을 뜯어 비닐류에 버리고</b>, 페트병은 찌그러뜨린 후 뚜껑을 닫아 전용 수거함에 넣어주세요.</p></div>", unsafe_allow_html=True)

    elif selected == "4. 신문지 없이 버린 깨진 유리병":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='danger-box'><h4 style='color:#FF5252; margin-top:0;'>❌ 경비원 아저씨의 고충</h4><p style='color:#424242;'>마대 자루를 정돈하거나 수거하는 과정에서 날카로운 유리에 손이나 다리를 베이는 인명 사고가 자주 발생합니다.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='info-box'><h4 style='color:#FF7E5F; margin-top:0;'>✅ 주민 올바른 수칙</h4><p style='color:#424242;'>깨진 유리는 <b>신문지나 두꺼운 종이로 겹겹이 싸서</b> 불연성 마대(특수 종량제 봉투)에 담아 배출해 주세요.</p></div>", unsafe_allow_html=True)

    elif selected == "5. 종량제 봉투에 넣은 폐건전지":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='danger-box'><h4 style='color:#FF5252; margin-top:0;'>❌ 경비원 아저씨의 고충</h4><p style='color:#424242;'>청소차나 압축 과정에서 폭발 및 화재가 발생하여 경비원 및 수거 기사의 안전을 심각하게 위협합니다.</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='info-box'><h4 style='color:#FF7E5F; margin-top:0;'>✅ 주민 올바른 수칙</h4><p style='color:#424242;'>폐건전지는 절대로 일반 쓰레기에 버리지 마시고 <b>관리사무소나 동별 폐건전지 전용 수거함</b>에 넣어주세요.</p></div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. 주민 참여
# ----------------------------------------------------
elif menu == "3. [주민 참여] 나의 분리배출 양심 지수":
    st.subheader("🧩 [자가진단] 나는 경비원 아저씨께 어떤 주민일까요?")
    st.write("3가지 질문에 답하고 나의 분리배출 점수를 확인해 보세요.")
    
    q1 = st.radio("1. 택배 박스를 버릴 때 비닐 테이프와 운송장을 제거하나요?", ["선택하세요", "항상 제거한다", "가끔 그대로 버린다", "전혀 신경 안 쓴다"], key="q1")
    q2 = st.radio("2. 컵라면/배달 용기 양념이 안 지워질 때 어떻게 버리나요?", ["선택하세요", "종량제 봉투(일반쓰레기)에 버린다", "그냥 플라스틱/스티로폼 수거함에 넣는다"], key="q2")
    q3 = st.radio("3. 투명 페트병 버릴 때 비닐 라벨을 떼어내나요?", ["선택하세요", "네, 반드시 떼어서 버립니다", "아니오, 붙은 채로 버립니다"], key="q3")
    
    st.markdown("---")
    if st.button("양심 지수 결과 확인하기"):
        if q1 == "선택하세요" or q2 == "선택하세요" or q3 == "선택하세요":
            st.error("⚠️ 모든 질문에 답변을 선택해 주세요.")
        else:
            score = 0
            if q1 == "항상 제거한다":
                score += 30
            if q2 == "종량제 봉투(일반쓰레기)에 버린다":
                score += 35
            if q3 == "네, 반드시 떼어서 버립니다":
                score += 35
                
            with st.spinner("분석 중..."):
                time.sleep(0.4)
            
            st.markdown(f"### 📊 나의 점수: **{score}점 / 100점**")
            
            if score == 100:
                st.balloons()
                st.success("🌟 **[100점 Perfect] 경비원 아저씨가 감사해하는 최고의 모범 주민입니다!**")
            elif score >= 60:
                st.warning("🙂 **[보통] 조금만 더 신경 써 주세요!** 경비원 아저씨의 손길이 한 번 더 가고 있습니다.")
            else:
                st.error("🚨 **[경고] 경비원 아저씨의 업무 부담을 크게 증가시키고 있습니다.** 올바른 배출법을 실천해 주세요!")

# ----------------------------------------------------
# 4. 공익 캠페인
# ----------------------------------------------------
elif menu == "4. [공익 캠페인] 경비원 아저씨 응원 게시판":
    st.subheader("💌 경비원 아저씨께 전하는 응원과 실천 다짐")
    
    with st.form(key="cheer_form_clean", clear_on_submit=True):
        input_name = st.text_input("동/호수 또는 닉네임", placeholder="예: 101동 주민")
        input_msg = st.text_area("응원 메시지", placeholder="예: 늘 고생 많으십니다. 박스 테이프 꼭 떼고 버릴게요!")
        submitted = st.form_submit_button("메시지 등록")
        
        if submitted:
            if not input_name.strip() or not input_msg.strip():
                st.warning("⚠️ 닉네임과 메시
