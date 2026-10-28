import os
import datetime
import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(
    page_title="아파트 분리배출 공영방송",
    page_icon="📢",
    layout="wide"
)

# 2. 커스텀 CSS (방송국 대시보드 스타일)
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Pretendard', sans-serif;
    }
    h1 {
        color: #1E3A8A !important;
        font-weight: 800 !important;
    }
    div.stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 음성 재생(TTS) JS 함수
def speak_text(text_content):
    # 안전하게 줄바꿈을 공백으로 변환
    clean_text = text_content.replace("\n", " ").replace('"', "'")
    tts_html = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'ko-KR';
            msg.rate = 0.9;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(tts_html, height=0)

# 4. 메인 타이틀
st.title("📢 우리아파트 Clean-Up 공영방송")
st.caption("매일 아침 주민들의 분리배출 의식을 바꾸는 방송국 시스템")

# 세션 상태 초기화
if "broadcast_log" not in st.session_state:
    st.session_state.broadcast_log = []

# 사이드바 메뉴
st.sidebar.header("🎙️ 방송국 메뉴")
menu = st.sidebar.radio(
    "채널 선택:",
    [
        "📻 아침 방송 송출 (메인)",
        "✨ AI 맞춤 대본 생성기",
        "🧩 분리배출 O/X 퀴즈",
        "📜 방송 송출 기록"
    ]
)

# -------------------------------------------------------------------
# 1. 아침 방송 송출 (메인)
# -------------------------------------------------------------------
if menu == "📻 아침 방송 송출 (메인)":
    st.subheader("📡 매일 아침 분리배출 안내 방송")
    
    st.info("💡 **방송 송출 방법**: 대본을 선택하거나 수정하신 후 아래 [방송 송출하기] 버튼을 누르면 아나운서 음성이 출력됩니다.")
    
    preset_scripts = {
        "[월요일] 핵심 4대 수칙 (비·행·분·섞)": "주민 여러분 안녕하십니까. 관리사무소에서 아침 분리배출 안내 말씀 드립니다. 올바른 분리배출을 위해 딱 네 가지만 기억해 주세요. 첫째 내용물은 비우고, 둘째 이물질은 헹구고, 셋째 라벨과 뚜껑은 분리하고, 넷째 다른 재질과 섞지 않는 것입니다. 주민 여러분의 작은 실천이 깨끗한 아파트를 만듭니다. 감사합니다.",
        "[화요일] 투명 페트병 전용 배출": "주민 여러분 좋은 아침입니다. 오늘은 투명 페트병 배출에 대해 안내해 드립니다. 음료수나 생수 페트병은 반드시 비닐 라벨을 떼어내고, 꾹 눌러 압착한 후 전용 수거함에 배출해 주셔야 합니다. 라벨을 떼지 않으면 재활용이 불가능합니다. 1초의 실천에 동참해 주시기 바랍니다.",
        "[수요일] 스티로폼 및 택배 상자": "주민 여러분 안녕하십니까. 택배 상자와 스티로폼 배출 수칙을 안내해 드립니다. 상자에 붙은 테이프와 운송장 스티커는 완전히 제거한 후 펼쳐서 배출해 주세요. 이물질이 묻은 컵라면 용기 등은 재활용이 되지 않으니 종량제 봉투에 버려주시기 바랍니다."
    }
    
    selected_title = st.selectbox("오늘 송출할 대본 선택:", list(preset_scripts.keys()))
    script_text = st.text_area("방송 대본 내용 (수정 가능):", value=preset_scripts[selected_title], height=160)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📢 지금 아침 방송 송출하기 (TTS 음성)"):
            if script_text.strip():
                speak_text(script_text)
                st.success("🔊 아침 공영방송 음성이 송출되고 있습니다!")
                st.session_state.broadcast_log.insert(0, {
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "title": selected_title,
                    "content": script_text
                })
            else:
                st.warning("방송할 대본을 입력해 주세요.")
                
    with col2:
        if st.button("⏹️ 방송 중지"):
            st.components.v1.html("<script>window.speechSynthesis.cancel();</script>", height=0)
            st.info("방송 송출이 중지되었습니다.")

# -------------------------------------------------------------------
# 2. AI 맞춤 대본 생성기
# -------------------------------------------------------------------
elif menu == "✨ AI 맞춤 대본 생성기":
    st.subheader("🤖 Gemini AI 방송 대본 작성")
    st.write("아파트 특이 상황에 맞는 아침 방송 대본을 AI가 자동으로 작성해 줍니다.")
    
    api_key = st.secrets.get("GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY", None)
    
    topic_input = st.text_input("오늘의 방송 상황/주제 입력:", value="비 오는 날 박스 배출 주의 및 음식물 쓰레기 비닐 배출 금지")
    
    if st.button("✨ 맞춤 대본 생성하기"):
        if not api_key:
            st.error("Secrets에 'GEMINI_API_KEY'가 설정되어 있지 않습니다.")
        elif not topic_input.strip():
            st.warning("주제를 입력해 주세요.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                prompt = f"""
                당신은 아파트 전문 공영방송 아나운서입니다.
                다음 상황에 맞춰 주민들의 분리배출 의식을 높일 수 있는 정중하고 명확한 아침 안내 방송 대본을 작성해 주세요.
                
                상황: {topic_input}
                
                조건:
                1. 아나운서 톤 (~합니다, ~해주시기 바랍니다)
                2. 소리 내어 읽기 적합한 30초 분량 (250자 내외)
                """
                
                with st.spinner("대본을 작성 중입니다..."):
                    response = model.generate_content(prompt)
                    ai_script = response.text
                    
                    st.markdown("### 🎙️ 생성된 방송 대본")
                    st.info(ai_script)
                    
                    if st.button("🔊 이 대본으로 음성 송출하기"):
                        speak_text(ai_script)
                        st.success("🔊 방송이 송출됩니다!")
                        st.session_state.broadcast_log.insert(0, {
                            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "title": f"[AI 생성] {topic_input[:15]}...",
                            "content": ai_script
                        })
            except Exception as e:
                st.error(f"API 오류: {str(e)}")

# -------------------------------------------------------------------
# 3. 분리배출 O/X 퀴즈
# -------------------------------------------------------------------
elif menu == "🧩 분리배출 O/X 퀴즈":
    st.subheader("🧩 주민 의식개선 분리배출 O/X 퀴즈")
    
    quizzes = [
        {
            "q": "1. 씻은 컵라면 용기는 스티로폼으로 분리배출한다.",
            "a": "X",
            "exp": "해설: 국물이 밴 스티로폼은 재활용이 불가능하므로 종량제 봉투에 버려야 합니다."
        },
        {
            "q": "2. 투명 페트병은 라벨을 제거하고 뚜껑을 닫아 배출해도 된다.",
            "a": "O",
            "exp": "해설: 뚜껑은 압착 후 닫아서 배출해도 선별 과정에서 분리 가능합니다 (단, 라벨 제거 필수)."
        }
    ]
    
    with st.form("quiz_form"):
        user_ans = []
        for idx, item in enumerate(quizzes):
            st.write(f"**{item['q']}**")
            ans = st.radio(f"선택 {idx+1}", ["O", "X"], key=f"q_{idx}", horizontal=True)
            user_ans.append(ans)
            st.markdown("---")
            
        if st.form_submit_button("정답 확인"):
            score = 0
            for idx, item in enumerate(quizzes):
                if user_ans[idx] == item["a"]:
                    st.success(f"Q{idx+1}: 정답입니다! 🎉")
                    score += 1
                else:
                    st.error(f"Q{idx+1}: 틀렸습니다. (정답: {item['a']})")
                st.caption(item["exp"])
            st.info(f"**최종 점수: {score} / {len(quizzes)}점**")

# -------------------------------------------------------------------
# 4. 방송 송출 기록
# -------------------------------------------------------------------
elif menu == "📜 방송 송출 기록":
    st.subheader("📋 아파트 공영방송 송출 이력")
    
    if not st.session_state.broadcast_log:
        st.info("아직 송출된 방송 기록이 없습니다.")
    else:
        for log in st.session_state.broadcast_log:
            with st.expander(f"🕒 [{log['time']}] {log['title']}"):
                st.write(log['content'])
GEMINI_API_KEY = "your_actual_api_key_here"
