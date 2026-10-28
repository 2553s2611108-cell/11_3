import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Trash Alarm | 분리수거 지킴이",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 설정: 분리수거함별 허용 품목
# -----------------------------
BIN_RULES = {
    "플라스틱": {
        "icon": "🧴",
        "color": "#3B82F6",
        "accepted": {"플라스틱 페트병", "플라스틱 용기", "플라스틱 포장재"},
        "description": "내용물을 비우고 가능한 한 헹군 뒤 배출해 주세요.",
    },
    "종이": {
        "icon": "📦",
        "color": "#B7791F",
        "accepted": {"신문·종이", "종이 상자", "종이 포장재"},
        "description": "젖거나 오염된 종이는 일반쓰레기로 배출해 주세요.",
    },
    "캔·고철": {
        "icon": "🥫",
        "color": "#64748B",
        "accepted": {"음료 캔", "철제 캔", "고철"},
        "description": "내용물을 비우고 가능한 경우 이물질을 제거해 주세요.",
    },
    "유리": {
        "icon": "🍾",
        "color": "#0F766E",
        "accepted": {"유리병"},
        "description": "깨진 유리는 일반 유리병 수거함에 넣지 말고 관리 안내를 확인해 주세요.",
    },
    "음식물": {
        "icon": "🍎",
        "color": "#16A34A",
        "accepted": {"음식물 쓰레기"},
        "description": "비닐, 뼈, 조개껍데기 등은 섞이지 않도록 해 주세요.",
    },
    "일반쓰레기": {
        "icon": "🗑️",
        "color": "#6B7280",
        "accepted": {"오염된 휴지", "복합 재질 쓰레기"},
        "description": "재활용이 어려운 품목인지 확인하고 배출해 주세요.",
    },
}

TRASH_TYPES = [
    "플라스틱 페트병", "플라스틱 용기", "플라스틱 포장재",
    "신문·종이", "종이 상자", "종이 포장재",
    "음료 캔", "철제 캔", "고철", "유리병",
    "음식물 쓰레기", "오염된 휴지", "복합 재질 쓰레기",
]

# -----------------------------
# 세션 상태
# -----------------------------
if "events" not in st.session_state:
    st.session_state.events = []
if "active_alert" not in st.session_state:
    st.session_state.active_alert = None
if "alarm_on" not in st.session_state:
    st.session_state.alarm_on = False

# -----------------------------
# 스타일
# -----------------------------
st.markdown("""
<style>
    .stApp { background: #F5F8F6; }
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1250px; }
    .hero {
        background: linear-gradient(120deg, #123C32 0%, #176B52 100%);
        padding: 1.7rem 1.8rem; border-radius: 22px; color: white;
        margin-bottom: 1rem; box-shadow: 0 8px 24px rgba(18,60,50,.12);
    }
    .hero h1 { color: white; margin: 0 0 .35rem 0; font-size: 2.1rem; }
    .hero p { color: #D9F4E8; margin: 0; font-size: 1rem; }
    .metric-card {
        background: white; border: 1px solid #E1EAE4; border-radius: 16px;
        padding: 1rem 1.1rem; min-height: 108px;
    }
    .metric-label { color: #64746B; font-size: .9rem; }
    .metric-value { color: #163D31; font-size: 1.8rem; font-weight: 750; margin-top: .25rem; }
    .section-card {
        background: white; border: 1px solid #E1EAE4; border-radius: 18px;
        padding: 1.2rem 1.3rem; margin-bottom: .8rem;
    }
    .muted { color: #65756C; font-size: .9rem; }
    .alert-card {
        background: #FFF1F0; border: 1px solid #F4B7B3; border-left: 6px solid #DC2626;
        padding: 1rem 1.2rem; border-radius: 14px; color: #7F1D1D;
    }
    .safe-card {
        background: #EAF8EF; border: 1px solid #B8E3C5; border-left: 6px solid #16A34A;
        padding: 1rem 1.2rem; border-radius: 14px; color: #14532D;
    }
    div.stButton > button { border-radius: 12px; min-height: 2.8rem; font-weight: 650; }
    [data-testid="stSidebar"] { background: #EDF4EF; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.markdown("## ♻️ Trash Alarm")
    st.caption("아파트 분리수거장 스마트 알림")
    st.divider()
    page = st.radio("메뉴", ["실시간 감지", "감지 기록", "분리배출 안내"], index=0)
    st.divider()
    st.markdown("**작동 상태**")
    if st.session_state.active_alert:
        st.error("오배출 감지 · 확인 필요")
    else:
        st.success("대기 중 · 이상 없음")
    st.caption("현재 버전은 품목 선택을 통한 시뮬레이션입니다.")

# -----------------------------
# 공통 헤더
# -----------------------------
st.markdown("""
<div class="hero">
  <h1>♻️ Trash Alarm</h1>
  <p>올바른 분리배출을 돕는 아파트 분리수거장 알림 시스템</p>
</div>
""", unsafe_allow_html=True)

events = st.session_state.events
wrong_count = sum(1 for e in events if not e["correct"])
today = datetime.now().date()
today_count = sum(1 for e in events if e["time"].date() == today)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">오늘 감지</div><div class="metric-value">{today_count}건</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">누적 오배출</div><div class="metric-value">{wrong_count}건</div></div>', unsafe_allow_html=True)
with c3:
    status = "경보 활성" if st.session_state.active_alert else "정상 대기"
    st.markdown(f'<div class="metric-card"><div class="metric-label">현재 상태</div><div class="metric-value" style="font-size:1.45rem">{status}</div></div>', unsafe_allow_html=True)

st.write("")

# -----------------------------
# 페이지: 실시간 감지
# -----------------------------
if page == "실시간 감지":
    left, right = st.columns([1.05, 0.95], gap="large")
    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📡 배출 감지 시뮬레이터")
        st.markdown("분리수거함과 투입된 쓰레기 종류를 선택한 다음 감지 버튼을 눌러 보세요.")
        selected_bin = st.selectbox("분리수거함", list(BIN_RULES.keys()), key="selected_bin")
        bin_info = BIN_RULES[selected_bin]
        st.markdown(
            f"<div style='background:#F3F7F4;border-radius:12px;padding:12px 14px;margin:8px 0 14px 0;'>"
            f"<span style='font-size:1.5rem'>{bin_info['icon']}</span> "
            f"<b>{selected_bin} 수거함</b><br><span class='muted'>{bin_info['description']}</span></div>",
            unsafe_allow_html=True
        )
        selected_trash = st.selectbox("투입된 쓰레기 종류", TRASH_TYPES, key="selected_trash")
        expected = selected_trash in bin_info["accepted"]
        if expected:
            st.caption("선택한 조합은 일반적인 분리배출 기준에 맞는 것으로 설정되어 있습니다.")
        else:
            st.caption("이 품목은 선택한 수거함의 허용 품목 목록에 없습니다.")
        detect_clicked = st.button("🔎 투입 품목 감지", type="primary", use_container_width=True)
        if detect_clicked:
            correct = selected_trash in bin_info["accepted"]
            event = {
                "time": datetime.now(),
                "bin": selected_bin,
                "trash": selected_trash,
                "correct": correct,
            }
            st.session_state.events.insert(0, event)
            if correct:
                st.session_state.active_alert = None
                st.session_state.alarm_on = False
                st.success(f"정상 배출: {selected_trash} → {selected_bin} 수거함")
            else:
                st.session_state.active_alert = {
                    "bin": selected_bin,
                    "trash": selected_trash,
                    "time": event["time"],
                }
                st.session_state.alarm_on = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🚨 쓰레기 경보기")
        alert = st.session_state.active_alert
        if alert:
            st.markdown(
                f"<div class='alert-card'><b>오배출이 감지되었습니다!</b><br><br>"
                f"잘못 들어간 쓰레기: <b>{alert['trash']}</b><br>"
                f"투입된 수거함: <b>{alert['bin']}</b><br>"
                f"감지 시각: {alert['time'].strftime('%Y-%m-%d %H:%M:%S')}</div>",
                unsafe_allow_html=True
            )
            st.write("")
            alarm_col, reset_col = st.columns(2)
            with alarm_col:
                if st.button("🔊 경보기 울리기", type="primary", use_container_width=True):
                    st.session_state.alarm_on = True
            with reset_col:
                if st.button("✓ 확인 및 해제", use_container_width=True):
                    st.session_state.active_alert = None
                    st.session_state.alarm_on = False
                    st.rerun()
            if st.session_state.alarm_on:
                st.warning("경보가 실행되었습니다. 아래 음성 경보가 재생되지 않으면 기기의 소리 설정을 확인해 주세요.")
                components.html("""
                <div style="font-family: sans-serif; padding: 4px 0;">
                  <button id="stopAlarm" style="padding:8px 12px;border-radius:8px;border:1px solid #bbb;background:white;cursor:pointer;">
                    경보음 중지
                  </button>
                  <span id="alarmStatus" style="margin-left:8px;color:#b91c1c;">경보음 실행 중</span>
                </div>
                <script>
                (function() {
                  let ctx = null, oscillator = null, gain = null, timer = null, stopped = false;
                  try {
                    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
                    if (AudioContextClass) {
                      ctx = new AudioContextClass();
                      oscillator = ctx.createOscillator();
                      gain = ctx.createGain();
                      oscillator.type = 'square';
                      oscillator.frequency.value = 880;
                      gain.gain.value = 0.035;
                      oscillator.connect(gain); gain.connect(ctx.destination);
                      oscillator.start();
                      let on = true;
                      timer = setInterval(() => {
                        if (!ctx || stopped) return;
                        on = !on;
                        gain.gain.setTargetAtTime(on ? 0.035 : 0.001, ctx.currentTime, 0.01);
                      }, 250);
                      document.getElementById('stopAlarm').addEventListener('click', () => {
                        stopped = true;
                        clearInterval(timer);
                        try { oscillator.stop(); } catch(e) {}
                        ctx.close();
                        document.getElementById('alarmStatus').textContent = '경보음 중지됨';
                      });
                    } else {
                      document.getElementById('alarmStatus').textContent = '이 브라우저는 경보음 재생을 지원하지 않습니다.';
                    }
                  } catch (e) {
                    document.getElementById('alarmStatus').textContent = '브라우저 설정으로 경보음이 차단되었습니다.';
                  }
                })();
                </script>
                """, height=60)
        else:
            st.markdown(
                "<div class='safe-card'><b>현재 감지된 오배출이 없습니다.</b><br><br>"
                "오배출이 감지되면 이 영역에 잘못 들어간 쓰레기와 수거함이 표시되고, 경보기 버튼이 활성화됩니다.</div>",
                unsafe_allow_html=True
            )
            st.button("🔊 경보기 울리기", disabled=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🧺 수거함별 허용 품목")
    cols = st.columns(3)
    for i, (name, info) in enumerate(BIN_RULES.items()):
        with cols[i % 3]:
            accepted = ", ".join(sorted(info["accepted"]))
            st.markdown(
                f"<div style='background:#F8FAF8;border:1px solid #E1EAE4;border-radius:12px;padding:12px;height:120px;'>"
                f"<div style='font-size:1.15rem'>{info['icon']} <b>{name}</b></div>"
                f"<div style='font-size:.85rem;color:#52645A;margin-top:8px'>{accepted}</div></div>",
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 페이지: 감지 기록
# -----------------------------
elif page == "감지 기록":
    st.subheader("🧾 감지 기록")
    st.caption("기록은 현재 브라우저 세션에만 저장되며, 앱을 새로 시작하면 초기화됩니다.")
    if not st.session_state.events:
        st.info("아직 감지 기록이 없습니다. '실시간 감지'에서 품목을 감지해 보세요.")
    else:
        rows = []
        for e in st.session_state.events:
            rows.append({
                "감지 시각": e["time"].strftime("%Y-%m-%d %H:%M:%S"),
                "수거함": e["bin"],
                "감지 품목": e["trash"],
                "결과": "정상 배출" if e["correct"] else "오배출",
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)
        csv_text = "감지 시각,수거함,감지 품목,결과\n" + "\n".join(
            f'"{r["감지 시각"]}","{r["수거함"]}","{r["감지 품목"]}","{r["결과"]}"' for r in rows
        )
        st.download_button(
            "⬇️ 기록 CSV 다운로드",
            data=csv_text.encode("utf-8-sig"),
            file_name="trash_alarm_records.csv",
            mime="text/csv",
        )
        if st.button("기록 전체 삭제"):
            st.session_state.events = []
            st.session_state.active_alert = None
            st.session_state.alarm_on = False
            st.rerun()

# -----------------------------
# 페이지: 분리배출 안내
# -----------------------------
elif page == "분리배출 안내":
    st.subheader("📘 분리배출 안내")
    st.info("아래 품목은 앱 시연을 위한 간단한 예시입니다. 실제 배출 전에는 거주 지역과 아파트의 분리배출 안내를 확인해 주세요.")
    for name, info in BIN_RULES.items():
        with st.expander(f"{info['icon']} {name} 수거함"):
            st.markdown(f"**예시 허용 품목:** {', '.join(sorted(info['accepted']))}")
            st.write(info["description"])

st.divider()
st.caption("Trash Alarm · 시연용 프로토타입 | 실제 자동 인식에는 카메라·영상 분석 모델·현장 경보 장치 연동이 추가로 필요합니다.")
