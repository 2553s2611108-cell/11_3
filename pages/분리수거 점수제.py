import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 기본 설정 및 시안 맞춤 디자인 CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="분리수거ON - 참여형 스마트 분리수거",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
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
    .sensor-box {
        background-color: #E8F5E9; border-radius: 12px; padding: 15px;
        border: 1px solid #C8E6C9; margin-bottom: 15px;
    }
    .quiz-box {
        background-color: #F3E5F5; border-radius: 12px; padding: 20px; border: 1px solid #E1BEE7;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 세션 상태 데이터 초기화 (이번 달 & 저번 달 데이터 포함)
# -----------------------------------------------------------------------------
# 이번 달 데이터
if "this_month_data" not in st.session_state:
    st.session_state.this_month_data = {
        "101동 & 102동": {
            "score": 12480, "delta": 120, "correct_ratio": 78, "incorrect_ratio": 22,
            "mistakes": [
                {"title": "페트병 라벨 미제거", "desc": "일반쓰레기로 분류됨", "how_to": "투명 페트병 비닐 라벨은 칼이나 손으로 떼어내어 '비닐류'에 버려주세요."},
                {"title": "캔과 일반쓰레기 혼합 배출", "desc": "재활용 처리 지연", "how_to": "캔 내부의 내용물과 이물질을 헹군 뒤 눌러서 '플라스틱/캔 수거함'에 따로 넣어주세요."}
            ]
        },
        "103동 & 104동": {
            "score": 11230, "delta": 95, "correct_ratio": 74, "incorrect_ratio": 26,
            "mistakes": [
                {"title": "음식물 잔여 플라스틱 용기", "desc": "재활용 불가", "how_to": "양념이나 국물이 묻은 플라스틱은 물로 깨끗이 씻은 후 배출하셔야 합니다. 안 씻길 경우 일반쓰레기로 버리세요."},
                {"title": "비닐 코팅 포장지 혼입", "desc": "일반쓰레기 분류", "how_to": "비닐이나 은박이 코팅된 종이 상자는 종이재활용이 불가하므로 일반 종량제 봉투에 버려주세요."}
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
                {"title": "비닐봉투째 재활용품 배출", "desc": "선별 불가", "how_to": "재활용품은 검은 비닐봉투에서 꺼내어 수거함에 낱개로 버려주셔야 선별이 가능합니다."},
                {"title": "스티로폼 이물질 부착", "desc": "재활용 불가", "how_to": "스티로폼 상자의 운송장 테이프와 상표 스티커를 전부 제거 후 배출하세요."}
            ]
        }
    }

# 저번 달 데이터 (기록 비교용)
if "last_month_data" not in st.session_state:
    st.session_state.last_month_data = {
        "101동 & 102동": {"score": 10920, "delta": 0, "correct_ratio": 72, "incorrect_ratio": 28, "mistakes": [{"title": "스티로폼 테이프 미제거", "desc": "일반쓰레기 분류", "how_to": "테이프를 모두 떼어내어 배출하세요."}]},
        "103동 & 104동": {"score": 11850, "delta": 0, "correct_ratio": 80, "incorrect_ratio": 20, "mistakes": [{"title": "유리병 깨짐 배출", "desc": "위험 요소", "how_to": "신문지에 싸서 불연성 봉투에 버려주세요."}]},
        "105동 & 106동": {"score": 9800, "delta": 0, "correct_ratio": 65, "incorrect_ratio": 35, "mistakes": [{"title": "음식물 비닐 혼입", "desc": "재활용 불가", "how_to": "비닐을 깨끗이 씻어 배출하세요."}]},
        "107동 & 108동": {"score": 8900, "delta": 0, "correct_ratio": 68, "incorrect_ratio": 32, "mistakes": [{"title": "택배박스 운송장 미제거", "desc": "선별 불가", "how_to": "스티커를 떼어내주세요."}]}
    }

if "cheers" not in st.session_state:
    st.session_state.cheers = [
        {"dong": "101동 & 102동", "msg": "오늘 페트병 비닐 다 떼서 버렸습니다! 이번 달도 1위 가봅시다!"},
        {"dong": "103동 & 104동", "msg": "배달 용기 기름때 물로 깨끗하게 씻어버리기 완료!"}
    ]

if "poll_votes" not in st.session_state:
    st.session_state.poll_votes = {"친환경 롤휴지 & 종량제봉투": 58, "주민센터 간식 수제쿠키": 74, "아파트 카페 커피 쿠폰": 42}

# 스마트 쓰레기통 센서 스캔 시뮬레이션
def simulate_bin_ai_scan():
    scenarios = [
        {
            "correct_ratio": 88, "incorrect_ratio": 12, "gained_score": 130,
            "mistakes": [{"title": "투명 페트병 라벨 미제거", "desc": "비닐 미분리 감지", "how_to": "라벨을 손으로 떼어내어 비닐 수거함에 버려주세요!"}]
        },
        {
            "correct_ratio": 62, "incorrect_ratio": 38, "gained_score": 70,
            "mistakes": [
                {"title": "음식물 잔여 플라스틱 배달용기", "desc": "세척 미흡", "how_to": "주방세제로 세척 후 배출해야 재활용이 가능합니다."},
                {"title": "택배 상자 비닐 테이프 미제거", "desc": "종이 재활용 불가", "how_to": "박스의 박스테이프와 운송장을 완전히 떼어내어 주세요."}
            ]
        }
    ]
    return random.choice(scenarios)

# -----------------------------------------------------------------------------
# 3. 앱 헤더 및 기간 선택 (이번 달 vs 저번 달)
# -----------------------------------------------------------------------------
st.markdown("<h1 class='main-title'>🌱 분리수거ON</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>작은 실천이 만드는 더 깨끗한 우리 아파트</p>", unsafe_allow_html=True)

# 저번달 / 이번달 선택 필터
selected_period = st.radio("📅 조회 기간 선택", ["이번 달 (2026년 10월)", "저번 달 (2026년 9월)"], horizontal=True)

current_dataset = st.session_state.this_month_data if "이번 달" in selected_period else st.session_state.last_month_data

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 동별 순위 & AI 분석", 
    "🤖 현장 쓰레기통 AI 스캔", 
    "🎯 주민 참여 미션 & 퀴즈", 
    "🎁 리워드 투표 & 응원"
])

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
            st.markdown(f"<div class='podium-card podium-1'><span class='rank-badge rank-1'>👑 1위</span><h3 style='color:#B78103;'>{sorted_dongs[0][0]}</h3><h2 style='color:#2E7D32;'>{sorted_dongs[0][0] if False else sorted_dongs[0][1]['score']:,}점</h2></div>", unsafe_allow_html=True)
    if len(sorted_dongs) > 2:
        with col3:
            st.markdown(f"<div class='podium-card'><span class='rank-badge rank-3'>3위</span><h4>{sorted_dongs[2][0]}</h4><h3>{sorted_dongs[2][1]['score']:,}점</h3></div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("🔍 동별 분리배출 상세 분석")
    st.caption("AI 쓰레기통 센서가 감지한 오배출 물품 항목을 클릭하면 올바른 배출 방법을 확인하실 수 있습니다.")

    for rank, (dong_name, data) in enumerate(sorted_dongs, 1):
        st.markdown(f"<div class='dong-analysis-card'>", unsafe_allow_html=True)
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
            for idx, m in enumerate(data.get("mistakes", [])):
                # 상호작용: 잘못 버린 항목 클릭 시 올바른 배출법을 보여주는 토글(Expander)
                with st.expander(f"❌ {m['title']} ({m['desc']})"):
                    st.success(f"💡 **올바르게 버리는 방법:**\n\n{m['how_to']}")
                    
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: 현장 AI 쓰레기통 원격 스캔 ---
with tab2:
    st.subheader("🤖 현장 AI 스마트 쓰레기통 원격 제어")
    st.write("아파트 쓰레기 수거장에 도착하셨나요? 내가 위치한 동을 선택하고 쓰레기통 부착 카메라로 AI 분석을 실행해보세요.")
    
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        selected_dong = st.selectbox("📍 내 아파트 동 선택", list(st.session_state.this_month_data.keys()))
        bin_loc = st.radio("🚮 수거장 위치 선택", ["1층 중앙 수거장", "지하주차장 수거장", "후문 분리수거장"])
        
        st.markdown("""
        <div class='sensor-box'>
            📡 <b>스마트 쓰레기통 온디바이스 AI 카메라:</b> <span style='color:green;'>정상 대기 중</span><br>
            ※ 실시간 쓰레기 투입 후 아래 버튼을 눌러 점수를 적립하세요.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📸 쓰레기통 부착 AI 카메라 스캔 실행", type="primary", use_container_width=True):
            with st.spinner("스마트 쓰레기통 내부 카메라가 투입된 쓰레기를 스캔 중입니다..."):
                res = simulate_bin_ai_scan()
                target = st.session_state.this_month_data[selected_dong]
                target["score"] += res["gained_score"]
                target["delta"] = res["gained_score"]
                target["correct_ratio"] = res["correct_ratio"]
                target["incorrect_ratio"] = res["incorrect_ratio"]
                target["mistakes"] = res["mistakes"]
                
                st.session_state.last_res = res
                st.session_state.last_dong = selected_dong
                st.success("스캔이 완료되어 이번 달 동 점수에 반영되었습니다!")

    with col_r:
        if "last_res" in st.session_state:
            res = st.session_state.last_res
            st.markdown(f"### 📊 [{st.session_state.last_dong}] AI 분석 결과")
            st.metric("획득 점수", f"+{res['gained_score']}점")
            
            st.markdown("🚨 **감지된 오배출 쓰레기 내역:**")
            for m in res["mistakes"]:
                st.warning(f"• **{m['title']}**: {m['desc']}")
                with st.expander(f"👉 [{m['title']}] 올바르게 버리는 법 확인"):
                    st.write(m["how_to"])
                
            st.divider()
            st.markdown("🛠️ **주민 직접 참여: 내가 스스로 오배출을 정정했어요!**")
            if st.button("✨ 잘못 버려진 쓰레기 다시 꺼내서 똑바로 버리기 (+30점 추가 보너스)"):
                st.session_state.this_month_data[st.session_state.last_dong]["score"] += 30
                st.success("정정 인증 완료! 우리 동 점수 30점이 추가되었습니다.")
                st.rerun()

# --- TAB 3: 주민 참여 미션 & 퀴즈 ---
with tab3:
    st.subheader("🎯 분리수거 OX 퀴즈 (매일 +10점 획득)")
    st.write("퀴즈를 풀고 올바른 분리배출 상식도 배우고, 우리 동 점수도 올려보세요!")
    
    st.markdown("""
    <div class='quiz-box'>
        <h4>Q. 택배 박스에 붙어있는 비닐 박스테이프와 운송장 스티커는 종이류와 함께 버려도 된다?</h4>
    </div>
    """, unsafe_allow_html=True)
    
    quiz_ans = st.radio("정답 선택", ["⭕ O (그대로 버린다)", "❌ X (떼어내고 버려야 한다)"], horizontal=True)
    user_dong_for_quiz = st.selectbox("점수를 적립할 내 아파트 동 선택", list(st.session_state.this_month_data.keys()), key="quiz_dong")
    
    if st.button("정답 제출하기"):
        if "❌ X" in quiz_ans:
            st.session_state.this_month_data[user_dong_for_quiz]["score"] += 10
            st.balloons()
            st.success(f"정답입니다! 🎉 테이프와 스티커는 이물질이므로 완전히 떼어내야만 종이 재활용이 가능합니다. [{user_dong_for_quiz}]에 +10점 적립!")
        else:
            st.error("틀렸습니다! 😅 비닐 테이프와 운송장은 반드시 떼어내야 종이 재활용이 가능합니다.")

# --- TAB 4: 리워드 투표 & 응원 한마디 ---
with tab4:
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
