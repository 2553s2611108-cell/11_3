import streamlit as st
import time

# 페이지 설정
st.set_page_config(
    page_title="K-재활용 공영방송 | 의식 개선 뉴스 센터",
    page_icon="♻️",
    layout="wide"
)

# 커스텀 CSS (공영방송 자막 & 뉴스 스타일)
st.markdown("""
    <style>
    .news-header {
        background-color: #0b3c5d;
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 26px;
        margin-bottom: 20px;
    }
    .ticker {
        background-color: #d9534f;
        color: white;
        padding: 8px 15px;
        font-weight: bold;
        border-radius: 4px;
        margin-bottom: 25px;
    }
    .stat-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-left: 5px solid #0b3c5d;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.markdown("<div class='news-header'>📺 K-재활용 공영방송 : 올바른 분리배출 특별기획</div>", unsafe_allow_html=True)

# 속보 전광판
st.markdown("<div class='ticker'>🚨 [속보] 무분별한 혼합 배출로 재활용품 선별장 마비 심각... 관리 인력 고충 증대</div>", unsafe_allow_html=True)

# 사이드바 메뉴
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3299/3299935.png", width=100)
st.sidebar.title("📺 방송 편성표")
menu = st.sidebar.radio(
    "시청할 프로그램을 선택하세요:",
    ["1. [뉴스데스크] 분리배출 실태", "2. [특집기획] 잘못 배출하면 생기는 일", "3. [시민참여] O/X 환경 퀴즈"]
)

# ----------------------------------------------------
# 1. 뉴스데스크
# ----------------------------------------------------
if menu == "1. [뉴스데스크] 분리배출 실태":
    st.subheader("📰 [보도] 잘못된 분리배출이 만드는 '관리의 경고'")
    st.write("우리가 무심코 버린 쓰레기가 재활용품 선별장과 아파트 관리원분들에게 미치는 영향입니다.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📊 수거 쓰레기 중 잔재물 비율", value="38.5%", delta="오염으로 인한 폐기")
    with col2:
        st.metric(label="💸 연간 불필요한 처리 비용", value="약 1,200억 원", delta="+12% 증가", delta_color="inverse")
    with col3:
        st.metric(label="⏱️ 관리원 1인당 추가 작업시간", value="일 평균 2.5시간", delta="선별 작업 부담")

    st.markdown("---")
    st.markdown("### 📽️ [현장 취재] 주요 관리 어려움 TOP 3")
    
    tab1, tab2, tab3 = st.tabs(["🔴 음식물 묻은 용기", "🔴 라벨 미제거 페트병", "🔴 혼합 배출(이물질)"])
    
    with tab1:
        st.warning("⚠️ **관리 현장의 목소리:** '양념이 묻은 컵라면 용기나 플라스틱은 재활용이 불가능해 전량 세척하거나 일반쓰레기로 재분류해야 합니다.'")
        st.info("💡 **올바른 배출 방법:** 물로 깨끗이 헹군 후 배출하고, 이물질이 지워지지 않으면 일반쓰레기(종량제 봉투)로 버려주세요.")
        
    with tab2:
        st.warning("⚠️ **관리 현장의 목소리:** '투명 페트병의 비닐 라벨을 떼지 않으면 재사용 등급이 떨어지고, 세척 및 절단 기계 고장의 원인이 됩니다.'")
        st.info("💡 **올바른 배출 방법:** 라벨을 떼어 비닐류로 버리고, 페트병은 압착하여 뚜껑을 닫아 배출합니다.")

    with tab3:
        st.warning("⚠️ **관리 현장의 목소리:** '종이 상자에 테이프나 운송장이 붙어있거나, 상자 안에 스티로폼을 넣은 채 버리면 일일이 손으로 다 뜯어내야 합니다.'")
        st.info("💡 **올바른 배출 방법:** 송장과 테이프를 완전히 제거하고 상자는 펼쳐서 배출해주세요.")

# ----------------------------------------------------
# 2. 특집기획
# ----------------------------------------------------
elif menu == "2. [특집기획] 잘못 배출하면 생기는 일":
    st.subheader("🔍 [기획탐구] 내가 버린 쓰레기, 관리소에서는?")
    st.write("품목을 선택하면 잘못 배출했을 때의 **관리상 문제점**과 **해결 가이드**를 보여드립니다.")
    
    item = st.selectbox(
        "버리려는 물품을 선택해보세요:",
        ["선택하세요", "택배 상자 (테이프 부착)", "음식물 묻은 배달 용기", "투명 페트병 (라벨 부착)", "깨진 유리병", "건전지 / 보조배터리"]
    )
    
    if item == "택배 상자 (테이프 부착)":
        st.error("❌ **발생하는 문제:** 박스 재활용 시 테이프 이물질로 인해 재질 저하, 수거 거부 발생")
        st.success("✅ **관리 개선 솔루션:** 테이프·운송장 제거 ➔ 상자 접어서 종이류 배출")
    elif item == "음식물 묻은 배달 용기":
        st.error("❌ **발생하는 문제:** 다른 깨끗한 플라스틱까지 오염시켜 전체 재활용 불가 및 악취 발생")
        st.success("✅ **관리 개선 솔루션:** 내용물 씻기 ➔ 안 씻기면 종량제 봉투 배출")
    elif item == "투명 페트병 (라벨 부착)":
        st.error("❌ **발생하는 문제:** 수거 후 별도 인력이 일일이 라벨을 제거해야 함 (비용 및 시간 소요)")
        st.success("✅ **관리 개선 솔루션:** 라벨 제거 ➔ 압착 후 전용 수거함 배출")
    elif item == "깨진 유리병":
        st.error("❌ **발생하는 문제:** 수거 및 관리 작업자의 인명 사고(베임, 다침) 위험 매우 높음")
        st.success("✅ **관리 개선 솔루션:** 신문지로 싸서 불연성 마대(특수 종량제 봉투)에 배출")
    elif item == "건전지 / 보조배터리":
        st.error("❌ **발생하는 문제:** 일반 쓰레기나 플라스틱에 섞여 배출될 경우 수거 차량 및 처리장 화재 원인")
        st.success("✅ **관리 개선 솔루션:** 전용 폐건전지 수거함에 별도 배출")

# ----------------------------------------------------
# 3. 시민참여 퀴즈
# ----------------------------------------------------
elif menu == "3. [시민참여] O/X 환경 퀴즈":
    st.subheader("🧩 [시민참여] 올바른 분리배출 의식 테스트")
    st.write("퀴즈를 풀고 환경을 지키는 '공영방송 인증 모범 시민'이 되어보세요!")
    
    score = 0
    
    q1 = st.radio("Q1. 씻기지 않는 컵라면 스티로폼 용기는 재활용에 버려야 한다?", ("선택하세요", "O", "X"))
    if q1 == "X":
        score += 1
        st.caption("✨ 정답! 이물질이 제거되지 않는 용기는 종량제 봉투로 버려야 관리자분들의 2차 분류 수고를 줄입니다.")
    elif q1 == "O":
        st.caption("❌ 오답! 오염된 용기는 재활용이 안 되며, 다른 재활용품까지 오염시킵니다.")
        
    st.markdown("---")
    q2 = st.radio("Q2. 깨진 유리병은 일반 유리병 수거함에 버려도 된다?", ("선택하세요", "O", "X"))
    if q2 == "X":
        score += 1
        st.caption("✨ 정답! 깨진 유리는 관리자가 다칠 수 있으므로 신문지에 싸서 불연성 마대에 버려야 합니다.")
    elif q2 == "O":
        st.caption("❌ 오답! 관리원의 부상 위험이 높습니다.")

    st.markdown("---")
    q3 = st.radio("Q3. 페트병의 비닐 라벨은 반드시 떼어서 비닐류로 따로 버려야 한다?", ("선택하세요", "O", "X"))
    if q3 == "O":
        score += 1
        st.caption("✨ 정답! 라벨을 제거해야 고품질 리사이클링이 가능합니다.")
    elif q3 == "X":
        st.caption("❌ 오답! 라벨 미제거 시 수거 및 재활용 과정에서 심각한 차질을 빚습니다.")

    st.markdown("---")
    if st.button("결과 확인 및 인증서 발급"):
        with st.spinner("결과 분석 중..."):
            time.sleep(1)
        st.balloons()
        st.success(f"🎊 3문제 중 {score}문제를 맞추셨습니다!")
        if score == 3:
            st.info("🏆 **[K-재활용 공영방송 인증] 최우수 환경 모범 시민입니다!**\n\n여러분의 올바른 배출이 관리소 및 선별장의 부담을 50% 이상 줄입니다.")
        else:
            st.warning("💪 올바른 분리배출법을 조금 더 학습하고 다시 도전해보세요!")

# 하단 공영방송 자막 푸터
st.markdown("---")
st.caption("📺 K-재활용 공영방송 | 본 프로그램은 분리배출 의식 개선 및 관리 환경 개선을 위해 제작되었습니다.")
