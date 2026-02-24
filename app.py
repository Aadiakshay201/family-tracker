import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
import time
import random
import json
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FamilyTrack",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PERSISTENT STORAGE (JSON file so data survives reloads) ─────────────────
DATA_FILE = "familytrack_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def save_data():
    try:
        data = {
            "members":   st.session_state.members,
            "chats":     {str(k): v for k, v in st.session_state.chats.items()},
            "my_name":   st.session_state.my_name,
            "my_emoji":  st.session_state.my_emoji,
            "next_id":   st.session_state.next_id,
            "dark_mode": st.session_state.dark_mode,
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
PALETTE      = ["#10b981","#3b82f6","#06b6d4","#f59e0b","#ec4899","#a78bfa","#34d399","#fb923c"]
EMOJIS       = ["👩","👨","🧒","👧","👴","👵","👦","🧑","🧔","🧓"]
EMOJI_PICKER = ["😊","😂","❤️","👍","🙏","🔥","😍","🎉","😢","😮","👋","✅","📍","🏠","🚗","⚠️","🆘","💪","🥰","😎"]

DEFAULT_MEMBERS = [
    {"id":1,"name":"Mom", "lat":17.4126,"lng":78.4482,"emoji":"👩","color":"#10b981","status":"online"},
    {"id":2,"name":"Dad", "lat":17.4435,"lng":78.3772,"emoji":"👨","color":"#3b82f6","status":"online"},
    {"id":3,"name":"Jake","lat":17.4399,"lng":78.4983,"emoji":"🧒","color":"#06b6d4","status":"online"},
    {"id":4,"name":"Lily","lat":17.4320,"lng":78.4510,"emoji":"👧","color":"#f59e0b","status":"away"},
]

DEFAULT_CHATS = {
    1: [
        {"sender":"Mom","emoji":"👩","text":"Hi! I'm home safe 🏠","time":"10:30 AM","me":False},
        {"sender":"You","emoji":"🧑","text":"Great! See you soon 😊","time":"10:31 AM","me":True},
        {"sender":"Mom","emoji":"👩","text":"Don't forget dinner at 7 ❤️","time":"10:32 AM","me":False},
    ],
    2: [
        {"sender":"Dad","emoji":"👨","text":"At work, will be back by 6 🏢","time":"9:15 AM","me":False},
        {"sender":"You","emoji":"🧑","text":"Ok Dad! Take care 👍","time":"9:16 AM","me":True},
    ],
    3: [
        {"sender":"Jake","emoji":"🧒","text":"Reached school! 🎒","time":"8:20 AM","me":False},
        {"sender":"You","emoji":"🧑","text":"Good boy! Study well 💪","time":"8:21 AM","me":True},
        {"sender":"Jake","emoji":"🧒","text":"Thanks 😎 will do!","time":"8:22 AM","me":False},
    ],
    4: [
        {"sender":"Lily","emoji":"👧","text":"Going to friend's place 🚗","time":"10:00 AM","me":False},
        {"sender":"You","emoji":"🧑","text":"Ok be back by 5 ⚠️","time":"10:01 AM","me":True},
    ],
}

# ─── SESSION STATE INIT ───────────────────────────────────────────────────────
def init_state():
    saved = load_data()

    if "members" not in st.session_state:
        st.session_state.members = saved["members"] if saved and "members" in saved else [m.copy() for m in DEFAULT_MEMBERS]

    if "chats" not in st.session_state:
        if saved and "chats" in saved:
            st.session_state.chats = {int(k): v for k, v in saved["chats"].items()}
        else:
            st.session_state.chats = {k: [msg.copy() for msg in v] for k, v in DEFAULT_CHATS.items()}

    if "my_name"        not in st.session_state: st.session_state.my_name        = saved.get("my_name","You")       if saved else "You"
    if "my_emoji"       not in st.session_state: st.session_state.my_emoji       = saved.get("my_emoji","🧑")       if saved else "🧑"
    if "next_id"        not in st.session_state: st.session_state.next_id        = saved.get("next_id", 5)          if saved else 5
    if "dark_mode"      not in st.session_state: st.session_state.dark_mode      = saved.get("dark_mode", True)     if saved else True
    if "active_chat_id" not in st.session_state: st.session_state.active_chat_id = st.session_state.members[0]["id"] if st.session_state.members else 1
    if "success"        not in st.session_state: st.session_state.success        = ""
    if "errors"         not in st.session_state: st.session_state.errors         = {}
    if "last_drift"     not in st.session_state: st.session_state.last_drift     = time.time()

init_state()

# ─── THEME VARIABLES ─────────────────────────────────────────────────────────
DM = st.session_state.dark_mode

if DM:
    BG          = "#060818"
    SURFACE     = "#0a0d20"
    SURFACE2    = "#0e1228"
    CARD        = "#111530"
    BORDER      = "rgba(255,255,255,0.07)"
    BORDER2     = "rgba(255,255,255,0.11)"
    TEXT        = "#e8ecff"
    MUTED       = "rgba(232,236,255,0.45)"
    DIM         = "rgba(232,236,255,0.22)"
    BUBBLE_ME   = "linear-gradient(135deg,#3b82f6,#6d28d9)"
    BUBBLE_OTH  = "#161b38"
    BUBBLE_BD   = "rgba(255,255,255,0.08)"
    INPUT_BG    = "#10142e"
    CHAT_BG     = "#0b0e22"
    PING_COLOR  = "rgba(59,130,246,0.15)"
    THEME_BTN   = "🌙 Dark"
    SVG_OPACITY = "0.04"
    GRID_COLOR  = "rgba(59,130,246,0.08)"
    DOT_COLOR   = "rgba(59,130,246,0.20)"
else:
    BG          = "#f0f4ff"
    SURFACE     = "#ffffff"
    SURFACE2    = "#f8faff"
    CARD        = "#ffffff"
    BORDER      = "rgba(0,0,0,0.08)"
    BORDER2     = "rgba(0,0,0,0.12)"
    TEXT        = "#1a1f3a"
    MUTED       = "rgba(26,31,58,0.55)"
    DIM         = "rgba(26,31,58,0.30)"
    BUBBLE_ME   = "linear-gradient(135deg,#3b82f6,#6d28d9)"
    BUBBLE_OTH  = "#e8eeff"
    BUBBLE_BD   = "rgba(0,0,0,0.07)"
    INPUT_BG    = "#f0f4ff"
    CHAT_BG     = "#f5f7ff"
    PING_COLOR  = "rgba(59,130,246,0.10)"
    THEME_BTN   = "☀️ Light"
    SVG_OPACITY = "0.06"
    GRID_COLOR  = "rgba(59,130,246,0.10)"
    DOT_COLOR   = "rgba(59,130,246,0.25)"

# ─── ANIMATED BACKGROUND + FULL CSS ──────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

/* ── ANIMATED BACKGROUND ── */
#ft-bg {{
    position: fixed;
    inset: 0;
    z-index: 0;
    background: {BG};
    overflow: hidden;
    pointer-events: none;
}}

/* Animated map grid lines */
#ft-bg::before {{
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient({GRID_COLOR} 1px, transparent 1px),
        linear-gradient(90deg, {GRID_COLOR} 1px, transparent 1px);
    background-size: 48px 48px;
    animation: grid-drift 30s linear infinite;
}}
@keyframes grid-drift {{
    0%   {{ transform: translate(0, 0); }}
    100% {{ transform: translate(48px, 48px); }}
}}

/* SVG world map watermark */
#ft-bg .map-bg {{
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: {SVG_OPACITY};
}}

/* Floating ping rings */
.ping-ring {{
    position: absolute;
    border-radius: 50%;
    border: 1.5px solid rgba(59,130,246,0.35);
    animation: ping-expand 4s ease-out infinite;
    pointer-events: none;
}}
.ping-ring:nth-child(1)  {{ width:60px;  height:60px;  top:20%;  left:15%; animation-delay:0s;   }}
.ping-ring:nth-child(2)  {{ width:40px;  height:40px;  top:65%;  left:72%; animation-delay:1.2s; }}
.ping-ring:nth-child(3)  {{ width:50px;  height:50px;  top:40%;  left:85%; animation-delay:2.4s; }}
.ping-ring:nth-child(4)  {{ width:35px;  height:35px;  top:75%;  left:30%; animation-delay:0.8s; }}
.ping-ring:nth-child(5)  {{ width:55px;  height:55px;  top:10%;  left:60%; animation-delay:3.1s; }}
@keyframes ping-expand {{
    0%   {{ transform: scale(0.3); opacity: 0.8; }}
    100% {{ transform: scale(3.5); opacity: 0; }}
}}

/* Floating dots */
.float-dot {{
    position: absolute;
    border-radius: 50%;
    background: {DOT_COLOR};
    animation: float-move linear infinite;
}}
.float-dot:nth-child(6)  {{ width:6px;  height:6px;  top:15%;  left:25%;  animation-duration:18s; animation-delay:0s;   }}
.float-dot:nth-child(7)  {{ width:4px;  height:4px;  top:55%;  left:80%;  animation-duration:22s; animation-delay:3s;   }}
.float-dot:nth-child(8)  {{ width:8px;  height:8px;  top:80%;  left:45%;  animation-duration:15s; animation-delay:6s;   }}
.float-dot:nth-child(9)  {{ width:5px;  height:5px;  top:35%;  left:65%;  animation-duration:20s; animation-delay:2s;   }}
.float-dot:nth-child(10) {{ width:7px;  height:7px;  top:70%;  left:10%;  animation-duration:25s; animation-delay:9s;   }}
@keyframes float-move {{
    0%   {{ transform: translateY(0px) translateX(0px);   opacity: 0.6; }}
    25%  {{ transform: translateY(-30px) translateX(15px); opacity: 1;   }}
    50%  {{ transform: translateY(-10px) translateX(30px); opacity: 0.4; }}
    75%  {{ transform: translateY(-40px) translateX(10px); opacity: 0.9; }}
    100% {{ transform: translateY(0px) translateX(0px);   opacity: 0.6; }}
}}

/* Glow orbs */
.glow-orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    animation: orb-pulse 8s ease-in-out infinite;
    pointer-events: none;
}}
.glow-orb.o1 {{ width:400px; height:400px; top:-100px; right:-100px; background:rgba(59,130,246,0.08); animation-delay:0s; }}
.glow-orb.o2 {{ width:300px; height:300px; bottom:-80px; left:-80px;  background:rgba(124,58,237,0.07); animation-delay:4s; }}
.glow-orb.o3 {{ width:250px; height:250px; top:40%;  left:40%;  background:rgba(6,182,212,0.05);  animation-delay:2s; }}
@keyframes orb-pulse {{
    0%,100% {{ transform: scale(1);    opacity: 0.6; }}
    50%      {{ transform: scale(1.3); opacity: 1;   }}
}}

/* ── STREAMLIT CHROME ── */
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    background: transparent !important;
    position: relative;
    z-index: 1;
}}
[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER} !important;
    backdrop-filter: blur(20px);
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
#MainMenu,footer,header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {{ display: none !important; }}

/* ── TYPOGRAPHY ── */
html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif !important;
    color: {TEXT} !important;
}}
h1,h2,h3 {{ color: {TEXT} !important; letter-spacing: -0.02em; }}

/* ── TABS ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: {SURFACE} !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid {BORDER} !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    background: transparent !important;
    border-radius: 9px !important;
    color: {MUTED} !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 6px 18px !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    background: linear-gradient(135deg, #3b82f6, #7c3aed) !important;
    color: #fff !important;
}}

/* ── INPUTS ── */
input, textarea {{
    background: {INPUT_BG} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER2} !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
input::placeholder, textarea::placeholder {{ color: {DIM} !important; }}
input:focus, textarea:focus {{
    border-color: rgba(59,130,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.10) !important;
}}

/* ── BUTTONS ── */
.stButton > button {{
    background: linear-gradient(135deg, #3b82f6, #7c3aed) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    padding: 0.45rem 1rem !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(59,130,246,0.30) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all .2s !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 22px rgba(59,130,246,0.45) !important;
}}

/* ── METRICS ── */
[data-testid="stMetric"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    backdrop-filter: blur(10px);
}}
[data-testid="stMetricValue"] {{ color: #3b82f6 !important; font-weight: 800 !important; }}
[data-testid="stMetricLabel"] {{ color: {MUTED} !important; font-size: 0.65rem !important; text-transform: uppercase; letter-spacing: 0.08em; }}

/* ── SELECT ── */
[data-testid="stSelectbox"] > div > div {{
    background: {INPUT_BG} !important;
    border: 1px solid {BORDER2} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
}}

/* ── DIVIDER ── */
hr {{ border-color: {BORDER} !important; }}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {{ width: 3px; height: 3px; }}
::-webkit-scrollbar-thumb {{ background: rgba(59,130,246,0.25); border-radius: 3px; }}

/* ── MAP IFRAME ── */
iframe {{ border-radius: 14px !important; border: 1px solid {BORDER2} !important; }}

/* ── EXPANDER ── */
[data-testid="stExpander"] {{
    background: {SURFACE2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}
</style>

<!-- ANIMATED BACKGROUND -->
<div id="ft-bg">
  <!-- Glow orbs -->
  <div class="glow-orb o1"></div>
  <div class="glow-orb o2"></div>
  <div class="glow-orb o3"></div>

  <!-- Ping rings (location pulses) -->
  <div class="ping-ring"></div>
  <div class="ping-ring"></div>
  <div class="ping-ring"></div>
  <div class="ping-ring"></div>
  <div class="ping-ring"></div>

  <!-- Floating dots -->
  <div class="float-dot"></div>
  <div class="float-dot"></div>
  <div class="float-dot"></div>
  <div class="float-dot"></div>
  <div class="float-dot"></div>

  <!-- World map SVG watermark -->
  <div class="map-bg">
    <svg viewBox="0 0 1000 500" width="95%" height="95%" fill="none"
         xmlns="http://www.w3.org/2000/svg" style="color:#3b82f6">
      <!-- Simplified world map continents as paths -->
      <!-- North America -->
      <path d="M 80 80 L 130 60 L 190 70 L 220 110 L 210 160 L 180 190 L 150 200 L 120 180 L 90 150 L 70 120 Z"
            fill="currentColor" opacity="0.4"/>
      <path d="M 150 200 L 180 220 L 200 260 L 185 290 L 160 300 L 145 270 L 140 240 Z"
            fill="currentColor" opacity="0.35"/>
      <!-- South America -->
      <path d="M 200 280 L 240 270 L 265 300 L 270 350 L 255 400 L 230 430 L 205 410 L 190 370 L 195 320 Z"
            fill="currentColor" opacity="0.4"/>
      <!-- Europe -->
      <path d="M 430 60 L 480 55 L 510 75 L 505 110 L 475 120 L 445 115 L 425 90 Z"
            fill="currentColor" opacity="0.45"/>
      <!-- Africa -->
      <path d="M 440 140 L 490 130 L 520 160 L 530 220 L 520 290 L 495 340 L 465 350 L 445 310 L 430 250 L 425 190 Z"
            fill="currentColor" opacity="0.4"/>
      <!-- Asia -->
      <path d="M 510 55 L 620 45 L 720 60 L 780 80 L 800 130 L 760 160 L 700 150 L 640 170 L 580 160 L 535 130 L 510 100 Z"
            fill="currentColor" opacity="0.45"/>
      <!-- India -->
      <path d="M 610 165 L 650 160 L 670 200 L 660 250 L 635 265 L 610 240 L 600 200 Z"
            fill="currentColor" opacity="0.5"/>
      <!-- South East Asia -->
      <path d="M 720 160 L 770 155 L 800 180 L 790 210 L 755 220 L 725 200 Z"
            fill="currentColor" opacity="0.4"/>
      <!-- Australia -->
      <path d="M 740 290 L 820 275 L 870 300 L 875 360 L 840 400 L 790 405 L 745 375 L 730 330 Z"
            fill="currentColor" opacity="0.4"/>
      <!-- Greenland -->
      <path d="M 270 30 L 330 20 L 370 45 L 355 80 L 310 90 L 270 70 Z"
            fill="currentColor" opacity="0.3"/>
      <!-- Grid lines (lat/lng) -->
      <line x1="0" y1="100" x2="1000" y2="100" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
      <line x1="0" y1="200" x2="1000" y2="200" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
      <line x1="0" y1="300" x2="1000" y2="300" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
      <line x1="0" y1="400" x2="1000" y2="400" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
      <line x1="200" y1="0" x2="200" y2="500" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
      <line x1="400" y1="0" x2="400" y2="500" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
      <line x1="600" y1="0" x2="600" y2="500" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
      <line x1="800" y1="0" x2="800" y2="500" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
    </svg>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def get_center(members):
    if not members: return [17.4262, 78.4462]
    return [sum(m["lat"] for m in members)/len(members),
            sum(m["lng"] for m in members)/len(members)]

def get_zoom(members):
    if len(members) <= 1: return 14
    lats   = [m["lat"] for m in members]
    lngs   = [m["lng"] for m in members]
    spread = max(max(lats)-min(lats), max(lngs)-min(lngs))
    if spread < 0.02: return 15
    if spread < 0.1:  return 13
    if spread < 0.5:  return 11
    return 9

def validate_member(name, lat, lng):
    errs = {}
    if not name or not name.strip(): errs["name"] = "⚠️ Name cannot be empty."
    if not (-90 <= lat <= 90):       errs["lat"]  = "⚠️ Latitude must be -90 to 90."
    if not (-180 <= lng <= 180):     errs["lng"]  = "⚠️ Longitude must be -180 to 180."
    return errs

def add_member(name, lat, lng, emoji, color):
    m = {
        "id":     st.session_state.next_id,
        "name":   name.strip(),
        "lat":    round(lat, 6),
        "lng":    round(lng, 6),
        "emoji":  emoji,
        "color":  color,
        "status": "online",
    }
    st.session_state.members.append(m)
    st.session_state.chats[m["id"]] = []
    st.session_state.next_id += 1
    save_data()
    return m

def remove_member(mid):
    st.session_state.members = [m for m in st.session_state.members if m["id"] != mid]
    st.session_state.chats.pop(mid, None)
    save_data()

def now_time():
    return datetime.now().strftime("%I:%M %p")

def send_message(member_id, text):
    if member_id not in st.session_state.chats:
        st.session_state.chats[member_id] = []
    st.session_state.chats[member_id].append({
        "sender": st.session_state.my_name,
        "emoji":  st.session_state.my_emoji,
        "text":   text,
        "time":   now_time(),
        "me":     True,
    })
    member  = next((m for m in st.session_state.members if m["id"] == member_id), None)
    replies = ["👍","On my way! 🚗","Ok! 😊","Noted ✅","📍 Sharing location","Will be there soon!","❤️","Got it!","😂 Sure!","🙏","Be safe! ⚠️"]
    if member and random.random() > 0.35:
        st.session_state.chats[member_id].append({
            "sender": member["name"],
            "emoji":  member["emoji"],
            "text":   random.choice(replies),
            "time":   now_time(),
            "me":     False,
        })
    save_data()

def simulate_drift():
    now = time.time()
    if now - st.session_state.last_drift > 6:
        for m in st.session_state.members:
            if m["status"] == "online":
                m["lat"] += random.uniform(-0.0001, 0.0001)
                m["lng"] += random.uniform(-0.0001, 0.0001)
        st.session_state.last_drift = now
        save_data()

simulate_drift()

# ─── MAP BUILDER ─────────────────────────────────────────────────────────────
def build_map():
    members = st.session_state.members
    center  = get_center(members)
    zoom    = get_zoom(members)

    fmap = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="CartoDB dark_matter" if DM else "CartoDB positron",
        prefer_canvas=True,
    )

    if not members:
        return fmap

    if len(members) > 1:
        lats = [m["lat"] for m in members]
        lngs = [m["lng"] for m in members]
        fmap.fit_bounds([[min(lats),min(lngs)],[max(lats),max(lngs)]], padding=[60,60])

    for m in members:
        sc   = "#10b981" if m["status"]=="online" else "#f59e0b"
        msgs = len(st.session_state.chats.get(m["id"], []))

        icon_html = f"""
        <div style="display:flex;flex-direction:column;align-items:center;">
          <div style="background:rgba(6,8,24,0.93);border:2.5px solid {m['color']};
            border-radius:10px;padding:4px 10px;display:flex;align-items:center;gap:5px;
            white-space:nowrap;
            box-shadow:0 4px 18px rgba(0,0,0,0.6),0 0 14px {m['color']}66;
            font-family:Segoe UI,sans-serif;">
            <span style="font-size:1rem;">{m['emoji']}</span>
            <span style="font-size:0.72rem;font-weight:800;color:#fff;">{m['name']}</span>
            <span style="width:7px;height:7px;border-radius:50%;background:{sc};
              box-shadow:0 0 6px {sc};display:inline-block;"></span>
          </div>
          <div style="width:2px;height:10px;background:{m['color']};"></div>
          <div style="width:11px;height:11px;border-radius:50%;background:{m['color']};
            box-shadow:0 0 14px {m['color']};"></div>
        </div>"""

        popup_html = f"""
        <div style="font-family:Segoe UI,sans-serif;padding:6px;min-width:175px;">
          <div style="text-align:center;font-size:1.5rem;margin-bottom:5px;">{m['emoji']}</div>
          <div style="font-weight:800;font-size:0.95rem;color:#111;text-align:center;margin-bottom:8px;">{m['name']}</div>
          <div style="font-size:0.72rem;color:#555;margin-bottom:3px;">📍 <b>Lat:</b> {m['lat']:.5f}</div>
          <div style="font-size:0.72rem;color:#555;margin-bottom:3px;">📍 <b>Lng:</b> {m['lng']:.5f}</div>
          <div style="font-size:0.72rem;color:#555;margin-bottom:3px;">🟢 <b>Status:</b> {m['status'].title()}</div>
          <div style="font-size:0.72rem;color:#555;">💬 <b>Messages:</b> {msgs}</div>
        </div>"""

        folium.Marker(
            location=[m["lat"], m["lng"]],
            popup=folium.Popup(popup_html, max_width=230),
            tooltip=f"{m['emoji']} {m['name']} • {m['status']}",
            icon=folium.DivIcon(html=icon_html, icon_size=(100,58), icon_anchor=(50,58)),
        ).add_to(fmap)

        folium.Circle(
            location=[m["lat"], m["lng"]],
            radius=130, color=m["color"],
            fill=True, fill_color=m["color"],
            fill_opacity=0.07, weight=1, dash_array="4 6",
        ).add_to(fmap)

    return fmap

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<div style='font-size:1.2rem;font-weight:900;letter-spacing:-0.03em;margin-bottom:2px;color:{TEXT}'>📡 FamilyTrack</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.67rem;color:{DIM};margin-top:0;margin-bottom:10px;'>Live Location & Chat</p>", unsafe_allow_html=True)

    # Dark / Light mode toggle
    mode_label = "☀️ Switch to Light" if DM else "🌙 Switch to Dark"
    if st.button(mode_label, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        save_data()
        st.rerun()

    st.divider()

    # My Profile
    with st.expander("👤 My Profile", expanded=False):
        new_name  = st.text_input("Your Name",  value=st.session_state.my_name,  key="my_name_inp")
        new_emoji = st.selectbox("Your Avatar", EMOJIS,
                                  index=EMOJIS.index(st.session_state.my_emoji) if st.session_state.my_emoji in EMOJIS else 0,
                                  key="my_emoji_inp")
        if st.button("💾 Save Profile"):
            st.session_state.my_name  = new_name
            st.session_state.my_emoji = new_emoji
            save_data()
            st.success("Profile saved!")

    st.divider()

    # Add Member
    with st.expander("➕ Add Member", expanded=True):
        name_val = st.text_input("Full Name *", placeholder="e.g. Priya Sharma", key="inp_name")
        lat_val  = st.number_input("Latitude *",  value=17.4262, min_value=-90.0,  max_value=90.0,  step=0.0001, format="%.4f", key="inp_lat")
        lng_val  = st.number_input("Longitude *", value=78.4462, min_value=-180.0, max_value=180.0, step=0.0001, format="%.4f", key="inp_lng")
        c1, c2   = st.columns(2)
        with c1: emoji_val = st.selectbox("Avatar", EMOJIS, key="inp_emoji")
        with c2: color_val = st.color_picker("Color", value=PALETTE[len(st.session_state.members) % len(PALETTE)], key="inp_color")

        for err in st.session_state.errors.values():
            st.error(err)
        if st.session_state.success:
            st.success(st.session_state.success)
            st.session_state.success = ""

        if st.button("📍 Add to Map & Save"):
            errs = validate_member(name_val, lat_val, lng_val)
            if errs:
                st.session_state.errors = errs
            else:
                st.session_state.errors = {}
                added = add_member(name_val, lat_val, lng_val, emoji_val, color_val)
                st.session_state.success = f"✅ {added['emoji']} **{added['name']}** saved permanently!"
            st.rerun()

    st.divider()

    # Members list
    st.markdown(f"<div style='font-size:0.68rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:{DIM};margin-bottom:8px;'>👨‍👩‍👧 Members ({len(st.session_state.members)})</div>", unsafe_allow_html=True)

    for m in st.session_state.members:
        sc = "#10b981" if m["status"]=="online" else "#f59e0b"
        ca, cb = st.columns([3, 1])
        with ca:
            st.markdown(
                f"<div style='font-size:0.85rem;font-weight:700;'>{m['emoji']} {m['name']} "
                f"<span style='width:6px;height:6px;border-radius:50%;background:{sc};"
                f"display:inline-block;box-shadow:0 0 5px {sc};'></span></div>"
                f"<div style='font-size:0.62rem;color:{DIM};font-family:monospace;'>"
                f"{m['lat']:.4f}, {m['lng']:.4f}</div>",
                unsafe_allow_html=True)
        with cb:
            if st.button("✕", key=f"rm_{m['id']}", help=f"Remove {m['name']}"):
                remove_member(m["id"])
                st.rerun()

    st.divider()
    if st.button("🔄 Refresh"):
        st.rerun()

# ─── MAIN PAGE ───────────────────────────────────────────────────────────────
ha, hb = st.columns([5, 1])
with ha:
    st.markdown(f"<h1 style='margin-bottom:2px;'>📡 FamilyTrack</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{MUTED};font-size:0.82rem;margin-top:0;margin-bottom:8px;'>Live Location & Family Chat · Data saves automatically</p>", unsafe_allow_html=True)
with hb:
    st.markdown(
        f"<div style='padding-top:16px;text-align:right;'>"
        f"<span style='display:inline-flex;align-items:center;gap:6px;"
        f"background:rgba(16,185,129,0.10);border:1px solid rgba(16,185,129,0.25);"
        f"border-radius:100px;padding:4px 12px;'>"
        f"<span style='width:7px;height:7px;border-radius:50%;background:#10b981;"
        f"box-shadow:0 0 8px #10b981;display:inline-block;animation:none;'></span>"
        f"<span style='font-size:0.7rem;font-weight:800;color:#10b981;'>LIVE</span>"
        f"</span></div>", unsafe_allow_html=True)

# Metrics
members    = st.session_state.members
online_cnt = sum(1 for m in members if m["status"]=="online")
away_cnt   = sum(1 for m in members if m["status"]=="away")
total_msgs = sum(len(v) for v in st.session_state.chats.values())

m1,m2,m3,m4 = st.columns(4)
m1.metric("👥 Members",   len(members))
m2.metric("🟢 Online",    online_cnt)
m3.metric("🟡 Away",      away_cnt)
m4.metric("💬 Messages",  total_msgs)

st.divider()

# ─── TABS ────────────────────────────────────────────────────────────────────
tab_map, tab_chat = st.tabs(["🗺️  Live Map", "💬  Family Chat"])

# ════════ MAP TAB ════════
with tab_map:
    if not members:
        st.info("👆 Add family members from the sidebar to see them on the map.")
    else:
        fmap     = build_map()
        map_data = st_folium(
            fmap,
            use_container_width=True,
            height=580,
            returned_objects=["last_clicked"],
            key="familymap",
        )
        if map_data and map_data.get("last_clicked"):
            lc = map_data["last_clicked"]
            st.caption(f"📍 Clicked: **{lc['lat']:.5f}, {lc['lng']:.5f}** — paste into sidebar to add a member here.")

        # Live location table
        st.markdown(f"<div style='font-size:0.8rem;font-weight:800;margin:14px 0 8px;color:{TEXT};'>📋 Live Locations</div>", unsafe_allow_html=True)
        hdr = st.columns([1,3,2,2,2])
        for col,lbl in zip(hdr,["","Name","Latitude","Longitude","Status"]):
            col.markdown(f"<span style='font-size:0.72rem;font-weight:800;color:{MUTED};text-transform:uppercase;letter-spacing:.07em;'>{lbl}</span>", unsafe_allow_html=True)
        st.markdown(f"<hr style='margin:4px 0 6px;border-color:{BORDER};'/>", unsafe_allow_html=True)

        for m in members:
            sc    = "#10b981" if m["status"]=="online" else "#f59e0b"
            st_lb = "🟢 Online" if m["status"]=="online" else "🟡 Away"
            c0,c1,c2,c3,c4 = st.columns([1,3,2,2,2])
            c0.markdown(f"<div style='font-size:1.3rem'>{m['emoji']}</div>", unsafe_allow_html=True)
            c1.markdown(f"<span style='font-weight:700;font-size:0.85rem;'>{m['name']}</span>", unsafe_allow_html=True)
            c2.markdown(f"<code style='color:#3b82f6;background:rgba(59,130,246,0.10);padding:2px 7px;border-radius:6px;font-size:0.72rem;'>{m['lat']:.5f}</code>", unsafe_allow_html=True)
            c3.markdown(f"<code style='color:#3b82f6;background:rgba(59,130,246,0.10);padding:2px 7px;border-radius:6px;font-size:0.72rem;'>{m['lng']:.5f}</code>", unsafe_allow_html=True)
            c4.markdown(f"<span style='background:{sc}18;border:1px solid {sc}44;color:{sc};font-size:0.65rem;font-weight:800;padding:3px 9px;border-radius:100px;'>{st_lb}</span>", unsafe_allow_html=True)

# ════════ CHAT TAB ════════
with tab_chat:
    if not members:
        st.info("👆 Add family members first to start chatting.")
    else:
        chat_left, chat_right = st.columns([1, 2.8], gap="medium")

        # Left: conversation list
        with chat_left:
            st.markdown(f"<div style='font-size:0.8rem;font-weight:800;margin-bottom:10px;color:{TEXT};'>💬 Conversations</div>", unsafe_allow_html=True)
            for m in members:
                msgs      = st.session_state.chats.get(m["id"], [])
                sc        = "#10b981" if m["status"]=="online" else "#f59e0b"
                last_msg  = msgs[-1]["text"][:26]+"…" if msgs else "No messages yet"
                is_active = m["id"] == st.session_state.active_chat_id
                card_bg   = f"rgba(59,130,246,0.09)" if is_active else SURFACE2
                card_bd   = "rgba(59,130,246,0.28)"  if is_active else BORDER

                st.markdown(
                    f"""<div style="background:{card_bg};border:1px solid {card_bd};
                    border-radius:12px;padding:10px 12px;margin-bottom:5px;">
                    <div style="display:flex;align-items:center;gap:9px;">
                      <div style="position:relative;flex-shrink:0;">
                        <span style="font-size:1.35rem;">{m['emoji']}</span>
                        <span style="position:absolute;bottom:-1px;right:-2px;width:9px;height:9px;
                          border-radius:50%;background:{sc};border:2px solid {SURFACE};
                          display:block;box-shadow:0 0 5px {sc};"></span>
                      </div>
                      <div style="flex:1;min-width:0;">
                        <div style="font-weight:700;font-size:0.82rem;color:{TEXT};">{m['name']}</div>
                        <div style="font-size:0.64rem;color:{DIM};
                          white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{last_msg}</div>
                      </div>
                      <div style="background:linear-gradient(135deg,#3b82f6,#7c3aed);color:#fff;
                        font-size:0.58rem;font-weight:800;padding:2px 6px;border-radius:100px;
                        flex-shrink:0;">{len(msgs)}</div>
                    </div></div>""",
                    unsafe_allow_html=True)

                if st.button(f"Open chat", key=f"open_{m['id']}"):
                    st.session_state.active_chat_id = m["id"]
                    st.rerun()

        # Right: active chat
        with chat_right:
            active = next((m for m in members if m["id"] == st.session_state.active_chat_id), members[0])
            sc     = "#10b981" if active["status"]=="online" else "#f59e0b"
            st_lb  = "Online" if active["status"]=="online" else "Away"

            # Chat header
            st.markdown(
                f"""<div style="background:{CARD};border:1px solid {BORDER2};
                border-radius:14px;padding:12px 16px;margin-bottom:10px;
                display:flex;align-items:center;gap:12px;
                box-shadow:0 2px 12px rgba(0,0,0,0.15);">
                  <span style="font-size:1.7rem;">{active['emoji']}</span>
                  <div style="flex:1;">
                    <div style="font-weight:800;font-size:0.95rem;color:{TEXT};">{active['name']}</div>
                    <div style="font-size:0.68rem;color:{sc};font-weight:600;display:flex;align-items:center;gap:5px;">
                      <span style="width:6px;height:6px;border-radius:50%;background:{sc};
                        box-shadow:0 0 6px {sc};display:inline-block;"></span>
                      {st_lb} &nbsp;·&nbsp;
                      <span style="color:{DIM};">
                        📍 {active['lat']:.4f}, {active['lng']:.4f}
                      </span>
                    </div>
                  </div>
                </div>""",
                unsafe_allow_html=True)

            # Messages
            msgs     = st.session_state.chats.get(active["id"], [])
            chat_html = f"<div style='height:340px;overflow-y:auto;padding:6px 4px;background:{CHAT_BG};border:1px solid {BORDER};border-radius:14px;margin-bottom:10px;'>"
            if not msgs:
                chat_html += f"<div style='text-align:center;color:{DIM};font-size:0.8rem;padding-top:120px;'>No messages yet. Say hi! 👋</div>"
            for msg in msgs:
                if msg["me"]:
                    chat_html += f"""
                    <div style="display:flex;justify-content:flex-end;margin:6px 10px 0;">
                      <div style="max-width:72%;">
                        <div style="background:{BUBBLE_ME};color:#fff;padding:9px 13px;
                          border-radius:16px 16px 4px 16px;font-size:0.82rem;line-height:1.45;
                          word-break:break-word;box-shadow:0 2px 12px rgba(59,130,246,0.20);">{msg['text']}</div>
                        <div style="font-size:0.59rem;color:{DIM};text-align:right;margin-top:3px;">{msg['time']}</div>
                      </div>
                    </div>"""
                else:
                    chat_html += f"""
                    <div style="display:flex;justify-content:flex-start;margin:6px 10px 0;gap:7px;align-items:flex-end;">
                      <span style="font-size:1rem;flex-shrink:0;">{msg['emoji']}</span>
                      <div style="max-width:72%;">
                        <div style="font-size:0.6rem;font-weight:700;color:{MUTED};margin-bottom:3px;">{msg['sender']}</div>
                        <div style="background:{BUBBLE_OTH};border:1px solid {BUBBLE_BD};color:{TEXT};
                          padding:9px 13px;border-radius:16px 16px 16px 4px;
                          font-size:0.82rem;line-height:1.45;word-break:break-word;">{msg['text']}</div>
                        <div style="font-size:0.59rem;color:{DIM};margin-top:3px;">{msg['time']}</div>
                      </div>
                    </div>"""
            chat_html += "<div style='height:10px;'></div></div>"
            st.markdown(chat_html, unsafe_allow_html=True)

            # Emoji quick-row
            st.markdown(f"<div style='font-size:0.6rem;color:{DIM};margin-bottom:4px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;'>Quick Emoji</div>", unsafe_allow_html=True)
            ecols = st.columns(len(EMOJI_PICKER))
            for i, emo in enumerate(EMOJI_PICKER):
                with ecols[i]:
                    if st.button(emo, key=f"emo_{active['id']}_{i}"):
                        send_message(active["id"], emo)
                        st.rerun()

            # Text + send
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            mc, bc = st.columns([5, 1])
            with mc:
                msg_text = st.text_input("msg", placeholder=f"Message {active['name']}…",
                                          key=f"msg_{active['id']}", label_visibility="collapsed")
            with bc:
                if st.button("Send ➤", key=f"send_{active['id']}"):
                    if msg_text and msg_text.strip():
                        send_message(active["id"], msg_text.strip())
                        st.rerun()

            # Share location
            if st.button(f"📍 Share My Location with {active['name']}", key=f"loc_{active['id']}"):
                my_lat = active["lat"] + random.uniform(-0.002, 0.002)
                my_lng = active["lng"] + random.uniform(-0.002, 0.002)
                send_message(active["id"], f"📍 My current location: {my_lat:.5f}, {my_lng:.5f}")
                st.rerun()

st.divider()
st.markdown(
    f"<div style='text-align:center;font-size:0.67rem;color:{DIM};padding-bottom:6px;'>"
    f"Built with ❤️ by Team AKSHAYY &nbsp;·&nbsp; FamilyTrack © 2025 &nbsp;·&nbsp; "
    f"Data saved to <code>familytrack_data.json</code></div>",
    unsafe_allow_html=True)