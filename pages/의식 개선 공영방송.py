
import streamlit as st
import time
import html

# ==================================================
# 1. 페이지 설정
# ==================================================
st.set_page_config(
    page_title="분리온 | 올바른 분리배출",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# 2. 디자인 CSS
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #101426;
    --navy-light: #1b2340;
    --blue: #5278f6;
    --mint: #48c9b0;
    --text: #202942;
    --muted: #8790a6;
    --surface: #ffffff;
    --page: #f4f6fc;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: var(--page);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: var(--navy);
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

.block-container {
    max-width: 1180px;
    padding: 1.5rem 2rem 3rem;
}

.main-header {
    background: linear-gradient(120deg, #11172d, #26365e);
    color: white;
    padding: 30px;
    border-radius: 24px;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
}

.eyebrow {
    color: #9fb4ff;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.hero-title {
    font-size: clamp(25px, 3.2vw, 38px);
    font-weight: 800;
    line-height: 1.4;
    margin-bottom: 12px;
}

.hero-desc {
    color: #d3daf0;
    font-size: 14px;
    line-height: 1.8;
}

.hero-pill {
    display: inline-block;
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.18);
    color: #e9edff;
    border-radius: 30px;
    padding: 7px 13px;
    font-size: 12px;
    margin-top: 15px;
}

.section-label {
    color: var(--blue);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.6px;
    margin-top: 8px;
    margin-bottom: 5px;
}

.section-title {
    color: var(--text);
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 5px;
}

.section-desc {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.8;
    margin-bottom: 20px;
}

.white-card {
    background: white;
    border: 1px solid #e9edf6;
    border-radius: 19px;
    padding: 21px;
    margin-bottom: 14px;
    box-shadow: 0 5px 20px rgba(30, 45, 90, .035);
}

.card-icon {
    font-size: 25px;
    margin-bottom: 12px;
}

.card-title {
    color: var(--text);
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 8px;
}

.card-desc {
    color: #7d879d;
    font-size: 12px;
    line-height: 1.8;
}

.metric-card {
    background: white;
    border: 1px solid #e7ebf5;
    border-radius: 18px;
    padding: 20px;
    min-height: 142px;
    box-shadow: 0 5px 18px rgba(30, 45, 90, .035);
}

.metric-label {
    color: #7c869d;
    font-size: 12px;
    margin-bottom: 12px;
}

.metric-value {
    color: var(--text);
    font-size: 27px;
    font-weight: 800;
}

.metric-note {
    color: #8992a7;
    font-size: 11px;
    margin-top: 9px;
}

.notice-card {
    background: #fff7e8;
    border: 1px solid #ffe8b8;
    border-radius: 16px;
    padding: 18px;
    margin: 12px 0;
    color: #674b19;
    font-size: 13px;
    line-height: 1.9;
}

.good-card {
    background: #effbf7;
    border: 1px solid #d7f3e9;
    border-radius: 16px;
    padding: 18px;
    margin: 12px 0;
    color: #176d59;
    font-size: 13px;
    line-height: 1.9;
}

.news-card {
    background: white;
    border-radius: 18px;
    padding: 21px;
    border: 1px solid #e8edf5;
    margin-bottom: 14px;
}

.news-tag {
    display: inline-block;
    background: #fff0f0;
    color: #d34b55;
    font-size: 11px;
    font-weight: 800;
    padding: 5px 9px;
    border-radius: 7px;
    margin-bottom: 10px;
}

.progress-track {
    height: 10px;
    background: #e9edf8;
    border-radius: 20px;
    overflow: hidden;
    margin: 14px 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #5278f6, #54cbb2);
    border-radius: 20px;
}

.score-card {
    background: linear-gradient(135deg, #182343, #344d84);
    color: white;
    border-radius: 22px;
    padding: 28px;
    text-align: center;
    margin: 20px 0;
}

.score-number {
    font-size: 54px;
    font-weight: 800;
    line-height: 1.3;
}

.score-caption {
    color: #d5defb;
    font-size: 13px;
}

.message-card {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 16px;
    padding: 17px;
    margin: 10px 0;
}

.message-name {
    color: #3455ba;
    font-weight: 800;
    font-size: 13px;
    margin-bottom: 8px;
}

.message-text {
    color: #424c62;
    font-size: 13px;
    line-height: 1.8;
    overflow-wrap: anywhere;
}

.footer {
    text-align: center;
    color: #929aaf;
    font-size: 11px;
    line-height: 1.9;
    padding: 25px 10px;
    margin-top: 25px;
    border-top: 1px solid #e4e8f1;
}

/* 상단 메뉴를 둥근 버튼처럼 표시 */
div[role="radiogroup"] {
    gap: 8px;
    margin: 12px 0 25px;
}

div[role="radiogroup"] label {
    background: white;
    border: 1px solid #e3e8f3;
    border-radius: 13px;
    padding: 10px 14px;
    transition: all .2s ease;
}

div[role="radiogroup"] label:has(input:checked) {
    background: #eaf0ff;
    border-color: #b9c9ff;
    color: #3455ba;
}

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 700;
    border: none;
    background: #4268ec;
    color: white;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #3153ce;
    color: white;
    border-color: transparent;
}

.stSelectbox > div > div,
.stTextInput input,
.stTextArea textarea {
    border-radius: 12px;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e8edf5;
    padding: 18px;
    border-radius: 16px;
}

[data-testid="stMetricValue"] {
    color: #27385e;
}

hr {
    border-color: #e5e9f3;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem .8rem 2rem;
    }

    .main-header {
        padding: 23px 18px;
        border-radius: 19px;
    }

    .hero-title {
        font-size: 25px;
    }

    .section-title {
        font-size: 20px;
    }

    .white-card, .news-card {
        padding: 16px;
    }

    div[role="radiogroup"] {
        gap: 5px;
    }

    div[role="radiogroup"] label {
        padding: 8px 9px;
        font-size: 12px;
    }

    .score-number {
        font-size: 44px;
    }
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 3. 세션 상태 초기화
# ==================================================
if "cheer_messages" not in st.session_state:
    st.session_state["cheer_messages"] = [
        {
            "name": "101동 주민",
            "msg": "상자 테이프 항상 떼고 버릴게요. 매번 고생 많으십니다!"
        },
        {
            "name": "502호 주민",
            "msg": "배달 용기 깨끗이 씻어서 버리는 습관 만들었습니다. 감사합니다."
        }
    ]

if "quiz_result" not in st.session_state:
    st.session_state["quiz_result"] = None

# ==================================================
# 4. 상단 브랜드 및 메인 배너
# ==================================================
st.markdown("""
<div class="main-header">
    <div class="eyebrow">PUBLIC INTEREST PROJECT · 2026</div>
    <div class="hero-title">♻️ 분리온<br>올바른 분리배출, 따뜻한 공동체</div>
    <div class="hero-desc">
        무심코 버린 쓰레기 하나가 누군가의 추가 노동이 되지 않도록.<br>
        올바른 분리배출로 아파트 경비원분들의 수고를 줄여 주세요.
    </div>
    <div class="hero-pill">주민 참여형 환경 개선 캠페인</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice-card">
    <b>📢 오늘의 공익 메시지</b><br>
    택배 상자의 테이프를 떼고, 페트병의 라벨을 제거하는 작은 실천이
    더 안전하고 깨끗한 분리배출 공간을 만듭니다.
</div>
""", unsafe_allow_html=True)

# ==================================================
# 5. 상단 네비게이션
# ==================================================
menu_items = [
    "🏠 홈",
    "📰 현장 보도",
    "🔎 배출 가이드",
    "🧩 양심 지수",
    "💌 응원 게시판"
]

selected_menu = st.radio(
    "메뉴",
    menu_items,
    horizontal=True,
    label_visibility="collapsed",
    key="main_navigation"
)

st.markdown("---")

# ==================================================
# 6. 홈 화면
# ==================================================
if selected_menu == "🏠 홈":
    st.markdown('<div class="section-label">WELCOME</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">오늘의 분리배출 브리핑</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">작은 실천으로 달라지는 우리 아파트를 만나 보세요.</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    home_cards = [
        (c1, "📰", "현장 보도", "분리배출 현장의 어려움과 주요 문제를 알아봐요."),
        (c2, "♻️", "배출 가이드", "자주 틀리는 5가지 배출 방법을 확인해요."),
        (c3, "💌", "응원 게시판", "감사 인사와 나의 실천 약속을 남겨요.")
    ]

    for col, icon, title, desc in home_cards:
        with col:
            st.markdown(f"""
            <div class="white-card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{title}</div>
                <div class="card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">TODAY\'S ACTION</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">오늘 실천할 세 가지</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="white-card">
        <div class="card-title">01. 📦 택배 상자 정리하기</div>
        <div class="card-desc">테이프와 송장을 떼고 상자를 납작하게 접어 주세요.</div>
    </div>
    <div class="white-card">
        <div class="card-title">02. 🧴 투명 페트병 비우기</div>
        <div class="card-desc">내용물을 비우고 라벨을 제거한 후 전용 수거함을 이용해요.</div>
    </div>
    <div class="white-card">
        <div class="card-title">03. 💙 감사 인사 전하기</div>
        <div class="card-desc">매일 수고하시는 경비원분들께 따뜻한 말 한마디를 건네요.</div>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 상단 메뉴에서 각 코너를 선택하면 더 자세한 내용을 볼 수 있어요.")

# ==================================================
# 7. 현장 보도
# ==================================================
elif selected_menu == "📰 현장 보도":
    st.markdown('<div class="section-label">FIELD REPORT</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">무심코 버린 쓰레기, 누군가에겐 과중한 노동입니다</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">분리배출 과정에서 발생할 수 있는 작업 부담과 안전 문제를 살펴봅니다.</div>',
        unsafe_allow_html=True
    )

    st.warning(
        "아래 수치는 기존 기획안에 기재된 예시입니다. "
        "공식 통계로 사용하려면 신뢰할 수 있는 조사 자료로 확인해 주세요."
    )

    metrics = [
        ("⏱️", "재작업 시간", "2.8시간", "기존 기획안의 일평균 예시"),
        ("♻️", "잘못된 배출 비율", "42.1%", "기존 기획안의 예시"),
        ("🩹", "부상 경험", "67.3%", "기존 기획안의 예시")
    ]

    cols = st.columns(3)

    for col, (icon, label, value, note) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{icon} {label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-title">🎙️ 현장 인터뷰</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="white-card">
        <div class="news-tag">현장 목소리 · 재구성 예시</div>
        <div style="font-size:16px;font-weight:700;line-height:1.9;color:#27334e;">
            "테이프가 붙은 상자를 다시 정리하고, 오염된 용기를 구분하는
            일이 반복됩니다. 주민분들이 조금만 신경 써 주셔도 큰 도움이 됩니다."
        </div>
        <div class="card-desc" style="margin-top:14px;">
            — 아파트 경비원 인터뷰 예시
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">⚠️ 우리가 기억할 점</div>',
                unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div class="notice-card">
            <b>❌ 잘못된 배출이 만드는 문제</b><br>
            · 재활용품의 오염<br>
            · 반복적인 재분류 작업<br>
            · 날카로운 폐기물로 인한 안전사고 위험
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="good-card">
            <b>✅ 주민이 실천할 수 있는 변화</b><br>
            · 배출 전 이물질 제거하기<br>
            · 품목별 수거함에 정확히 넣기<br>
            · 위험한 폐기물은 안전하게 포장하기
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# 8. 배출 가이드
# ==================================================
elif selected_menu == "🔎 배출 가이드":
    st.markdown('<div class="section-label">RECYCLING GUIDE</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">헷갈리는 분리배출, 한 번에 해결하기</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">품목을 선택하면 문제점과 올바른 배출 방법을 확인할 수 있습니다.</div>',
        unsafe_allow_html=True
    )

    guide_data = {
        "택배 상자": {
            "icon": "📦",
            "problem": "테이프와 송장이 붙어 있으면 종이류 재활용에 방해가 될 수 있어요.",
            "solution": "테이프와 송장을 제거하고 상자를 납작하게 접어 종이류로 배출하세요.",
            "tip": "젖거나 기름에 오염된 종이는 일반 종이류와 분리하세요."
        },
        "배달 플라스틱 용기": {
            "icon": "🥡",
            "problem": "음식물과 양념이 남아 있으면 다른 재활용품까지 오염될 수 있어요.",
            "solution": "내용물을 비우고 깨끗하게 헹군 뒤 재질에 맞게 분리하세요.",
            "tip": "세척해도 오염이 심하게 남는 용기는 지역 배출 기준을 확인하세요."
        },
        "투명 페트병": {
            "icon": "🧴",
            "problem": "내용물과 라벨이 남아 있으면 재활용 품질이 떨어질 수 있어요.",
            "solution": "내용물을 비우고 라벨을 제거한 뒤 찌그러뜨려 뚜껑을 닫아 전용 수거함에 배출하세요.",
            "tip": "전용 수거함 운영 여부와 세부 방법은 거주 지역 안내를 확인하세요."
        },
        "깨진 유리": {
            "icon": "⚠️",
            "problem": "깨진 유리는 수거와 운반 과정에서 손을 다치게 할 수 있어요.",
            "solution": "두꺼운 종이 등으로 안전하게 감싸고 지역 규정에 맞는 불연성 폐기물 수거 방법을 이용하세요.",
            "tip": "깨진 유리를 일반 유리병 재활용함에 넣지 마세요. 지역별 배출 기준을 확인하세요."
        },
        "폐건전지": {
            "icon": "🔋",
            "problem": "일반 쓰레기에 섞인 건전지는 처리 과정에서 화재 등의 위험을 일으킬 수 있어요.",
            "solution": "일반 종량제 봉투에 넣지 말고 폐건전지 전용 수거함에 배출하세요.",
            "tip": "전용 수거함은 관리사무소나 주민센터에 문의해 확인할 수 있어요."
        }
    }

    selected_item = st.selectbox(
        "어떤 품목을 버리려고 하나요?",
        list(guide_data.keys()),
        key="guide_select"
    )

    item = guide_data[selected_item]

    st.markdown(f"""
    <div class="white-card">
        <div class="card-icon">{item['icon']}</div>
        <div class="card-title" style="font-size:20px;">{selected_item}</div>
        <div class="notice-card">
            <b>⚠️ 주의할 점</b><br>{item['problem']}
        </div>
        <div class="good-card">
            <b>✅ 올바른 배출 방법</b><br>{item['solution']}
        </div>
        <div class="card-desc">💡 참고: {item['tip']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📋 다섯 가지 실천 체크리스트</div>',
                unsafe_allow_html=True)

    checklist = [
        "택배 상자의 테이프와 송장을 제거했어요.",
        "배달 용기의 음식물과 양념을 씻어 냈어요.",
        "투명 페트병의 라벨을 제거했어요.",
        "깨진 유리를 안전하게 포장했어요.",
        "폐건전지를 전용 수거함에 넣었어요."
    ]

    for i, task in enumerate(checklist):
        st.checkbox(task, key=f"checklist_{i}")

# ==================================================
# 9. 양심 지수
# ==================================================
elif selected_menu == "🧩 양심 지수":
    st.markdown('<div class="section-label">MY ECO SCORE</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">나의 분리배출 양심 지수</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">세 가지 질문으로 나의 분리배출 습관을 확인해 보세요.</div>',
        unsafe_allow_html=True
    )

    with st.form("quiz_form"):
        q1 = st.radio(
            "01. 택배 상자의 테이프와 송장을 제거하나요?",
            ["선택하세요", "항상 제거한다", "가끔 그대로 버린다", "전혀 신경 쓰지 않는다"],
            key="quiz_q1"
        )

        q2 = st.radio(
            "02. 배달 용기의 양념이 깨끗하게 지워지지 않으면 어떻게 하나요?",
            ["선택하세요", "지역 기준에 따라 일반 쓰레기로 배출한다",
             "그대로 재활용 수거함에 넣는다"],
            key="quiz_q2"
        )

        q3 = st.radio(
            "03. 투명 페트병의 라벨을 제거하나요?",
            ["선택하세요", "네, 제거한다", "아니요, 그대로 버린다"],
            key="quiz_q3"
        )

        quiz_submit = st.form_submit_button(
            "내 양심 지수 확인하기",
            use_container_width=True
        )

    if quiz_submit:
        if "선택하세요" in (q1, q2, q3):
            st.error("세 가지 질문에 모두 답변해 주세요.")
            st.session_state["quiz_result"] = None
        else:
            score = 0
            score += 30 if q1 == "항상 제거한다" else 0
            score += 35 if q2 == "지역 기준에 따라 일반 쓰레기로 배출한다" else 0
            score += 35 if q3 == "네, 제거한다" else 0

            st.session_state["quiz_result"] = score

    score = st.session_state["quiz_result"]

    if score is not None:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-caption">MY RECYCLING SCORE</div>
            <div class="score-number">{score}<span style="font-size:22px;"> / 100</span></div>
            <div class="progress-track">
                <div class="progress-fill" style="width:{score}%;"></div>
            </div>
            <div class="score-caption">나의 분리배출 실천 점수</div>
        </div>
        """, unsafe_allow_html=True)

        if score == 100:
            st.success(
                "🌟 완벽한 실천! 올바른 분리배출 습관을 잘 지키고 있어요."
            )
            st.balloons()
        elif score >= 60:
            st.info(
                "🙂 좋은 출발이에요! 놓친 항목을 하나씩 실천해 보세요."
            )
        else:
            st.warning(
                "🌱 지금부터 하나씩 바꿔 봐요. 작은 습관도 큰 도움이 됩니다."
            )

        st.caption(
            "이 점수는 학습과 실천을 위한 참고용이며, "
            "개인의 인격이나 실제 환경 기여도를 평가하지 않습니다."
        )

# ==================================================
# 10. 응원 게시판
# ==================================================
elif selected_menu == "💌 응원 게시판":
    st.markdown('<div class="section-label">COMMUNITY</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">따뜻한 마음을 전해 주세요</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">경비원분들께 감사 인사를 전하고, 나의 실천 약속을 남겨 보세요.</div>',
        unsafe_allow_html=True
    )

    with st.form("cheer_form", clear_on_submit=True):
        input_name = st.text_input(
            "닉네임",
            max_chars=30,
            placeholder="예: 101동 주민"
        )

        input_msg = st.text_area(
            "응원 메시지",
            max_chars=500,
            placeholder="예: 늘 고생 많으십니다. 박스 테이프 꼭 떼고 버릴게요!"
        )

        submitted = st.form_submit_button(
            "💙 응원 메시지 등록하기",
            use_container_width=True
        )

        if submitted:
            if not input_name.strip() or not input_msg.strip():
                st.warning("닉네임과 응원 메시지를 모두 입력해 주세요.")
            else:
                st.session_state["cheer_messages"].insert(
                    0,
                    {
                        "name": input_name.strip(),
                        "msg": input_msg.strip()
                    }
                )
                st.session_state["cheer_messages"] = (
                    st.session_state["cheer_messages"][:100]
                )
                st.success("응원 메시지가 등록되었습니다!")

    st.markdown("---")
    st.markdown('<div class="section-title">💌 주민 응원 전광판</div>',
                unsafe_allow_html=True)

    messages = st.session_state.get("cheer_messages", [])

    if not messages:
        st.info("첫 번째 응원 메시지를 남겨 주세요!")
    else:
        for message in messages:
            safe_name = html.escape(str(message.get("name", "익명")))
            safe_msg = html.escape(str(message.get("msg", "")))

            st.markdown(f"""
            <div class="message-card">
                <div class="message-name">💙 {safe_name}</div>
                <div class="message-text">{safe_msg}</div>
            </div>
            """, unsafe_allow_html=True)

    st.caption(
        "안내: 현재 게시판은 Streamlit 세션에 저장됩니다. "
        "앱이 재시작되면 메시지가 사라질 수 있습니다."
    )

# ==================================================
# 11. 푸터
# ==================================================
st.markdown("""
<div class="footer">
    <b>♻️ 분리온 | 올바른 분리배출, 따뜻한 공동체</b><br>
    아파트 경비원 업무 부담 완화 및 올바른 분리배출을 위한 공익 프로젝트<br>
    정확한 배출 방법은 거주 지역과 아파트 관리사무소의 안내를 확인해 주세요.
</div>
""", unsafe_allow_html=True)
