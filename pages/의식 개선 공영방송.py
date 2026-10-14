import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="아파트 분리배출 공영방송 시스템",
    page_icon="📢",
    layout="wide"
)

# 2. API 키 확인 및 Gemini 클라이언트 초기화
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ `GEMINI_API_KEY`가 설정되지 않았습니다. Secrets 설정을 완료해주세요.")

# 3. 사이드바 - 기본 설정 및 가이드
st.sidebar.title("📢 방송 시스템 메뉴")
menu = st.sidebar.radio(
    "메뉴 선택",
    ["🎙️ 오늘의 아침 방송 생성", "🔍 자주 틀리는 분리배출 Q&A", "📅 요일별 방송 가이드"]
)

st.sidebar.markdown("---")
st.sidebar.caption("💡 **사용 팁:** 매일 아침 8시~9시 사이 아파트 단내 방송으로 송출하시면 효과적입니다.")

# -------------------------------------------------------------------
# 메뉴 1: 오늘의 아침 방송 생성
# -------------------------------------------------------------------
if menu == "🎙️ 오늘의 아침 방송 생성":
    st.title("🎙️ 아파트 분리배출 아침 공영방송")
    st.subheader("매일 아침 주민들의 분리배출 의식을 개선하는 맞춤형 안내 방송")

    col1, col2 = st.columns(2)
    
    with col1:
        season = st.selectbox("현재 계절/특수 상황", ["평일 일반", "주말 아침 (배출량 증가)", "여름철 (음식물/악취)", "겨울철/김장철", "명절 연휴 후"])
        target_item = st.selectbox("오늘의 중점 교정 품목", [
            "자동 추천 (AI 선택)",
            "배달용기 / 비닐류 (이물질 제거)",
            "택배 상자 (테이프·운송장 제거)",
            "투명 페트병 (라벨 제거 및 압축)",
            "스티로폼 (이물질/스티커 제거)",
            "음식물 쓰레기 (일반쓰레기 혼입 금지)"
        ])

    with col2:
        tone = st.radio("방송 톤앤매너", ["친근하고 따뜻한 어조", "정중하고 정직한 어조", "명확하고 강조하는 어조"])
        duration = st.select_slider("방송 예상 시간", options=["30초 (요약)", "1분 (권장)", "1분 30초 (상세)"])

    if st.button("📢 방송 원고 및 음성 생성하기", type="primary"):
        if not api_key:
            st.error("Secrets에 `GEMINI_API_KEY`를 먼저 등록해주세요.")
        else:
            with st.spinner("AI 방송 아나운서가 원고를 작성하고 있습니다..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    prompt = f"""
                    당신은 아파트 단지 공영방송 전문 아나운서입니다.
                    주민들의 올바른 쓰레기 분리배출 의식을 높이기 위한 아침 안내 방송 원고를 작성해주세요.

                    - 상황: {season}
                    - 중점 강조 품목: {target_item}
                    - 어조: {tone}
                    - 분량: {duration} 내외
                    - 구성 요건:
                      1. 따뜻한 아침 인사말 (예: "주민 여러분, 안녕하십니까. 즐거운 아침입니다.")
                      2. 오늘 강조할 분리배출 실천 포인트 (이유와 올바른 방법)
                      3. 올바른 분리배출이 아파트 관리비 절감 및 환경 보호에 주는 이점 언급
                      4. 정중한 마무리 인사

                    방송 원고만 깔끔하게 출력해주세요.
                    """

                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents=prompt,
                    )

                    script_text = response.text

                    st.success("🎉 방송 원고가 성공적으로 생성되었습니다!")
                    
                    # 원고 출력
                    st.markdown("### 📝 오늘의 방송 원고")
                    st.info(script_text)

                    # 브라우저 음성 읽기(TTS) 안내 및 텍스트 제공
                    st.markdown("---")
                    st.markdown("### 🔊 방송 송출 (음성 듣기)")
                    st.caption("아래 플레이어 버튼을 눌러 방송 음성을 직접 듣거나 방송 장비에 연결하여 송출하세요.")
                    
                    # HTML5 Web Speech API를 활용한 가벼운 오디오 재생 구현
                    tts_code = f"""
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;">
                        <button onclick="speakText()" style="background-color: #ff4b4b; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer;">
                            ▶️ 방송 음성 재생
                        </button>
                        <button onclick="stopText()" style="background-color: #555555; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-left: 10px;">
                            ⏹️ 정지
                        </button>
                    </div>

                    <script>
                    var synth = window.speechSynthesis;
                    function speakText() {{
                        if (synth.speaking) {{ synth.cancel(); }}
                        var text = `{script_text.replace('\n', ' ')}`;
                        var utterance = new SpeechSynthesisUtterance(text);
                        utterance.lang = 'ko-KR';
                        utterance.rate = 0.9; // 아침 방송용 약간 천천히
                        synth.speak(utterance);
                    }}
                    function stopText() {{
                        synth.cancel();
                    }}
                    </script>
                    """
                    st.components.v1.html(tts_code, height=100)

                except APIError as e:
                    st.error(f"Gemini API 호출 중 오류가 발생했습니다: {e}")
                except Exception as e:
                    st.error(f"알 수 없는 오류가 발생했습니다: {e}")

# -------------------------------------------------------------------
# 메뉴 2: 자주 틀리는 분리배출 Q&A
# 
streamlit
google-genai
GEMINI_API_KEY = "발급받은_실제_API_키_입력"
