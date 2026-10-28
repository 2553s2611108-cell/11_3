import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Trash Alarm | 현장 관제",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 수거함 규칙: 실제 아파트 기준에 맞게 수정하세요.
# ============================================================
BIN_RULES = {
    "플라스틱": {"icon": "🧴", "accepted": {"플라스틱 페트병", "플라스틱 용기", "플라스틱 포장재"}, "color": "#3978F6"},
    "종이": {"icon": "📦", "accepted": {"신문·종이", "종이 상자", "종이 포장재"}, "color": "#B7791F"},
    "캔·고철": {"icon": "🥫", "accepted": {"음료 캔", "철제 캔", "고철"}, "color": "#64748B"},
    "유리": {"icon": "🍾", "accepted": {"유리병"}, "color": "#0F766E"},
    "음식물": {"icon": "🍎", "accepted": {"음식물 쓰레기"}, "color": "#16A34A"},
    "일반쓰레기": {"icon": "🗑️", "accepted": {"오염된 휴지", "복합 재질 쓰레기"}, "color": "#6B7280"},
}
TRASH_TYPES = [
    "플라스틱 페트병", "플라스틱 용기", "플라스틱 포장재",
    "신문·종이", "종이 상자", "종이 포장재",
    "음료 캔", "철제 캔", "고철", "유리병",
    "음식물 쓰레기", "오염된 휴지", "복합 재질 쓰레기",
]

if "events" not in st.session_state:
    st.session_state.events = []
if "active_alert" not in st.session_state:
    st.session_state.active_alert = None
if "alarm_enabled" not in st.session_state:
    st.session_state.alarm_enabled = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter','Noto Sans KR',sans-serif; }
.stApp { background:#F3F6F8; color:#172B3A; }
.block-container { max-width:1450px; padding-top:1.25rem; padding-bottom:2.5rem; }
[data-testid="stSidebar"] { background:#102A36; }
[data-testid="stSidebar"] * { color:#EAF2F5 !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { background:rgba(255,255,255,.06); border-radius:10px; padding:7px 10px; }
.topbar { display:flex; justify-content:space-between; align-items:center; gap:16px; padding:20px 24px; background:#102A36; border-radius:18px; color:#fff; margin-bottom:18px; }
.brand { font-size:1.65rem; font-weight:800; letter-spacing:-.5px; }
.subbrand { color:#B8CBD3; font-size:.9rem; margin-top:4px; }
.live-pill { display:inline-block; border:1px solid #2C5D60; background:#163F43; color:#8AF0C2; padding:7px 12px; border-radius:99px; font-size:.82rem; font-weight:700; white-space:nowrap; }
.metric { background:white; border:1px solid #E1E8EC; border-radius:15px; padding:16px 18px; min-height:105px; box-shadow:0 3px 12px rgba(16,42,54,.025); }
.metric-label { color:#71818C; font-size:.82rem; font-weight:600; }
.metric-value { font-size:1.7rem; font-weight:800; color:#152F3C; margin-top:6px; }
.panel { background:white; border:1px solid #E1E8EC; border-radius:16px; padding:19px 20px; margin-bottom:14px; }
.panel-title { color:#193543; font-size:1.05rem; font-weight:800; margin-bottom:3px; }
.panel-sub { color:#7A8992; font-size:.84rem; margin-bottom:14px; }
.bin-card { background:#fff; border:1px solid #E1E8EC; border-radius:14px; padding:15px; min-height:130px; }
.bin-icon { font-size:1.45rem; }
.bin-name { font-size:.95rem; font-weight:800; margin-top:7px; color:#243B48; }
.bin-status { display:inline-block; border-radius:99px; padding:4px 8px; font-size:.74rem; font-weight:700; margin-top:8px; }
.status-ok { background:#E8F7EF; color:#167348; }
.status-alert { background:#FDE8E7; color:#B42318; }
.status-wait { background:#EEF2F5; color:#667782; }
.alert-panel { background:#FFF0EF; border:1px solid #F6C1BD; border-left:6px solid #D92D20; border-radius:15px; padding:18px; }
.ok-panel { background:#EAF8F0; border:1px solid #B8E5C9; border-left:6px solid #12A05C; border-radius:15px; padding:18px; }
.small-muted { color:#778791; font-size:.82rem; }
div.stButton > button { border-radius:10px; min-height:2.7rem; font-weight:700; }
div[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }
hr { border-color:#E3E9ED; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ♻️ TRASH ALARM")
    st.caption("APARTMENT RECYCLING CONTROL")
    st.divider()
    page = st.radio("관제 메뉴", ["현장 관제", "오배출 이력", "배출 기준 설정"], label_visibility="visible")
    st.divider()
    st.markdown("### 시스템 상태")
    if st.session_state.active_alert:
        st.error("ALARM · 확인 필요")
    else:
        st.success("STANDBY · 경보 없음")
    st.caption("현재 연결: 웹 대시보드")
    st.caption("카메라/현장 센서는 별도 연동이 필요합니다.")

events = st.session_state.events
today = datetime.now().date()
today_events = [e for e in events if e["time"].date() == today]
today_wrong = [e for e in today_events if not e["correct"]]
active = st.session_state.active_alert

st.markdown("""
<div class="topbar">
  <div>
    <div class="brand">♻️ Trash Alarm</div>
    <div class="subbrand">공동주택 분리수거장 · 오배출 감지 관제 시스템</div>
  </div>
  <div class="live-pill">● DASHBOARD ONLINE</div>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric"><div class="metric-label">오늘 감지 이벤트</div><div class="metric-value">{len(today_events)} <span style="font-size:.9rem;font-weight:600">건</span></div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric"><div class="metric-label">오늘 오배출</div><div class="metric-value" style="color:#D92D20">{len(today_wrong)} <span style="font-size:.9rem;font-weight:600">건</span></div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric"><div class="metric-label">등록 수거함</div><div class="metric-value">{len(BIN_RULES)} <span style="font-size:.9rem;font-weight:600">개</span></div></div>', unsafe_allow_html=True)
with m4:
    label = "경보 발생" if active else "정상 대기"
    color = "#D92D20" if active else "#16804A"
    st.markdown(f'<div class="metric"><div class="metric-label">경보 시스템</div><div class="metric-value" style="color:{color};font-size:1.35rem">{label}</div></div>', unsafe_allow_html=True)

st.write("")

if page == "현장 관제":
    left, right = st.columns([1.15, .85], gap="medium")
    with left:
        st.markdown('<div class="panel"><div class="panel-title">수거함 상태 모니터링</div><div class="panel-sub">최근 감지 결과를 기준으로 수거함별 상태를 표시합니다.</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, (bin_name, info) in enumerate(BIN_RULES.items()):
            latest_wrong = next((e for e in events if e["bin"] == bin_name and not e["correct"]), None)
            with cols[idx % 3]:
                if active and active["bin"] == bin_name:
                    badge = '<span class="bin-status status-alert">● 경보 발생</span>'
                    note = f"오배출: {active['trash']}"
                elif latest_wrong:
                    badge = '<span class="bin-status status-wait">최근 오배출 이력</span>'
                    note = f"최근: {latest_wrong['trash']}"
                else:
                    badge = '<span class="bin-status status-ok">● 정상 대기</span>'
                    note = "현재 활성 경보 없음"
                st.markdown(
                    f'<div class="bin-card"><div class="bin-icon">{info["icon"]}</div><div class="bin-name">{bin_name} 수거함</div>{badge}<div class="small-muted" style="margin-top:8px">{note}</div></div>',
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel"><div class="panel-title">감지 이벤트 입력</div><div class="panel-sub">현장 장치 연동 전 테스트 또는 관리자가 확인한 감지 결과를 입력합니다.</div>', unsafe_allow_html=True)
        with st.form("event_form", clear_on_submit=False):
            c1, c2 = st.columns(2)
            with c1:
                selected_bin = st.selectbox("감지된 수거함", list(BIN_RULES.keys()))
            with c2:
                selected_trash = st.selectbox("감지된 쓰레기 종류", TRASH_TYPES)
            event_source = st.selectbox("이벤트 출처", ["관리자 확인 입력", "테스트 이벤트"])
            submitted = st.form_submit_button("감지 결과 처리", type="primary", use_container_width=True)
        if submitted:
            correct = selected_trash in BIN_RULES[selected_bin]["accepted"]
            event = {
                "time": datetime.now(),
                "bin": selected_bin,
                "trash": selected_trash,
                "correct": correct,
                "source": event_source,
            }
            st.session_state.events.insert(0, event)
            st.session_state.last_result = event
            if not correct:
                st.session_state.active_alert = {
                    "bin": selected_bin, "trash": selected_trash,
                    "time": event["time"], "source": event_source,
                }
                st.session_state.alarm_enabled = True
            else:
                st.success(f"정상 배출 확인: {selected_trash} → {selected_bin}")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel"><div class="panel-title">🚨 경보 제어 센터</div><div class="panel-sub">오배출 이벤트가 확인되면 경보 상태가 유지됩니다.</div>', unsafe_allow_html=True)
        if active:
            st.markdown(
                f'<div class="alert-panel"><div style="font-size:1.05rem;font-weight:800;color:#A32118">오배출 감지 · 즉시 확인 필요</div>'
                f'<div style="font-size:1.8rem;font-weight:800;color:#8E1D17;margin:12px 0 5px">{active["trash"]}</div>'
                f'<div style="color:#7F2924">감지 수거함: <b>{active["bin"]}</b></div>'
                f'<div style="color:#7F2924">감지 시각: {active["time"].strftime("%Y-%m-%d %H:%M:%S")}</div>'
                f'<div style="color:#7F2924">이벤트 출처: {active.get("source","감지 시스템")}</div></div>',
                unsafe_allow_html=True
            )
            st.write("")
            if st.session_state.alarm_enabled:
                st.error("경보 상태: 활성화")
                if st.button("🔊 경보음 다시 재생", type="primary", use_container_width=True):
                    components.html("""
                    <script>
                    (async function(){
                      try {
                        const C=window.AudioContext||window.webkitAudioContext;
                        const c=new C(); await c.resume();
                        const g=c.createGain(); g.gain.value=0.05; g.connect(c.destination);
                        const o=c.createOscillator(); o.type='square'; o.frequency.value=880; o.connect(g); o.start();
                        let on=true, count=0;
                        const t=setInterval(()=>{on=!on;g.gain.setTargetAtTime(on?0.05:0.001,c.currentTime,.01);count++;if(count>18){clearInterval(t);o.stop();c.close();}},220);
                      } catch(e) {}
                    })();
                    </script>
                    """, height=1)
                    st.toast("브라우저 경보음 재생을 요청했습니다.")
                if st.button("확인 완료 · 경보 해제", use_container_width=True):
                    st.session_state.active_alert = None
                    st.session_state.alarm_enabled = False
                    st.rerun()
            else:
                if st.button("경보 활성화", type="primary", use_container_width=True):
                    st.session_state.alarm_enabled = True
                    st.rerun()
        else:
            st.markdown('<div class="ok-panel"><div style="font-size:1.02rem;font-weight:800;color:#16643D">현재 활성 경보 없음</div><div style="margin-top:8px;color:#286548">오배출 감지 이벤트가 들어오면 이 패널에 품목·수거함·시각이 표시되고 경보 제어가 활성화됩니다.</div></div>', unsafe_allow_html=True)
            st.write("")
            st.button("🔊 경보음 재생", disabled=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">최근 감지 이벤트</div><div class="panel-sub">최근 이벤트 5건 · 오배출은 경보 이력으로 보관됩니다.</div>', unsafe_allow_html=True)
    if events:
        recent = [{
            "감지 시각": e["time"].strftime("%H:%M:%S · %Y-%m-%d"),
            "수거함": e["bin"],
            "감지 품목": e["trash"],
            "판정": "정상" if e["correct"] else "오배출",
            "출처": e.get("source", "시스템"),
        } for e in events[:5]]
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.caption("아직 이벤트가 없습니다. 현장 감지 이벤트 입력에서 첫 이벤트를 등록할 수 있습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "오배출 이력":
    st.markdown('<div class="panel"><div class="panel-title">오배출 이력</div><div class="panel-sub">세션에서 수집한 감지 결과입니다. 앱이 재시작되면 초기화됩니다.</div>', unsafe_allow_html=True)
    wrong_events = [e for e in events if not e["correct"]]
    if wrong_events:
        data = [{
            "감지 시각": e["time"].strftime("%Y-%m-%d %H:%M:%S"),
            "수거함": e["bin"], "잘못 들어간 쓰레기": e["trash"],
            "이벤트 출처": e.get("source", "시스템"),
        } for e in wrong_events]
        st.dataframe(data, use_container_width=True, hide_index=True)
        csv_data = "감지 시각,수거함,잘못 들어간 쓰레기,이벤트 출처\n" + "\n".join(
            f'"{r["감지 시각"]}","{r["수거함"]}","{r["잘못 들어간 쓰레기"]}","{r["이벤트 출처"]}"' for r in data
        )
        st.download_button("오배출 이력 CSV 다운로드", csv_data.encode("utf-8-sig"), "trash_alarm_history.csv", "text/csv")
    else:
        st.success("현재 기록된 오배출이 없습니다.")
    if st.button("전체 이력 초기화"):
        st.session_state.events = []
        st.session_state.active_alert = None
        st.session_state.alarm_enabled = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "배출 기준 설정":
    st.markdown('<div class="panel"><div class="panel-title">수거함별 허용 품목</div><div class="panel-sub">현재 규칙은 데모용 기본값입니다. 실제 아파트·지자체 기준에 맞게 app.py의 BIN_RULES를 수정하세요.</div>', unsafe_allow_html=True)
    for name, info in BIN_RULES.items():
        with st.expander(f'{info["icon"]} {name} 수거함'):
            st.write("허용 품목 예시: " + ", ".join(sorted(info["accepted"])))
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("TRASH ALARM · 운영 화면 시안 | 실제 자동 감지 및 현장 스피커 작동에는 카메라/AI 또는 센서와의 통신 연동이 필요합니다.")
