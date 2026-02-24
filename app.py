import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
import time
import random

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FamilyTrack",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── STYLES ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#060818;}
[data-testid="stSidebar"]{background:#0a0d20;border-right:1px solid rgba(255,255,255,0.06);}
[data-testid="stSidebar"] *{color:#e0e6ff;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
html,body,[class*="css"]{font-family:'Plus Jakarta Sans','Segoe UI',sans-serif;color:#e0e6ff;}
h1,h2,h3{color:#ffffff!important;letter-spacing:-0.02em;}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"]{
    background:#0a0d20;border-radius:12px;padding:4px;gap:4px;
    border:1px solid rgba(255,255,255,0.07);
}
[data-testid="stTabs"] [data-baseweb="tab"]{
    background:transparent;border-radius:9px;color:rgba(224,230,255,0.5);
    font-weight:600;font-size:0.82rem;padding:6px 16px;
}
[data-testid="stTabs"] [aria-selected="true"]{
    background:linear-gradient(135deg,#3b82f6,#7c3aed)!important;
    color:#fff!important;
}

/* Inputs */
input,textarea{
    background:#10142e!important;color:#e0e6ff!important;
    border:1px solid rgba(255,255,255,0.10)!important;border-radius:10px!important;
    font-family:'Plus Jakarta Sans','Segoe UI',sans-serif!important;
}
input::placeholder,textarea::placeholder{color:rgba(224,230,255,0.3)!important;}
textarea:focus,input:focus{border-color:rgba(59,130,246,0.5)!important;box-shadow:0 0 0 3px rgba(59,130,246,0.10)!important;}

/* Buttons */
.stButton>button{
    background:linear-gradient(135deg,#3b82f6,#7c3aed)!important;
    color:#fff!important;border:none!important;border-radius:10px!important;
    font-weight:700!important;font-size:0.82rem!important;
    padding:0.45rem 1rem!important;
    box-shadow:0 4px 14px rgba(59,130,246,0.30)!important;
    transition:all .2s!important;width:100%;
    font-family:'Plus Jakarta Sans','Segoe UI',sans-serif!important;
}
.stButton>button:hover{transform:translateY(-1px)!important;box-shadow:0 6px 20px rgba(59,130,246,0.45)!important;}

/* Metrics */
[data-testid="stMetric"]{background:#0e1228;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:10px 14px!important;}
[data-testid="stMetricValue"]{color:#3b82f6!important;font-weight:800!important;font-size:1.4rem!important;}
[data-testid="stMetricLabel"]{color:rgba(224,230,255,0.4)!important;font-size:0.65rem!important;text-transform:uppercase;letter-spacing:0.08em;}

/* Divider */
hr{border-color:rgba(255,255,255,0.06)!important;}

/* Scrollbar */
::-webkit-scrollbar{width:3px;height:3px;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.10);border-radius:3px;}

/* Select box */
[data-testid="stSelectbox"] > div > div{
    background:#10142e!important;border:1px solid rgba(255,255,255,0.10)!important;
    border-radius:10px!important;color:#e0e6ff!important;
}

/* Number input */
[data-testid="stNumberInput"] input{text-align:left!important;}

/* Chat message bubble styles */
.chat-bubble-me {
    display:flex;justify-content:flex-end;margin-bottom:8px;
}
.chat-bubble-other {
    display:flex;justify-content:flex-start;margin-bottom:8px;
}
.bubble {
    max-width:75%;padding:8px 13px;border-radius:16px;
    font-size:0.82rem;line-height:1.45;word-break:break-word;
}
.bubble-me {
    background:linear-gradient(135deg,#3b82f6,#6d28d9);
    color:#fff;border-bottom-right-radius:4px;
}
.bubble-other {
    background:#161b38;border:1px solid rgba(255,255,255,0.08);
    color:#e0e6ff;border-bottom-left-radius:4px;
}
.bubble-time {
    font-size:0.6rem;color:rgba(224,230,255,0.3);
    margin-top:3px;text-align:right;
}
.bubble-time-left {text-align:left!important;}
.bubble-sender {
    font-size:0.65rem;font-weight:700;color:rgba(224,230,255,0.45);
    margin-bottom:3px;
}

/* Member card in chat list */
.chat-member-card {
    display:flex;align-items:center;gap:10px;
    padding:9px 12px;border-radius:12px;
    cursor:pointer;margin-bottom:4px;
    border:1px solid transparent;
    transition:all .2s;
}
.chat-member-card:hover{background:rgba(255,255,255,0.03);border-color:rgba(255,255,255,0.07);}
.chat-member-card.active-chat{background:rgba(59,130,246,0.08);border-color:rgba(59,130,246,0.22);}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
PALETTE = ["#10b981","#3b82f6","#06b6d4","#f59e0b","#ec4899","#a78bfa","#34d399","#fb923c"]
EMOJIS  = ["👩","👨","🧒","👧","👴","👵","👦","🧑","🧔","🧓"]
EMOJI_PICKER = ["😊","😂","❤️","👍","🙏","🔥","😍","🎉","😢","😮","👋","✅","📍","🏠","🚗","⚠️","🆘","💪","🥰","😎"]

# ─── SESSION STATE ───────────────────────────────────────────────────────────
def init_state():
    if "members" not in st.session_state:
        st.session_state.members = [
            {"id":1,"name":"Mom", "lat":17.4126,"lng":78.4482,"emoji":"👩","color":"#10b981","status":"online"},
            {"id":2,"name":"Dad", "lat":17.4435,"lng":78.3772,"emoji":"👨","color":"#3b82f6","status":"online"},
            {"id":3,"name":"Jake","lat":17.4399,"lng":78.4983,"emoji":"🧒","color":"#06b6d4","status":"online"},
            {"id":4,"name":"Lily","lat":17.4320,"lng":78.4510,"emoji":"👧","color":"#f59e0b","status":"away"},
        ]
    if "next_id"        not in st.session_state: st.session_state.next_id        = 5
    if "success"        not in st.session_state: st.session_state.success        = ""
    if "errors"         not in st.session_state: st.session_state.errors         = {}
    if "active_tab"     not in st.session_state: st.session_state.active_tab     = "map"
    if "active_chat_id" not in st.session_state: st.session_state.active_chat_id = 1
    if "my_name"        not in st.session_state: st.session_state.my_name        = "You"
    if "my_emoji"       not in st.session_state: st.session_state.my_emoji       = "🧑"

    # Per-member chat storage: {member_id: [{"sender","emoji","text","time"}]}
    if "chats" not in st.session_state:
        st.session_state.chats = {
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

    # Simulate live location drift
    if "last_update" not in st.session_state:
        st.session_state.last_update = time.time()

init_state()

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
    m = {"id":st.session_state.next_id,"name":name.strip(),
         "lat":round(lat,6),"lng":round(lng,6),
         "emoji":emoji,"color":color,"status":"online"}
    st.session_state.members.append(m)
    st.session_state.chats[m["id"]] = []
    st.session_state.next_id += 1
    return m

def remove_member(mid):
    st.session_state.members = [m for m in st.session_state.members if m["id"] != mid]
    st.session_state.chats.pop(mid, None)

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
    # Simulate auto-reply from member
    member   = next((m for m in st.session_state.members if m["id"] == member_id), None)
    replies  = ["👍","On my way! 🚗","Ok! 😊","Noted ✅","📍 Sharing location","Will be there soon!","❤️","Got it!","😂 Sure!"]
    if member and random.random() > 0.4:
        st.session_state.chats[member_id].append({
            "sender": member["name"],
            "emoji":  member["emoji"],
            "text":   random.choice(replies),
            "time":   now_time(),
            "me":     False,
        })

def simulate_location_drift():
    """Slightly move online members to simulate real-time GPS updates."""
    now = time.time()
    if now - st.session_state.last_update > 5:
        for m in st.session_state.members:
            if m["status"] == "online":
                m["lat"] += random.uniform(-0.0001, 0.0001)
                m["lng"] += random.uniform(-0.0001, 0.0001)
        st.session_state.last_update = now

simulate_location_drift()

# ─── MAP BUILDER ─────────────────────────────────────────────────────────────
def build_map():
    members = st.session_state.members
    center  = get_center(members)
    zoom    = get_zoom(members)

    fmap = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="CartoDB dark_matter",
        prefer_canvas=True,
    )

    if not members:
        return fmap

    if len(members) > 1:
        lats = [m["lat"] for m in members]
        lngs = [m["lng"] for m in members]
        fmap.fit_bounds([[min(lats),min(lngs)],[max(lats),max(lngs)]], padding=[60,60])

    for m in members:
        status_color = "#10b981" if m["status"]=="online" else "#f59e0b"
        icon_html = f"""
        <div style="display:flex;flex-direction:column;align-items:center;">
          <div style="background:rgba(6,8,24,0.93);border:2.5px solid {m['color']};
            border-radius:10px;padding:4px 10px;display:flex;align-items:center;gap:5px;
            white-space:nowrap;box-shadow:0 4px 18px rgba(0,0,0,0.6),0 0 12px {m['color']}66;
            font-family:Segoe UI,sans-serif;">
            <span style="font-size:1rem;">{m['emoji']}</span>
            <span style="font-size:0.72rem;font-weight:800;color:#fff;">{m['name']}</span>
            <span style="width:7px;height:7px;border-radius:50%;background:{status_color};
              box-shadow:0 0 6px {status_color};display:inline-block;"></span>
          </div>
          <div style="width:2px;height:10px;background:{m['color']};"></div>
          <div style="width:11px;height:11px;border-radius:50%;background:{m['color']};
            box-shadow:0 0 14px {m['color']};"></div>
        </div>"""

        msg_count = len(st.session_state.chats.get(m["id"], []))
        popup_html = f"""
        <div style="font-family:Segoe UI,sans-serif;padding:6px;min-width:175px;">
          <div style="text-align:center;font-size:1.5rem;margin-bottom:5px;">{m['emoji']}</div>
          <div style="font-weight:800;font-size:0.95rem;color:#fff;text-align:center;margin-bottom:8px;">{m['name']}</div>
          <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);margin-bottom:3px;">
            📍 <b style="color:#3b82f6;">Lat:</b> {m['lat']:.5f}
          </div>
          <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);margin-bottom:3px;">
            📍 <b style="color:#3b82f6;">Lng:</b> {m['lng']:.5f}
          </div>
          <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);margin-bottom:3px;">
            🟢 <b style="color:{status_color};">Status:</b> {m['status'].title()}
          </div>
          <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);">
            💬 <b style="color:#7c3aed;">Messages:</b> {msg_count}
          </div>
        </div>"""

        folium.Marker(
            location=[m["lat"], m["lng"]],
            popup=folium.Popup(popup_html, max_width=230),
            tooltip=f"{m['emoji']} {m['name']} • {m['status']}",
            icon=folium.DivIcon(html=icon_html, icon_size=(100,58), icon_anchor=(50,58)),
        ).add_to(fmap)

        folium.Circle(
            location=[m["lat"], m["lng"]],
            radius=120, color=m["color"],
            fill=True, fill_color=m["color"],
            fill_opacity=0.07, weight=1, dash_array="4 6",
        ).add_to(fmap)

    return fmap

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📡 FamilyTrack")
    st.markdown("<p style='font-size:0.68rem;color:rgba(224,230,255,0.3);margin-top:-10px;margin-bottom:12px;'>Live Location & Chat</p>", unsafe_allow_html=True)

    # Identity
    with st.expander("👤 My Profile", expanded=False):
        st.session_state.my_name  = st.text_input("Your Name",  value=st.session_state.my_name,  key="my_name_inp")
        st.session_state.my_emoji = st.selectbox("Your Avatar", EMOJIS, index=EMOJIS.index(st.session_state.my_emoji) if st.session_state.my_emoji in EMOJIS else 0, key="my_emoji_inp")

    st.divider()

    # Add Member
    with st.expander("➕ Add Member", expanded=False):
        name_val = st.text_input("Full Name *", placeholder="e.g. Priya",     key="inp_name")
        lat_val  = st.number_input("Latitude *",  value=17.4262, min_value=-90.0,  max_value=90.0,  step=0.0001, format="%.4f", key="inp_lat")
        lng_val  = st.number_input("Longitude *", value=78.4462, min_value=-180.0, max_value=180.0, step=0.0001, format="%.4f", key="inp_lng")
        c1, c2  = st.columns(2)
        with c1: emoji_val = st.selectbox("Avatar", EMOJIS, key="inp_emoji")
        with c2: color_val = st.color_picker("Color", value=PALETTE[len(st.session_state.members)%len(PALETTE)], key="inp_color")

        for err in st.session_state.errors.values():
            st.error(err)
        if st.session_state.success:
            st.success(st.session_state.success)
            st.session_state.success = ""

        if st.button("📍 Add to Map"):
            errs = validate_member(name_val, lat_val, lng_val)
            if errs:
                st.session_state.errors = errs
            else:
                st.session_state.errors = {}
                added = add_member(name_val, lat_val, lng_val, emoji_val, color_val)
                st.session_state.success = f"✅ {added['emoji']} **{added['name']}** added!"
            st.rerun()

    st.divider()

    # Members list with remove
    st.markdown(f"### 👨‍👩‍👧 Members ({len(st.session_state.members)})")
    for m in st.session_state.members:
        sc = "#10b981" if m["status"]=="online" else "#f59e0b"
        ca, cb = st.columns([3,1])
        with ca:
            st.markdown(
                f"<span style='font-size:0.88rem;'>**{m['emoji']} {m['name']}**</span> "
                f"<span style='width:6px;height:6px;border-radius:50%;background:{sc};display:inline-block;box-shadow:0 0 5px {sc};'></span><br>"
                f"<span style='font-size:0.65rem;color:rgba(224,230,255,0.35);font-family:monospace;'>{m['lat']:.4f}, {m['lng']:.4f}</span>",
                unsafe_allow_html=True)
        with cb:
            if st.button("✕", key=f"rm_{m['id']}"):
                remove_member(m["id"])
                st.rerun()

    st.divider()
    if st.button("🔄 Refresh"):
        st.rerun()

# ─── MAIN PAGE ───────────────────────────────────────────────────────────────
# Header
ha, hb = st.columns([5,1])
with ha:
    st.markdown("# 📡 FamilyTrack")
    st.markdown("<p style='color:rgba(224,230,255,0.4);font-size:0.82rem;margin-top:-12px;margin-bottom:8px;'>Live Location & Family Chat</p>", unsafe_allow_html=True)
with hb:
    st.markdown(
        "<div style='padding-top:16px;text-align:right;'>"
        "<span style='display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,0.10);"
        "border:1px solid rgba(16,185,129,0.25);border-radius:100px;padding:4px 12px;'>"
        "<span style='width:7px;height:7px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;display:inline-block;'></span>"
        "<span style='font-size:0.7rem;font-weight:800;color:#10b981;'>LIVE</span></span></div>",
        unsafe_allow_html=True)

# Metrics
members = st.session_state.members
online  = sum(1 for m in members if m["status"]=="online")
away    = sum(1 for m in members if m["status"]=="away")
total_msgs = sum(len(v) for v in st.session_state.chats.values())

m1,m2,m3,m4 = st.columns(4)
m1.metric("👥 Members",     len(members))
m2.metric("🟢 Online",      online)
m3.metric("🟡 Away",        away)
m4.metric("💬 Messages",    total_msgs)

st.divider()

# ─── TABS: MAP | CHAT ────────────────────────────────────────────────────────
tab_map, tab_chat = st.tabs(["🗺️  Live Map", "💬  Family Chat"])

# ════════════════ MAP TAB ════════════════
with tab_map:
    if not members:
        st.info("👆 Add family members from the sidebar to see them on the map.")
    else:
        fmap     = build_map()
        map_data = st_folium(
            fmap,
            use_container_width=True,
            height=600,
            returned_objects=["last_clicked"],
            key="familymap",
        )
        if map_data and map_data.get("last_clicked"):
            lc = map_data["last_clicked"]
            st.caption(f"📍 Clicked: **{lc['lat']:.5f}, {lc['lng']:.5f}** — copy to sidebar to add a member here.")

        # Live location table
        st.markdown("#### 📋 Live Locations")
        hdr = st.columns([1,3,2,2,2])
        for col,lbl in zip(hdr,["","Name","Latitude","Longitude","Status"]):
            col.markdown(f"**{lbl}**")
        st.markdown("<hr style='margin:3px 0 6px;border-color:rgba(255,255,255,0.06);'/>", unsafe_allow_html=True)
        for m in members:
            sc = "#10b981" if m["status"]=="online" else "#f59e0b"
            st_lbl = "🟢 Online" if m["status"]=="online" else "🟡 Away"
            c0,c1,c2,c3,c4 = st.columns([1,3,2,2,2])
            c0.markdown(f"<div style='font-size:1.3rem'>{m['emoji']}</div>", unsafe_allow_html=True)
            c1.markdown(f"**{m['name']}**")
            c2.markdown(f"<code style='color:#3b82f6;background:rgba(59,130,246,0.08);padding:2px 6px;border-radius:5px;font-size:0.75rem;'>{m['lat']:.5f}</code>", unsafe_allow_html=True)
            c3.markdown(f"<code style='color:#3b82f6;background:rgba(59,130,246,0.08);padding:2px 6px;border-radius:5px;font-size:0.75rem;'>{m['lng']:.5f}</code>", unsafe_allow_html=True)
            c4.markdown(f"<span style='background:rgba({','.join(str(int(sc.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.12);border:1px solid {sc}44;color:{sc};font-size:0.65rem;font-weight:800;padding:2px 9px;border-radius:100px;'>{st_lbl}</span>", unsafe_allow_html=True)

# ════════════════ CHAT TAB ════════════════
with tab_chat:
    if not members:
        st.info("👆 Add family members first to start chatting with them.")
    else:
        chat_left, chat_right = st.columns([1, 2.8], gap="medium")

        # ── Chat member list (left)
        with chat_left:
            st.markdown("#### 💬 Conversations")
            for m in members:
                msgs      = st.session_state.chats.get(m["id"], [])
                unread    = len(msgs)
                sc        = "#10b981" if m["status"]=="online" else "#f59e0b"
                last_msg  = msgs[-1]["text"][:28]+"…" if msgs else "No messages yet"
                is_active = m["id"] == st.session_state.active_chat_id
                card_bg   = "rgba(59,130,246,0.08)" if is_active else "transparent"
                card_bd   = "rgba(59,130,246,0.25)" if is_active else "rgba(255,255,255,0.06)"

                st.markdown(
                    f"""<div style="background:{card_bg};border:1px solid {card_bd};
                    border-radius:12px;padding:10px 12px;margin-bottom:6px;cursor:pointer;">
                    <div style="display:flex;align-items:center;gap:8px;">
                      <div style="position:relative;flex-shrink:0;">
                        <span style="font-size:1.4rem;">{m['emoji']}</span>
                        <span style="position:absolute;bottom:-1px;right:-3px;width:9px;height:9px;
                          border-radius:50%;background:{sc};border:2px solid #0a0d20;display:block;
                          box-shadow:0 0 5px {sc};"></span>
                      </div>
                      <div style="flex:1;min-width:0;">
                        <div style="font-weight:700;font-size:0.82rem;">{m['name']}</div>
                        <div style="font-size:0.65rem;color:rgba(224,230,255,0.35);
                          white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{last_msg}</div>
                      </div>
                      <div style="background:linear-gradient(135deg,#3b82f6,#7c3aed);color:#fff;
                        font-size:0.6rem;font-weight:800;padding:2px 7px;border-radius:100px;">{unread}</div>
                    </div></div>""",
                    unsafe_allow_html=True)

                if st.button(f"Open", key=f"chat_open_{m['id']}", help=f"Chat with {m['name']}"):
                    st.session_state.active_chat_id = m["id"]
                    st.rerun()

        # ── Active chat window (right)
        with chat_right:
            active_member = next((m for m in members if m["id"] == st.session_state.active_chat_id), members[0])
            sc = "#10b981" if active_member["status"]=="online" else "#f59e0b"
            st_lbl = "Online" if active_member["status"]=="online" else "Away"

            # Chat header
            st.markdown(
                f"""<div style="background:#0e1228;border:1px solid rgba(255,255,255,0.07);
                border-radius:14px;padding:12px 16px;margin-bottom:12px;
                display:flex;align-items:center;gap:12px;">
                  <span style="font-size:1.8rem;">{active_member['emoji']}</span>
                  <div>
                    <div style="font-weight:800;font-size:0.95rem;">{active_member['name']}</div>
                    <div style="font-size:0.68rem;color:{sc};font-weight:600;display:flex;align-items:center;gap:5px;">
                      <span style="width:6px;height:6px;border-radius:50%;background:{sc};
                        box-shadow:0 0 6px {sc};display:inline-block;"></span>{st_lbl}
                      &nbsp;·&nbsp;
                      <span style="color:rgba(224,230,255,0.35);">
                        📍 {active_member['lat']:.4f}, {active_member['lng']:.4f}
                      </span>
                    </div>
                  </div>
                </div>""",
                unsafe_allow_html=True)

            # Message history
            msgs = st.session_state.chats.get(active_member["id"], [])
            chat_html = "<div style='height:360px;overflow-y:auto;padding:4px 2px;display:flex;flex-direction:column;gap:2px;'>"
            for msg in msgs:
                if msg["me"]:
                    chat_html += f"""
                    <div style="display:flex;justify-content:flex-end;margin-bottom:6px;">
                      <div style="max-width:72%;">
                        <div style="background:linear-gradient(135deg,#3b82f6,#6d28d9);color:#fff;
                          padding:8px 13px;border-radius:16px 16px 4px 16px;
                          font-size:0.82rem;line-height:1.45;word-break:break-word;
                          box-shadow:0 2px 12px rgba(59,130,246,0.25);">{msg['text']}</div>
                        <div style="font-size:0.6rem;color:rgba(224,230,255,0.28);text-align:right;margin-top:3px;">{msg['time']}</div>
                      </div>
                    </div>"""
                else:
                    chat_html += f"""
                    <div style="display:flex;justify-content:flex-start;margin-bottom:6px;gap:7px;align-items:flex-end;">
                      <span style="font-size:1.1rem;flex-shrink:0;">{msg['emoji']}</span>
                      <div style="max-width:72%;">
                        <div style="font-size:0.62rem;font-weight:700;color:rgba(224,230,255,0.4);margin-bottom:3px;">{msg['sender']}</div>
                        <div style="background:#161b38;border:1px solid rgba(255,255,255,0.08);color:#e0e6ff;
                          padding:8px 13px;border-radius:16px 16px 16px 4px;
                          font-size:0.82rem;line-height:1.45;word-break:break-word;">{msg['text']}</div>
                        <div style="font-size:0.6rem;color:rgba(224,230,255,0.28);margin-top:3px;">{msg['time']}</div>
                      </div>
                    </div>"""
            chat_html += "</div>"
            st.markdown(chat_html, unsafe_allow_html=True)

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

            # Emoji quick-picker row
            st.markdown("<div style='font-size:0.65rem;color:rgba(224,230,255,0.3);margin-bottom:4px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;'>Quick Emoji</div>", unsafe_allow_html=True)
            emoji_cols = st.columns(len(EMOJI_PICKER))
            for i, emo in enumerate(EMOJI_PICKER):
                with emoji_cols[i]:
                    if st.button(emo, key=f"emo_{active_member['id']}_{i}"):
                        send_message(active_member["id"], emo)
                        st.rerun()

            # Text input + send
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            msg_col, btn_col = st.columns([5, 1])
            with msg_col:
                msg_text = st.text_input(
                    "Type a message…",
                    placeholder=f"Message {active_member['name']}…",
                    key=f"msg_inp_{active_member['id']}",
                    label_visibility="collapsed",
                )
            with btn_col:
                if st.button("Send ➤", key=f"send_{active_member['id']}"):
                    if msg_text and msg_text.strip():
                        send_message(active_member["id"], msg_text.strip())
                        st.rerun()

            # Location share button
            if st.button(f"📍 Share My Location with {active_member['name']}", key=f"loc_{active_member['id']}"):
                my_lat = active_member["lat"] + random.uniform(-0.002, 0.002)
                my_lng = active_member["lng"] + random.uniform(-0.002, 0.002)
                send_message(active_member["id"], f"📍 My location: {my_lat:.5f}, {my_lng:.5f}")
                st.rerun()

st.divider()
st.markdown(
    "<div style='text-align:center;font-size:0.68rem;color:rgba(224,230,255,0.15);padding-bottom:6px;'>"
    "Built with ❤️ by Team AKSHAYY &nbsp;·&nbsp; FamilyTrack © 2025</div>",
    unsafe_allow_html=True)