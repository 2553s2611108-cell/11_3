import streamlit as st
import pandas as pd
import json
import os
from PIL import Image

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 Gemini API 연동
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="우리동네 ecoScan - 분리수거 점수제",
    page_icon="♻️",
    layout="wide"
)

# Gemini API 초기화 (google-genai SDK 사용)
gemini_client = None
try:
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        from google import genai
        gemini_client = genai.Client(api_key=api_key)
except Exception as e:
    gemini_client = None

# -----------------------------------------------------------------------------
# 2. 세션 상태 (Session State) 초기화
# -----------------------------------------------------------------------------
if "neighborhood_scores" not in st.session_state:
    st.session_state.neighborhood_scores = {
        "성정1동": {"score": 820, "scans": 15},
        "두정동": {"score": 950, "scans": 20},
        "신부동": {"score": 640, "scans": 12},
        "불당동": {"score": 1100, "scans": 22},
        "쌍용2동": {"score": 780, "scans": 14}
    }

if "recent_scans" not in st.session_state:
    st.session_state.recent_scans = []

# -----------------------------------------------------------------------------
# 3. AI 쓰레기 분석 함수 (Gemini / Mock AI)
# -----------------------------------------------------------------------------
def analyze_waste_image(image: Image.Image):
    """
    Gemini 2.5 Flash Lite 모델을 활용한 쓰레기통 이미지 스캔 및 분석.
    API 호출 오류 시 모의 데이터(Mock Data)를 안전하게 반환.
    """
    prompt = """
    당신은 스마트 분리수거 AI 센서입니다. 제공된 쓰레기통 내부 이미지를 분석하여 다음 형식의 JSON만 정확히 출력하세요:
    {
      "correct_ratio": <잘 올바르게 분리배출된 비율(0-100 정수)>,
      "incorrect_ratio": <잘못 배출된 비율(0-100 정수, 두 합은 100)>,
      "calculated_score": <산출된 점수(0-100점)>,
      "detected_items": ["포착된 주요 쓰레기 항목들"],
      "major_mistakes": ["잘못 배출된 주요 쓰레기 명칭 및 이유 (예: 라벨 미제거 페트병, 음식물 묻은 컵)"],
      "improvement_guide": "주민들이 개선해야 할 핵심 분리수거 팁 한 줄 요약"
    }
    """
    
    if gemini_client:
        try:
            # gemini-2.5-flash-lite 모델 호출
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=[prompt, image],
                config={'response_mime_type': 'application/json'}
            )
            result = json.loads(response.text)
            return result
        except Exception as e:
            st.warning(f"AI API 연동 중 오류 발생 ({str(e)}). 시뮬레이션 모드로 전환합니다.")
    
    # API 키가 없거나 오류 시 반환할 안전한 시뮬레이션 데이터
    return {
        "correct_ratio": 75,
        "incorrect_ratio": 25,
        "calculated_score": 75,
        "detected_items": ["투명 페트병", "종이컵", "비닐 봉투", "플라스틱 배달 용기"],
        "major_mistakes": ["페트병 비닐 라벨 미제거", "배달 용기에 음식물 양념 잔여"],
        "improvement_guide": "플라스틱 용기는 내용물을 물로 깨끗이 헹구고 비닐 라벨은 반드시 제거 후 배출해주세요!"
    }

# -----------------------------------------------------------------------------
# 4. UI 사이드바 및 헤더
# -----------------------------------------------------------------------------
st.title("♻️ 우리동네 ecoScan")
st.caption("AI 스마트 쓰레기통 분석 기반 동별 분리수거 점수제 & 리워드 시스템")

with st.sidebar:
    st.header("⚙️ 앱 설정 및 정보")
    selected_dong = st.selectbox("현재 스마트 쓰레기통 위치 (동 선택)", list(st.session_state.neighborhood_scores.keys()))
    
    st.divider()
    if gemini_client:
        st.success("🟢 Gemini 2.5 Flash Lite 연동됨")
    else:
        st.info("🟡 Gemini API Key 미설정 (시뮬레이션 모드 작동 중)")
        st.caption("Streamlit Secrets에 `GEMINI_API_KEY`를 등록하면 실제 AI 이미지 분석이 작동합니다.")

# -----------------------------------------------------------------------------
# 5. 메인 탭 구성
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📸 AI 쓰레기통 스캔", "🏆 동별 리더보드 & 점수", "🎁 동네 리워드 혜택"])

# --- TAB 1: AI 쓰레기통 스캔 ---
with tab1:
    st.subheader(f"📍 [{selected_dong}] 스마트 쓰레기통 AI 분석")
    st.write("쓰레기통 내부 사진을 촬영하거나 업로드하면 AI가 올바른 배출 비율과 오배출 항목을 분석합니다.")
    
    upload_option = st.radio("이미지 입력 방식 선택", ["샘플 테스트", "파일 업로드", "카메라 촬영"], horizontal=True)
    
    input_image = None
    if upload_option == "샘플 테스트":
        # 기본 안내용 플레이스홀더 이미지 생성
        input_image = Image.new('RGB', (400, 300), color=(220, 235, 220))
        st.info("테스트용 모의 스캔 환경입니다. [AI 분석 실행] 버튼을 눌러보세요.")
    elif upload_option == "파일 업로드":
        uploaded_file = st.file_uploader("쓰레기통 내부 이미지 업로드", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            input_image = Image.open(uploaded_file)
    elif upload_option == "카메라 촬영":
        camera_file = st.camera_input("카메라로 촬영")
        if camera_file:
            input_image = Image.open(camera_file)

    if input_image:
        st.image(input_image, caption="스캔 대상 쓰레기통 이미지", use_container_width=True)
        
        if st.button("🚀 AI 분석 실행", type="primary"):
            with st.spinner("AI가 쓰레기 분류 상태를 분석 중입니다..."):
                analysis = analyze_waste_image(input_image)
                
                # 결과 반영
                score = analysis.get("calculated_score", 70)
                st.session_state.neighborhood_scores[selected_dong]["score"] += score
                st.session_state.neighborhood_scores[selected_dong]["scans"] += 1
                st.session_state.recent_scans.insert(0, {
                    "dong": selected_dong,
                    "score": score,
                    "correct": analysis.get("correct_ratio", 0),
                    "incorrect": analysis.get("incorrect_ratio", 0)
                })
                
                st.success("✅ AI 분석 완료! 점수가 해당 동에 반영되었습니다.")
                st.divider()
                
                # 점수 및 비율 Metric
                col1, col2, col3 = st.columns(3)
                col1.metric("획득 점수", f"+{score}점")
                col2.metric("올바른 배출 비율", f"{analysis.get('correct_ratio')}%")
                col3.metric("잘못된 배출 비율", f"{analysis.get('incorrect_ratio')}%", delta=f"-{analysis.get('incorrect_ratio')}%", delta_color="inverse")
                
                # 주요 오배출 정보 및 개선 가이드
                col_a, col_b = st.columns(2)
                with col_a:
                    st.warning("⚠️ 감지된 주요 오배출(잘못 배출된 쓰레기)")
                    mistakes = analysis.get("major_mistakes", [])
                    if mistakes:
                        for m in mistakes:
                            st.write(f"- {m}")
                    else:
                        st.write("- 특이 오배출 항목 없음 (완벽함!)")
                
                with col_b:
                    st.info("💡 올바른 분리배출 개선 가이드")
                    st.write(analysis.get("improvement_guide", "이물질을 제거하고 재질별로 분류해주세요."))

# --- TAB 2: 동별 리더보드 ---
with tab2:
    st.subheader("🏆 우리동네 분리수거 점수 랭킹")
    st.write("주민들이 올바르게 분리배출을 진행할수록 동별 누적 점수가 올라갑니다.")
    
    # 데이터프레임 변환
    df_scores = pd.DataFrame.from_dict(st.session_state.neighborhood_scores, orient="index")
    df_scores = df_scores.reset_index().rename(columns={"index": "동 이름", "score": "누적 점수", "scans": "스캔 횟수"})
    df_scores = df_scores.sort_values(by="누적 점수", ascending=False).reset_index(drop=True)
    df_scores.index += 1  # 1위부터 시작
    
    # 1위 동 강조
    top_dong = df_scores.iloc[0]["동 이름"]
    top_score = df_scores.iloc[0]["누적 점수"]
    
    st.balloons() if top_score > 2000 else None
    
    st.success(f"🥇 현재 1위: **{top_dong}** ({top_score}점) - 이달의 우수 동 유력 후보!")
    
    # 차트 시각화
    st.bar_chart(df_scores.set_index("동 이름")["누적 점수"])
    
    # 리더보드 표
    st.table(df_scores)

# --- TAB 3: 동네 리워드 혜택 ---
with tab3:
    st.subheader("🎁 이달의 분리수거 우수 동 리워드 안내")
    st.write("매월 말 점수가 가장 높은 동의 공용 공간/주민센터에 소소한 생필품과 간식을 제공합니다!")
    
    df_scores = pd.DataFrame.from_dict(st.session_state.neighborhood_scores, orient="index").reset_index()
    top_row = df_scores.sort_values(by="score", ascending=False).iloc[0]
    
    st.markdown(f"""
    ### 🏆 10월 현재 리워드 확정 예정 동: **[{top_row['index']}]**
    - **누적 점수:** {top_row['score']} 점
    - **지급 예정 리워드 세트:**
      - 🧻 **주민 공용 생필품:** 친환경 롤휴지 세트 & 종량제 봉투(20L) 각 가구 지급
      - 🍪 **마을 쉼터 간식박스:** 주민센터 및 노인정 내 고급 음료 & 과자 세트 배치
      - 🪴 **환경 지원:** 주민센터 내 미니 화분 나눔 행사 지원
    """)
    
    st.progress(min(top_row['score'] / 2000, 1.0), text=f"목표 점수 2,000점 중 {top_row['score']}점 달성")
