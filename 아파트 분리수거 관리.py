import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(page_title="아파트 분리수거 관리", page_icon="♻️", layout="wide", initial_sidebar_state="expanded")

# 이 앱은 메인 화면만 디자인합니다. 사이드바는 기본 상태로 유지합니다.
# 신고 기능은 메인 화면의 버튼과 신고 페이지 양쪽에서 접근할 수 있습니다.
if "page" not in st.session_state:
    st.session_state.page = "메인 페이지"
if "reports" not in st.session_state:
    st.session_state.reports = []

def go(page):
    st.session_state.page = page

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Noto Sans KR',sans-serif}
.stApp{background:#fff;color:#26342d}
.block-container{max-width:1200px;padding-top:1rem}
.hero{min-height:310px;display:flex;flex-direction:column;justify-content:center;padding:45px 7%;color:#fff;background:linear-gradient(90deg,rgba(12,37,53,.72),rgba(12,37,53,.12)),url('https://images.unsplash.com/photo-1449844908441-8829872d2607?auto=format&fit=crop&w=2000&q=85') center/cover}
.hero .eyebrow{font-size:11px;letter-spacing:3px;margin-bottom:13px;color:#eaf4f6}
.hero h1{color:#fff;font-size:clamp(30px,4.5vw,48px);line-height:1.12;margin:0;font-weight:800}
.hero p{color:#f3f7f8;font-size:13px;line-height:1.9;max-width:440px;margin-top:15px}
.environment{margin:0 -1rem 40px;padding:30px 7%;min-height:220px;display:flex;align-items:center;background:linear-gradient(110deg,#079ba4 0%,#0ba5ad 57%,#fff 57%,#fff 100%)}
.envtext{color:white;width:44%;padding-right:25px}.envtext h2{color:white;font-size:27px;margin:7px 0}.envtext p{font-size:12px;line-height:1.8;color:#e9ffff}
.envimage{width:56%;height:160px;background:url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1000&q=80') center/cover;box-shadow:0 8px 25px #163b3b22}
.eyebrow2{text-align:center;font-size:10px;letter-spacing:2px;color:#15868a;margin:8px 0}
.title{text-align:center;font-size:24px;font-weight:700;margin:0 0 7px;color:#26342d}.subtitle{text-align:center;font-size:12px;color:#77817a;margin-bottom:23px}
.stat{background:#fff;border:1px solid #e3ece7;border-radius:4px;padding:17px 18px;min-height:108px}
.label{font-size:12px;color:#68766d}.value{font-size:27px;font-weight:700;color:#176d4b;margin-top:5px}.note{font-size:10px;color:#15834c;margin-top:3px}
.card,.news{border:1px solid #e2eae5;padding:18px;background:#fff;height:100%}.icon{font-size:23px;color:#168b80}.card h3{font-size:16px;margin:8px 0}.card p,.news p{font-size:12px;color:#77817a;line-height:1.8}.tag{font-size:10px;color:#12868a;letter-spacing:1px;font-weight:700}.news h4{font-size:15px;margin:9px 0}
.footer1{background:#28734c;color:#fff;text-align:center;padding:15px;font-size:11px;letter-spacing:1px;margin-top:45px}.footer2{background:#1d3027;color:#dce7df;padding:26px 5%;font-size:11px;line-height:2}
.stButton>button[kind="primary"]{background:#19734b;border-color:#19734b;color:white}
@media(max-width:700px){.hero{min-height:250px;padding:30px 7%}.environment{margin:0 0 30px;padding:22px 5%;background:#079ba4;display:block}.envtext,.envimage{width:100%}.envimage{margin-top:18px;height:135px}.title{font-size:21px}}
</style>
""", unsafe_allow_html=True)

# Sidebar page links (if this is used as a standalone app); normal Streamlit sidebar is not hidden.
with st.sidebar:
    st.markdown("## ♻️ 그린 아파트")
    st.caption("분리수거 관리 시스템")
    if st.button("메인 페이지", use_container_width=True):
        go("메인 페이지")
    if st.button("신고하기", use_container_width=True):
        go("신고하기")
    st.divider()
    st.caption("※ 시연용 앱이며 신고 데이터는 세션에 임시 저장됩니다.")

if st.session_state.page == "메인 페이지":
    st.markdown("""
    <section class="hero">
     <div class="eyebrow">SAMPLE PREMIUM · GREEN APARTMENT</div>
     <h1>We Execute<br>Your Green Vision</h1>
     <p>올바른 분리배출과 주민 참여로 더 쾌적한 아파트를 만듭니다.<br>작은 실천이 지속 가능한 환경으로 이어집니다.</p>
    </section>
    <section class="environment">
     <div class="envtext"><div style="font-size:10px;letter-spacing:2px">모든 세대를 위한 환경 프로젝트</div>
     <h2>Environment</h2><h3 style="color:white;font-size:17px;margin:0">깨끗한 우리 아파트</h3>
     <p>분리배출 현황을 확인하고 올바른 배출 습관을 함께 만들어 갑니다.</p></div>
     <div class="envimage"></div>
    </section>
    <div class="eyebrow2">GREEN LIFE · STATUS</div><div class="title">우리 아파트 분리수거 현황</div>
    <div class="subtitle">깨끗한 공동주택은 올바른 분리배출에서 시작됩니다.</div>
    """, unsafe_allow_html=True)

    pending = sum(1 for r in st.session_state.reports if r.get("상태") != "처리 완료")
    cols = st.columns(4)
    for col, label, value, note in zip(cols,
        ["분리배출 참여율","분리수거 점수","처리 대기 신고","이번 달 안내"],
        ["86%","82점",f"{pending}건","4회"],
        ["이번 달 기준 · 예시","100점 만점 · 예시","접수 내역 기준","공용방송 계획 · 예시"]):
        with col:
            st.markdown(f'<div class="stat"><div class="label">{label}</div><div class="value">{value}</div><div class="note">↑ {note}</div></div>',unsafe_allow_html=True)

    st.markdown('<div style="height:35px"></div><div class="eyebrow2">OUR SERVICE</div><div class="title">주민을 위한 분리수거 서비스</div><div class="subtitle">왼쪽 사이드바에서 기존 기능 페이지를 선택할 수 있습니다.</div>',unsafe_allow_html=True)
    cols=st.columns(3)
    for col,icon,title,desc in zip(cols,["♻️","🏆","📢"],["Trash Alarm","분리수거 점수제","의식개선 공용방송"],["분리수거 일정과 배출 전 체크리스트를 확인합니다.","동별 분리배출 참여 점수와 실천 방법을 확인합니다.","주민에게 안내할 분리배출 방송 문구를 확인합니다."]):
        with col: st.markdown(f'<div class="card"><div class="icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)

    st.markdown('<div style="height:35px"></div><div class="eyebrow2">GREEN NEWS</div><div class="title">깨끗한 아파트를 위한 안내</div><div class="subtitle">오늘의 올바른 분리배출 실천</div>',unsafe_allow_html=True)
    n1,n2=st.columns(2)
    with n1: st.markdown('<div class="news"><div class="tag">SEPARATION GUIDE</div><h4>재활용품은 비우고, 헹구고, 분리해 주세요</h4><p>내용물을 비우고 이물질을 제거한 뒤 재질에 맞게 분류하면 자원 재활용에 도움이 됩니다.</p></div>',unsafe_allow_html=True)
    with n2: st.markdown('<div class="news"><div class="tag">RESIDENT NOTICE</div><h4>분리수거장 이용 후 주변을 정리해 주세요</h4><p>수거함 밖에 재활용품을 두지 말고 지정된 장소와 배출 안내를 확인해 주세요.</p></div>',unsafe_allow_html=True)

    st.markdown('<div style="height:32px"></div>',unsafe_allow_html=True)
    left,right=st.columns(2)
    with left:
        st.markdown("### 품목별 배출 상태")
        st.progress(.90,text="종이류 · 양호");st.progress(.82,text="플라스틱류 · 양호");st.progress(.74,text="캔·금속류 · 보통");st.progress(.68,text="유리병 · 개선 필요")
    with right:
        st.markdown("### 관리 안내")
        st.info("분리수거장 넘침, 오배출, 시설 파손 등은 신고 페이지에서 등록할 수 있습니다.")
        if st.button("🚨 문제 신고하기", type="primary", use_container_width=True):
            go("신고하기")
            st.rerun()
        st.caption("참여율과 점수는 디자인 시연을 위한 예시 값입니다.")

    st.markdown('<div class="footer1">SAMPLE PREMIUM · GREEN APARTMENT LIFE</div><div class="footer2"><b>♻ GREEN LIFE</b><br>주민과 함께 만드는 쾌적한 공동주택 환경<br><br>분리수거 관리 시연 웹사이트 · 현황 지표는 예시 데이터입니다.</div>',unsafe_allow_html=True)

elif st.session_state.page == "신고하기":
    st.markdown('<div class="eyebrow2">RESIDENT SERVICE</div><div class="title">분리수거 문제 신고하기</div><div class="subtitle">불편 사항을 사진과 함께 알려주세요.</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["신고하기", "신고 내역"])
    with tab1:
        with st.form("report_form", clear_on_submit=True):
            title = st.text_input("신고 제목", placeholder="예: 103동 분리수거장이 가득 찼어요")
            c1,c2 = st.columns(2)
            with c1:
                category = st.selectbox("신고 유형", ["분리배출 오류","수거함 넘침","시설 파손","악취·청결 문제","기타"])
            with c2:
                location = st.selectbox("위치", ["101동","102동","103동","104동","공용 분리수거장","기타 위치"])
            photo = st.file_uploader("사진 첨부 (선택)", type=["png","jpg","jpeg","webp"])
            content = st.text_area("신고 내용", placeholder="발생한 문제와 위치를 자세히 작성해 주세요.", height=140)
            submitted = st.form_submit_button("신고 접수하기", type="primary", use_container_width=True)
        if submitted:
            if not title.strip():
                st.error("신고 제목을 입력해 주세요.")
            elif not content.strip():
                st.error("신고 내용을 입력해 주세요.")
            else:
                photo_bytes, photo_name = None, None
                if photo is not None:
                    try:
                        photo_bytes, photo_name = photo.getvalue(), photo.name
                    except Exception:
                        st.error("사진 파일을 읽을 수 없습니다. 다시 선택해 주세요.")
                        st.stop()
                st.session_state.reports.append({
                    "번호": str(uuid.uuid4())[:8].upper(),
                    "접수 시각": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "제목": title.strip(), "유형": category, "위치": location,
                    "내용": content.strip(), "상태": "접수",
                    "사진 이름": photo_name, "사진 데이터": photo_bytes
                })
                st.success("신고가 접수되었습니다. ‘신고 내역’에서 확인할 수 있습니다.")
                st.rerun()
    with tab2:
        reports = list(reversed(st.session_state.reports))
        if not reports:
            st.info("아직 등록된 신고가 없습니다.")
        else:
            st.caption(f"총 {len(reports)}건")
            state_filter = st.selectbox("상태별 보기", ["전체","접수","확인 중","처리 완료"])
            for report in reports:
                if state_filter != "전체" and report["상태"] != state_filter:
                    continue
                with st.container(border=True):
                    p1,p2 = st.columns([3,1])
                    p1.markdown(f"#### {report['제목']}")
                    p2.markdown(f"**상태: {report['상태']}**")
                    st.caption(f"{report['번호']} · {report['접수 시각']} · {report['유형']} · {report['위치']}")
                    st.write(report["내용"])
                    if report.get("사진 데이터"):
                        try:
                            st.image(report["사진 데이터"], caption=report.get("사진 이름") or "첨부 사진", width=360)
                        except Exception:
                            st.caption("첨부 사진을 표시할 수 없습니다.")
                    new_state = st.selectbox("신고 상태 변경", ["접수","확인 중","처리 완료"], index=["접수","확인 중","처리 완료"].index(report["상태"]), key=f"state_{report['번호']}")
                    if new_state != report["상태"]:
                        for saved in st.session_state.reports:
                            if saved["번호"] == report["번호"]:
                                saved["상태"] = new_state
                        st.rerun()
    st.warning("시연용 저장 방식입니다. 앱 세션이 종료되거나 재시작되면 신고 내역이 유지되지 않을 수 있습니다.")
    if st.button("← 메인 페이지로 돌아가기"):
        go("메인 페이지")
        st.rerun()

else:
    go("메인 페이지")
    st.rerun()
