import streamlit as st
import json
import os
from PIL import Image

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 Gemini API 연동
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="분리수거ON - 아파트 동별 ecoScore & AI 진단",
    page_icon="🌱",
    layout="wide"
)

# 시안 스타일 맞춤 커스텀 CSS
st.markdown("""
    <style>
    .main-title { color: #2E7D32; font-weight: 800; margin-bottom: 0px; }
    .sub-title { color: #666; font-size: 0.95rem; margin-bottom: 20px; }
    .podium-card {
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        background-color: #ffffff;
        border: 1px solid #E0E0E0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .podium-1 { border: 2px solid #FFD54F; background: #FFFDF0; }
    .rank-badge {
        font-weight: bold; padding: 4px 12px; border-radius: 12px; color: white; display: inline-block; margin-bottom: 8px;
    }
    .rank-1 { background-color: #FFB300; }
    .rank-2 { background-color: #90A4AE; }
    .rank-3 { background-color: #BCAAA4; }
    .dong-analysis-card {
        background-color: #ffffff;
        border: 1px solid #EAEAEA;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    </style>
""", unsafe_allow_html=True)

# Gemini API 초기화
gemini_client = None
try:
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        from google import genai
        gemini_client = genai.Client(api_key=api_key)
except Exception:
    gemini_client = None

# -----------------------------------------------------------------------------
# 2. 세션 상태 데이터 초기화
# -----------------------------------------------------------------------------
if "dong_data" not in st.session_state:
    st.session_state.dong_data = {
        "101동 & 102동": {
            "score": 12480,
            "delta": 120,
            "correct_ratio": 78,
            "incorrect_ratio": 22,
            "mistakes": [
                {"title": "페트병 라벨 제거 안 함", "desc": "일반쓰레기로 분류됨"},
                {"title": "캔과 일반쓰레기 혼합", "desc": "겉은 재활용 가능"}
            ],
            "guide": "페트병은 라벨을 떼서 비닐류로, 캔은 내용물을 비운 후 따로 배출해주세요!"
        },
        "103동 & 104동": {
            "score": 11230,
            "delta": 95,
            "correct_ratio": 74,
            "incorrect_ratio": 26,
            "mistakes": [
                {"title": "음식물 묻은 플라스틱 용기", "desc": "재활용 불가"},
                {"title": "종이류에 비닐 코팅 포장지", "desc": "일반쓰레기로 분류"}
            ],
            "guide": "양념이나 음식물이 묻은 플라스틱은 헹궈서 배출하고, 안 씻기면 일반쓰레기로 버려주세요."
        },
        "105동 & 106동": {
            "score": 10870,
            "delta": 80,
            "correct_ratio": 69,
            "incorrect_ratio": 31,
            "mistakes": [
                {"title": "유리병 뚜껑 미분리", "desc": "일반쓰레기 혼입"},
                {"title": "폐건전지 혼합 배출", "desc": "유해폐기물 분류"}
            ],
            "guide": "유리병 뚜껑은 철/플라스틱으로 따로 버리고, 건전지는 전용 수거함에 넣어주세요."
        },
        "107동 & 108동": {
            "score": 9320,
            "delta": 60,
            "correct_ratio": 72,
            "incorrect_ratio": 28,
            "mistakes": [
                {"title": "비닐봉투째 재활용품 담기", "desc": "분리배출 시도 불가"},
                {"title": "스티로폼 이물질 혼입", "desc": "재활용 불가"}
            ],
            "guide": "재활용품은 비닐봉투에서 전부 꺼내서 품목별 수거함에 낱개로 배출해야 합니다."
        }
    }

# -----------------------------------------------------------------------------
# 3. AI 분석 함수 (Gemini 2.5 Flash Lite / Mock Fallback)
# -----------------------------------------------------------------------------
def analyze_waste_image(image: Image.Image):
    prompt = """
    당신은 아파트 AI 스마트 쓰레기통 센서입니다. 쓰레기통 스캔 이미지를 분석하여 
    다음 JSON 형식으로만 출력을 생성하세요:
    {
      "correct_ratio": <올바르게 배출된 비율(0~100 정수)>,
      "incorrect_ratio": <잘못 배출된 비율(0~100 정수, 두 비율 합은 100)>,
      "gained_score": <이번 스캔으로 추가할 점수(10~150 정수)>,
      "mistakes": [
        {"title": "잘못 배출된 쓰레기 항목 명칭", "desc": "원인 및 분류 (예: 일반쓰레기 분류/재활용 불가)"}
      ],
      "guide": "주민들에게 전할 한 줄 올바른 분리배출 팁"
    }
    """
    if gemini_client:
        try:
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=[prompt, image],
                config={'response_mime_type': 'application/json'}
            )
            return json.loads(response.text)
        except Exception:
            pass
            
    return {
        "correct_ratio": 82,
        "incorrect_ratio": 18,
        "gained_score": 110,
        "mistakes": [
            {"title": "택배 박스 테이프 미제거", "desc": "종이 재활용 저해"},
            {"title": "투명 페트병 라벨 부착", "desc": "라벨 별도 배출 필요"}
        ],
        "guide": "택배 박스의 비닐 테이프와 운송장은 꼭 떼어낸 뒤 펼쳐서 배출해주세요!"
    }

# -----------------------------------------------------------------------------
# 4. 앱 헤더 및 메인 탭
# -----------------------------------------------------------------------------
st.markdown("<h1 class='main-title'>🌱 분리수거ON</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>작은 실천이 만드는 더 깨끗한 우리 아파트</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏆 아파트 동별 순위 & 분석", "📸 AI 쓰레기통 스캔", "🎁 이달의 리워드 혜택"])

# --- TAB 1: 아파트 동별 순위 & 분석 (시안 느낌 메인 화면) ---
with tab1:
    st.subheader("🥇 동별 누적 점수 순위")
    
    # 점수순 정렬
    sorted_dongs = sorted(st.session_state.dong_data.items(), key=lambda x: x[1]["score"], reverse=True)
    
    # 상단 포디움 3개 동
    col1, col2, col3 = st.columns(3)
    if len(sorted_dongs) > 1:
        d2_name, d2_info = sorted_dongs[1]
        with col1:
            st.markdown(f"""
            <div class='podium-card'>
                <span class='rank-badge rank-2'>2위</span>
                <h4>{d2_name}</h4>
                <h3>{d2_info['score']:,}점</h3>
                <p style='color:#2E7D32;'>▲ +{d2_info['delta']}</p>
            </div>
            """, unsafe_allow_html=True)

    if len(sorted_dongs) > 0:
        d1_name, d1_info = sorted_dongs[0]
        with col2:
            st.markdown(f"""
            <div class='podium-card podium-1'>
                <span class='rank-badge rank-1'>👑 1위</span>
                <h3 style='color:#B78103;'>{d1_name}</h3>
                <h2 style='color:#2E7D32;'>{d1_info['score']:,}점</h2>
                <p style='color:#2E7D32;'>▲ +{d1_info['delta']}</p>
            </div>
            """, unsafe_allow_html=True)

    if len(sorted_dongs) > 2:
        d3_name, d3_info = sorted_dongs[2]
        with col3:
            st.markdown(f"""
            <div class='podium-card'>
                <span class='rank-badge rank-3'>3위</span>
                <h4>{d3_name}</h4>
                <h3>{d3_info['score']:,}점</h3>
                <p style='color:#2E7D32;'>▲ +{d3_info['delta']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("🔍 동별 분리배출 상세 분석")
    st.caption("AI 센서가 감지한 분리배출 비율과 오배출 쓰레기 세부 내역입니다.")

    for rank, (dong_name, data) in enumerate(sorted_dongs, 1):
        st.markdown(f"<div class='dong-analysis-card'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1.5, 1.2, 1.2, 2.5])
        
        with c1:
            st.markdown(f"#### {rank}위. {dong_name}")
            st.markdown(f"**{data['score']:,}점** *(▲ +{data['delta']})*")
            
        with c2:
            st.metric("잘 분리배출", f"{data['correct_ratio']}%")
            st.progress(data['correct_ratio'] / 100)
            
        with c3:
            st.metric("잘못 배출", f"{data['incorrect_ratio']}%")
            st.progress(data['incorrect_ratio'] / 100)
            
        with c4:
            st.markdown("🚨 **주요 잘못 배출한 쓰레기**")
            for m in data.get("mistakes", []):
                st.markdown(f"- **{m['title']}** : {m['desc']}")
            st.info(f"💡 **개선 팁:** {data.get('guide', '')}")
            
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: AI 쓰레기통 스캔 ---
with tab2:
    st.subheader("📸 스마트 쓰레기통 스캔하기")
    st.write("쓰레기통 내부를 촬영해 올리면 AI가 분석하여 해당 동의 누적 점수에 자동 반영합니다.")
    
    selected_dong = st.selectbox("스캔할 아파트 동 선택", list(st.session_state.dong_data.keys()))
    
    upload_type = st.radio("업로드 방식", ["샘플 테스트", "사진 업로드", "카메라 촬영"], horizontal=True)
    
    sample_img = None
    if upload_type == "사진 업로드":
        file = st.file_uploader("쓰레기통 이미지 선택", type=["jpg", "png", "jpeg"])
        if file: sample_img = Image.open(file)
    elif upload_type == "카메라 촬영":
        cam = st.camera_input("촬영하기")
        if cam: sample_img = Image.open(cam)
    else:
        sample_img = Image.new('RGB', (300, 300), color=(210, 230, 210))
        
    if sample_img:
        st.image(sample_img, width=300, caption="스캔 준비 완료")
        if st.button("🚀 AI 분석 및 점수 획득", type="primary"):
            with st.spinner("AI가 쓰레기통 내부를 진단 중입니다..."):
                res = analyze_waste_image(sample_img)
                
                # 세션 데이터 업데이트
                target = st.session_state.dong_data[selected_dong]
                target["score"] += res["gained_score"]
                target["delta"] = res["gained_score"]
                target["correct_ratio"] = res["correct_ratio"]
                target["incorrect_ratio"] = res["incorrect_ratio"]
                target["mistakes"] = res["mistakes"]
                target["guide"] = res["guide"]
                
                st.success(f"🎉 분석 성공! [{selected_dong}]에 +{res['gained_score']}점이 누적되었습니다.")
                st.rerun()

# --- TAB 3: 이달의 리워드 혜택 ---
with tab3:
    st.subheader("🎁 1위 동 우수 주민 보상 혜택")
    st.write("매월 점수가 가장 높은 동의 엘리베이터 공용함 및 주민센터에 보상을 배치합니다.")
    
    top_dong_name, top_dong_info = sorted_dongs[0]
    
    st.markdown(f"""
    ### 🏆 이달의 1위 유력 동: **{top_dong_name}**
    - **현재 누적 점수:** {top_dong_info['score']:,} 점
    - **이번 달 보상 구성:**
      - 🧻 **주민 공용 생필품:** 친환경 롤휴지 & 종량제 봉투 세트
      - 🍪 **동별 간식박스:** 엘리베이터 신선 간식함 및 음료 증정
      - ☕ **카페 쿠폰:** 우수 분리배출 주민 대상 아메리카노 쿠폰
    """)
    
    goal_score = 15000
    st.progress(min(top_dong_info['score'] / goal_score, 1.0), text=f"목표 {goal_score:,}점 중 {top_dong_info['score']:,}점 달성")
