import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(page_title="GREEN LIFE | 아파트 분리수거", page_icon="♻️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Noto Sans KR',sans-serif}
.stApp{background:#fff;color:#202923}
.block-container{max-width:1180px;padding-top:.5rem;padding-bottom:0}
[data-testid="stSidebar"]{display:none}
div[data-testid="stToolbar"]{visibility:hidden}
.brand{font-size:19px;font-weight:800;letter-spacing:1px;color:#244d38;padding:12px 0}
.brand span{font-weight:400;color:#789783}
.nav-label{text-align:center;font-size:12px;color:#49534c;padding-top:16px}
.hero{min-height:330px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;color:white;padding:45px 20px;background:linear-gradient(90deg,rgba(12,35,30,.62),rgba(12,35,30,.15)),linear-gradient(0deg,rgba(10,30,22,.25),transparent),url('https://images.unsplash.com/photo-1511818966892-d7d671e672a2?auto=format&fit=crop&w=2000&q=85');background-size:cover;background-position:center 52%;margin:0 -4rem}
.hero-kicker{font-size:11px;letter-spacing:4px;margin-bottom:12px}
.hero h1{color:white;font-size:clamp(32px,5vw,52px);font-weight:600;letter-spacing:-1px;margin:0}
.hero p{color:#f4f7f4;font-size:14px;line-height:1.9;margin-top:14px}
.quick{background:#fff;border:1px solid #edf0ed;box-shadow:0 8px 25px #1c372012;padding:16px;margin:-25px 0 40px;position:relative}
.metric{background:#fbfcfb;border:1px solid #e8eee9;padding:15px;min-height:100px}
.mlabel{font-size:12px;color:#758078}.mvalue{font-size:25px;font-weight:700;color:#2c6847}.mnote{font-size:10px;color:#929a94}
.kicker{text-align:center;font-size:10px;letter-spacing:2px;color:#66816d;margin-bottom:8px}
.stitle{text-align:center;font-size:25px;font-weight:700;letter-spacing:-.7px;margin-bottom:8px;color:#252d27}
.subtitle{text-align:center;color:#7a817c;font-size:12px;margin-bottom:24px}
.rule{height:2px;background:#2e6848;margin:14px 0 22px}
.card{border:1px solid #e8ece8;padding:20px 18px;min-height:150px;background:white}
.icon{font-size:25px;color:#2e6848;margin-bottom:10px}.card h3{font-size:16px;margin:0 0 9px}.card p{font-size:12px;line-height:1.8;color:#788078;min-height:43px}
.news{border:1px solid #edf0ed;padding:20px;height:100%;background:white}.tag{color:#2f6b49;font-size:10px;letter-spacing:1px;font-weight:700}.news h4{font-size:15px;margin:9px 0}.news p{font-size:12px;color:#7b837d;line-height:1.7}
.footerbar{background:#2e6848;color:white;padding:16px;text-align:center;font-size:11px;letter-spacing:1px;margin-top:48px}
.footermain{background:#1e3027;color:#dfe8e1;padding:28px 5%;font-size:11px;line-height:2}
.stButton>button{border-radius:2px;border:1px solid #d9e2db;font-size:12px;min-height:42px}
.stButton>button[kind="primary"]{background:#2e6848;border-color:#2e6848;color:white}
div[data-testid="stMetric"]{border:1px solid #e8eee9;border-radius:0;background:#fbfcfb}
@media(max-width:700px){.hero{min-height:260px;margin:0 -1rem}.stitle{font-size:21px}.quick{margin-top:-18px}}
</style>
""", unsafe_allow_html=True)

if "reports" not in st.session_state: st.session_state.reports = []
if "page" not in st.session_state: st.session_state.page = "메인 페이지"
def go(page):
    st.session_state.page = page
def status_label(s):
    return {"접수":"🟡 접수","확인 중":"🔵 확인 중","처리 완료":"🟢 처리 완료"}.get(s,s)

a,b = st.columns([1.5, 5], vertical_alignment="center")
with a:
    st.markdown('<div class="brand">◧ GREEN <span>LIFE</span></div>',unsafe_allow_html=True)
with b:
    nav_cols = st.columns(5)
    nav_items = [
        ("메인 페이지", "메인 페이지"),
        ("Trash Alarm", "Trash Alarm"),
        ("분리수거 점수제", "분리수거 점수제"),
        ("의식개선 공용방송", "의식개선 공용방송"),
        ("신고하기", "신고하기"),
    ]
    for col, (label, target) in zip(nav_cols, nav_items):
        with col:
            if st.button(label, key=f"topnav_{target}", type="primary" if st.session_state.page == target else "secondary", use_container_width=True):
                go(target)
                st.rerun()
st.markdown('<div style="height:1px;background:#eee"></div>',unsafe_allow_html=True)

if st.session_state.page == "메인 페이지":
    st.markdown("""<section class="hero"><div class="hero-kicker">GREEN APARTMENT · BETTER TOMORROW</div><h1>Enjoy Green Life</h1><p>올바른 분리배출로 완성하는 쾌적한 주거 환경<br>우리 아파트의 작은 실천이 더 나은 내일을 만듭니다.</p></section>""",unsafe_allow_html=True)
    st.markdown('<div class="quick">',unsafe_allow_html=True)
    cols=st.columns(4)
    metrics=[("분리배출 참여율","86%","이번 달 기준 · 예시"),("환경 관리 점수","82점","100점 만점 · 예시"),("미처리 신고",f"{sum(1 for r in st.session_state.reports if r['상태']!='처리 완료')}건","접수 내역 기준"),("환경 안내","04회","월간 안내 계획 · 예시")]
    for col,(label,value,note) in zip(cols,metrics):
        with col: st.markdown(f'<div class="metric"><div class="mlabel">{label}</div><div class="mvalue">{value}</div><div class="mnote">{note}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="kicker">OUR APARTMENT</div><div class="stitle">우리 아파트가 선보이는 그린 라이프</div><div class="subtitle">함께 지키는 분리배출, 함께 누리는 깨끗한 공간</div><div class="rule"></div>',unsafe_allow_html=True)
    cols=st.columns(3)
    cards=[("♻","분리수거 현황","품목별 배출 상태와 아파트 환경 관리 지표를 한눈에 확인합니다."),("⌂","주민 참여 안내","올바른 분리배출 방법을 확인하고 생활 속 환경 실천에 참여합니다."),("✉","불편 사항 신고","수거함 넘침, 오배출, 시설 파손 등을 사진과 함께 간편하게 신고합니다.")]
    for i,(col,(icon,title,desc)) in enumerate(zip(cols,cards)):
        with col:
            st.markdown(f'<div class="card"><div class="icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
            if i==2:
                if st.button("신고 페이지 바로가기 →",key="report_link",use_container_width=True): go("신고하기"); st.rerun()
            else: st.button("안내 확인",key=f"guide{i}",disabled=True,use_container_width=True)
    st.markdown('<div style="height:38px"></div><div class="kicker">GREEN NEWS</div><div class="stitle">깨끗한 아파트를 위한 안내</div><div class="subtitle">작은 습관이 만드는 큰 변화</div>',unsafe_allow_html=True)
    n1,n2=st.columns(2)
    with n1: st.markdown('<div class="news"><div class="tag">SEPARATION GUIDE</div><h4>재활용품, 비우고 헹구고 분리해 주세요</h4><p>내용물을 비우고 이물질을 제거한 뒤 재질에 맞게 분류하면 재활용에 도움이 됩니다.</p></div>',unsafe_allow_html=True)
    with n2: st.markdown('<div class="news"><div class="tag">RESIDENT NOTICE</div><h4>분리수거장 이용 후 주변을 정리해 주세요</h4><p>수거함 밖에 재활용품을 두지 말고 지정된 장소와 배출 안내를 확인해 주세요.</p></div>',unsafe_allow_html=True)
    st.markdown('<div style="height:36px"></div><div class="kicker">CURRENT STATUS</div><div class="stitle">아파트 분리수거 현황</div><div class="subtitle">품목별 상태는 화면 구성을 위한 예시 데이터입니다.</div><div class="rule"></div>',unsafe_allow_html=True)
    left,right=st.columns([1.1,1])
    with left:
        st.markdown("**품목별 배출 상태**")
        st.progress(.90,text="종이류 · 양호"); st.progress(.82,text="플라스틱류 · 양호"); st.progress(.74,text="캔·금속류 · 보통"); st.progress(.68,text="유리병 · 개선 필요")
    with right:
        st.markdown("**함께 만드는 깨끗한 분리수거장**")
        st.write("배출 장소가 넘치거나 분리배출 기준이 지켜지지 않는 경우 신고 페이지를 이용해 주세요.")
        st.warning("사진 첨부 전 사람의 얼굴이나 차량 번호 등 개인정보가 포함되어 있지 않은지 확인해 주세요.")
        if st.button("문제 신고하기",type="primary",use_container_width=True): go("신고하기"); st.rerun()
    st.markdown('<div class="footerbar">GREEN LIFE　·　환경을 생각하는 아파트 관리</div><div class="footermain"><b>◧ GREEN LIFE</b><br>주민과 함께 만드는 쾌적한 공동주택 환경<br><br>분리수거 관리 시연 웹사이트 · 현황 지표는 예시 데이터입니다.</div>',unsafe_allow_html=True)

elif st.session_state.page == "Trash Alarm":
    st.markdown('<div class="kicker">SCHEDULE & REMINDER</div><div class="stitle">Trash Alarm</div><div class="subtitle">분리수거 일정과 배출 전 확인 사항을 안내합니다.</div><div class="rule"></div>', unsafe_allow_html=True)
    st.info("아래 일정은 예시입니다. 실제 아파트 관리 규정에 맞게 수정해 사용하세요.")
    schedule = [
        ("월요일", "종이류 · 플라스틱류", "내용물을 비우고 가능한 경우 헹군 뒤 배출해 주세요."),
        ("수요일", "캔·금속류 · 유리병", "품목별로 나누고 깨지기 쉬운 물품은 안전하게 포장해 주세요."),
        ("금요일", "비닐류 · 투명 페트병", "투명 페트병은 내용물을 비우고 라벨을 제거해 주세요."),
    ]
    for day, items, note in schedule:
        with st.container(border=True):
            st.markdown(f"### {day}")
            st.markdown(f"**배출 품목:** {items}")
            st.write(note)
    st.subheader("배출 전 체크리스트")
    for item in ["내용물을 비웠나요?", "재질에 맞게 분류했나요?", "지정된 장소와 시간을 확인했나요?"]:
        st.checkbox(item, key=f"check_{item}")

elif st.session_state.page == "분리수거 점수제":
    st.markdown('<div class="kicker">RECYCLING SCORE</div><div class="stitle">분리수거 점수제</div><div class="subtitle">동별 분리배출 참여 현황을 확인합니다.</div><div class="rule"></div>', unsafe_allow_html=True)
    st.caption("아래 점수는 화면 구성을 위한 예시 데이터입니다.")
    for building, score, label in [("101동", 91, "우수"), ("102동", 85, "양호"), ("103동", 78, "보통"), ("104동", 72, "개선 필요")]:
        c1, c2, c3 = st.columns([1, 3, 1])
        c1.markdown(f"**{building}**")
        c2.progress(score / 100, text=f"{score}점")
        c3.write(label)
    st.subheader("점수를 높이는 분리배출 방법")
    st.markdown("""
    - 재활용품의 내용물을 비우고 오염을 줄이기
    - 종이, 플라스틱, 캔, 유리 등을 종류별로 분류하기
    - 배출 장소 주변을 깨끗하게 이용하기
    - 분리배출이 어려운 품목은 관리사무소 안내 확인하기
    """)

elif st.session_state.page == "의식개선 공용방송":
    st.markdown('<div class="kicker">RESIDENT ANNOUNCEMENT</div><div class="stitle">의식개선 공용방송</div><div class="subtitle">주민에게 올바른 분리배출 방법을 안내하는 방송 문구입니다.</div><div class="rule"></div>', unsafe_allow_html=True)
    announcements = {
        "기본 안내": "주민 여러분, 깨끗한 아파트 환경을 위해 분리배출 시 재활용품의 내용물을 비우고 종류별로 분리해 주시기 바랍니다. 지정된 배출 장소와 시간을 지켜 주셔서 감사합니다.",
        "투명 페트병 안내": "투명 페트병은 내용물을 비우고 라벨을 제거한 뒤 지정된 수거함에 배출해 주세요. 올바른 분리배출이 자원 재활용에 도움이 됩니다.",
        "배출 장소 정리": "분리수거장 이용 후에는 주변을 정리해 주시고, 재활용품을 수거함 밖에 두지 않도록 협조 부탁드립니다. 쾌적한 공동생활을 위해 주민 여러분의 참여를 부탁드립니다.",
    }
    chosen = st.selectbox("방송 문구 선택", list(announcements.keys()))
    st.text_area("방송 문구", value=announcements[chosen], height=180, key="announcement_text")
    st.caption("문구를 필요에 맞게 수정해 관리사무소 안내에 활용할 수 있습니다.")

elif st.session_state.page == "신고하기":
    st.markdown("""<section class="hero" style="min-height:220px"><div class="hero-kicker">RESIDENT SERVICE</div><h1>Report a Concern</h1><p>분리수거장 문제를 알려주세요.<br>주민의 신고가 더 깨끗한 아파트를 만듭니다.</p></section>""",unsafe_allow_html=True)
    st.markdown('<div style="height:28px"></div><div class="kicker">CUSTOMER SERVICE</div><div class="stitle">신고하기</div><div class="subtitle">문제 내용을 작성하고 필요한 경우 사진을 첨부해 주세요.</div>',unsafe_allow_html=True)
    tab1,tab2=st.tabs(["신고 접수","신고 내역"])
    with tab1:
        with st.form("report_form",clear_on_submit=True):
            title=st.text_input("신고 제목",placeholder="예: 103동 분리수거장 수거함이 가득 찼어요")
            c1,c2=st.columns(2)
            with c1: category=st.selectbox("신고 유형",["분리배출 오류","수거함 넘침","시설 파손","악취·청결 문제","기타"])
            with c2: location=st.selectbox("위치",["101동","102동","103동","104동","공용 분리수거장","기타 위치"])
            photo=st.file_uploader("사진 첨부 (선택)",type=["png","jpg","jpeg","webp"])
            content=st.text_area("신고 내용",placeholder="발생한 문제와 위치를 자세히 작성해 주세요.",height=145)
            submitted=st.form_submit_button("신고 접수하기",type="primary",use_container_width=True)
        if submitted:
            if not title.strip(): st.error("신고 제목을 입력해 주세요.")
            elif not content.strip(): st.error("신고 내용을 입력해 주세요.")
            else:
                pdata,pname=None,None
                if photo is not None:
                    try: pdata,pname=photo.getvalue(),photo.name
                    except Exception: st.error("사진을 읽을 수 없습니다. 다른 파일을 선택해 주세요.")
                st.session_state.reports.append({"번호":str(uuid.uuid4())[:8].upper(),"접수 시각":datetime.now().strftime("%Y-%m-%d %H:%M"),"제목":title.strip(),"유형":category,"위치":location,"내용":content.strip(),"상태":"접수","사진 이름":pname,"사진 데이터":pdata})
                st.success("신고가 접수되었습니다. 신고 내역 탭에서 확인할 수 있습니다."); st.rerun()
    with tab2:
        reports=list(reversed(st.session_state.reports))
        if not reports: st.info("아직 등록된 신고가 없습니다.")
        else:
            st.caption(f"총 {len(reports)}건의 신고 · 현재 세션 기준")
            filt=st.selectbox("상태별 보기",["전체","접수","확인 중","처리 완료"])
            for r in reports:
                if filt!="전체" and r["상태"]!=filt: continue
                with st.container(border=True):
                    p1,p2=st.columns([3,1])
                    p1.markdown(f"#### {r['제목']}"); p2.markdown(f"**{status_label(r['상태'])}**")
                    st.caption(f"신고 번호: {r['번호']} · {r['접수 시각']} · {r['유형']} · {r['위치']}")
                    st.write(r["내용"])
                    if r.get("사진 데이터"):
                        try: st.image(r["사진 데이터"],caption=r.get("사진 이름","첨부 사진"),width=360)
                        except Exception: st.caption("첨부 사진을 표시할 수 없습니다.")
                    options=["접수","확인 중","처리 완료"]
                    new=st.selectbox("신고 상태 변경",options,index=options.index(r["상태"]),key=f"status_{r['번호']}")
                    if new!=r["상태"]:
                        for saved in st.session_state.reports:
                            if saved["번호"]==r["번호"]: saved["상태"]=new
                        st.rerun()
    st.warning("시연용 앱입니다. 신고 내역과 사진은 세션에 임시 저장되므로 앱 재시작 후 유지되지 않을 수 있습니다.")
    st.markdown('<div class="footerbar">GREEN LIFE　·　주민 신고 센터</div><div class="footermain"><b>◧ GREEN LIFE</b><br>더 나은 주거 환경을 위해 의견을 보내주세요.</div>',unsafe_allow_html=True)
    if st.button("← 메인 페이지로 돌아가기"): go("메인 페이지"); st.rerun()
else:
    go("메인 페이지")
    st.rerun()
