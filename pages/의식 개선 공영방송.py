import streamlit as st
from google import genai
from gtts import gTTS
import io

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="아파트 쓰레기 배출 안내 방송 생성기",
    page_icon="📢",
    layout="wide"
)

# 2. Gemini API 클라이언트 초기화 함수
def get_gemini_client():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("⚠️ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. Secrets 설정을 확인해 주세요.")
        st.stop()
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 메인 화면 헤더
st.title("📢 아파트 쓰레기 배출 의식 개선 공영방송 도우미")
st.caption("올바른 쓰레기 배출 문화를 위한 맞춤형 아침 방송 원고 및 음성 생성 서비스")
st.markdown("---")

# 4. 사이드바 - 방송 설정 입력
st.sidebar.header("🎛️ 방송 설정")

topic = st.sidebar.selectbox(
    "방송 주제/이슈 선택",
    [
        "재활용품 올바른 분리배출 안내 (페트박스, 라벨 제거 등)",
        "음식물 쓰레기 물기 제거 및 배출 방법",
        "대형 폐기물 스티커 부착 및 무단투기 방지",
        "종량제 봉투 정량 사용 및 지정 장소 배출",
        "주말/연휴 끝 올바른 쓰레기장 이용 매너",
        "직접 입력"
    ]
)

if topic == "직접 입력":
    custom_topic = st.sidebar.text_input("원하는 방송 주제를 입력하세요", placeholder="예: 박스 테이프 제거 후 배출 안내")
else:
    custom_topic = topic

tone = st.sidebar.radio(
    "방송 어조 선택",
    ["정중하고 친절한 어조", "밝고 활기찬 어조", "단호하고 명확한 어조 (계도용)"]
)

target_length = st.sidebar.select_slider(
    "방송 분량 (예상 소요 시간)",
    options=["30초 분량 (간결함)", "1분 분량 (적당함)", "1분 30초 분량 (상세함)"],
    value="1분 분량 (적당함)"
)

# 5. 메인 영역 - 원고 생성 버튼 및 결과 출력
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 원고 생성 설정 확인")
    st.write(f"• **주제:** {custom_topic}")
    st.write(f"• **어조:** {tone}")
    st.write(f"• **분량:** {target_length}")
    
    generate_btn = st.button("✨ 방송 원고 & 음성 생성하기", use_container_width=True, type="primary")

# 세션 상태 초기화 (결과 유지용)
if "script_text" not in st.session_state:
    st.session_state.script_text = ""
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if generate_btn:
    if not custom_topic.strip():
        st.warning("방송 주제를 입력해 주세요.")
    else:
        with st.spinner("Gemini가 명확하고 친근한 방송 원고를 작성하고 있습니다..."):
            try:
                client = get_gemini_client()
                
                # 프롬프트 구성
                prompt = f"""
                당신은 아파트 관리사무소의 공영방송 담당자입니다.
                입주민들의 쓰레기 배출 의식을 개선하고 올바른 분리수거를 독려하기 위한 아침 방송 원고를 작성해 주세요.

                [조건]
                1. 주제: {custom_topic}
                2. 방송 어조: {tone}
                3. 분량: {target_length}
                4. 아파트 아침 공영방송에 어울리는 인사말과 마무리를 포함할 것.
                5. 듣는 입주민이 불쾌하지 않으면서도 핵심 수칙을 명확히 이해할 수 있도록 구성할 것.
                6. 실제 방송에서 그대로 읽을 수 있는 대본 형식(괄호 안의 효과음이나 지시문 제외)으로만 작성할 것.
                """
                
                # Gemini 2.5 Flash Lite 모델 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=prompt
                )
                
                script = response.text.strip()
                st.session_state.script_text = script

                # gTTS를 활용하여 음성 파일 생성
                tts = gTTS(text=script, lang='ko')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.session_state.audio_bytes = fp.read()

                st.success("방송 원고 및 음성이 성공적으로 생성되었습니다!")

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# 결과 출력 영역
with col2:
    st.subheader("🎙️ 생성된 방송 원고 & 음성")
    if st.session_state.script_text:
        # 원고 출력
        st.text_area("방송 원고 (복사하여 사용 가능)", value=st.session_state.script_text, height=280)
        
        # 음성 오디오 플레이어
        if st.session_state.audio_bytes:
            st.markdown("##### 🔊 방송 음성 미리듣기")
            st.audio(st.session_state.audio_bytes, format="audio/mp3")
            
            # 음성 파일 다운로드 버튼
            st.download_button(
                label="📥 MP3 음성 파일 다운로드",
                data=st.session_state.audio_bytes,
                file_name="morning_announcement.mp3",
                mime="audio/mp3"
            )
    else:
        st.info("왼쪽의 [방송 원고 & 음성 생성하기] 버튼을 눌러주세요.")

# 하단 도움말
st.markdown("---")
st.markdown("💡 **팁**: 방송 전 음성 오디오를 미리 들어보며 속도와 억양을 확인해 보세요. 작성된 원고를 텍스트 박스에서 직접 수정하여 사용할 수도 있습니다.")
  
