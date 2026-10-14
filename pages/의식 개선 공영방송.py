import streamlit as st
import google.generativeai as genai

# 1. 페이지 기본 설정 (의식 개선 공영방송 스타일 UI)
st.set_page_config(
    page_title="공공 캠페인 방송 스크립트 에디터",
    page_icon="📺",
    layout="wide"
)

# 2. 타이틀 및 안내문
st.title("📺 의식 개선 공영방송 캠페인 에디터")
st.caption("공익적 가치를 전하는 신뢰와 품격의 문장으로 캠페인 메시지를 재창작합니다.")

# 3. API 키 확인 (Streamlit Secrets에서 가져오기)
api_key = st.secrets.get("GEMINI_API_KEY")

with st.sidebar:
    st.header("⚙️ 설정 및 안내")
    if api_key:
        st.success("API Key가 정상적으로 연결되었습니다.")
    else:
        st.error("GEMINI_API_KEY가 Secrets에 설정되지 않았습니다.")
        st.info("Streamlit Community Cloud의 Secrets 설정을 확인해 주세요.")
    
    st.markdown("---")
    st.markdown("""
    **💡 사용 팁**
    - 평소 전달하고 싶었던 캠페인 메시지나 표어를 자유롭게 입력하세요.
    - 정제되지 않은 문장도 공영방송 방송용 멘트로 교정됩니다.
    """)

# 4. 사용자 입력 폼
st.subheader("📝 캠페인 메시지 입력")
col1, col2 = st.columns([3, 1])

with col1:
    topic_input = st.text_input(
        "캠페인 주제 또는 원본 문구",
        placeholder="예: 횡단보도 스마트폰 사용 금지, 올바른 쓰레기 분리배출, 스토킹 범죄 예방 등"
    )

with col2:
    media_type = st.selectbox(
        "캠페인 주 타겟/어조",
        ["전 국민 대상 (표준적/신뢰)", "청소년/청년 대상 (부드러운 권유)", "고령층 대상 (쉬운 명확한 언어)"]
    )

generate_btn = st.button("🎬 방송용 스크립트 생성하기", use_container_width=True, type="primary")

# 5. Gemini AI 생성 로직
if generate_btn:
    if not api_key:
        st.error("API 키가 누락되어 작업을 진행할 수 없습니다. Secrets 설정을 확인해 주세요.")
    elif not topic_input.strip():
        st.warning("주제 또는 원본 문구를 입력해 주세요.")
    else:
        with st.spinner("공영방송 톤앤매너에 맞춰 스크립트를 재창작 중입니다..."):
            try:
                # Gemini 설정 및 생성
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash-lite")

                prompt = f"""
                당신은 대한민국 공영방송(KBS, EBS 등)의 공익광고 전문 카피라이터이자 스크립트 작가입니다.
                다음 입력된 캠페인 주제를 바탕으로 국민들의 의식을 개선하고 공감대를 형성할 수 있는 방송용 원고를 작성해 주세요.

                [입력 데이터]
                - 캠페인 주제/원문: {topic_input}
                - 타겟 및 어조: {media_type}

                [작성 가이드라인]
                1. 억지로 가르치려 들지 말고, 공감과 실천을 이끌어내는 정갈하고 품격 있는 언어를 사용할 것.
                2. 아래 형식에 맞추어 명확히 구분을 지어 작성할 것.

                ---
                [1. TV 공익광고 하단 자막 스크립트]
                (도입부, 본론, 결론/슬로건 3단계로 구성)

                [2. 카드뉴스/SNS용 핵심 메시지]
                (메인 카피 1개, 서브 카피 2개)

                [3. 라디오/오디오 내레이션 원고]
                (15초 내외로 읽을 수 있는 부드러운 오
streamlit
google-generativeai
GEMINI_API_KEY = "여기에_발급받은_Gemini_API_Key를_입력하세요"
