import os
import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="우리아파트 분리배출 공영방송",
    page_icon="📢",
    layout="wide"
)

# Custom CSS for Mobile UI Design Theme (Orange & Cream, Card Layout)
st.markdown("""
    <style>
    /* 전체 배경색 및 폰트 설정 */
    .stApp {
        background-color: #F8F6F0;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 헤더 스타일링 */
    h1 {
        color: #FF5E36 !important;
        font-weight: 800 !important;
    }
    
    /* 메인 카드 박스 디자인 */
    div[data-testid="stMetricValue"] {
        color: #FF5E36 !important;
        font-weight: bold;
    }
    
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #FFEBE3;
    }

    /* 버튼 스타일링 (주황색 테마) */
    .stButton>button {
        background-color: #FF5E36 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 10px rgba(255, 94, 54, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #E04B26 !important;
        transform: translateY(-2px);
    }

    /* Expander / 카드 모듈 디자인 */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #FFE0D3 !important;
        color: #333333 !important;
        font-weight: 600;
    }

    /* 사이드바 스타일링 */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #EFEFEF;
    }
    
    /* Info / Success / Warning 박스 커스텀 */
    .stAlert {
        border-radius: 16px !important;
        border: none !important;
    }
    
    /* 검색창 & 텍스트 입력창 라운딩 */
    .stTextInput input, .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid #E0E0E0 !important;
        background-color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# App Title & Header
st.title("📢 우리아파트 Clean-Up 공영방송")
st.caption("주민 모두가 함께 만드는 올바른 분리배출 문화 챌린지")

# Sidebar Menu
st.sidebar.header("📺 방송국 채널")
menu = st.sidebar.radio(
    "이동할 메뉴를 선택하세요:",
    [
        "📺 오늘의 방송 (메인)",
        "🔍 분리배출 가이드",
        "🧩 분리배출 O/X 퀴즈",
        "📸 주민 실천 인증 게시판",
        "🤖 AI 분리배출 상담소"
    ]
)

# -------------------------------------------------------------------
# 1. 메인 방송 (대시보드)
# -------------------------------------------------------------------
if menu == "📺 오늘의 방송 (메인)":
    st.subheader("📡 오늘의 아파트 환경 방송")
    
    st.info("""
    **[안내 방송]** 
    주민 여러분, 안녕하십니까! 아파트 환경 관리 방송국입니다. 
    오늘도 올바른 분리배출을 통해 깨끗한 우리 아파트와 지구를 만드는데 동참해주세요!
    - **오늘의 강조사항**: 라벨 제거하지 않은 투명 페트병은 재활용이 불가능합니다. 꼭 라벨을 떼서 배출해주세요!
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("오늘의 올바른 배출률", "82%", "+5%")
    col2.metric("이번 달 챌린지 참여 수", "142건", "+12건")
    col3.metric("절감된 폐기물 비용", "약 450,000원", "목표 달성 중")

    st.markdown("---")
    st.subheader("💡 3대 핵심 배출 수칙 (비·행·분·섞)")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.success("1. 비운다")
        st.caption("용기 안의 내용물을 깨끗이 비워주세요.")
    with c2:
        st.info("2. 헹군다")
        st.caption("이물질이나 음식물은 물로 헹궈주세요.")
    with c3:
        st.warning("3. 분리한다")
        st.caption("라벨, 뚜껑 등 다른 재질은 분리해주세요.")
    with c4:
        st.error("4. 섞지 않는다")
        st.caption("종류별, 재질별로 구분하여 배출해주세요.")

# -------------------------------------------------------------------
# 2. 분리배출 가이드
# -------------------------------------------------------------------
elif menu == "🔍 분리배출 가이드":
    st.subheader("🔍 품목별 올바른 배출 방법")
    
    guide_data = {
        "투명 페트병": "내용물 비우기 ➔ 라벨 제거 ➔ 압착 후 뚜껑 닫아서 **전용 수거함**에 배출",
        "플라스틱류": "내용물 비우고 헹군 후 배출 (부속품 등 다른 재질은 제거)",
        "종이팩/우유팩": "내용물 헹구기 ➔ 펼쳐서 말리기 ➔ 일반 종이류와 **구분하여 전용함**에 배출",
        "스티로폼": "흰색 스티로폼 상자만 가능. 운송장 스티커, 테이프 완전히 제거 후 배출 (컵라면 용기는 씻어도 종량제 봉투)",
        "비닐류": "내용물 비우고 깨끗이 씻어 배출 (이물질 안 닦이면 종량제 봉투)",
        "유리병": "담배꽁초 등 이물질 넣지 않기 ➔ 깨진 유리는 신문지에 싸서 **종량제 봉투/특량제 봉투**"
    }
    
    search_term = st.text_input("찾고 싶은 품목을 검색하세요 (예: 페트병, 스티로폼, 종이팩):")
    
    st.markdown("---")
    for item, guide in guide_data.items():
        if search_term == "" or search_term.lower() in item.lower():
            with st.expander(f"📦 {item}"):
                st.write(guide)

# -------------------------------------------------------------------
# 3. 분리배출 O/X 퀴즈
# -------------------------------------------------------------------
elif menu == "🧩 분리배출 O/X 퀴즈":
    st.subheader("🧩 착각하기 쉬운 분리배출 O/X 퀴즈")
    st.write("퀴즈를 통해 잘못 알고 있던 분리배출 상식을 바로잡아 보세요!")
    
    quizzes = [
        {
            "question": "1. 깨끗하게 씻은 컵라면 스티로폼 용기는 스티로폼으로 분리배출한다.",
            "answer": "X",
            "explanation": "해설: 라면 국물이 밴 스티로폼 용기는 재활용이 불가능하므로 일반 쓰레기(종량제 봉투)로 버려야 합니다."
        },
        {
            "question": "2. 투명 페트병은 라벨을 제거하고 뚜껑을 닫아서 배출해도 된다.",
            "answer": "O",
            "explanation": "해설: 뚜껑은 페트병과 함께 압착 후 닫아서 배출해도 재활용 공정에서 선별 가능합니다. (단, 라벨은 반드시 제거해야 합니다)"
        },
        {
            "question": "3. 씻지 않은 찌꺼기가 남은 비닐은 비닐류 수거함에 버려도 된다.",
            "answer": "X",
            "explanation": "해설: 이물질이나 음식물이 묻은 비닐은 재활용을 오염시키므로 일반 쓰레기로 버려야 합니다."
        }
    ]
    
    score = 0
    with st.form("quiz_form"):
        user_answers = []
        for idx, q in enumerate(quizzes):
            st.markdown(f"**{q['question']}**")
            ans = st.radio(f"정답 선택 ({idx+1}번)", ["O", "X"], key=f"q_{idx}", horizontal=True)
            user_answers.append(ans)
            st.markdown("---")
            
        submitted = st.form_submit_button("정답 확인하기")
        
        if submitted:
            st.subheader("📊 퀴즈 결과")
            for idx, q in enumerate(quizzes):
                if user_answers[idx] == q["answer"]:
                    st.success(f"Q{idx+1}: 정답입니다! 🎉")
                    score += 1
                else:
                    st.error(f"Q{idx+1}: 틀렸습니다. 😅 (선택: {user_answers[idx]} / 정답: {q['answer']})")
                st.caption(q["explanation"])
            
            st.info(f"**총 점수: {score} / {len(quizzes)}점**")

# -------------------------------------------------------------------
# 4. 주민 실천 인증 게시판
# -------------------------------------------------------------------
elif menu == "📸 주민 실천 인증 게시판":
    st.subheader("📸 분리배출 실천 인증 & 노하우 공유")
    st.write("올바른 분리배출 모습을 인증하고 깨끗한 아파트를 함께 만들어가요!")
    
    if "posts" not in st.session_state:
        st.session_state.posts = [
            {"name": "101동 주민", "content": "오늘 투명 페트병 라벨 싹 떼고 압착해서 버렸습니다! 뿌듯하네요.", "likes": 5},
            {"name": "203동 주민", "content": "택배 상자 테이프랑 운송장 스티커 꼭 제거하고 버립시다!", "likes": 8}
        ]
        
    with st.form("post_form"):
        author = st.text_input("작성자 (예: 105동 주민)", max_chars=20)
        content = st.text_area("인증 내용 및 나만의 분리배출 팁", max_chars=200)
        submit_post = st.form_submit_button("인증글 등록하기")
        
        if submit_post:
            if author and content:
                st.session_state.posts.insert(0, {"name": author, "content": content, "likes": 0})
                st.success("인증글이 성공적으로 등록되었습니다!")
                st.rerun()
            else:
                st.warning("작성자와 내용을 모두 입력해주세요.")
                
    st.markdown("---")
    st.subheader("💬 주민 참여 피드")
    
    for idx, post in enumerate(st.session_state.posts):
        with st.container():
            st.markdown(f"**👤 {post['name']}**")
            st.write(post['content'])
            col_like, _ = st.columns([1, 5])
            if col_like.button(f"❤️ 응원하기 ({post['likes']})", key=f"like_{idx}"):
                post['likes'] += 1
                st.rerun()
            st.markdown("---")

# -------------------------------------------------------------------
# 5. AI 분리배출 상담소
# -------------------------------------------------------------------
elif menu == "🤖 AI 분리배출 상담소":
    st.subheader("🤖 Gemini AI 분리배출 도우미")
    st.write("버리기 애매하거나 헷갈리는 물품의 이름을 입력하시면 올바른 배출 방법을 알려드립니다.")
    
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    
    user_query = st.text_input("질문할 품목을 입력하세요 (예: 코팅된 전단지, 깨진 유리컵, 스프링 노트):")
    
    if st.button("AI에게 물어보기"):
        if not api_key:
            st.error("Secrets 설정에 'GEMINI_API_KEY'가 설정되어 있지 않습니다.")
        elif not user_query:
            st.warning("질문할 물품을 입력해주세요.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                prompt = f"""
                당신은 아파트 분리배출 전문 안내 AI입니다.
                다음 물품의 올바른 분리배출 방법(종량제 봉투 / 재활용 / 특수배출 등)과 이유, 배출 시 주의사항을 친절하고 핵심만 요약해서 3줄 이내로 답변해주세요.
                
                물품: {user_query}
                """
                
                with st.spinner("AI가 올바른 배출 방법을 확인 중입니다..."):
                    response = model.generate_content(prompt)
                    st.success("💡 AI 배출 가이드 답변")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {str(e)}")
