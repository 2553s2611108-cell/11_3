import streamlit as st

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="분리수거ON - 아파트 동별 ecoScore",
    page_icon="🌱",
    layout="wide"
)

# 커스텀 CSS 스타일링
css_style = """
<style>
.main-title { color: #2E7D32; font-weight: 800; margin-bottom: 0px; }
.sub-title { color: #666; font-size: 0.95rem; margin-bottom: 15px; }
.podium-card {
    border-radius: 16px; padding: 20px; text-align: center;
    background-color: #ffffff; border: 1px solid #E0E0E0;
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
    background-color: #ffffff; border: 1px solid #EAEAEA;
    border-radius: 16px; padding: 20px; margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 세션 상태 데이터 초기화 (이번 달 & 저번 달)
# -----------------------------------------------------------------------------
if "this_month_data" not in st.session_state:
    st.session_state.this_month_data = {
        "101동 & 102동": {
            "score": 12480, "delta": 120, "correct_ratio": 78, "incorrect_ratio": 22,
            "mistakes": [
                {"title": "페트병 라벨 미제거", "desc": "일반쓰레기로 분류됨", "how_to": "투명 페트병 비닐 라벨은 떼어내어 '비닐류' 수거함에 버려주세요."},
                {"title": "캔과 일반쓰레기 혼합 배출", "desc": "재활용 처리 지연", "how_to": "캔 내부 내용물을 헹군 뒤 눌러서 '캔/플라스틱 수거함'에 따로 넣어주세요."}
            ]
        },
        "103동 & 104동": {
            "score": 11230, "delta": 95, "correct_ratio": 74, "incorrect_ratio": 26,
            "mistakes": [
                {"title": "음식물 잔여 플라스틱 용기", "desc": "재활용 불가", "how_to": "양념이나 국물이 묻은 플라스틱은 물로 깨끗이 씻은 후 배출하셔야 합니다. 안 씻길 경우 일반종량제 봉투에 버리세요."},
                {"title": "비닐 코팅 포장지 혼입", "desc": "일반쓰레기 분류", "how_to": "비닐이나 은박이 코팅된 종이 상자는 종이재활용이 불가하므로 일반 쓰레기로 버려주세요."}
            ]
        },
        "105동 & 106동": {
            "score": 10870, "delta": 80, "correct_ratio": 69, "incorrect_ratio": 31,
            "mistakes": [
                {"title": "유리병 병뚜껑 미분리", "desc": "일반쓰레기 혼입", "how_to": "유리병의 철재나 플라스틱 병뚜껑은 분리하여 소재별로 배출해야 합니다."},
                {"title": "폐건전지 혼합 배출", "desc": "유해폐기물 위험", "how_to": "건전지는 화재 위험이 있으므로 수거장의 '폐건전지 전용 수거함'에 넣어주세요."}
            ]
        },
        "107동 & 108동": {
            "score": 9320, "delta": 60, "correct_ratio": 72, "incorrect_ratio": 28,
            "mistakes": [
                {"title": "비닐봉투째 재활용품 배출", "desc": "선별 불가", "how_to": "재활용품은 비닐봉투에서 꺼내어 수거함에 낱개로 버려주셔야 선별이 가능합니다."},
                {"title": "스티로폼 이물질 부착", "desc": "재활용 불가", "how_to": "스티로폼 상자의 운송장 테이프와 상표 스티커를 전부 제거 후 배출하세요."}
            ]
        }
    }

if "last_month_data" not in st.session_state:
    st.session_state.last_month_data = {
        "101동 & 102동": {
            "score": 10920, "delta": 0, "correct_ratio": 72, "incorrect_ratio": 28,
            "mistakes": [{"title": "스티로폼 테이프 미제거", "desc": "일반쓰레기 분류", "how_to": "테이프를 모두 떼어내어 배출하세요."}]
        },
        "103동 & 104동": {
            "score": 11850, "delta": 0, "correct_ratio": 80, "incorrect_ratio": 20,
            "mistakes": [{"title": "유리병 깨짐 배출", "desc": "위험 요소", "how_to": "신문지에 싸서 불연성 봉투에 버려주세요."}]
        },
        "105동 & 106동": {
            "score": 9800, "delta": 0, "correct_ratio": 65, "incorrect_ratio": 35,
            "mistakes": [{"title": "음식물 비닐 혼입", "desc": "재활용 불가", "how_to": "비닐을 깨끗이 씻어 배출하세요."}]
        },
        "107동 & 108동": {
            "score": 8900, "delta": 0, "correct_ratio": 68, "incorrect_ratio": 32,
            "mistakes": [{"title": "택배박스 운송장 미제거", "desc": "선별 불가", "how_to": "스티커를 떼어내주세요."}]
        }
    }

if "cheers" not in st.session_state:
    st.session_state.cheers = [
        {"dong": "101동 & 102동", "msg": "오늘 페트병 비닐 다 떼서 버렸습니다! 이번 달도 1위 유지해봐요!"},
        {"dong": "103동 & 104동", "msg": "배달 용기 기름때 물로 깨끗하게 씻어버리기 완료!"}
    ]

if "poll_votes" not in st.session_state:
    st.session_state.poll_votes = {"친환경 롤휴지 & 종량제봉투": 58, "주민센터 간식 수제쿠키": 74, "아파트 카페 커피 쿠폰": 42}

# -----------------------------------------------------------------------------
# 3. 앱 헤더 및 기간 선택 (이번 달 vs 저번 달)
# -----------------------------------------------------------------------------
st.markdown("<h1 class='main-title'>🌱 분리수거ON</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>작은 실천이 만드는 더 깨끗한 우리 아파트</p>", unsafe_allow_html=True)

# 조회 기간 필터
selected_period = st.radio("📅 조회 기간 선택", ["이번 달 (2026년 10월)", "저번 달 (2026년 9월)"], horizontal=True)

current_dataset = st.session_state.this_month_data if "이번 달" in selected_period else st.session_state.last_month_data

# 2개의 메인 탭 구성
tab1, tab2 = st.tabs(["🏆 동별 순위 & AI 분석", "🎁 리워드 투표 & 응원"])

# --- TAB 1: 아파트 동별 순위 & 상세 분석 ---
with tab1:
    st.subheader(f"🥇 {selected_period} 동별 누적 점수 순위")
    sorted_dongs = sorted(current_dataset.items(), key=lambda x: x[1]["score"], reverse=True)
    
    col1, col2, col3 = st.columns(3)
    if len(sorted_dongs) > 1:
        with col1:
            st.markdown(f"<div class='podium-card'><span class='rank-badge rank-2'>2위</span><h4>{sorted_dongs[1][0]}</h4><h3>{sorted_dongs[1][1]['score']:,}점</h3></div>", unsafe_allow_html=True)
    if len(sorted_dongs) > 0:
        with col2:
            st.markdown(f"<div class='podium-card podium-1'><span class='rank-badge rank-1'>👑 1위</span><h3 style='color:#B78103;'>{sorted_dongs[0][0]}</h3><h2 style='color:#2E7D32;'>{sorted_dongs[0][1]['score']:,}점</h2></div>", unsafe_allow_html=True)
    if len(sorted_dongs) > 2:
        with col3:
            st.markdown(f"<div class='podium-card'><span class='rank-badge rank-3'>3위</span><h4>{sorted_dongs[2][0]}</h4><h3>{sorted_dongs[2][1]['score']:,}점</h3></div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("🔍 동별 분리배출 상세 분석")
    st.caption("잘못 버린 쓰레기 항목을 누르시면 올바른 분리배출 방법을 확인하실 수 있습니다.")

    for rank, (dong_name, data) in enumerate(sorted_dongs, 1):
        st.markdown("<div class='dong-analysis-card'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1.5, 1.2, 1.2, 2.8])
        
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
            st.markdown("🚨 **잘못 버린 물품 (누르면 올바른 배출법 표시)**")
            for m in data.get("mistakes", []):
                with st.expander(f"❌ {m['title']} ({m['desc']})"):
                    st.success(f"💡 **올바르게 버리는 방법:**\n\n{m['how_to']}")
                    
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: 리워드 투표 & 응원 한마디 ---
with tab2:
    col_v, col_c = st.columns([1, 1])
    
    with col_v:
        st.subheader("🗳️ 이달의 우수 동 리워드 투표")
        st.write("1위 동 주민들에게 지급될 리워드 품목을 직접 골라주세요!")
        
        selected_poll = st.radio("원하는 보상 선택", list(st.session_state.poll_votes.keys()))
        if st.button("투표 제출하기"):
            st.session_state.poll_votes[selected_poll] += 1
            st.success("투표가 성공적으로 반영되었습니다!")
            
        st.write("📊 **주민 실시간 투표 현황:**")
        for item, count in st.session_state.poll_votes.items():
            st.write(f"- {item}: **{count}표**")

    with col_c:
        st.subheader("💬 우리 동 분리수거 응원 게시판")
        write_dong = st.selectbox("내 아파트 동 선택", list(st.session_state.this_month_data.keys()), key="comment_dong")
        comment_text = st.text_input("동 주민들과 함께 나누고 싶은 다짐이나 팁 한마디")
        
        if st.button("댓글 작성하기"):
            if comment_text:
                st.session_state.cheers.insert(0, {"dong": write_dong, "msg": comment_text})
                st.success("댓글 등록 완료!")
                st.rerun()
                
        st.write("💬 **최근 동별 주민 응원 메시지:**")
        for c in st.session_state.cheers[:5]:
            st.info(f"**[{c['dong']}]** {c['msg']}")
