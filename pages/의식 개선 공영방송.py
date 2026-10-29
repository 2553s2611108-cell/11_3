
import streamlit as st
import html

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="분리온 | 에코 라이프",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 보라색 교육 앱 디자인
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

:root {
    --purple: #8247f5;
    --purple-dark: #6533d8;
    --lavender: #f0e9ff;
    --ink: #27233b;
    --muted: #88859b;
    --line: #ece9f4;
    --bg: #f7f5fc;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1120px;
    padding: 1.5rem 2rem 3rem;
}

[data-testid="stSidebar"] {
    background: #fff;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: var(--ink);
}

/* 상단 로고 */
.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px 0 22px;
}

.brand-icon {
    background: var(--purple);
    color: white;
    width: 43px;
    height: 43px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}

.brand-name {
    color: var(--ink);
    font-size: 21px;
    font-weight: 800;
}

.brand-sub {
    color: var(--muted);
    font-size: 11px;
}

/* 보라색 메인 배너 */
.hero {
    background: linear-gradient(135deg, #8649fb, #7139e7);
    color: white;
    padding: 32px;
    border-radius: 27px;
    margin: 8px 0 23px;
    box-shadow: 0 12px 30px rgba(130, 71, 245, .18);
}

.hero-label {
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 700;
    color: #e6d9ff;
    margin-bottom: 15px;
}

.hero-title {
    font-size: clamp(25px, 3vw, 36px);
    font-weight: 800;
    line-height: 1.45;
    margin-bottom: 12px;
}

.hero-desc {
    font-size: 13px;
    color: #f0e8ff;
    line-height: 1.9;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,.17);
    border: 1px solid rgba(255,255,255,.25);
    padding: 8px 13px;
    border-radius: 30px;
    margin-top: 18px;
    font-size: 11px;
}

/* 제목 */
.eyebrow {
    color: var(--purple);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.7px;
    margin: 20px 0 7px;
}

.section-title {
    color: var(--ink);
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 7px;
}

.section-desc {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.9;
    margin-bottom: 20px;
}

/* 카드 */
.app-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow: 0 5px 20px rgba(54, 34, 95, .035);
}

.card-icon {
    width: 48px;
    height: 48px;
    border-radius: 15px;
    background: var(--lavender);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    margin-bottom: 15px;
}

.card-title {
    color: var(--ink);
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 8px;
}

.card-desc {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.9;
}

/* 통계 */
.metric-card {
    background: white;
    padding: 19px;
    border-radius: 19px;
    border: 1px solid var(--line);
    min-height: 130px;
}

.metric-label {
    color: var(--muted);
    font-size: 12px;
}

.metric-number {
    color: var(--purple);
    font-size: 29px;
    font-weight: 800;
    margin: 14px 0 7px;
}

.metric-note {
    color: var(--muted);
    font-size: 11px;
}

/* 안내 카드 */
.purple-note {
    background: #f1eaff;
    color: #5835a6;
    border-radius: 17px;
    padding: 18px;
    font-size: 13px;
    line-height: 1.9;
    margin: 12px 0;
}

.green-note {
    background: #eafaf3;
    color: #24775a;
    border-radius: 17px;
    padding: 18px;
    font-size: 13px;
    line-height: 1.9;
    margin: 12px 0;
}

.yellow-note {
    background: #fff7e8;
    color: #78551b;
    border-radius: 17px;
    padding: 18px;
    font-size: 13px;
    line-height: 1.9;
    margin: 12px 0;
}

/* 점수 */
.score-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 23px;
    padding: 28px 20px;
    text-align: center;
    margin: 20px 0;
}

.score-circle {
    width: 145px;
    height: 145px;
    border-radius: 50%;
    border: 8px solid #e9ddff;
    background: #faf7ff;
    margin: 0 auto 18px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.score-number {
    color: var(--purple);
    font-size: 38px;
    font-weight: 800;
    line-height: 1.3;
}

.score-small {
    color: var(--muted);
    font-size: 11px;
}

.progress-track {
    height: 10px;
    background: #eee9f7;
    border-radius: 20px;
    overflow: hidden;
    margin: 15px 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #a984ff, #8247f5);
    border-radius: 20px;
}

/* 응원 게시판 */
.message-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 17px;
    padding: 17px;
    margin: 11px 0;
}

.message-name {
    color: var(--purple);
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 8px;
}

.message-body {
    color: #4f4b61;
    font-size: 13px;
    line-height: 1.9;
    overflow-wrap: anywhere;
}

/* 네비게이션 */
div[role="radiogroup"] {
    gap: 8px;
    margin: 8px 0 22px;
}

div[role="radiogroup"] label {
    background: white;
    border: 1px solid #e9e4f3;
    border-radius: 13px;
    padding: 10px 13px;
    font-size: 13px;
}

div[role="radiogroup"] label:has(input:checked) {
    background: var(--purple);
    color: white;
    border-color: var(--purple);
}

.stButton > button,
.stFormSubmitButton > button {
    background: var(--purple);
    color: white;
    border: 1px solid var(--purple);
    border-radius: 13px;
    min-height: 45px;
    font-weight: 700;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: var(--purple-dark);
    border-color: var(--purple-dark);
    color: white;
}

.stSelectbox > div > div,
.stTextInput input,
.stTextArea textarea {
    border-radius: 12px;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid var(--line);
    border-radius: 16px;
}

.footer {
    border-top: 1px solid var(--line);
    color: var(--muted);
    text-align: center;
    padding: 24px 10px;
    margin-top: 28px;
    font-size: 11px;
    line-height: 1.9;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem .8rem 2rem;
    }

    .hero {
        padding: 23px 18px;
        border-radius: 21px;
    }

    .hero-title {
        font-size: 25px;
    }

    .section-title {
        font-size: 20px;
    }

    .app-card {
        padding: 17px;
    }

    div[role="radiogroup"] {
        gap: 5px;
    }

    div[role="radiogroup"] label {
        padding: 8px;
        font-size: 11px;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 세션 상태
# ==========================================
if "cheer_messages" not in st.session_state:
    st.session_state["cheer_messages"] = [
        {
            "name": "101동 주민",
            "msg": "상자 테이프 항상 떼고 버릴게요. 매번 고생 많으십니다!"
        },
        {
            "name": "502호 주민",
            "msg": "배달 용기를 깨끗이 씻어 버리겠습니다. 감사합니다."
        }
    ]

if "quiz_result" not in st.session_state:
    st.session_state["quiz_result"] = None

# ==========================================
# 4. 로고
# ==========================================
st.markdown("""
<div class="brand">
    <div class="brand-icon">♻️</div>
    <div>
        <div class="brand-name">분리온</div>
        <div class="brand-sub">ECO LIFE · BETTER COMMUNITY</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. 메인 배너
# ==========================================
st.markdown("""
<div class="hero">
    <div class="hero-label">WELCOME TO BUNRI-ON</div>
    <div class="hero-title">
        올바른 분리배출,<br>
        따뜻한 공동체 💜
    </div>
    <div class="hero-desc">
        작은 습관이 만드는 큰 변화.<br>
        우리 아파트와 경비원분들을 위한 친환경 실천을 시작해 보세요.
    </div>
    <div class="hero-badge">♻️ 오늘도 함께하는 에코 라이프</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. 메뉴
# ==========================================
menu_items = [
    "🏠 홈",
    "📊 대시보드",
    "📚 배출 가이드",
    "🏆 양심 지수",
    "💌 응원 게시판"
]

menu = st.radio(
    "메뉴 선택",
    menu_items,
    horizontal=True,
    label_visibility="collapsed",
    key="main_menu"
)

st.markdown("---")

# ==========================================
# 7. 홈
# ==========================================
if menu == "🏠 홈":
    st.markdown('<div class="eyebrow">GET STARTED</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">오늘의 에코 미션</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">세 가지 작은 실천으로 깨끗한 아파트를 만들어요.</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(3)

    cards = [
        ("📦", "택배 상자 정리", "테이프와 송장을 제거하고 납작하게 접어요."),
        ("🧴", "페트병 라벨 제거", "내용물을 비우고 라벨을 분리해요."),
        ("💜", "감사 인사 전하기", "경비원분들께 따뜻한 말 한마디를 건네요.")
    ]

    for col, (icon, title, desc) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div class="app-card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{title}</div>
                <div class="card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">MY DAILY CHECK</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">오늘의 체크리스트</div>',
                unsafe_allow_html=True)

    tasks = [
        "택배 상자의 테이프를 제거했어요.",
        "재활용품의 내용물을 비웠어요.",
        "쓰레기를 종류별 수거함에 넣었어요.",
        "경비원분들의 수고를 기억했어요."
    ]

    for i, task in enumerate(tasks):
        st.checkbox(task, key=f"home_task_{i}")

    st.markdown("""
    <div class="purple-note">
        <b>💡 오늘의 한마디</b><br>
        올바른 분리배출은 쓰레기를 버리는 순간부터 시작됩니다.
        작은 배려가 누군가의 안전과 휴식을 지켜 줄 수 있어요.
    </div>
    """, unsafe_allow_html=True)

    if st.button("📚 분리배출 배우러 가기", use_container_width=True):
        st.session_state["main_menu"] = "📚 배출 가이드"
        st.rerun()

# ==========================================
# 8. 대시보드
# ==========================================
elif menu == "📊 대시보드":
    st.markdown('<div class="eyebrow">MY DASHBOARD</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">우리 아파트 에코 대시보드</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">안전하고 올바른 분리배출을 위한 실천 정보를 확인하세요.</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(3)

    metrics = [
        ("📦", "오늘의 실천 미션", "3개", "생활 속 실천"),
        ("♻️", "핵심 분리배출 품목", "5종", "자주 헷갈리는 품목"),
        ("💌", "응원 메시지", f"{len(st.session_state['cheer_messages'])}개", "현재 세션 기준")
    ]

    for col, (icon, title, value, note) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{icon} {title}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">FIELD REPORT</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">경비원분들의 고충</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="app-card">
        <div class="card-icon">🧤</div>
        <div class="card-title">반복되는 재분류 작업</div>
        <div class="card-desc">
            테이프가 붙은 상자, 음식물이 남은 용기 등은
            재분류와 추가 정리 작업을 유발할 수 있습니다.
        </div>
    </div>
    <div class="app-card">
        <div class="card-icon">🩹</div>
        <div class="card-title">작업 안전 지키기</div>
        <div class="card-desc">
            깨진 유리와 날카로운 폐기물은 안전하게 포장하고,
            지역 배출 규정에 따라 처리해야 합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("안내: 이 화면의 품목 수와 미션 수는 앱의 안내 항목을 기준으로 표시합니다.")

# ==========================================
# 9. 배출 가이드
# ==========================================
elif menu == "📚 배출 가이드":
    st.markdown('<div class="eyebrow">CHOOSE YOUR ITEM</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">무엇을 버리려고 하나요?</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">품목을 선택해 올바른 분리배출 방법을 배워 보세요.</div>',
        unsafe_allow_html=True
    )

    guide = {
        "택배 상자": (
            "📦",
            "테이프와 송장이 붙어 있으면 종이 재활용에 방해가 될 수 있어요.",
            "테이프와 송장을 제거하고 납작하게 접어 종이류로 배출하세요.",
            "젖거나 기름에 심하게 오염된 종이는 지역 배출 기준을 확인하세요."
        ),
        "배달 플라스틱 용기": (
            "🥡",
            "음식물과 양념이 남으면 다른 재활용품까지 오염될 수 있어요.",
            "내용물을 비우고 깨끗하게 헹군 후 재질에 맞게 분리하세요.",
            "오염이 지워지지 않는 용기는 지역 배출 기준을 확인하세요."
        ),
        "투명 페트병": (
            "🧴",
            "내용물과 라벨이 남으면 재활용 품질이 떨어질 수 있어요.",
            "내용물을 비우고 라벨을 제거한 후 찌그러뜨려 뚜껑을 닫아 전용 수거함에 넣으세요.",
            "아파트의 투명 페트병 전용 수거함 안내를 확인하세요."
        ),
        "깨진 유리": (
            "⚠️",
            "깨진 유리는 수거와 운반 과정에서 부상을 유발할 수 있어요.",
            "두꺼운 종이 등으로 안전하게 감싸고 지역 규정에 맞는 방법으로 배출하세요.",
            "깨진 유리를 일반 유리병 재활용함에 넣지 마세요."
        ),
        "폐건전지": (
            "🔋",
            "일반 쓰레기에 섞인 건전지는 처리 과정에서 화재 위험을 일으킬 수 있어요.",
            "일반 종량제 봉투에 넣지 말고 폐건전지 전용 수거함에 배출하세요.",
            "관리사무소나 주민센터에서 수거함 위치를 확인하세요."
        )
    }

    items = list(guide.keys())
    selected = st.selectbox("품목 선택", items, key="guide_item")
    icon, problem, solution, tip = guide[selected]

    st.markdown(f"""
    <div class="app-card">
        <div class="card-icon">{icon}</div>
        <div class="card-title" style="font-size:21px;">{selected}</div>
        <div class="purple-note">
            <b>🔎 알아보기</b><br>{problem}
        </div>
        <div class="green-note">
            <b>✅ 올바른 배출 방법</b><br>{solution}
        </div>
        <div class="card-desc">💡 참고: {tip}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">실천 체크리스트</div>',
                unsafe_allow_html=True)

    checklist = [
        "테이프와 송장을 제거했어요.",
        "용기의 내용물을 비우고 씻었어요.",
        "페트병 라벨을 제거했어요.",
        "깨진 유리를 안전하게 포장했어요.",
        "폐건전지를 전용 수거함에 넣었어요."
    ]

    for i, task in enumerate(checklist):
        st.checkbox(task, key=f"guide_check_{i}")

# ==========================================
# 10. 양심 지수
# ==========================================
elif menu == "🏆 양심 지수":
    st.markdown('<div class="eyebrow">MY ECO SCORE</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">나의 분리배출 양심 지수</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">세 가지 질문으로 나의 생활 습관을 확인해 보세요.</div>',
        unsafe_allow_html=True
    )

    with st.form("eco_quiz"):
        q1 = st.radio(
            "01. 택배 상자의 테이프와 송장을 제거하나요?",
            ["선택하세요", "항상 제거한다", "가끔 그대로 버린다", "전혀 신경 쓰지 않는다"]
        )

        q2 = st.radio(
            "02. 양념이 지워지지 않는 용기는 어떻게 버리나요?",
            ["선택하세요", "지역 기준에 따라 일반 쓰레기로 배출한다",
             "그대로 재활용 수거함에 넣는다"]
        )

        q3 = st.radio(
            "03. 투명 페트병의 라벨을 제거하나요?",
            ["선택하세요", "네, 제거한다", "아니요, 그대로 버린다"]
        )

        submitted = st.form_submit_button(
            "내 점수 확인하기",
            use_container_width=True
        )

    if submitted:
        if "선택하세요" in (q1, q2, q3):
            st.session_state["quiz_result"] = None
            st.warning("세 가지 질문에 모두 답변해 주세요.")
        else:
            score = 0
            if q1 == "항상 제거한다":
                score += 30
            if q2 == "지역 기준에 따라 일반 쓰레기로 배출한다":
                score += 35
            if q3 == "네, 제거한다":
                score += 35

            st.session_state["quiz_result"] = score

    score = st.session_state["quiz_result"]

    if score is not None:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-small">MY RECYCLING SCORE</div>
            <div class="score-circle">
                <div class="score-number">{score}</div>
                <div class="score-small">POINTS</div>
            </div>
            <div class="card-title">나의 실천 점수</div>
            <div class="progress-track">
                <div class="progress-fill" style="width:{score}%;"></div>
            </div>
            <div class="score-small">{score} / 100점</div>
        </div>
        """, unsafe_allow_html=True)

        if score == 100:
            st.success("🌟 완벽해요! 올바른 분리배출 습관을 잘 지키고 있어요.")
            st.balloons()
        elif score >= 60:
            st.info("💜 좋은 출발이에요! 놓친 항목을 하나씩 실천해 보세요.")
        else:
            st.warning("🌱 괜찮아요. 오늘부터 작은 습관을 바꿔 보세요.")

        st.caption("이 점수는 학습을 위한 참고용이며 개인의 인격을 평가하지 않습니다.")

# ==========================================
# 11. 응원 게시판
# ==========================================
elif menu == "💌 응원 게시판":
    st.markdown('<div class="eyebrow">COMMUNITY</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">따뜻한 마음을 전해 주세요 💜</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">경비원분들께 감사 인사와 실천 약속을 남겨 보세요.</div>',
        unsafe_allow_html=True
    )

    with st.form("cheer_form", clear_on_submit=True):
        name = st.text_input(
            "닉네임",
            max_chars=30,
            placeholder="예: 101동 주민"
        )

        message = st.text_area(
            "응원 메시지",
            max_chars=500,
            placeholder="늘 고생 많으십니다. 테이프 꼭 떼고 버릴게요!"
        )

        send = st.form_submit_button(
            "💜 응원 메시지 등록하기",
            use_container_width=True
        )

        if send:
            if not name.strip() or not message.strip():
                st.warning("닉네임과 메시지를 모두 입력해 주세요.")
            else:
                st.session_state["cheer_messages"].insert(
                    0,
                    {
                        "name": name.strip(),
                        "msg": message.strip()
                    }
                )

                st.session_state["cheer_messages"] = (
                    st.session_state["cheer_messages"][:100]
                )

                st.success("응원 메시지가 등록되었어요!")

    st.markdown('<div class="eyebrow">COMMUNITY BOARD</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-title">주민 응원 게시판</div>',
                unsafe_allow_html=True)

    messages = st.session_state.get("cheer_messages", [])

    if not messages:
        st.info("첫 번째 응원 메시지를 남겨 주세요.")
    else:
        for entry in messages:
            safe_name = html.escape(str(entry.get("name", "익명")))
            safe_msg = html.escape(str(entry.get("msg", "")))

            st.markdown(f"""
            <div class="message-card">
                <div class="message-name">💜 {safe_name}</div>
                <div class="message-body">{safe_msg}</div>
            </div>
            """, unsafe_allow_html=True)

    st.caption("게시판은 현재 세션에 저장되며 앱이 재시작되면 내용이 사라질 수 있습니다.")

# ==========================================
# 12. 푸터
# ==========================================
st.markdown("""
<div class="footer">
    <b>♻️ 분리온 · ECO LIFE</b><br>
    올바른 분리배출로 만드는 안전하고 따뜻한 공동체<br>
    지역별 분리배출 기준은 관리사무소 또는 지자체 안내를 확인해 주세요.
</div>
""", unsafe_allow_html=True)
