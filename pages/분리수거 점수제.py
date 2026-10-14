import streamlit as st
import json
import os
from PIL import Image

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 Gemini API 연동
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="분리수거ON - 아파트 동별 분리수거 점수제",
    page_icon="🌱",
    layout="wide"
)

# 커스텀 CSS 스타일링 (시안 느낌 구현)
st.markdown("""
    <style>
    .main-title {
        color: #2E7D32;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }
    .podium-card {
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        background-color: #ffffff;
        border: 1px solid #E0E0E0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .podium-1 {
        border: 2px solid #FFD54F;
        background: #FFFDF0;
    }
    .rank-badge {
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 12px;
        color: white;
        display: inline-block;
        margin-bottom: 8px;
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
    .mistake-box {
        background-color: #FFF5F5;
        border-radius: 12px;
        padding: 12px;
        border-left: 4px solid #FF5252;
    }
    </style>
""", unsafe_allow_html=True)

# Gemini API 초기화 (google-genai SDK)
gemini_client = None
try:
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        from google import genai
        gemini_client = genai.Client(api_key=api_key)
except Exception:
    gemini_client = None

# -----------------------------------------------------------------------------
# 2. 세션 상태 (Session State) 데이터 초기화 (초기 이미지 시안 기반 데이터)
# -----------------------------------------------------------------------------
if "dong_data" not in st.session_state:
    st.session_state.dong_data = {
        "101동": {
            "score": 12480,
            "delta": 120,
            "correct_ratio": 78,
            "incorrect_ratio": 22,
            "mistakes": [
                {"title": "페트병 라벨 제거 안 함", "desc": "일반쓰레기로 분류됨"},
                {"title": "캔과 일반쓰레기 혼합", "desc": "겉은 재활용 가능"}
            ]
        },
        "102동": {
            "score": 11230,
            "delta": 95,
            "correct_ratio": 74,
            "incorrect_ratio": 26,
            "mistakes": [
                {"title": "음식물 묻은 플라스틱 용기", "desc": "재활용 불가"},
                {"title": "종이류에 비닐 코팅된 포장지", "desc": "일반쓰레기로 분류됨"}
            ]
        },
        "103동": {
            "score": 10870,
            "delta": 80,
            "correct_ratio": 69,
            "incorrect_ratio": 31,
            "mistakes": [
                {"title": "유리병 뚜껑 미분리", "desc": "일반쓰레기로 분류됨"},
                {"title": "건전지 혼합 배출", "desc": "유해폐기물로 분류"}
            ]
        },
        "104동": {
            "score": 9320,
            "delta": 60,
            "correct_ratio": 72,
            "incorrect_ratio": 28,
            "mistakes": [
                {"title": "비닐봉투에 재활용품 담기", "desc": "분리배출 시도 불가"},
                {"title": "스티로폼 이물질 혼입", "desc": "재활용 불가"}
            ]
        },
        "105동": {
            "score": 8760,
            "delta": 55,
            "correct_ratio": 65,
            "incorrect_ratio": 35,
            "mistakes": [
                {"title": "택배 상자 운송장 미제거", "desc": "종이재활용 불가"}
            ]
        }
    }

# -----------------------------------------------------------------------------
# 3. AI 분석 함수 (Gemini 2.5 Flash Lite)
# -----------------------------------------------------------------------------
def analyze_waste_image(image: Image.Image):
    prompt = """
    당신은 아파트 AI 스마트 쓰레기통 분석기입니다. 제공된 이미지를 분석하여 
    다음 JSON 형식으로만 결과를 반환하세요:
    {
      "correct_ratio": <올바르게 배출된 비율(0~100 정수)>,
      "incorrect_ratio": <잘못 배출된 비율(0~100 정수, 두 비율 합은 100)>,
      "gained_score": <이번 스캔으로 얻은 점수(10~100 정수)>,
      "mistakes": [
        {"title": "잘못 넣은 쓰레기 항목 명칭", "desc": "원인 및 분류 안내 (예: 재활용 불가/일반쓰레기 분류)"}
      ]
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
            
    # Mock fallback 데이터
    return {
        "correct_ratio": 80,
        "incorrect_ratio": 20,
        "gained_score": 100,
        "mistakes": [
            {"title": "페트병 라벨 미제거", "desc": "비닐 라벨은 떼서 비닐류로 분리"},
            {"title": "음식물 양념 묻은 용기", "desc": "세척 후 배출 필요 (재활용 불가)"}
        ]
    }

# -----------------------------------------------------------------------------
# 4. 헤더 및 사이드바
# -----------------------------------------------------------------------------
st.markdown("<h1 class='main-title'>🌱 분리수거ON</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>작은 실천이 만드는 더 깨끗한 우리 아파트</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📸 AI 쓰레기통 스캔")
    selected_dong_input = st.selectbox("스캔할 아파트 동 선택", list(st.session_state.dong_data.keys()))
    
    upload_file = st.file_uploader("쓰레기통 내부 사진 업로드", type=["jpg", "jpeg", "png"])
    camera_file = st.camera_input("또는 직접 촬영")
    
    target_image = None
    if upload_file:
        target_image = Image.open(upload_file)
    elif camera_file:
        target_image = Image.open(camera_file)
        
    if st.button("🚀 쓰레기 스캔 및 점수 반영", type="primary", use_container_width=True):
        if target_image is None:
            # 테스트용 기본 이미지
            target_image = Image.new('RGB', (300, 300), color=(200, 230, 200))
            
        with st.spinner("AI가 분석 중입니다..."):
            result = analyze_waste_image(target_image)
            
            # 동 데이터 업데이트
            dong = st.session_state.dong_data[selected_dong_input]
            dong["score"] += result["gained_score"]
            dong["delta"] = result["gained_score"]
            dong["correct_ratio"] = result["correct_ratio"]
            dong["incorrect_ratio"] = result["incorrect_ratio"]
            if result.get("mistakes"):
                dong["mistakes"] = result["mistakes"]
                
            st.success(f"[{selected_dong_input}] 분석 완료! +{result['gained_score']}점이 추가되었습니다.")

# -----------------------------------------------------------------------------
# 5. 메인 화면 - 아파트 동별 누적 점수 순위 (상단 포디움)
# -----------------------------------------------------------------------------
st.subheader("🏆 아파트 동별 누적 점수 순위")
st.caption("지금까지의 누적 점수로 집계된 동별 순위입니다.")

# 점수순 정렬
sorted_dongs = sorted(st.session_state.dong_data.items(), key=lambda x: x[1]["score"], reverse=True)

col1, col2, col3 = st.columns(3)

# 2위
if len(sorted_dongs) > 1:
    d2_name, d2_info = sorted_dongs[1]
    with col1:
        st.markdown(f"""
        <div class='podium-card'>
            <span class='rank-badge rank-2'>2위</span>
            <h3>{d2_name}</h3>
            <h2>{d2_info['score']:,}점</h2>
            <p style='color:#2E7D32;'>▲ +{d2_info['delta']}</p>
        </div>
        """, unsafe_allow_html=True)

# 1위 (중앙 강조)
if len(sorted_dongs) > 0:
    d1_name, d1_info = sorted_dongs[0]
    with col2:
        st.markdown(f"""
        <div class='podium-card podium-1'>
            <span class='rank-badge rank-1'>👑 1위</span>
            <h2 style='color:#B78103;'>{d1_name}</h2>
            <h1 style='color:#2E7D32;'>{d1_info['score']:,}점</h1>
            <p style='color:#2E7D32;'>▲ +{d1_info['delta']}</p>
        </div>
        """, unsafe_allow_html=True)

# 3위
if len(sorted_dongs) > 2:
    d3_name, d3_info = sorted_dongs[2]
    with col3:
        st.markdown(f"""
        <div class='podium-card'>
            <span class='rank-badge rank-3'>3위</span>
            <h3>{d3_name}</h3>
            <h2>{d3_info['score']:,}점</h2>
            <p style='color:#2E7D32;'>▲ +{d3_info['delta']}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 6. 메인 화면 - 동별 분리배출 분석 (하단 카드 리스트)
# -----------------------------------------------------------------------------
st.subheader("🔍 동별 분리배출 분석")
st.caption("AI가 분석한 각 동의 분리배출 현황과 잘못 배출한 쓰레기 유형입니다.")

for rank, (dong_name, data) in enumerate(sorted_dongs, 1):
    with st.container():
        st.markdown(f"<div class='dong-analysis-card'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1.5, 1.5, 1.5, 3])
        
        with c1:
            st.markdown(f"### {rank}위. {dong_name}")
            st.markdown(f"**{data['score']:,}점**")
            st.caption(f"▲ +{data['delta']}")
            
        with c2:
            st.metric("잘 분리배출", f"{data['correct_ratio']}%")
            st.progress(data['correct_ratio'] / 100)
            
        with c3:
            st.metric("잘못 배출", f"{data['incorrect_ratio']}%")
            st.progress(data['incorrect_ratio'] / 100)
            
        with c4:
            st.markdown("🚨 **주요 잘못 배출한 쓰레기**")
            if data.get("mistakes"):
                for m in data["mistakes"]:
                    st.markdown(f"- **{m['title']}** : {m['desc']}")
            else:
                st.write("오배출 항목 없이 깨끗하게 관리되고 있습니다.")
                
        st.markdown("</div>", unsafe_allow_html=True)
