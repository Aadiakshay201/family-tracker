import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FamilyTrack – Live Location",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="collapsedControl"],[data-testid="stSidebar"]{display:none!important;}
[data-testid="stAppViewContainer"]{background:#0b0d1a!important;}
.block-container{padding:0!important;max-width:100%!important;}
iframe{border:none!important;display:block!important;}
</style>
""", unsafe_allow_html=True)

components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>FamilyTrack</title>

<!-- Leaflet real map -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>

<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:       #0b0d1a;
  --surface:  #111425;
  --card:     #161929;
  --border:   rgba(255,255,255,0.07);
  --blue:     #4f8cff;
  --indigo:   #6c63ff;
  --cyan:     #00d4ff;
  --green:    #00e676;
  --amber:    #ffb347;
  --red:      #ff5c5c;
  --text:     #e8ecff;
  --muted:    rgba(232,236,255,0.40);
  --dimmed:   rgba(232,236,255,0.18);
}

html,body{
  height:100%; width:100%;
  background:var(--bg);
  color:var(--text);
  font-family:'Outfit',sans-serif;
  overflow:hidden;
}

/* ═══════════════════════════════════════ TOPBAR */
#topbar{
  position:fixed; top:0; left:0; right:0; z-index:1000;
  height:58px;
  background:rgba(11,13,26,0.92);
  backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);
  display:flex; align-items:center; justify-content:space-between;
  padding:0 20px;
}

.tb-left{display:flex;align-items:center;gap:14px;}
.brand{
  display:flex;align-items:center;gap:9px;
  font-size:1.15rem;font-weight:800;letter-spacing:-.02em;
}
.brand-icon{
  width:34px;height:34px;border-radius:10px;
  background:linear-gradient(135deg,var(--blue),var(--indigo));
  display:flex;align-items:center;justify-content:center;
  font-size:1rem;
  box-shadow:0 4px 16px rgba(79,140,255,0.4);
}
.brand-name{
  background:linear-gradient(135deg,#fff 0%,var(--cyan) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}

.live-pill{
  display:flex;align-items:center;gap:6px;
  background:rgba(0,230,118,0.10);
  border:1px solid rgba(0,230,118,0.25);
  border-radius:100px; padding:4px 12px;
  font-size:.72rem; font-weight:600; color:var(--green);
  letter-spacing:.06em; text-transform:uppercase;
}
.live-dot{
  width:6px;height:6px;border-radius:50%;background:var(--green);
  box-shadow:0 0 8px var(--green);
  animation:pulse-dot 1.4s ease-in-out infinite;
}
@keyframes pulse-dot{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.4;transform:scale(.7);}}

.tb-right{display:flex;align-items:center;gap:10px;}
.tb-btn{
  border:1px solid var(--border);background:var(--card);
  color:var(--text);border-radius:10px;padding:6px 14px;
  font-family:'Outfit',sans-serif;font-size:.82rem;font-weight:600;
  cursor:pointer;transition:all .2s;display:flex;align-items:center;gap:6px;
}
.tb-btn:hover{background:rgba(79,140,255,0.12);border-color:rgba(79,140,255,0.35);color:#fff;}
.tb-btn-primary{
  background:linear-gradient(135deg,var(--blue),var(--indigo));
  border-color:transparent;color:#fff;
  box-shadow:0 4px 16px rgba(79,140,255,0.35);
}
.tb-btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 24px rgba(79,140,255,0.5);}
.tb-btn-sos{background:rgba(255,92,92,0.12);border-color:rgba(255,92,92,0.3);color:var(--red);}
.tb-btn-sos:hover{background:rgba(255,92,92,0.25);}

/* ═══════════════════════════════════════ LAYOUT */
#layout{
  position:fixed; top:58px; left:0; right:0; bottom:0;
  display:grid;
  grid-template-columns:310px 1fr 280px;
}

/* ═══════════════════════════════════════ LEFT PANEL */
#left{
  background:var(--surface);
  border-right:1px solid var(--border);
  display:flex;flex-direction:column;
  overflow:hidden;
}

.panel-head{
  padding:16px 18px 12px;
  border-bottom:1px solid var(--border);
  font-size:.68rem;font-weight:700;letter-spacing:.14em;
  text-transform:uppercase;color:var(--dimmed);
  display:flex;align-items:center;justify-content:space-between;
}
.panel-head-action{
  background:rgba(79,140,255,0.12);border:1px solid rgba(79,140,255,0.25);
  color:var(--blue);border-radius:7px;padding:3px 10px;
  font-size:.7rem;font-weight:600;cursor:pointer;
  font-family:'Outfit',sans-serif;
  transition:all .2s;text-transform:none;letter-spacing:0;
}
.panel-head-action:hover{background:rgba(79,140,255,0.22);}

/* Metrics */
.metrics-grid{
  display:grid;grid-template-columns:1fr 1fr;
  gap:8px;padding:14px 14px 10px;
}
.metric{
  background:var(--card);border:1px solid var(--border);
  border-radius:12px;padding:10px 12px;
  display:flex;flex-direction:column;gap:2px;
}
.metric-val{
  font-family:'JetBrains Mono',monospace;
  font-size:1.5rem;font-weight:600;line-height:1;
}
.metric-lbl{font-size:.67rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-top:3px;}
.val-green{color:var(--green);}
.val-amber{color:var(--amber);}
.val-red{color:var(--red);}
.val-blue{color:var(--blue);}

/* Members */
.members-scroll{flex:1;overflow-y:auto;padding:6px 10px;}
.members-scroll::-webkit-scrollbar{width:3px;}
.members-scroll::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px;}

.member-card{
  display:flex;align-items:center;gap:11px;
  padding:10px 10px;border-radius:13px;
  cursor:pointer;transition:all .2s;
  border:1px solid transparent;margin-bottom:5px;
}
.member-card:hover{background:rgba(255,255,255,.04);border-color:var(--border);}
.member-card.active{background:rgba(79,140,255,0.09);border-color:rgba(79,140,255,0.28);}

.avatar{
  width:42px;height:42px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:1.35rem;flex-shrink:0;position:relative;
  border:2px solid transparent;
}
.avatar-online{border-color:var(--green);box-shadow:0 0 10px rgba(0,230,118,.25);}
.avatar-idle{border-color:var(--amber);box-shadow:0 0 10px rgba(255,179,71,.2);}
.avatar-offline{border-color:#444;}
.status-ring{
  position:absolute;bottom:0;right:0;
  width:11px;height:11px;border-radius:50%;
  border:2px solid var(--surface);
}
.ring-online{background:var(--green);}
.ring-idle{background:var(--amber);}
.ring-offline{background:#555;}

.m-info{flex:1;min-width:0;}
.m-name{font-weight:700;font-size:.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.m-place{font-size:.75rem;color:var(--muted);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.m-time{font-size:.68rem;color:var(--dimmed);margin-top:2px;}
.m-badge{
  font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:100px;
  white-space:nowrap;flex-shrink:0;
}
.badge-online{background:rgba(0,230,118,.12);color:var(--green);}
.badge-idle{background:rgba(255,179,71,.12);color:var(--amber);}
.badge-offline{background:rgba(80,80,80,.3);color:#888;}

/* Alerts section */
.alerts-wrap{
  border-top:1px solid var(--border);
  padding:10px 12px 12px;
  max-height:200px;overflow-y:auto;
}
.alerts-wrap::-webkit-scrollbar{width:3px;}
.alerts-wrap::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px;}
.alert-item{
  display:flex;gap:9px;align-items:flex-start;
  padding:8px 9px;border-radius:10px;margin-bottom:5px;
  font-size:.78rem;cursor:pointer;transition:all .15s;
}
.alert-item:hover{filter:brightness(1.2);}
.ai-blue{background:rgba(79,140,255,.07);border:1px solid rgba(79,140,255,.15);}
.ai-amber{background:rgba(255,179,71,.07);border:1px solid rgba(255,179,71,.15);}
.ai-green{background:rgba(0,230,118,.07);border:1px solid rgba(0,230,118,.15);}
.ai-red{background:rgba(255,92,92,.07);border:1px solid rgba(255,92,92,.15);}
.alert-body{flex:1;}
.alert-msg{color:var(--text);line-height:1.35;}
.alert-t{font-size:.66rem;color:var(--dimmed);margin-top:2px;}

/* ═══════════════════════════════════════ MAP */
#map-wrap{position:relative;overflow:hidden;}
#map{width:100%;height:100%;}

/* Leaflet dark override */
.leaflet-tile-pane{filter:brightness(.75) contrast(1.1) saturate(.85) hue-rotate(195deg);}
.leaflet-layer{filter:none!important;}

/* Map overlay controls */
.map-top{
  position:absolute;top:14px;left:14px;z-index:500;
  display:flex;align-items:center;gap:8px;
}
.map-search-box{
  background:rgba(11,13,26,0.88);backdrop-filter:blur(16px);
  border:1px solid var(--border);border-radius:11px;
  padding:7px 14px;display:flex;align-items:center;gap:8px;
  font-size:.83rem;color:var(--muted);min-width:220px;
  box-shadow:0 4px 20px rgba(0,0,0,.4);
}
.map-filter-btn{
  background:rgba(11,13,26,0.88);backdrop-filter:blur(16px);
  border:1px solid var(--border);border-radius:11px;
  padding:7px 12px;color:var(--text);font-size:.78rem;font-weight:600;
  cursor:pointer;font-family:'Outfit',sans-serif;
  box-shadow:0 4px 20px rgba(0,0,0,.4);transition:all .2s;
  display:flex;align-items:center;gap:5px;
}
.map-filter-btn:hover{border-color:rgba(79,140,255,.4);color:var(--blue);}
.map-filter-btn.active-f{background:rgba(79,140,255,.15);border-color:rgba(79,140,255,.35);color:var(--blue);}

.map-zoom-ctrl{
  position:absolute;right:14px;bottom:100px;z-index:500;
  display:flex;flex-direction:column;gap:4px;
}
.mzc-btn{
  width:34px;height:34px;background:rgba(11,13,26,0.88);backdrop-filter:blur(16px);
  border:1px solid var(--border);border-radius:9px;
  color:var(--text);font-size:1.1rem;cursor:pointer;
  display:flex;align-items:center;justify-content:center;transition:all .2s;
  box-shadow:0 4px 14px rgba(0,0,0,.3);
}
.mzc-btn:hover{background:rgba(79,140,255,.2);border-color:rgba(79,140,255,.4);}

.map-legend{
  position:absolute;bottom:14px;left:14px;z-index:500;
  background:rgba(11,13,26,0.88);backdrop-filter:blur(16px);
  border:1px solid var(--border);border-radius:12px;padding:10px 14px;
  font-size:.73rem;box-shadow:0 4px 20px rgba(0,0,0,.4);
}
.leg-row{display:flex;align-items:center;gap:7px;color:var(--muted);margin-bottom:5px;}
.leg-row:last-child{margin-bottom:0;}
.leg-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0;}
.leg-zone{width:16px;height:9px;border-radius:4px;opacity:.7;flex-shrink:0;}

/* ═══════════════════════════════════════ RIGHT PANEL */
#right{
  background:var(--surface);
  border-left:1px solid var(--border);
  display:flex;flex-direction:column;
  overflow:hidden;
}

/* Detail card */
#detail-card{
  padding:16px;
  border-bottom:1px solid var(--border);
}
.dc-header{
  background:linear-gradient(135deg,rgba(79,140,255,.12),rgba(108,99,255,.08));
  border:1px solid rgba(79,140,255,.2);
  border-radius:16px;padding:16px;text-align:center;margin-bottom:12px;
}
.dc-avatar{font-size:2.8rem;margin-bottom:6px;}
.dc-name{font-size:1.05rem;font-weight:800;letter-spacing:-.01em;}
.dc-place{font-size:.78rem;color:var(--muted);margin-top:4px;}
.dc-status{display:flex;align-items:center;justify-content:center;gap:5px;font-size:.75rem;color:var(--green);margin-top:6px;font-weight:600;}

.dc-stats{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.dc-stat{
  background:var(--card);border:1px solid var(--border);
  border-radius:10px;padding:8px 10px;text-align:center;
}
.dcs-n{font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:600;color:#fff;}
.dcs-l{font-size:.63rem;color:var(--dimmed);text-transform:uppercase;letter-spacing:.07em;margin-top:2px;}

.dc-actions{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:10px;}
.dca-btn{
  border:1px solid var(--border);background:var(--card);
  color:var(--text);border-radius:10px;padding:8px;
  font-family:'Outfit',sans-serif;font-size:.78rem;font-weight:600;
  cursor:pointer;transition:all .2s;display:flex;align-items:center;justify-content:center;gap:5px;
}
.dca-btn:hover{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.15);}
.dca-primary{background:linear-gradient(135deg,var(--blue),var(--indigo));border-color:transparent;color:#fff;}
.dca-primary:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(79,140,255,.35);}

/* Timeline */
#timeline-wrap{
  flex:1;overflow-y:auto;padding:12px 14px;
}
#timeline-wrap::-webkit-scrollbar{width:3px;}
#timeline-wrap::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px;}
.tl-item{position:relative;padding-left:22px;padding-bottom:14px;}
.tl-item::before{
  content:'';position:absolute;left:5px;top:12px;bottom:0;
  width:1px;background:var(--border);
}
.tl-item:last-child::before{display:none;}
.tl-dot{
  position:absolute;left:0;top:5px;
  width:12px;height:12px;border-radius:50%;
  border:2px solid var(--surface);
}
.tl-text{font-size:.78rem;color:rgba(232,236,255,.65);line-height:1.4;}
.tl-text strong{color:var(--text);}
.tl-time{font-size:.66rem;color:var(--dimmed);margin-top:2px;}

/* Safe zones panel */
#zones-wrap{
  border-top:1px solid var(--border);
  padding:12px 14px;
}
.zone-item{
  display:flex;align-items:center;gap:9px;
  background:var(--card);border:1px solid var(--border);
  border-radius:10px;padding:8px 10px;margin-bottom:5px;
  font-size:.78rem;cursor:pointer;transition:all .2s;
}
.zone-item:hover{border-color:rgba(79,140,255,.3);}
.zone-icon{width:28px;height:28px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:.9rem;flex-shrink:0;}
.zone-info{flex:1;}
.zone-name{font-weight:600;font-size:.8rem;}
.zone-addr{font-size:.68rem;color:var(--muted);}
.zone-status{font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:100px;}
.zs-active{background:rgba(0,230,118,.12);color:var(--green);}

.add-zone-btn{
  width:100%;border:1px dashed rgba(79,140,255,.25);background:transparent;
  color:var(--blue);border-radius:10px;padding:7px;
  font-family:'Outfit',sans-serif;font-size:.78rem;font-weight:600;
  cursor:pointer;transition:all .2s;margin-top:4px;
}
.add-zone-btn:hover{background:rgba(79,140,255,.08);}

/* ═══════════════════════════════════════ Leaflet custom markers */
.custom-marker{
  background:transparent;border:none;
}
.marker-wrap{
  display:flex;flex-direction:column;align-items:center;
  cursor:pointer;
}
.marker-bubble{
  background:rgba(11,13,26,.92);
  backdrop-filter:blur(10px);
  border:2px solid;
  border-radius:12px;
  padding:4px 8px;
  display:flex;align-items:center;gap:5px;
  box-shadow:0 4px 20px rgba(0,0,0,.5);
  white-space:nowrap;
  font-family:'Outfit',sans-serif;
}
.marker-emoji{font-size:1.1rem;}
.marker-name{font-size:.72rem;font-weight:700;color:#fff;}
.marker-tail{
  width:2px;height:10px;margin-top:-1px;
}
.marker-dot{
  width:10px;height:10px;border-radius:50%;
  margin-top:-1px;
  box-shadow:0 0 12px currentColor;
}
.pulse-ring{
  position:absolute;
  width:30px;height:30px;border-radius:50%;
  border:2px solid;
  animation:expand 2s ease-out infinite;
  opacity:0;
  transform:translate(-50%,-50%);
  pointer-events:none;
}
@keyframes expand{
  0%{transform:translate(-50%,-50%) scale(.3);opacity:.8;}
  100%{transform:translate(-50%,-50%) scale(2.5);opacity:0;}
}

/* Zone circle popup */
.leaflet-popup-content-wrapper{
  background:rgba(17,20,37,.95);
  backdrop-filter:blur(14px);
  border:1px solid var(--border);
  border-radius:12px;
  color:var(--text);
  font-family:'Outfit',sans-serif;
  box-shadow:0 8px 32px rgba(0,0,0,.5);
}
.leaflet-popup-tip{background:rgba(17,20,37,.95);}
.leaflet-popup-content{margin:10px 14px!important;font-size:.82rem;}

/* Animate in */
@keyframes slide-in-left{from{transform:translateX(-20px);opacity:0;}to{transform:translateX(0);opacity:1;}}
@keyframes slide-in-right{from{transform:translateX(20px);opacity:0;}to{transform:translateX(0);opacity:1;}}
#left{animation:slide-in-left .4s ease;}
#right{animation:slide-in-right .4s ease;}
</style>
</head>
<body>

<!-- TOP BAR -->
<div id="topbar">
  <div class="tb-left">
    <div class="brand">
      <div class="brand-icon">📡</div>
      <span class="brand-name">FamilyTrack</span>
    </div>
    <div class="live-pill"><span class="live-dot"></span>Live</div>
  </div>
  <div class="tb-right">
    <select id="circle-sel" style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:6px 12px;color:var(--text);font-family:'Outfit',sans-serif;font-size:.82rem;cursor:pointer;">
      <option>👨‍👩‍👧‍👦 Johnson Family</option>
      <option>👴 Extended Circle</option>
    </select>
    <button class="tb-btn" onclick="sendCheckin()">📲 Check-In</button>
    <button class="tb-btn tb-btn-sos" onclick="triggerSOS()">🚨 SOS</button>
    <button class="tb-btn tb-btn-primary">+ Add Member</button>
  </div>
</div>

<!-- LAYOUT -->
<div id="layout">

  <!-- LEFT PANEL -->
  <div id="left">
    <!-- Metrics -->
    <div class="panel-head">
      Family Overview
      <button class="panel-head-action" onclick="refreshAll()">↺ Refresh</button>
    </div>
    <div class="metrics-grid">
      <div class="metric"><div class="metric-val val-blue" id="m-total">4</div><div class="metric-lbl">Members</div></div>
      <div class="metric"><div class="metric-val val-green" id="m-online">3</div><div class="metric-lbl">Online</div></div>
      <div class="metric"><div class="metric-val val-amber" id="m-away">1</div><div class="metric-lbl">Away</div></div>
      <div class="metric"><div class="metric-val val-red" id="m-sos">0</div><div class="metric-lbl">SOS Active</div></div>
    </div>

    <!-- Members -->
    <div class="panel-head">Members</div>
    <div class="members-scroll" id="members-list">
      <!-- injected by JS -->
    </div>

    <!-- Alerts -->
    <div class="panel-head" style="border-top:1px solid var(--border);">Recent Activity</div>
    <div class="alerts-wrap" id="alerts-list">
      <!-- injected by JS -->
    </div>
  </div>

  <!-- MAP -->
  <div id="map-wrap">
    <div id="map"></div>

    <!-- Map overlay -->
    <div class="map-top">
      <div class="map-search-box">🔍&nbsp; Search location…</div>
      <button class="map-filter-btn active-f" onclick="toggleFilter(this,'all')">All Members</button>
      <button class="map-filter-btn" onclick="toggleFilter(this,'zones')">Safe Zones</button>
      <button class="map-filter-btn" onclick="toggleFilter(this,'routes')">Routes</button>
    </div>

    <div class="map-zoom-ctrl">
      <button class="mzc-btn" onclick="MAP.zoomIn()">+</button>
      <button class="mzc-btn" onclick="MAP.zoomOut()">−</button>
      <button class="mzc-btn" onclick="fitAll()" title="Fit all members">⊙</button>
    </div>

    <div class="map-legend">
      <div class="leg-row"><div class="leg-dot" style="background:var(--green)"></div>Online</div>
      <div class="leg-row"><div class="leg-dot" style="background:var(--amber)"></div>Away</div>
      <div class="leg-row"><div class="leg-zone" style="background:var(--blue)"></div>Safe Zone</div>
    </div>
  </div>

  <!-- RIGHT PANEL -->
  <div id="right">

    <!-- Detail card -->
    <div id="detail-card">
      <div class="panel-head" style="border-bottom:none;padding:0 0 10px;">Selected Member</div>
      <div class="dc-header">
        <div class="dc-avatar" id="dc-avatar">👩</div>
        <div class="dc-name" id="dc-name">Mom</div>
        <div class="dc-place" id="dc-place">📍 Home · Banjara Hills</div>
        <div class="dc-status"><span style="width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block;box-shadow:0 0 6px var(--green);"></span>Online · Active</div>
      </div>
      <div class="dc-stats">
        <div class="dc-stat"><div class="dcs-n" id="dc-speed">0.0</div><div class="dcs-l">km/h</div></div>
        <div class="dc-stat"><div class="dcs-n" id="dc-battery">98%</div><div class="dcs-l">Battery</div></div>
        <div class="dc-stat"><div class="dcs-n" id="dc-accuracy">±3m</div><div class="dcs-l">Accuracy</div></div>
        <div class="dc-stat"><div class="dcs-n" id="dc-checkins">5</div><div class="dcs-l">Check-ins</div></div>
      </div>
      <div class="dc-actions">
        <button class="dca-btn" onclick="alert('Calling…')">📞 Call</button>
        <button class="dca-btn dca-primary" onclick="alert('Message sent!')">💬 Message</button>
      </div>
    </div>

    <!-- Timeline -->
    <div class="panel-head" style="border-top:none;">Today's Timeline</div>
    <div id="timeline-wrap">
      <!-- injected by JS -->
    </div>

    <!-- Safe zones -->
    <div id="zones-wrap">
      <div class="panel-head" style="padding:0 0 10px;border-bottom:none;">Safe Zones</div>
      <div class="zone-item"><div class="zone-icon" style="background:rgba(0,230,118,.12);">🏠</div><div class="zone-info"><div class="zone-name">Home</div><div class="zone-addr">Banjara Hills, Hyderabad</div></div><span class="zone-status zs-active">Active</span></div>
      <div class="zone-item"><div class="zone-icon" style="background:rgba(79,140,255,.12);">🏫</div><div class="zone-info"><div class="zone-name">School</div><div class="zone-addr">DPS, Secunderabad</div></div><span class="zone-status zs-active">Active</span></div>
      <div class="zone-item"><div class="zone-icon" style="background:rgba(108,99,255,.12);">🏢</div><div class="zone-info"><div class="zone-name">Work</div><div class="zone-addr">HITEC City, Hyderabad</div></div><span class="zone-status zs-active">Active</span></div>
      <button class="add-zone-btn">+ Add Safe Zone</button>
    </div>
  </div>
</div>

<script>
// ═══════════════════════════════════════════ DATA
const MEMBERS = [
  {
    id:0, emoji:'👩', name:'Mom', status:'online',
    lat:17.4126, lng:78.4482,  // Banjara Hills
    place:'Home · Banjara Hills', timeAgo:'Just now',
    speed:0, battery:'97%', accuracy:'±2m', checkins:5,
    color:'#00e676', zoneColor:'rgba(0,230,118,',
    timeline:[
      {dot:'#00e676',text:'Arrived at <strong>Home</strong>',time:'10:45 AM'},
      {dot:'#4f8cff',text:'Left <strong>Grocery Store</strong>',time:'10:18 AM'},
      {dot:'#4f8cff',text:'Arrived at <strong>Grocery Store</strong>',time:'9:52 AM'},
      {dot:'#4f8cff',text:'Left <strong>Home</strong>',time:'9:30 AM'},
      {dot:'#00e676',text:'Device came <strong>online</strong>',time:'7:05 AM'},
    ]
  },
  {
    id:1, emoji:'👨', name:'Dad', status:'online',
    lat:17.4435, lng:78.3772,  // HITEC City
    place:'Work · HITEC City', timeAgo:'2 min ago',
    speed:0, battery:'62%', accuracy:'±4m', checkins:3,
    color:'#4f8cff', zoneColor:'rgba(79,140,255,',
    timeline:[
      {dot:'#4f8cff',text:'Arrived at <strong>HITEC City</strong>',time:'9:10 AM'},
      {dot:'#4f8cff',text:'Left <strong>Home</strong>',time:'8:35 AM'},
      {dot:'#00e676',text:'Device came <strong>online</strong>',time:'7:00 AM'},
    ]
  },
  {
    id:2, emoji:'🧒', name:'Jake', status:'online',
    lat:17.4399, lng:78.4983,  // Secunderabad
    place:'School · DPS Secunderabad', timeAgo:'5 min ago',
    speed:0, battery:'81%', accuracy:'±3m', checkins:2,
    color:'#00d4ff', zoneColor:'rgba(0,212,255,',
    timeline:[
      {dot:'#00d4ff',text:'Arrived at <strong>DPS School</strong>',time:'8:20 AM'},
      {dot:'#4f8cff',text:'Left <strong>Home</strong>',time:'7:55 AM'},
      {dot:'#00e676',text:'Device came <strong>online</strong>',time:'7:10 AM'},
    ]
  },
  {
    id:3, emoji:'👧', name:'Lily', status:'idle',
    lat:17.4320, lng:78.4510,  // Jubilee Hills
    place:'Jubilee Hills (last seen)', timeAgo:'41 min ago',
    speed:0, battery:'34%', accuracy:'±8m', checkins:1,
    color:'#ffb347', zoneColor:'rgba(255,179,71,',
    timeline:[
      {dot:'#ffb347',text:'Last seen near <strong>Jubilee Hills</strong>',time:'10:02 AM'},
      {dot:'#4f8cff',text:'Left <strong>Home</strong>',time:'9:15 AM'},
      {dot:'#00e676',text:'Device came <strong>online</strong>',time:'7:22 AM'},
    ]
  }
];

const SAFE_ZONES = [
  {lat:17.4126,lng:78.4482,radius:400,label:'Home',   color:'#00e676'},
  {lat:17.4399,lng:78.4983,radius:350,label:'School', color:'#4f8cff'},
  {lat:17.4435,lng:78.3772,radius:350,label:'Work',   color:'#6c63ff'},
];

const ALERTS = [
  {cls:'ai-green', icon:'✅', msg:'Jake arrived at DPS School', time:'8 min ago'},
  {cls:'ai-blue',  icon:'🏠', msg:'Mom arrived home', time:'45 min ago'},
  {cls:'ai-amber', icon:'⚠️', msg:'Lily left safe zone', time:'1 hr ago'},
  {cls:'ai-blue',  icon:'📍', msg:'Dad checked in at Work', time:'2 hrs ago'},
  {cls:'ai-green', icon:'🔋', msg:'Jake battery charged to 81%', time:'3 hrs ago'},
];

// ═══════════════════════════════════════════ MAP INIT
const MAP = L.map('map', {
  center:[17.4262, 78.4462],
  zoom:13,
  zoomControl:false,
  attributionControl:true
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
  attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  maxZoom:19
}).addTo(MAP);

// ═══════════════════════════════════════════ MARKERS & ZONES
let markers = {};
let zoneCircles = [];
let selectedId = 0;

function makeMarkerHTML(m) {
  return `
  <div class="marker-wrap" onclick="selectMember(${m.id})">
    <div class="marker-bubble" style="border-color:${m.color}88;">
      <span class="marker-emoji">${m.emoji}</span>
      <span class="marker-name">${m.name}</span>
    </div>
    <div class="marker-tail" style="background:${m.color};width:2px;height:10px;"></div>
    <div class="marker-dot" style="background:${m.color};color:${m.color};width:10px;height:10px;border-radius:50%;"></div>
  </div>`;
}

function createMarker(m) {
  const icon = L.divIcon({
    html: makeMarkerHTML(m),
    className:'custom-marker',
    iconAnchor:[40,52],
    iconSize:[80,52]
  });
  const mk = L.marker([m.lat,m.lng],{icon,zIndexOffset:m.id===selectedId?1000:0})
    .addTo(MAP)
    .bindPopup(`
      <div style="font-family:'Outfit',sans-serif;">
        <div style="font-weight:700;font-size:.9rem;margin-bottom:4px;">${m.emoji} ${m.name}</div>
        <div style="color:rgba(232,236,255,.55);font-size:.78rem;">📍 ${m.place}</div>
        <div style="color:rgba(232,236,255,.35);font-size:.7rem;margin-top:3px;">Updated ${m.timeAgo}</div>
        <div style="display:flex;gap:8px;margin-top:8px;font-size:.72rem;">
          <span style="background:rgba(79,140,255,.15);padding:2px 8px;border-radius:6px;color:var(--blue);">🔋 ${m.battery}</span>
          <span style="background:rgba(0,230,118,.1);padding:2px 8px;border-radius:6px;color:var(--green);">${m.status}</span>
        </div>
      </div>
    `);
  mk.on('click',()=>selectMember(m.id));
  return mk;
}

MEMBERS.forEach(m => { markers[m.id] = createMarker(m); });

SAFE_ZONES.forEach(z => {
  const c = L.circle([z.lat,z.lng],{
    radius:z.radius,
    color:z.color,
    fillColor:z.color,
    fillOpacity:.07,
    weight:1.5,
    dashArray:'6 6'
  }).addTo(MAP);
  const lbl = L.marker([z.lat,z.lng],{
    icon:L.divIcon({
      html:`<div style="background:rgba(11,13,26,.8);border:1px solid ${z.color}44;border-radius:8px;padding:3px 9px;font-family:'Outfit',sans-serif;font-size:.68rem;font-weight:700;color:${z.color};white-space:nowrap;">${z.label}</div>`,
      className:'',iconAnchor:[30,8],iconSize:[60,16]
    })
  }).addTo(MAP);
  zoneCircles.push(c,lbl);
});

// ═══════════════════════════════════════════ RENDER MEMBERS LIST
function renderMembers() {
  const el = document.getElementById('members-list');
  el.innerHTML = MEMBERS.map(m=>`
  <div class="member-card ${m.id===selectedId?'active':''}" id="mc-${m.id}" onclick="selectMember(${m.id})">
    <div class="avatar avatar-${m.status}">
      ${m.emoji}
      <div class="status-ring ring-${m.status}"></div>
    </div>
    <div class="m-info">
      <div class="m-name">${m.name}</div>
      <div class="m-place">📍 ${m.place}</div>
      <div class="m-time">${m.timeAgo}</div>
    </div>
    <span class="m-badge badge-${m.status}">${m.status==='online'?'Live':m.status==='idle'?'Away':'Offline'}</span>
  </div>`).join('');
}

// ═══════════════════════════════════════════ RENDER ALERTS
function renderAlerts() {
  document.getElementById('alerts-list').innerHTML = ALERTS.map(a=>`
  <div class="alert-item ${a.cls}">
    <span style="font-size:1rem;flex-shrink:0;">${a.icon}</span>
    <div class="alert-body">
      <div class="alert-msg">${a.msg}</div>
      <div class="alert-t">${a.time}</div>
    </div>
  </div>`).join('');
}

// ═══════════════════════════════════════════ RENDER TIMELINE
function renderTimeline(id) {
  const m = MEMBERS[id];
  document.getElementById('timeline-wrap').innerHTML = m.timeline.map(t=>`
  <div class="tl-item">
    <div class="tl-dot" style="background:${t.dot};box-shadow:0 0 6px ${t.dot}55;"></div>
    <div class="tl-text">${t.text}</div>
    <div class="tl-time">${t.time}</div>
  </div>`).join('');
}

// ═══════════════════════════════════════════ SELECT MEMBER
function selectMember(id) {
  selectedId = id;
  const m = MEMBERS[id];
  // Update detail card
  document.getElementById('dc-avatar').textContent = m.emoji;
  document.getElementById('dc-name').textContent   = m.name;
  document.getElementById('dc-place').textContent  = '📍 ' + m.place;
  document.getElementById('dc-speed').textContent  = m.speed.toFixed(1);
  document.getElementById('dc-battery').textContent= m.battery;
  document.getElementById('dc-accuracy').textContent = m.accuracy;
  document.getElementById('dc-checkins').textContent  = m.checkins;
  // Fly to member
  MAP.flyTo([m.lat,m.lng],15,{animate:true,duration:.8});
  setTimeout(()=>markers[id].openPopup(),900);
  renderMembers();
  renderTimeline(id);
}

// ═══════════════════════════════════════════ FIT ALL
function fitAll() {
  const bounds = L.latLngBounds(MEMBERS.map(m=>[m.lat,m.lng]));
  MAP.flyToBounds(bounds.pad(.25),{animate:true,duration:1});
}

// ═══════════════════════════════════════════ FILTER BUTTONS
function toggleFilter(btn, type) {
  document.querySelectorAll('.map-filter-btn').forEach(b=>b.classList.remove('active-f'));
  btn.classList.add('active-f');
  const showZones  = type!=='routes';
  const showMarkers= type!=='zones';
  zoneCircles.forEach(c=>showZones?MAP.addLayer(c):MAP.removeLayer(c));
  Object.values(markers).forEach(mk=>showMarkers?MAP.addLayer(mk):MAP.removeLayer(mk));
}

// ═══════════════════════════════════════════ SIMULATE MOVEMENT
let tick = 0;
function simulateLive() {
  tick++;
  MEMBERS.forEach((m,i) => {
    if(m.status==='idle') return;
    // Tiny random drift to simulate GPS updates
    const jitter = 0.00008;
    m.lat += (Math.random()-.5)*jitter;
    m.lng += (Math.random()-.5)*jitter;
    // Update marker position
    markers[i].setLatLng([m.lat,m.lng]);
    // Occasionally update speed
    if(tick % 5 === i) m.speed = Math.random()*2.5;
  });
  // Update selected member speed
  const sel = MEMBERS[selectedId];
  document.getElementById('dc-speed').textContent = sel.speed.toFixed(1);
  // Update metric: randomise a bit for realism
  if(tick % 8 === 0) {
    const onlineCount = MEMBERS.filter(m=>m.status==='online').length;
    document.getElementById('m-online').textContent = onlineCount;
  }
}
setInterval(simulateLive, 2000);

// ═══════════════════════════════════════════ ACTIONS
function sendCheckin() {
  const toast = document.createElement('div');
  toast.style.cssText='position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:rgba(0,230,118,.15);border:1px solid rgba(0,230,118,.35);border-radius:12px;padding:10px 22px;font-family:Outfit,sans-serif;font-size:.85rem;color:#00e676;z-index:9999;font-weight:600;backdrop-filter:blur(12px);transition:opacity .5s;';
  toast.textContent='✅ Check-in request sent to all members!';
  document.body.appendChild(toast);
  setTimeout(()=>{toast.style.opacity='0';setTimeout(()=>toast.remove(),600);},2800);
}

function triggerSOS() {
  document.getElementById('m-sos').textContent='1';
  document.getElementById('m-sos').style.color='var(--red)';
  const toast = document.createElement('div');
  toast.style.cssText='position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:rgba(255,92,92,.15);border:1px solid rgba(255,92,92,.35);border-radius:12px;padding:10px 22px;font-family:Outfit,sans-serif;font-size:.85rem;color:#ff5c5c;z-index:9999;font-weight:700;backdrop-filter:blur(12px);animation:none;';
  toast.textContent='🚨 SOS Alert sent to all family members!';
  document.body.appendChild(toast);
  setTimeout(()=>{
    toast.remove();
    document.getElementById('m-sos').textContent='0';
  },4000);
}

function refreshAll() {
  const btn = document.querySelector('.panel-head-action');
  btn.textContent='↺ …';
  setTimeout(()=>{
    btn.textContent='↺ Refresh';
    renderMembers();
  },800);
}

// ═══════════════════════════════════════════ INIT
renderMembers();
renderAlerts();
renderTimeline(0);
</script>
</body>
</html>
""", height=820, scrolling=False)
