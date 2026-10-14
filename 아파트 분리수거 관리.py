import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(
    page_title="우리 아파트 분리수거 관리",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 기본 스타일
# -----------------------------
st.markdown("""
<style>
    .stApp { background: #f5f8f6; }
    .block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1200px; }
    .hero {
        padding: 1.7rem 1.8rem; border-radius: 20px;
        background: linear-gradient(120deg, #e0f2e8, #f0f8f3);
        border: 1px solid #d4e8dc; margin-bottom: 1.1rem;
    }
    .hero h1 { margin: 0; color: #174d36; }
    .hero p { margin: .45rem 0 0 0; color: #426653; font-size: 1.02rem; }
    .small-muted { color: #66756d; font-size: .92rem; }
    div[data-testid="stMetric"] {
        background: white; padding: 1rem; border-radius: 15px;
        border: 1px solid #e2ebe5;
    }
    div.stButton > button { border-radius: 10px; min-height: 2.6rem; }
    .feature-note {
        background: white; border: 1px solid #e2ebe5; border-radius: 15px;
        padding: 1rem 1.1rem; min-height: 120px;
    }
</style>
""", unsafe_allow_html=True)

# 데모용 데이터: 실제 서비스에서는 데이터베이스 사용을 권장합니다.
if "reports" not in st.session_state:
    st.session_state.reports = []
if "page" not in st.session_state:
    st.session_state.page = "메인 페이지"

def go(page):
    st.session_state.page = page

def status_badge(status):
    mapping = {
        "접수": "🟡 접수",
        "확인 중": "🔵 확인 중",
        "처리 완료": "🟢 처리 완료",
    }
    return mapping.get(status, status)

# -----------------------------
# 사이드바 내비게이션
# -----------------------------
with st.sidebar:
    st.markdown("## ♻️ 그린 아파트")
    st.caption("분리수거 관리 시스템")
    st.divider()
    pages = [
        "메인 페이지",
        "Trash Alarm",
        "분리수거 점수제",
        "의식개선 공용방송",
        "신고하기",
    ]
    for page in pages:
        if st.button(page, key=f"nav_{page}", use_container_width=True,
                     type="primary" if st.session_state.page == page else "secondary"):
            go(page)
            st.rerun()
    st.divider()
    st.caption("※ 현재 버전은 시연용이며, 신고 데이터는 세션에 임시 저장됩니다.")

page = st.session_state.page

# -----------------------------
# 메인 페이지
# -----------------------------
if page == "메인 페이지":
    st.markdown("""
    <div class="hero">
      <h1>♻️ 우리 아파트 분리수거 현황</h1>
      <p>깨끗한 공동주택은 올바른 분리배출에서 시작됩니다. 현황을 확인하고 필요한 기능으로 이동하세요.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("분리배출 참여율", "86%", "이번 달 기준")
    col2.metric("분리수거 점수", "82점", "100점 만점")
    col3.metric("처리 대기 신고", str(sum(1 for r in st.session_state.reports if r["상태"] != "처리 완료")), "접수 내역 기준")
    col4.metric("이번 달 안내", "4회", "공용방송 계획")

    st.subheader("기능 바로가기")
    st.caption("원하는 기능을 선택하면 해당 페이지로 이동합니다.")
    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="feature-note"><h4>⏰ Trash Alarm</h4><p>분리수거 요일과 배출 시간을 확인하고, 배출일을 놓치지 않도록 안내합니다.</p></div>', unsafe_allow_html=True)
        if st.button("Trash Alarm 열기", use_container_width=True):
            go("Trash Alarm"); st.rerun()
    with b:
        st.markdown('<div class="feature-note"><h4>🏆 분리수거 점수제</h4><p>동별 분리배출 참여 점수를 확인하고 올바른 분리수거를 독려합니다.</p></div>', unsafe_allow_html=True)
        if st.button("분리수거 점수제 열기", use_container_width=True):
            go("분리수거 점수제"); st.rerun()
    with c:
        st.markdown('<div class="feature-note"><h4>📢 의식개선 공용방송</h4><p>분리배출 방법과 자주 발생하는 실수를 공용방송 문구로 안내합니다.</p></div>', unsafe_allow_html=True)
        if st.button("공용방송 열기", use_container_width=True):
            go("의식개선 공용방송"); st.rerun()

    st.subheader("아파트 분리수거 현황")
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("#### 품목별 배출 상태")
        st.progress(0.90, text="종이류 · 양호")
        st.progress(0.82, text="플라스틱 · 양호")
        st.progress(0.74, text="캔·금속류 · 보통")
        st.progress(0.68, text="유리병 · 개선 필요")
        st.caption("표시된 수치는 화면 구성을 위한 예시 데이터입니다.")
    with right:
        st.markdown("#### 관리 안내")
        st.info("배출 장소가 넘치거나 분리배출 기준이 지켜지지 않는 경우 신고 페이지를 이용해 주세요.")
        st.warning("사진을 첨부할 때는 사람의 얼굴, 차량 번호 등 개인정보가 나오지 않도록 확인해 주세요.")
        if st.button("🚨 문제 신고하기", type="primary", use_container_width=True):
            go("신고하기"); st.rerun()

    st.subheader("최근 신고 내역")
    if not st.session_state.reports:
        st.write("아직 등록된 신고가 없습니다.")
    else:
        for report in reversed(st.session_state.reports[-3:]):
            with st.container(border=True):
                st.markdown(f"**{report['제목']}** · {status_badge(report['상태'])}")
                st.caption(f"{report['접수 시각']} · 신고 번호 {report['번호']}")
                st.write(report["내용"][:120] + ("…" if len(report["내용"]) > 120 else ""))

# -----------------------------
# Trash Alarm 페이지
# -----------------------------
elif page == "Trash Alarm":
    st.title("⏰ Trash Alarm")
    st.write("분리수거 일정과 배출 전 확인 사항을 안내하는 페이지입니다.")
    st.info("아래 일정은 예시입니다. 실제 아파트 관리 규정에 맞게 수정해 사용하세요.")
    schedule = [
        ("월요일", "종이류 · 플라스틱류", "내용물을 비우고 가능한 경우 헹군 뒤 배출"),
        ("수요일", "캔·금속류 · 유리병", "품목별로 나누고 깨지기 쉬운 물품은 안전하게 포장"),
        ("금요일", "비닐류 · 투명 페트병", "투명 페트병은 내용물을 비우고 라벨을 제거"),
    ]
    for day, items, note in schedule:
        with st.container(border=True):
            st.subheader(day)
            st.markdown(f"**배출 품목:** {items}")
            st.write(note)
    st.subheader("배출 전 체크리스트")
    for item in ["내용물을 비웠나요?", "재질에 맞게 분류했나요?", "지정된 장소와 시간을 확인했나요?"]:
        st.checkbox(item, key=f"alarm_{item}")
    if st.button("메인 페이지로 돌아가기"):
        go("메인 페이지"); st.rerun()

# -----------------------------
# 분리수거 점수제 페이지
# -----------------------------
elif page == "분리수거 점수제":
    st.title("🏆 분리수거 점수제")
    st.write("동별 분리배출 참여 현황을 점수로 확인하는 예시 페이지입니다.")
    st.caption("아래 점수는 실제 측정값이 아닌 시연용 예시입니다.")
    scores = [
        ("101동", 91, "우수"),
        ("102동", 85, "양호"),
        ("103동", 78, "보통"),
        ("104동", 72, "개선 필요"),
    ]
    for building, score, label in scores:
        c1, c2, c3 = st.columns([1, 3, 1])
        c1.markdown(f"**{building}**")
        c2.progress(score / 100, text=f"{score}점")
        c3.write(label)
    st.subheader("점수 높이는 방법")
    st.markdown("""
    - 재활용품의 내용물을 비우고 오염을 줄이기
    - 종이, 플라스틱, 캔, 유리 등을 종류별로 분류하기
    - 배출 장소 주변을 깨끗하게 이용하기
    - 분리배출이 어려운 품목은 관리사무소 안내 확인하기
    """)
    if st.button("메인 페이지로 돌아가기"):
        go("메인 페이지"); st.rerun()

# -----------------------------
# 의식개선 공용방송 페이지
# -----------------------------
elif page == "의식개선 공용방송":
    st.title("📢 의식개선 공용방송")
    st.write("주민에게 올바른 분리배출 방법을 알리는 공용방송 문구 예시입니다.")
    announcements = {
        "기본 안내": "주민 여러분, 깨끗한 아파트 환경을 위해 분리배출 시 재활용품의 내용물을 비우고 종류별로 분리해 주시기 바랍니다. 지정된 배출 장소와 시간을 지켜 주셔서 감사합니다.",
        "투명 페트병 안내": "투명 페트병은 내용물을 비우고 라벨을 제거한 뒤 지정된 수거함에 배출해 주세요. 올바른 분리배출이 자원 재활용에 도움이 됩니다.",
        "배출 장소 정리": "분리수거장 이용 후에는 주변을 정리해 주시고, 재활용품을 수거함 밖에 두지 않도록 협조 부탁드립니다. 쾌적한 공동생활을 위해 주민 여러분의 참여를 부탁드립니다.",
    }
    chosen = st.selectbox("방송 문구 선택", list(announcements.keys()))
    st.text_area("방송 문구", value=announcements[chosen], height=180, key="broadcast_text")
    st.caption("필요한 경우 문구를 수정해 관리사무소 안내에 맞게 활용하세요.")
    if st.button("메인 페이지로 돌아가기"):
        go("메인 페이지"); st.rerun()

# -----------------------------
# 신고하기 페이지
# -----------------------------
elif page == "신고하기":
    st.title("🚨 분리수거 문제 신고")
    st.write("분리수거장 혼잡, 재활용품 오배출, 시설 파손 등 문제를 신고할 수 있습니다.")
    tab_report, tab_history = st.tabs(["📝 신고하기", "📋 신고내역"])

    with tab_report:
        with st.form("report_form", clear_on_submit=True):
            title = st.text_input("신고 제목", placeholder="예: 103동 분리수거장에 재활용품이 쌓여 있어요")
            category = st.selectbox("신고 유형", [
                "분리배출 오류", "수거함 넘침", "시설 파손", "악취·청결 문제", "기타"
            ])
            location = st.selectbox("위치", [
                "101동", "102동", "103동", "104동", "공용 분리수거장", "기타 위치"
            ])
            uploaded_photo = st.file_uploader(
                "사진 첨부 (선택)", type=["png", "jpg", "jpeg", "webp"],
                help="PNG, JPG, JPEG, WEBP 파일을 첨부할 수 있습니다."
            )
            content = st.text_area(
                "신고 내용", placeholder="어떤 문제가 발생했는지 자세히 작성해 주세요.",
                height=140
            )
            submitted = st.form_submit_button("신고 접수하기", type="primary", use_container_width=True)

        if submitted:
            if not title.strip():
                st.error("신고 제목을 입력해 주세요.")
            elif not content.strip():
                st.error("신고 내용을 입력해 주세요.")
            else:
                photo_bytes = None
                photo_name = None
                if uploaded_photo is not None:
                    try:
                        photo_bytes = uploaded_photo.getvalue()
                        photo_name = uploaded_photo.name
                    except Exception:
                        photo_bytes = None
                        photo_name = None

                report = {
                    "번호": str(uuid.uuid4())[:8].upper(),
                    "접수 시각": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "제목": title.strip(),
                    "유형": category,
                    "위치": location,
                    "내용": content.strip(),
                    "상태": "접수",
                    "사진 이름": photo_name,
                    "사진 데이터": photo_bytes,
                }
                st.session_state.reports.append(report)
                st.success("신고가 접수되었습니다. '신고내역' 탭에서 확인할 수 있습니다.")
                if photo_name:
                    st.caption(f"첨부 사진: {photo_name}")
                st.rerun()

    with tab_history:
        reports = list(reversed(st.session_state.reports))
        if not reports:
            st.info("아직 신고 내역이 없습니다. '신고하기' 탭에서 첫 신고를 등록해 보세요.")
        else:
            st.caption(f"총 {len(reports)}건의 신고가 있습니다. (현재 세션 기준)")
            filter_status = st.selectbox("상태별 보기", ["전체", "접수", "확인 중", "처리 완료"])
            filtered = reports if filter_status == "전체" else [r for r in reports if r["상태"] == filter_status]
            for report in filtered:
                with st.container(border=True):
                    top1, top2 = st.columns([3, 1])
                    top1.markdown(f"### {report['제목']}")
                    top2.markdown(f"**{status_badge(report['상태'])}**")
                    st.caption(
                        f"신고 번호: {report['번호']} · {report['접수 시각']} · "
                        f"유형: {report['유형']} · 위치: {report['위치']}"
                    )
                    st.write(report["내용"])
                    if report.get("사진 데이터"):
                        try:
                            st.image(report["사진 데이터"], caption=report.get("사진 이름", "첨부 사진"), width=360)
                        except Exception:
                            st.caption("첨부 사진을 표시할 수 없습니다.")
                    status_options = ["접수", "확인 중", "처리 완료"]
                    current_status = report["상태"]
                    new_status = st.selectbox(
                        "신고 상태 변경",
                        status_options,
                        index=status_options.index(current_status),
                        key=f"status_{report['번호']}"
                    )
                    if new_status != current_status:
                        for saved in st.session_state.reports:
                            if saved["번호"] == report["번호"]:
                                saved["상태"] = new_status
                        st.rerun()

    st.warning("주의: 이 앱은 시연용입니다. 세션이 끝나거나 앱이 재시작되면 신고 내역과 첨부 사진이 유지되지 않을 수 있습니다. 실제 운영에는 데이터베이스와 접근 권한 관리가 필요합니다.")

else:
    st.error("페이지를 찾을 수 없습니다.")
    if st.button("메인 페이지로 이동"):
        go("메인 페이지")
        st.rerun()

st.divider()
st.caption("♻️ 그린 아파트 · 분리수거 관리 시연 앱")
