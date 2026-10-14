import os
import json
import streamlit as st
from PIL import Image
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 디자인
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="클린동네 - AI 분리수거 점수제",
    page_icon="♻️",
    layout="wide",
)

st.title("♻️ 클린동네: AI 스마트 분리수거 점수제")
st.caption("쓰레기통을 AI로 스캔하고 점수를 쌓아 우리 동네에 생필품과 간식을 선물하세요!")

# -----------------------------------------------------------------------------
# 2. 세션 상태(Session State) 초기화 (데이터 유지)
# -----------------------------------------------------------------------------
if "neighborhood_scores" not in st.state_counts if hasattr(st, "state_counts") else "neighborhood_scores" not in st.session_state:
    st.session_state.neighborhood_scores = {
        "성수1동": 1250,
        "역삼1동": 980,
        "한남동": 840,
        "연남동": 620,
        "판교동": 450
    }

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------------------------------
# 3. Gemini API 설정 및 AI 분석 함수
# -----------------------------------------------------------------------------
def get_gemini_api_key():
    """Secrets 또는 환경변수에서 API 키 로드"""
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    return os.environ.get("GEMINI_API_KEY", "")

def analyze_waste_image(image):
    """Gemini AI를 활용한 쓰레기 이미지 분석"""
    api_key = get_gemini_api_key()
    
    if not api_key:
        return None, "GEMINI_API_KEY가 설정되지 않았습니다. Secrets를 확인해주세요."
    
    try:
        genai.configure(api_key=api_key)
        # 요구사항에 명시된 gemini-2.5-flash-lite 사용
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        
        prompt = """
        당신은 분리수거 전문 AI입니다. 제공된 쓰레기통/쓰레기 사진을 분석하여 오직 아래 JSON 형식으로만 답변해주세요.
        다른 설명이나 마크다운 텍스트(예: ```json)는 절대 포함하지 마세요.

        {
            "correct_ratio": 이미지 내 잘 분리배출된 쓰레기 비율 (0~100 사이 정수),
            "incorrect_ratio": 잘못 배출된 쓰레기 비율 (0~100 사이 정수, 두 합은 100이 되도록),
            "score": 이번 배출에 부여할 점수 (0~100 사이 정수),
            "main_mistakes": ["잘못 배출된 대표 쓰레기 1", "잘못 배출된 대표 쓰레기 2"],
            "improvement_tips": ["올바른 분리배출 방법 조언 1", "올바른 분리배출 방법 조언 2"]
        }
        """
        
        response = model.generate_content([prompt, image])
        
        # JSON 응답 파싱 및 정제
        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.split("\n", 1)[1]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text.rsplit("\n", 1)[0]
            if cleaned_text.startswith("json"):
                cleaned_text = cleaned_text[4:].strip()
                
        result = json.loads(cleaned_text)
        return result, None

    except Exception as e:
        return None, f"AI 분석 중 오류가 발생했습니다: {str(e)}"

# -----------------------------------------------------------------------------
# 4. 사이드바 - 동 선택 & 메뉴
# -----------------------------------------------------------------------------
st.sidebar.header("📍 내 정보 설정")
user_dong = st.sidebar.selectbox(
    "소속 동을 선택하세요",
    options=list(st.session_state.neighborhood_scores.keys()) + ["기타/신규동 추가"],
    index=0
)

if user_dong == "기타/신규동 추가":
    new_dong = st.sidebar.text_input("동 이름을 입력하세요 (예: 청담동)")
    if new_dong:
        user_dong = new_dong
        if user_dong not in st.session_state.neighborhood_scores:
            st.session_state.neighborhood_scores[user_dong] = 0

# -----------------------------------------------------------------------------
# 5. 메인 탭 구성
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📸 AI 쓰레기통 스캔", "🏆 동별 리더보드 & 보상", "💡 올바른 분리배출 팁"])

# --- TAB 1: AI 스캔 및 피드백 ---
with tab1:
    st.subheader("쓰레기통 스캔 및 분석")
    st.write(f"현재 선택된 동: **{user_dong}**")
    
    uploaded_file = st.file_uploader("쓰레기통 또는 배출할 쓰레기 사진을 업로드하세요", type=["jpg", "jpeg", "png"])
    
    col1, col2 = st.columns([1, 1])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        with col1:
            st.image(image, caption="업로드된 쓰레기 사진", use_container_width=True)
            
        with col2:
            if st.button("🔍 AI 분석 시작하기", type="primary", use_container_width=True):
                with st.spinner("Gemini AI가 쓰레기 배출 상태를 분석 중입니다..."):
                    result, error = analyze_waste_image(image)
                    
                    if error:
                        st.error(error)
                        st.warning("⚠️ API 키가 없거나 오류 발생 시 아래 '테스트용 시뮬레이션'으로 결과를 확인할 수 있습니다.")
                    elif result:
                        st.success("분석이 완료되었습니다!")
                        
                        # 점수 및 비율 표시
                        score = result.get("score", 0)
                        correct = result.get("correct_ratio", 0)
                        incorrect = result.get("incorrect_ratio", 0)
                        
                        st.metric(label="📊 이번 배출 획득 점수", value=f"{score}점")
                        
                        # 비율 바 표시
                        st.write(f"✅ 잘 된 배출: **{correct}%** | ❌ 잘못된 배출: **{incorrect}%**")
                        st.progress(correct / 100)
                        
                        # 주요 잘못 배출된 항목
                        st.subheader("❌ 주요 오배출 항목")
                        mistakes = result.get("main_mistakes", [])
                        if mistakes:
                            for item in mistakes:
                                st.write(f"- {item}")
                        else:
                            st.write("잘못 배출된 항목이 없습니다! 완벽합니다.")
                            
                        # 개선 팁
                        st.subheader("💡 올바른 배출 가이드")
                        tips = result.get("improvement_tips", [])
                        for tip in tips:
                            st.info(f"👉 {tip}")
                            
                        # 점수 적립
                        st.session_state.neighborhood_scores[user_dong] += score
                        st.balloons()
                        st.success(f"🎉 {user_dong}에 **{score}점**이 성공적으로 적립되었습니다!")

    else:
        st.info("사진을 업로드하면 AI가 분석을 시작합니다. (테스트를 위한 임시 체험 기능 제공)")
        if st.button("🧪 시뮬레이션 테스트 실행 (사진 없이 테스트)"):
            sample_result = {
                "correct_ratio": 75,
                "incorrect_ratio": 25,
                "score": 75,
                "main_mistakes": ["페트병에 비닐 라벨이 붙어있음", "음료 용기에 내용물 미헹굼"],
                "improvement_tips": ["페트병 라벨을 제거 후 투명 페트병 전용 수거함에 넣어주세요.", "용기 내부를 물로 깨끗이 헹궈 배출해주세요."]
            }
            st.metric(label="📊 이번 배출 획득 점수", value="75점")
            st.write("✅ 잘 된 배출: **75%** | ❌ 잘못된 배출: **25%**")
            st.progress(0.75)
            
            st.subheader("❌ 주요 오배출 항목")
            for item in sample_result["main_mistakes"]:
                st.write(f"- {item}")
                
            st.subheader("💡 올바른 배출 가이드")
            for tip in sample_result["improvement_tips"]:
                st.info(f"👉 {tip}")
                
            st.session_state.neighborhood_scores[user_dong] += 75
            st.success(f"🎉 시뮬레이션 결과로 {user_dong}에 **75점**이 적립되었습니다!")

# --- TAB 2: 동별 리더보드 & 보상 혜택 ---
with tab2:
    st.subheader("🏆 우리 동네 분리수거 랭킹")
    st.write("가장 높은 점수를 기록한 동네 주민분들께 매월 소소한 생필품과 간식을 드립니다!")
    
    # 점수 순으로 정렬
    sorted_scores = sorted(st.session_state.neighborhood_scores.items(), key=lambda x: x[1], reverse=0 == 0, reverse=True)
    
    top_dong, top_score = sorted_scores[0]
    
    st.accent = st.markdown(
        f"""
        <div style="background-color:#e8f5e9; padding:20px; border-radius:10px; border:2px solid #2e7d32; text-align:center;">
            <h2 style="color:#2e7d32; margin:0;">🥇 현재 1위: {top_dong} ({top_score}점)</h2>
            <p style="margin-top:10px; color:#333;">🎁 <b>이번 달 지급 예정 보상:</b> 쓰레기 종량제 봉투(20L) 10매 세트 & 주민센터 카페 아메리카노 쿠폰</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    
    # 랭킹 테이블 표시
    cols = st.columns([1, 2, 2])
    cols[0].write("**순위**")
    cols[1].write("**동 이름**")
    cols[2].write("**누적 점수**")
    
    for rank, (dong, score) in enumerate(sorted_scores, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}위"
        cols = st.columns([1, 2, 2])
        cols[0].write(medal)
        cols[1].write(f"**{dong}**" if dong == user_dong else dong)
        cols[2].write(f"{score} 점")

# --- TAB 3: 분리수거 가이드 ---
with tab3:
    st.subheader("💡 자주 실수하는 올바른 분리배출 방법")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        ### 🥤 투명 페트병
        - **내용물 비우기**: 물로 깨끗이 헹굽니다.
        - **라벨 제거**: 비닐 라벨을 떼어 비닐류로 배출합니다.
        - **압착 및 뚜껑 닫기**: 찌그러뜨린 후 뚜껑을 닫아 배출합니다.
        """)
        
        st.markdown("""
        ### 📦 택배 상자/종이류
        - **테이프 및 운송장 제거**: 비닐 테이프와 운송장 스티커를 반드시 떼어냅니다.
        - **상부/하부 접기**: 펼쳐서 납작하게 눌러 배출합니다.
        """)

    with col_b:
        st.markdown("""
        ### 🍕 음식물 묻은 용기 (컵라면 등)
        - **세척 불가능 시**: 양념이 스며든 스티로폼이나 종이 용기는 **일반 쓰레기(종량제 봉투)**로 배출합니다.
        - **햇빛 건조**: 국물 자국은 햇빛에 말리면 하얗게 탈색되어 재활용이 가능해집니다.
        """)
