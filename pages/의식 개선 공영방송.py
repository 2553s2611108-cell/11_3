import streamlit as st
from gtts import gTTS
import google.generativeai as genai
import io

# 1. 페이지 설정
st.set_page_config(
    page_title="아파트 공영방송 - 쓰레기 배출 안내",
    page_icon="📢",
    layout="wide"
)

# 2. Gemini API 설정
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# 3. 타이틀 및 안내
st.title("📢 아파트 아침 공영방송 안내문 & 음성 생성기")
st.caption("올바른 쓰레기 배출 문화를 만들기 위한 아파트 아침 방송용 멘트 작성 및 음성 생성 앱입니다.")

# 4. 사이드바 - 설정
st.sidebar.header("🎙️ 방송 설정")
category = st.sidebar.selectbox(
    "방송 주제 선택",
    ["음식물 쓰레기 물기 제거", "재활용품 올바른 분리배출", "대형 폐기물 스티커 부착", "밤샘 무단투기 금지 및 에티켓", "직접 입력"]
)

tone = st.sidebar.radio(
    "방송 어조(Tone)",
    ["정중하고 따뜻한 어조", "경각심을 주는 단호한 어조", "위트 있고 친근한 어조"]
)

# 기본 템플릿 문구
default_texts = {
    "음식물 쓰레기 물기 제거": "입주민 여러분, 안녕하십니까. 관리사무소에서 안내 말씀드립니다. 음식물 쓰레기를 버리실 때는 물기를 꼭 짜서 배출해 주시기 바랍니다. 물기만 잘 제거해도 악취와 침출수를 크게 줄일 수 있습니다. 깨끗한 아파트 단지를 위해 입주민 여러분의 적극적인 협조 부탁드립니다. 감사합니다.",
    "재활용품 올바른 분리배출": "입주민 여러분, 안녕하십니까. 비닐류와 플라스틱은 이물질을 깨끗이 헹군 후 배출해 주셔야 재활용이 가능합니다. 페트병은 라벨을 제거하고 착착 접어서 버려주시기 바랍니다. 작은 실천이 우리 아파트의 환경을 바꿉니다. 감사합니다.",
    "대형 폐기물 스티커 부착": "입주민 여러분, 안녕하십니까. 가구나 가전 등 대형 폐기물을 배출하실 때에는 반드시 관할 구청 스티커를 부착하거나 앱을 통해 신고 후 배출하셔야 합니다. 미부착 폐기물은 수거되지 않으니 협조 바랍니다.",
    "밤샘 무단투기 금지 및 에티켓": "입주민 여러분, 안녕하십니까. 늦은 밤시간 복도나 지정되지 않은 장소에 쓰레기를 투기하는 행위는 이웃에게 큰 불편을 줍니다. 지정된 시간과 장소에 배출해 주시길 당부드립니다.",
    "직접 입력": ""
}

# 5. 메인 화면 구성
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 방송 원고 작성")
    
    # Gemini AI 원고 작성 버튼 (Secrets 설정된 경우만)
    if api_key:
        if st.button("✨ AI로 방송 원고 새로 쓰기"):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash-lite')
                prompt = f"아파트 아침 공영방송용 멘트를 작성해줘. 주제: '{category}', 어조: '{tone}'. 방송 길이는 30초~40초 분량(200자 내외)으로, 주민들이 듣기 편하고 명확하게 작성해줘."
                
                with st.spinner("AI가 방송 원고를 작성하고 있습니다..."):
                    response = model.generate_content(prompt)
                    script_text = response.text
                    st.session_state["script_text"] = script_text
            except Exception as e:
                st.error(f"AI 원고 생성 중 오류가 발생했습니다: {e}")
    else:
        st.info("💡 Tip: Gemini API Key를 설정하면 AI가 자동으로 어조에 맞는 방송 원고를 작성해 드립니다.")

    # 텍스트 에어리어 (세션 상태 활용)
    initial_value = st.session_state.get("script_text", default_texts.get(category, ""))
    user_text = st.text_area("방송할 텍스트를 확인 및 수정하세요:", value=initial_value, height=220)

with col2:
    st.subheader("🔊 방송 음성(MP3) 생성")
    
    if user_text.strip():
        if st.button("▶️ 방송 음성 생성하기", type="primary"):
            try:
                with st.spinner("한국어 음성을 생성하는 중입니다..."):
                    # gTTS를 이용한 한국어 음성 생성
                    tts = gTTS(text=user_text, lang='ko')
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    
                    st.success("음성 생성이 완료되었습니다!")
                    
                    # 미리듣기 오디오 플레이어
                    st.audio(fp, format='audio/mp3')
                    
                    # 다운로드 버튼
                    st.download_button(
                        label="📥 MP3 파일 다운로드 (방송 장비용)",
                        data=fp,
                        file_name="morning_broadcast.mp3",
                        mime="audio/mp3"
                    )
            except Exception as e:
                st.error(f"음성 파일 생성 중 오류가 발생했습니다: {e}")
    else:
        st.warning("왼쪽 상자에 방송할 내용을 입력하거나 선택해 주세요.")

# 6. 하단 안내 탭
st.markdown("---")
st.subheader("📌 방송 시 주의사항")
st.markdown("""
- **방송 스피커 점검**: 음성 생성 후 미리듣기로 음량이 적절한지 먼저 확인하세요.
- **적정 송출 시간**: 입주민의 수면을 방해하지 않도록 **오전 8시 30분 ~ 9시 사이** 송출을 권장합니다.
- **다운로드한 MP3 활용**: MP3 파일을 USB에 담거나, 관리사무소 방송용 PC에 저장하여 매일 아침 간편하게 재생할 수 있습니다.
""")
streamlit
gTTS
google-generativeai
GEMINI_API_KEY = "발급받은_실제_API_KEY_입력"
