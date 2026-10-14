import os
import json
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 Custom CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="분리수거 ON - 아파트 동별 누적 점수",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .rank-card {
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        background-color: white;
    }
    .rank-1 {
        border: 2px solid #fbc02d;
        background-color: #fffde7;
    }
    .rank-2 {
        border: 1px solid #cfd8dc;
        background-color: #f8f9fa;
    }
    .rank-3 {
        border: 1px solid #ffe0b2;
        background-color: #fff8e1;
    }
    .badge-plus {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .mistake-box {
        background-color: #fff5f5;
        border-radius: 12px;
        padding: 10px;
        margin-top: 5px;
        border-left: 4px solid #ff5252;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 세션 상태 (동별 데이터 초기화)
# -----------------------------------------------------------------------------
if "dong_data" not in st.session_state:
    st.session_state.dong_data = {
        "101동 & 102동": {
            "score": 12480,
            "change": 120,
            "correct_ratio": 78,
            "incorrect_ratio": 22,
            "mistakes": [
                ("페트병 라벨 제거 안 함", "일반쓰레기로 분류됨"),
                ("캔과 일반쓰레기 혼합", "겉은 재활용 가능")
            ]
        },
        "103동 & 104동": {
            "score": 11230,
            "change": 95,
            "correct_ratio": 74,
            "incorrect_ratio": 26,
            "mistakes": [
                ("음식물 묻은 플라스틱 용기", "재활용 불가"),
                ("종이류에 비닐 코팅된 포장지", "일반쓰레기로 분류됨")
            ]
        },
        "105동 & 106동": {
            "score": 10870,
            "change": 80,
            "correct_ratio": 69,
            "incorrect_ratio": 31,
            "mistakes": [
                ("유리병 뚜껑 미분리", "일반쓰레기로 분류됨"),
                ("건전지 혼합 배출", "유해폐기물로 분류")
            ]
        },
        "107동 & 108동": {
            "score": 9320,
            "change": 60,
            "correct_ratio": 72,
            "incorrect_ratio": 28,
            "mistakes": [
                ("비닐봉투에 재활용품 담기", "분리배출 시도 불가"),
                ("스티로폼 이물질 혼입", "재활용 불가")
            ]
        }
    }

# -----------------------------------------------------------------------------
# 3. 도넛 차트 생성 함수
# -----------------------------------------------------------------------------
def create_donut_chart(correct, incorrect):
    fig = go.Figure(data=[go.Pie(
        labels=['잘 분리배출', '잘못 배출'],
        values=[correct, incorrect],
        hole=0.65,
        marker_colors=['#00a86b', '#ff6b6b'],
        textinfo='none',
        hoverinfo='label+percent'
    )])
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=130,
        width=130,
        annotations=[dict(
            text=f"<b>{correct}%</b><br><span style='font-size:10px;color:gray;'>잘 분리배출</span>",
            x=0.5, y=0.5, font_size=14, showarrow=False
        )]
    )
    return fig

# -----------------------------------------------------------------------------
# 4. Gemini AI 분석 함수
# -----------------------------------------------------------------------------
def analyze_waste_image(image):
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    if not api_key:
        return None, "GEMINI_API_KEY가 설정되지 않았습니다."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        
        prompt = """당신은 분리수거 전문 AI입니다. 쓰레기통/쓰레기 사진을 분석하여 오직 JSON 형식으로만 답변하세요.
{
    "correct_ratio": 75,
    "incorrect_ratio": 25,
    "added_score": 100,
    "mistakes": [
        ["잘못 배출된 항목명 1", "사유 설명 1"],
        ["잘못 배출된 항목명 2", "사유 설명 2"]
    ]
}"""
        response = model.generate_content([prompt, image])
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("\n", 1)[0]
            if text.startswith("json"):
                text = text[4:].strip()
        return json.loads(text), None
    except Exception as e:
        return None, str(e)

# -----------------------------------------------------------------------------
# 5. 헤더 화면
# -----------------------------------------------------------------------------
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.title("🌱 분리수거 ON")
    st.caption("작은 실천이 만드는 더 깨끗한 우리 동네 | 함께하는 분리수거! 더 좋은 우리 아파트!")
with col_h2:
    selected_tab = st.selectbox("메뉴 선택", ["🏠 홈", "📸 AI 쓰레기 스캔", "🎁 보상함", "👤 마이페이지"])

# -----------------------------------------------------------------------------
# 6. 메인 화면 - 🏠 홈
# -----------------------------------------------------------------------------
if selected_tab == "🏠 홈":
    st.subheader("🏆 아파트 동별 누적 점수 순위")
    st.caption("지금까지의 누적 점수로 집계된 동별 순위입니다.")

    sorted_dongs = sorted(
        list(st.session_state.dong_data.items()),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    col_rank2, col_rank1, col_rank3 = st.columns([1, 1.1, 1])

    if len(sorted_dongs) >= 3:
        # 2위
        with col_rank2:
            d_name, d_info = sorted_dongs[1]
            score_str = f"{d_info['score']:,}"
            change_str = str(d_info['change'])
            html_content = f'<div class="rank-card rank-2"><span style="font-size:24px;">🥈</span><h4 style="margin:5px 0;">{d_name}</h4><h3 style="margin:5px 0; color:#333;">{score_str}점</h3><span class="badge-plus">▲ +{change_str}</span></div>'
            st.markdown(html_content, unsafe_allow_html=True)

        # 1위
        with col_rank1:
            d_name, d_info = sorted_dongs[0]
            score_str = f"{d_info['score']:,}"
            change_str = str(d_info['change'])
            html_content = f'<div class="rank-card rank-1"><span style="font-size:28px;">👑 🥇</span><h3 style="margin:5px 0; color:#1b5e20;">{d_name}</h3><h2 style="margin:5px 0; color:#d81b60;">{score_str}점</h2><span class="badge-plus">▲ +{change_str}</span></div>'
            st.markdown(html_content, unsafe_allow_html=True)

        # 3위
        with col_rank3:
            d_name, d_info = sorted_dongs[2]
            score_str = f"{d_info['score']:,}"
            change_str = str(d_info['change'])
            html_content = f'<div class="rank-card rank-3"><span style="font-size:24px;">🥉</span><h4 style="margin:5px 0;">{d_name}</h4><h3 style="margin:5px 0; color:#333;">{score_str}점</h3><span class="badge-plus">▲ +{change_str}</span></div>'
            st.markdown(html_content, unsafe_allow_html=True)

    st.write("")
    st.divider()

    st.subheader("🔍 동별 분리배출 분석")
    st.caption("AI가 분석한 각 동의 분리배출 현황과 잘못 배출한 쓰레기 유형입니다.")

    for idx, (dong_name, data) in enumerate(sorted_dongs, 1):
        with st.container():
            c1, c2, c3 = st.columns([1.5, 1.2, 2.3])
            
            with c1:
                st.markdown(f"### {idx}. {dong_name}")
                score_str = f"{data['score']:,}"
                st.markdown(f"## **{score_str}점**")
                change_str = str(data['change'])
                st.markdown(f"<span class='badge-plus'>▲ +{change_str}</span>", unsafe_allow_html=True)

            with
