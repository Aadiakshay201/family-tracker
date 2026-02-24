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
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:#0b0d1a; --surface:#111425; --card:#161929;
  --border:rgba(255,255,255,0.07);
  --blue:#4f8cff; --indigo:#6c63ff; --cyan:#00d4ff;
  --green:#00e676; --amber:#ffb347; --red:#ff5c5c;
  --text:#e8ecff; --muted:rgba(232,236,255,0.40); --dimmed:rgba(232,236,255,0.18);
}
html,body{height:100%;width:100%;background:var(--bg);color:var(--text);font-family:'Outfit',sans-serif;overflow:hidden;}

/* ── TOPBAR ── */
#topbar{
  position:fixed;top:0;left:0;right:0;z-index:1000;height:58px;
  background:rgba(11,13,26,0.95);backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;padding:0 20px;
}
.tb-left{display:flex;align-items:center;gap:14px;}
.brand{display:flex;align-items:center;gap:9px;font-size:1.15rem;font-weight:800;letter-spacing:-.02em;}
.brand-icon{
  width:34px;height:34px;border-radius:10px;
  background:linear-gradient(135deg,var(--blue),var(--indigo));
  display:flex;align-items:center;justify-content:center;font-size:1rem;
  box-shadow:0 4px 16px rgba(79,140,255,0.4);
}
.brand-name{background:linear-gradient(135deg,#fff 0%,var(--cyan) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.live-pill{display:flex;align-items:center;gap:6px;background:rgba(0,230,118,0.10);border:1px solid rgba(0,230,118,0.25);border-radius:100px;padding:4px 12px;font-size:.72rem;font-weight:600;color:var(--green);letter-spacing:.06em;text-transform:uppercase;}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:pulse-dot 1.4s ease-in-out infinite;}
@keyframes pulse-dot{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.4;transform:scale(.7);}}
.tb-right{display:flex;align-items:center;gap:10px;}
.tb-btn{border:1px solid var(--border);background:var(--card);color:var(--text);border-radius:10px;padding:6px 14px;font-family:'Outfit',sans-serif;font-size:.82rem;font-weight:600;cursor:pointer;transition:all .2s;display:flex;align-items:center;gap:6px;}
.tb-btn:hover{background:rgba(79,140,255,0.12);border-color:rgba(79,140,255,0.35);color:#fff;}
.tb-btn-primary{background:linear-gradient(135deg,var(--blue),var(--indigo));border-color:transparent;color:#fff;box-shadow:0 4px 16px rgba(79,140,255,0.35);}
.tb-btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 24px rgba(79,140,255,0.5);}
.tb-btn-sos{background:rgba(255,92,92,0.12);border-color:rgba(255,92,92,0.3);color:var(--red);}
.tb-btn-sos:hover{background:rgba(255,92,92,0.25);}

/* ── LAYOUT ── */
#layout{position:fixed;top:58px;left:0;right:0;bottom:0;display:grid;grid-template-columns:310px 1fr 280px;}

/* ── LEFT PANEL ── */
#left{background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;}
.panel-head{padding:14px 16px 10px;border-bottom:1px solid var(--border);font-size:.68rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--dimmed);display:flex;align-items:center;justify-content:space-between;}
.panel-head-action{background:rgba(79,140,255,0.12);border:1px solid rgba(79,140,255,0.25);color:var(--blue);border-radius:7px;padding:3px 10px;font-size:.7rem;font-weight:600;cursor:pointer;font-family:'Outfit',sans-serif;transition:all .2s;text-transform:none;letter-spacing:0;}
.panel-head-action:hover{background:rgba(79,140,255,0.22);}
.metrics-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:12px 12px 8px;}
.metric{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px 12px;display:flex;flex-direction:column;gap:2px;}
.metric-val{font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:600;line-height:1;}
.metric-lbl{font-size:.67rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-top:3px;}
.val-green{color:var(--green);} .val-amber{color:var(--amber);} .val-red{color:var(--red);} .val-blue{color:var(--blue);}
.members-scroll{flex:1;overflow-y:auto;padding:6px 8px;}
.members-scroll::-webkit-scrollbar{width:3px;}
.members-scroll::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px;}
.member-card{display:flex;align-items:center;gap:11px;padding:9px 10px;border-radius:13px;cursor:pointer;transition:all .2s;border:1px solid transparent;margin-bottom:4px;}
.member-card:hover{background:rgba(255,255,255,.04);border-color:var(--border);}
.member-card.active{background:rgba(79,140,255,0.09);border-color:rgba(79,140,255,0.28);}
.avatar{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.35rem;flex-shrink:0;position:relative;border:2px solid transparent;}
.avatar-online{border-color:var(--green);box-shadow:0 0 10px rgba(0,230,118,.25);}
.avatar-idle{border-color:var(--amber);box-shadow:0 0 10px rgba(255,179,71,.2);}
.avatar-offline{border-color:#444;}
.status-ring{position:absolute;bottom:0;right:0;width:11px;height:11px;border-radius:50%;border:2px solid var(--surface);}
.ring-online{background:var(--green);} .ring-idle{background:var(--amber);} .ring-offline{background:#555;}
.m-info{flex:1;min-width:0;}
.m-name{font-weight:700;font-size:.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.m-place{font-size:.75rem;color:var(--muted);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.m-time{font-size:.68rem;color:var(--dimmed);margin-top:2px;}
.m-badge{font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:100px;white-space:nowrap;flex-shrink:0;}
.badge-online{background:rgba(0,230,118,.12);color:var(--green);}
.badge-idle{background:rgba(255,179,71,.12);color:var(--amber);}
.badge-offline{background:rgba(80,80,80,.3);color:#888;}
.alerts-wrap{border-top:1px solid var(--border);padding:8px 10px 10px;max-height:190px;overflow-y:auto;}
.alerts-wrap::-webkit-scrollbar{width:3px;}
.alerts-wrap::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px;}
.alert-item{display:flex;gap:9px;align-items:flex-start;padding:7px 9px;border-radius:10px;margin-bottom:4px;font-size:.78rem;cursor:pointer;transition:all .15s;}
.alert-item:hover{filter:brightness(1.2);}
.ai-blue{background:rgba(79,140,255,.07);border:1px solid rgba(79,140,255,.15);}
.ai-amber{background:rgba(255,179,71,.07);border:1px solid rgba(255,179,71,.15);}
.ai-green{background:rgba(0,230,118,.07);border:1px solid rgba(0,230,118,.15);}
.alert-msg{color:var(--text);line-height:1.35;}
.alert-t{font-size:.66rem;color:var(--dimmed);margin-top:2px;}

/* ── MAP ── */
#map-wrap{position:relative;overflow:hidden;}
#map{width:100%;height:100%;}
.leaflet-tile-pane{filter:brightness(.75) contrast(1.1) saturate(.85) hue-rotate(195deg);}
.map-top{position:absolute;top:14px;left:14px;z-index:500;display:flex;align-items:center;gap:8px;}
.map-search-box{background:rgba(11,13,26,0.88);backdrop-filter:blur(16px);border:1px solid var(--border);border-radius:11px;padding:7px 14px;display:flex;align-items:center;gap:8px;font-size:.83rem;color:var(--muted);min-width:220px;box-shadow:0 4px 20px rgba(0,0,0,.4);}
.map-filter-btn{background:rgba(11,13,26,0.88);backdrop-filter:blur(16px);border:1px solid var(--border);border-radius:11px;padding:7px 12px;color:var(--text);font-size:.78rem;font-weight:600;cursor:pointer;font-family:'Outfit',sans-serif;box-shadow:0 4px 20px rgba(0,0,0,.4);transition:all .2s;display:flex;align-items:center;gap:5px;}
.map-filter-btn:hover{border-color:rgba(79,140,255,.4);color:var(--blue);}
.map-filter-btn.active-f{background:rgba(79,140,255,.15);border-color:rgba(79,140,255,.35);color:var(--blue);}
.map-zoom-ctrl{position:absolute;right:14px;bottom:80px;z-index:500;display:flex;flex-direction:column;gap:4px;}
.mzc-btn{width:34px;height:34px;background:rgba(11,13,26,0.88);backdrop-filter:blur(16px);border:1px solid var(--border);border-radius:9px;color:var(--text);font-size:1.1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;box-shadow:0 4px 14px rgba(0,0,0,.3);}
.mzc-btn:hover{background:rgba(79,140,255,.2);border-color:rgba(79,140,255,.4);}
.map-legend{position:absolute;bottom:14px;left:14px;z-index:500;background:rgba(11,13,26,0.88);backdrop-filter:blur(16px);border:1px solid var(--border);border-radius:12px;padding:10px 14px;font-size:.73rem;box-shadow:0 4px 20px rgba(0,0,0,.4);}
.leg-row{display:flex;align-items:center;gap:7px;color:var(--muted);margin-bottom:5px;}
.leg-row:last-child{margin-bottom:0;}
.leg-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0;}
.leg-zone{width:16px;height:9px;border-radius:4px;opacity:.7;flex-shrink:0;}
.custom-marker{background:transparent;border:none;}
.marker-wrap{display:flex;flex-direction:column;align-items:center;cursor:pointer;}
.marker-bubble{background:rgba(11,13,26,.92);backdrop-filter:blur(10px);border:2px solid;border-radius:12px;padding:4px 8px;display:flex;align-items:center;gap:5px;box-shadow:0 4px 20px rgba(0,0,0,.5);white-space:nowrap;font-family:'Outfit',sans-serif;}
.marker-emoji{font-size:1.1rem;}
.marker-name{font-size:.72rem;font-weight:700;color:#fff;}
.leaflet-popup-content-wrapper{background:rgba(17,20,37,.95);backdrop-filter:blur(14px);border:1px solid var(--border);border-radius:12px;color:var(--text);font-family:'Outfit',sans-serif;box-shadow:0 8px 32px rgba(0,0,0,.5);}
.leaflet-popup-tip{background:rgba(17,20,37,.95);}
.leaflet-popup-content{margin:10px 14px!important;font-size:.82rem;}

/* ── RIGHT PANEL ── */
#right{background:var(--surface);border-left:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;}
#detail-card{padding:14px;border-bottom:1px solid var(--border);}
.dc-header{background:linear-gradient(135deg,rgba(79,140,255,.12),rgba(108,99,255,.08));border:1px solid rgba(79,140,255,.2);border-radius:16px;padding:14px;text-align:center;margin-bottom:10px;}
.dc-avatar{font-size:2.6rem;margin-bottom:5px;}
.dc-name{font-size:1rem;font-weight:800;letter-spacing:-.01em;}
.dc-place{font-size:.76rem;color:var(--muted);margin-top:4px;}
.dc-status{display:flex;align-items:center;justify-content:center;gap:5px;font-size:.73rem;color:var(--green);margin-top:6px;font-weight:600;}
.dc-stats{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.dc-stat{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:8px 10px;text-align:center;}
.dcs-n{font-family:'JetBrains Mono',monospace;font-size:1.05rem;font-weight:600;color:#fff;}
.dcs-l{font-size:.63rem;color:var(--dimmed);text-transform:uppercase;letter-spacing:.07em;margin-top:2px;}
.dc-actions{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px;}
.dca-btn{border:1px solid var(--border);background:var(--card);color:var(--text);border-radius:10px;padding:7px;font-family:'Outfit',sans-serif;font-size:.78rem;font-weight:600;cursor:pointer;transition:all .2s;display:flex;align-items:center;justify-content:center;gap:5px;}
.dca-btn:hover{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.15);}
.dca-primary{background:linear-gradient(135deg,var(--blue),var(--indigo));border-color:transparent;color:#fff;}
.dca-primary:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(79,140,255,.35);}
#timeline-wrap{flex:1;overflow-y:auto;padding:10px 14px;}
#timeline-wrap::-webkit-scrollbar{width:3px;}
#timeline-wrap::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px;}
.tl-item{position:relative;padding-left:22px;padding-bottom:14px;}
.tl-item::before{content:'';position:absolute;left:5px;top:12px;bottom:0;width:1px;background:var(--border);}
.tl-item:last-child::before{display:none;}
.tl-dot{position:absolute;left:0;top:5px;width:12px;height:12px;border-radius:50%;border:2px solid var(--surface);}
.tl-text{font-size:.78rem;color:rgba(232,236,255,.65);line-height:1.4;}
.tl-text strong{color:var(--text);}
.tl-time{font-size:.66rem;color:var(--dimmed);margin-top:2px;}
#zones-wrap{border-top:1px solid var(--border);padding:10px 12px;}
.zone-item{display:flex;align-items:center;gap:9px;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:8px 10px;margin-bottom:5px;font-size:.78rem;cursor:pointer;transition:all .2s;}
.zone-item:hover{border-color:rgba(79,140,255,.3);}
.zone-icon{width:28px;height:28px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:.9rem;flex-shrink:0;}
.zone-info{flex:1;}
.zone-name{font-weight:600;font-size:.8rem;}
.zone-addr{font-size:.68rem;color:var(--muted);}
.zone-status{font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:100px;background:rgba(0,230,118,.12);color:var(--green);}
.add-zone-btn{width:100%;border:1px dashed rgba(79,140,255,.25);background:transparent;color:var(--blue);border-radius:10px;padding:7px;font-family:'Outfit',sans-serif;font-size:.78rem;font-weight:600;cursor:pointer;transition:all .2s;margin-top:4px;}
.add-zone-btn:hover{background:rgba(79,140,255,.08);}

/* ══════════════════════════════════════ ADD MEMBER MODAL */
#modal-overlay{
  display:none;position:fixed;inset:0;z-index:2000;
  background:rgba(7,9,26,0.80);backdrop-filter:blur(8px);
  align-items:center;justify-content:center;
}
#modal-overlay.open{display:flex;}
#modal{
  background:var(--surface);border:1px solid rgba(79,140,255,.25);
  border-radius:20px;width:560px;max-width:95vw;max-height:90vh;
  overflow:hidden;display:flex;flex-direction:column;
  box-shadow:0 24px 80px rgba(0,0,0,.7);
  animation:modal-in .25s ease;
}
@keyframes modal-in{from{transform:scale(.94) translateY(16px);opacity:0;}to{transform:scale(1) translateY(0);opacity:1;}}
.modal-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:18px 22px;border-bottom:1px solid var(--border);
}
.modal-title{font-size:1rem;font-weight:800;letter-spacing:-.01em;}
.modal-close{background:rgba(255,255,255,.06);border:1px solid var(--border);border-radius:8px;width:30px;height:30px;cursor:pointer;color:var(--muted);font-size:1rem;display:flex;align-items:center;justify-content:center;transition:all .2s;}
.modal-close:hover{background:rgba(255,92,92,.15);border-color:rgba(255,92,92,.3);color:var(--red);}
.modal-body{padding:20px 22px;overflow-y:auto;flex:1;}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;}
.form-group{display:flex;flex-direction:column;gap:6px;margin-bottom:14px;}
.form-group.half{margin-bottom:0;}
label{font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--dimmed);}
input,select{
  background:var(--card);border:1px solid var(--border);border-radius:10px;
  padding:9px 12px;color:var(--text);font-family:'Outfit',sans-serif;font-size:.88rem;
  outline:none;transition:all .2s;width:100%;
}
input:focus,select:focus{border-color:rgba(79,140,255,.5);box-shadow:0 0 0 3px rgba(79,140,255,.10);}
input::placeholder{color:var(--dimmed);}
select option{background:var(--card);}

/* emoji picker */
.emoji-row{display:flex;gap:8px;flex-wrap:wrap;}
.emoji-opt{
  width:38px;height:38px;border-radius:9px;border:2px solid var(--border);
  background:var(--card);font-size:1.2rem;cursor:pointer;
  display:flex;align-items:center;justify-content:center;transition:all .2s;
}
.emoji-opt:hover{border-color:rgba(79,140,255,.4);background:rgba(79,140,255,.08);}
.emoji-opt.selected{border-color:var(--blue);background:rgba(79,140,255,.15);box-shadow:0 0 0 3px rgba(79,140,255,.12);}

/* map picker inside modal */
.map-pick-label{font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--dimmed);margin-bottom:6px;display:block;}
#modal-map{height:200px;border-radius:12px;border:1px solid var(--border);overflow:hidden;margin-bottom:6px;}
.modal-map-hint{font-size:.72rem;color:var(--dimmed);display:flex;align-items:center;gap:5px;margin-bottom:14px;}
#picked-coords{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--blue);}

.modal-footer{padding:14px 22px;border-top:1px solid var(--border);display:flex;gap:10px;justify-content:flex-end;}
.btn-cancel{background:transparent;border:1px solid var(--border);color:var(--muted);border-radius:10px;padding:8px 20px;font-family:'Outfit',sans-serif;font-size:.85rem;font-weight:600;cursor:pointer;transition:all .2s;}
.btn-cancel:hover{border-color:rgba(255,255,255,.2);color:var(--text);}
.btn-add{background:linear-gradient(135deg,var(--blue),var(--indigo));border:none;color:#fff;border-radius:10px;padding:8px 24px;font-family:'Outfit',sans-serif;font-size:.85rem;font-weight:700;cursor:pointer;box-shadow:0 4px 16px rgba(79,140,255,.35);transition:all .2s;}
.btn-add:hover{transform:translateY(-1px);box-shadow:0 6px 24px rgba(79,140,255,.5);}
.btn-add:disabled{opacity:.45;cursor:not-allowed;transform:none;}

/* validation */
.input-error{border-color:rgba(255,92,92,.5)!important;}
.err-msg{font-size:.7rem;color:var(--red);margin-top:3px;}

/* toast */
.toast{
  position:fixed;bottom:24px;left:50%;transform:translateX(-50%);
  border-radius:12px;padding:10px 22px;font-family:'Outfit',sans-serif;
  font-size:.85rem;z-index:9999;font-weight:600;
  backdrop-filter:blur(12px);pointer-events:none;
  transition:opacity .5s;
}
</style>
</head>
<body>

<!-- ═══════════ TOPBAR ═══════════ -->
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
    <button class="tb-btn tb-btn-primary" onclick="openModal()">+ Add Member</button>
  </div>
</div>

<!-- ═══════════ MAIN LAYOUT ═══════════ -->
<div id="layout">

  <!-- LEFT PANEL -->
  <div id="left">
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
    <div class="panel-head">Members</div>
    <div class="members-scroll" id="members-list"></div>
    <div class="panel-head" style="border-top:1px solid var(--border);">Recent Activity</div>
    <div class="alerts-wrap" id="alerts-list"></div>
  </div>

  <!-- MAP -->
  <div id="map-wrap">
    <div id="map"></div>
    <div class="map-top">
      <div class="map-search-box">🔍&nbsp; Search location…</div>
      <button class="map-filter-btn active-f" onclick="toggleFilter(this,'all')">All Members</button>
      <button class="map-filter-btn" onclick="toggleFilter(this,'zones')">Safe Zones</button>
    </div>
    <div class="map-zoom-ctrl">
      <button class="mzc-btn" onclick="MAP.zoomIn()">+</button>
      <button class="mzc-btn" onclick="MAP.zoomOut()">−</button>
      <button class="mzc-btn" onclick="fitAll()" title="Fit all">⊙</button>
    </div>
    <div class="map-legend">
      <div class="leg-row"><div class="leg-dot" style="background:var(--green)"></div>Online</div>
      <div class="leg-row"><div class="leg-dot" style="background:var(--amber)"></div>Away</div>
      <div class="leg-row"><div class="leg-zone" style="background:var(--blue)"></div>Safe Zone</div>
    </div>
  </div>

  <!-- RIGHT PANEL -->
  <div id="right">
    <div id="detail-card">
      <div class="panel-head" style="border-bottom:none;padding:0 0 10px;">Selected Member</div>
      <div class="dc-header">
        <div class="dc-avatar" id="dc-avatar">👩</div>
        <div class="dc-name" id="dc-name">Mom</div>
        <div class="dc-place" id="dc-place">📍 Home · Banjara Hills</div>
        <div class="dc-status">
          <span style="width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block;box-shadow:0 0 6px var(--green);"></span>
          Online · Active
        </div>
      </div>
      <div class="dc-stats">
        <div class="dc-stat"><div class="dcs-n" id="dc-speed">0.0</div><div class="dcs-l">km/h</div></div>
        <div class="dc-stat"><div class="dcs-n" id="dc-battery">97%</div><div class="dcs-l">Battery</div></div>
        <div class="dc-stat"><div class="dcs-n" id="dc-accuracy">±2m</div><div class="dcs-l">Accuracy</div></div>
        <div class="dc-stat"><div class="dcs-n" id="dc-checkins">5</div><div class="dcs-l">Check-ins</div></div>
      </div>
      <div class="dc-actions">
        <button class="dca-btn" onclick="showToast('📞 Calling…','blue')">📞 Call</button>
        <button class="dca-btn dca-primary" onclick="showToast('💬 Message sent!','green')">💬 Message</button>
      </div>
    </div>
    <div class="panel-head" style="border-top:none;">Today's Timeline</div>
    <div id="timeline-wrap"></div>
    <div id="zones-wrap">
      <div class="panel-head" style="padding:0 0 10px;border-bottom:none;">Safe Zones</div>
      <div id="zones-list">
        <div class="zone-item"><div class="zone-icon" style="background:rgba(0,230,118,.12);">🏠</div><div class="zone-info"><div class="zone-name">Home</div><div class="zone-addr">Banjara Hills, Hyderabad</div></div><span class="zone-status">Active</span></div>
        <div class="zone-item"><div class="zone-icon" style="background:rgba(79,140,255,.12);">🏫</div><div class="zone-info"><div class="zone-name">School</div><div class="zone-addr">DPS, Secunderabad</div></div><span class="zone-status">Active</span></div>
        <div class="zone-item"><div class="zone-icon" style="background:rgba(108,99,255,.12);">🏢</div><div class="zone-info"><div class="zone-name">Work</div><div class="zone-addr">HITEC City, Hyderabad</div></div><span class="zone-status">Active</span></div>
      </div>
      <button class="add-zone-btn">+ Add Safe Zone</button>
    </div>
  </div>
</div>

<!-- ═══════════ ADD MEMBER MODAL ═══════════ -->
<div id="modal-overlay" onclick="overlayClick(event)">
  <div id="modal">
    <div class="modal-header">
      <div class="modal-title">➕ Add Family Member</div>
      <button class="modal-close" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-body">

      <!-- Name + Relation -->
      <div class="form-row">
        <div class="form-group half">
          <label>Full Name *</label>
          <input id="f-name" type="text" placeholder="e.g. Sarah Johnson"/>
          <div class="err-msg" id="err-name"></div>
        </div>
        <div class="form-group half">
          <label>Relation</label>
          <select id="f-relation">
            <option value="👩 Mom">👩 Mom</option>
            <option value="👨 Dad">👨 Dad</option>
            <option value="🧒 Son">🧒 Son</option>
            <option value="👧 Daughter">👧 Daughter</option>
            <option value="👴 Grandpa">👴 Grandpa</option>
            <option value="👵 Grandma">👵 Grandma</option>
            <option value="👦 Brother">👦 Brother</option>
            <option value="👩 Sister">👩 Sister</option>
            <option value="🧑 Other">🧑 Other</option>
          </select>
        </div>
      </div>

      <!-- Phone -->
      <div class="form-group">
        <label>Phone Number</label>
        <input id="f-phone" type="tel" placeholder="+91 98765 43210"/>
      </div>

      <!-- Avatar emoji -->
      <div class="form-group">
        <label>Choose Avatar</label>
        <div class="emoji-row" id="emoji-row">
          👩 👨 🧒 👧 👴 👵 👦 🧑 🧔 👩‍🦱 👨‍🦳 🧓
        </div>
      </div>

      <!-- Status -->
      <div class="form-group">
        <label>Initial Status</label>
        <select id="f-status">
          <option value="online">🟢 Online</option>
          <option value="idle">🟡 Away</option>
          <option value="offline">⚫ Offline</option>
        </select>
      </div>

      <!-- Map location picker -->
      <span class="map-pick-label">📍 Pin Location on Map *</span>
      <div id="modal-map"></div>
      <div class="modal-map-hint">
        🖱️ Click anywhere on the map to set this member's location &nbsp;·&nbsp;
        <span id="picked-coords">Not picked yet</span>
      </div>
      <div class="err-msg" id="err-loc"></div>

    </div>
    <div class="modal-footer">
      <button class="btn-cancel" onclick="closeModal()">Cancel</button>
      <button class="btn-add" id="btn-add-confirm" onclick="confirmAddMember()">Add Member</button>
    </div>
  </div>
</div>

<script>
// ═══════════════════════════════════════════════════════ DATA
// Single source of truth — all member data lives here
const MEMBERS = [
  {
    id:0, emoji:'👩', name:'Mom', status:'online',
    lat:17.4126, lng:78.4482,
    place:'Home · Banjara Hills', timeAgo:'Just now',
    speed:0, battery:'97%', accuracy:'±2m', checkins:5,
    color:'#00e676',
    timeline:[
      {dot:'#00e676', text:'Arrived at <strong>Home</strong>',      time:'10:45 AM'},
      {dot:'#4f8cff', text:'Left <strong>Grocery Store</strong>',   time:'10:18 AM'},
      {dot:'#4f8cff', text:'Arrived at <strong>Grocery Store</strong>', time:'9:52 AM'},
      {dot:'#4f8cff', text:'Left <strong>Home</strong>',            time:'9:30 AM'},
      {dot:'#00e676', text:'Device came <strong>online</strong>',   time:'7:05 AM'},
    ]
  },
  {
    id:1, emoji:'👨', name:'Dad', status:'online',
    lat:17.4435, lng:78.3772,
    place:'Work · HITEC City', timeAgo:'2 min ago',
    speed:0, battery:'62%', accuracy:'±4m', checkins:3,
    color:'#4f8cff',
    timeline:[
      {dot:'#4f8cff', text:'Arrived at <strong>HITEC City</strong>', time:'9:10 AM'},
      {dot:'#4f8cff', text:'Left <strong>Home</strong>',             time:'8:35 AM'},
      {dot:'#00e676', text:'Device came <strong>online</strong>',    time:'7:00 AM'},
    ]
  },
  {
    id:2, emoji:'🧒', name:'Jake', status:'online',
    lat:17.4399, lng:78.4983,
    place:'School · DPS Secunderabad', timeAgo:'5 min ago',
    speed:0, battery:'81%', accuracy:'±3m', checkins:2,
    color:'#00d4ff',
    timeline:[
      {dot:'#00d4ff', text:'Arrived at <strong>DPS School</strong>', time:'8:20 AM'},
      {dot:'#4f8cff', text:'Left <strong>Home</strong>',             time:'7:55 AM'},
      {dot:'#00e676', text:'Device came <strong>online</strong>',    time:'7:10 AM'},
    ]
  },
  {
    id:3, emoji:'👧', name:'Lily', status:'idle',
    lat:17.4320, lng:78.4510,
    place:'Jubilee Hills (last seen)', timeAgo:'41 min ago',
    speed:0, battery:'34%', accuracy:'±8m', checkins:1,
    color:'#ffb347',
    timeline:[
      {dot:'#ffb347', text:'Last seen near <strong>Jubilee Hills</strong>', time:'10:02 AM'},
      {dot:'#4f8cff', text:'Left <strong>Home</strong>',                    time:'9:15 AM'},
      {dot:'#00e676', text:'Device came <strong>online</strong>',           time:'7:22 AM'},
    ]
  }
];

const SAFE_ZONES = [
  {lat:17.4126, lng:78.4482, radius:400, label:'Home',   color:'#00e676'},
  {lat:17.4399, lng:78.4983, radius:350, label:'School', color:'#4f8cff'},
  {lat:17.4435, lng:78.3772, radius:350, label:'Work',   color:'#6c63ff'},
];

const ALERTS_DATA = [
  {cls:'ai-green', icon:'✅', msg:'Jake arrived at DPS School',     time:'8 min ago'},
  {cls:'ai-blue',  icon:'🏠', msg:'Mom arrived home',               time:'45 min ago'},
  {cls:'ai-amber', icon:'⚠️', msg:'Lily left safe zone',            time:'1 hr ago'},
  {cls:'ai-blue',  icon:'📍', msg:'Dad checked in at Work',         time:'2 hrs ago'},
  {cls:'ai-green', icon:'🔋', msg:'Jake battery charged to 81%',    time:'3 hrs ago'},
];

// Marker colours cycle for new members
const NEW_MEMBER_COLORS = ['#ff6bcb','#a78bfa','#34d399','#fb923c','#f472b6','#38bdf8'];

// ═══════════════════════════════════════════════════════ MAP
const MAP = L.map('map', {center:[17.4262,78.4462], zoom:13, zoomControl:false, attributionControl:true});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
  attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  maxZoom:19
}).addTo(MAP);

// ═══════════════════════════════════════════════════════ MARKERS
// markers is a plain object keyed by member id — NO index-based access
const markers = {};
let zoneCircles = [];
let selectedId = 0;

function makeMarkerHTML(m) {
  return `<div class="marker-wrap">
    <div class="marker-bubble" style="border-color:${m.color}99;">
      <span class="marker-emoji">${m.emoji}</span>
      <span class="marker-name">${m.name}</span>
    </div>
    <div style="width:2px;height:10px;background:${m.color};margin:0 auto;"></div>
    <div style="width:10px;height:10px;border-radius:50%;background:${m.color};margin:0 auto;box-shadow:0 0 10px ${m.color};"></div>
  </div>`;
}

function createMarker(m) {
  const icon = L.divIcon({html:makeMarkerHTML(m), className:'custom-marker', iconAnchor:[40,52], iconSize:[80,52]});
  const mk = L.marker([m.lat, m.lng], {icon})
    .addTo(MAP)
    .bindPopup(popupHTML(m));
  mk.on('click', () => selectMember(m.id));
  return mk;
}

function popupHTML(m) {
  return `<div style="font-family:'Outfit',sans-serif;">
    <div style="font-weight:700;font-size:.9rem;margin-bottom:4px;">${m.emoji} ${m.name}</div>
    <div style="color:rgba(232,236,255,.55);font-size:.78rem;">📍 ${m.place}</div>
    <div style="color:rgba(232,236,255,.35);font-size:.7rem;margin-top:3px;">Updated ${m.timeAgo}</div>
    <div style="display:flex;gap:8px;margin-top:8px;font-size:.72rem;">
      <span style="background:rgba(79,140,255,.15);padding:2px 8px;border-radius:6px;color:#4f8cff;">🔋 ${m.battery}</span>
      <span style="background:rgba(0,230,118,.1);padding:2px 8px;border-radius:6px;color:#00e676;">${m.status}</span>
    </div>
  </div>`;
}

// Create markers exactly ONCE at startup
MEMBERS.forEach(m => { markers[m.id] = createMarker(m); });

// Safe zone circles — created once
SAFE_ZONES.forEach(z => {
  const c = L.circle([z.lat,z.lng], {
    radius:z.radius, color:z.color, fillColor:z.color,
    fillOpacity:.07, weight:1.5, dashArray:'6 6'
  }).addTo(MAP);
  const lbl = L.marker([z.lat,z.lng], {
    icon: L.divIcon({
      html:`<div style="background:rgba(11,13,26,.8);border:1px solid ${z.color}44;border-radius:8px;padding:3px 9px;font-family:'Outfit',sans-serif;font-size:.68rem;font-weight:700;color:${z.color};white-space:nowrap;">${z.label}</div>`,
      className:'', iconAnchor:[30,8], iconSize:[60,16]
    })
  }).addTo(MAP);
  zoneCircles.push(c, lbl);
});

// ═══════════════════════════════════════════════════════ RENDER MEMBERS LIST
function renderMembers() {
  document.getElementById('members-list').innerHTML = MEMBERS.map(m => `
  <div class="member-card ${m.id===selectedId?'active':''}" onclick="selectMember(${m.id})">
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

// ═══════════════════════════════════════════════════════ RENDER ALERTS
function renderAlerts() {
  document.getElementById('alerts-list').innerHTML = ALERTS_DATA.map(a => `
  <div class="alert-item ${a.cls}">
    <span style="font-size:1rem;flex-shrink:0;">${a.icon}</span>
    <div><div class="alert-msg">${a.msg}</div><div class="alert-t">${a.time}</div></div>
  </div>`).join('');
}

// ═══════════════════════════════════════════════════════ RENDER TIMELINE
function renderTimeline(id) {
  const m = MEMBERS.find(x => x.id === id);
  document.getElementById('timeline-wrap').innerHTML = (m.timeline || []).map(t => `
  <div class="tl-item">
    <div class="tl-dot" style="background:${t.dot};box-shadow:0 0 6px ${t.dot}55;"></div>
    <div class="tl-text">${t.text}</div>
    <div class="tl-time">${t.time}</div>
  </div>`).join('');
}

// ═══════════════════════════════════════════════════════ UPDATE METRICS
function updateMetrics() {
  document.getElementById('m-total').textContent  = MEMBERS.length;
  document.getElementById('m-online').textContent = MEMBERS.filter(m=>m.status==='online').length;
  document.getElementById('m-away').textContent   = MEMBERS.filter(m=>m.status==='idle').length;
}

// ═══════════════════════════════════════════════════════ SELECT MEMBER
function selectMember(id) {
  selectedId = id;
  const m = MEMBERS.find(x => x.id === id);
  document.getElementById('dc-avatar').textContent    = m.emoji;
  document.getElementById('dc-name').textContent      = m.name;
  document.getElementById('dc-place').textContent     = '📍 ' + m.place;
  document.getElementById('dc-speed').textContent     = m.speed.toFixed(1);
  document.getElementById('dc-battery').textContent   = m.battery;
  document.getElementById('dc-accuracy').textContent  = m.accuracy;
  document.getElementById('dc-checkins').textContent  = m.checkins;
  MAP.flyTo([m.lat, m.lng], 15, {animate:true, duration:.8});
  setTimeout(() => markers[id] && markers[id].openPopup(), 900);
  renderMembers();
  renderTimeline(id);
}

// ═══════════════════════════════════════════════════════ FIT ALL
function fitAll() {
  const bounds = L.latLngBounds(MEMBERS.map(m => [m.lat, m.lng]));
  MAP.flyToBounds(bounds.pad(.25), {animate:true, duration:1});
}

// ═══════════════════════════════════════════════════════ FILTER
function toggleFilter(btn, type) {
  document.querySelectorAll('.map-filter-btn').forEach(b => b.classList.remove('active-f'));
  btn.classList.add('active-f');
  const showZones   = type !== 'routes';
  const showMarkers = type !== 'zones';
  zoneCircles.forEach(c => showZones ? MAP.addLayer(c) : MAP.removeLayer(c));
  Object.values(markers).forEach(mk => showMarkers ? MAP.addLayer(mk) : MAP.removeLayer(mk));
}

// ═══════════════════════════════════════════════════════ LIVE SIMULATION
// Uses member id as key — never index — so new members added later work fine
let tick = 0;
function simulateLive() {
  tick++;
  MEMBERS.forEach(m => {
    if (m.status === 'idle' || m.status === 'offline') return;
    const jitter = 0.00007;
    m.lat += (Math.random() - .5) * jitter;
    m.lng += (Math.random() - .5) * jitter;
    // Only update the marker for this specific member by ID
    if (markers[m.id]) markers[m.id].setLatLng([m.lat, m.lng]);
    if (tick % 6 === m.id % 6) m.speed = Math.random() * 2.5;
  });
  // Update speed display for selected member only
  const sel = MEMBERS.find(x => x.id === selectedId);
  if (sel) document.getElementById('dc-speed').textContent = sel.speed.toFixed(1);
}
setInterval(simulateLive, 2000);

// ═══════════════════════════════════════════════════════ ADD MEMBER MODAL
let pickedLat = null, pickedLng = null;
let modalMap  = null;
let pickMarker = null;
let selectedEmoji = '👩';

const EMOJIS = ['👩','👨','🧒','👧','👴','👵','👦','🧑','🧔','👩‍🦱','👨‍🦳','🧓'];

function openModal() {
  // Reset form
  document.getElementById('f-name').value    = '';
  document.getElementById('f-phone').value   = '';
  document.getElementById('f-relation').value = '👩 Mom';
  document.getElementById('f-status').value  = 'online';
  document.getElementById('err-name').textContent = '';
  document.getElementById('err-loc').textContent  = '';
  document.getElementById('f-name').classList.remove('input-error');
  pickedLat = null; pickedLng = null;
  document.getElementById('picked-coords').textContent = 'Not picked yet';
  selectedEmoji = '👩';

  // Render emoji picker
  document.getElementById('emoji-row').innerHTML = EMOJIS.map(e =>
    `<button class="emoji-opt${e===selectedEmoji?' selected':''}" onclick="pickEmoji(this,'${e}')">${e}</button>`
  ).join('');

  document.getElementById('modal-overlay').classList.add('open');

  // Init mini map inside modal (only once)
  if (!modalMap) {
    modalMap = L.map('modal-map', {center:[17.4262,78.4462], zoom:12, zoomControl:true, attributionControl:false});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19}).addTo(modalMap);
    modalMap.on('click', e => {
      pickedLat = e.latlng.lat;
      pickedLng = e.latlng.lng;
      document.getElementById('picked-coords').textContent =
        `${pickedLat.toFixed(5)}, ${pickedLng.toFixed(5)}`;
      document.getElementById('err-loc').textContent = '';
      if (pickMarker) modalMap.removeLayer(pickMarker);
      pickMarker = L.circleMarker([pickedLat,pickedLng], {
        radius:8, color:'#4f8cff', fillColor:'#4f8cff', fillOpacity:.8, weight:2
      }).addTo(modalMap);
    });
  } else {
    // Re-center on Hyderabad when re-opening
    modalMap.setView([17.4262,78.4462], 12);
    if (pickMarker) { modalMap.removeLayer(pickMarker); pickMarker = null; }
    setTimeout(() => modalMap.invalidateSize(), 50);
  }
  setTimeout(() => modalMap.invalidateSize(), 100);
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('open');
}

function overlayClick(e) {
  if (e.target === document.getElementById('modal-overlay')) closeModal();
}

function pickEmoji(btn, emoji) {
  document.querySelectorAll('.emoji-opt').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  selectedEmoji = emoji;
}

function confirmAddMember() {
  const name = document.getElementById('f-name').value.trim();
  let valid = true;

  // Validate name
  document.getElementById('err-name').textContent = '';
  document.getElementById('f-name').classList.remove('input-error');
  if (!name) {
    document.getElementById('err-name').textContent = 'Name is required.';
    document.getElementById('f-name').classList.add('input-error');
    valid = false;
  }

  // Validate location
  document.getElementById('err-loc').textContent = '';
  if (pickedLat === null) {
    document.getElementById('err-loc').textContent = 'Please click the map to set a location.';
    valid = false;
  }

  if (!valid) return;

  const status   = document.getElementById('f-status').value;
  const relation = document.getElementById('f-relation').value;
  const phone    = document.getElementById('f-phone').value.trim();
  const newId    = Date.now(); // unique numeric id
  const color    = NEW_MEMBER_COLORS[MEMBERS.length % NEW_MEMBER_COLORS.length];

  const newMember = {
    id:       newId,
    emoji:    selectedEmoji,
    name:     name,
    status:   status,
    lat:      pickedLat,
    lng:      pickedLng,
    place:    relation.split(' ').slice(1).join(' ') + ' · Added now',
    timeAgo:  'Just added',
    speed:    0,
    battery:  '100%',
    accuracy: '±5m',
    checkins: 0,
    color:    color,
    phone:    phone,
    timeline: [
      {dot: color, text: `<strong>${name}</strong> joined FamilyTrack`, time: 'Just now'}
    ]
  };

  // Push to MEMBERS array
  MEMBERS.push(newMember);

  // Create ONE marker on the main map
  markers[newId] = createMarker(newMember);

  // Update UI
  updateMetrics();
  renderMembers();

  // Add alert
  ALERTS_DATA.unshift({
    cls:'ai-green', icon:'👤',
    msg:`${selectedEmoji} ${name} was added to the family circle`,
    time:'Just now'
  });
  renderAlerts();

  closeModal();
  showToast(`✅ ${name} added to FamilyTrack!`, 'green');

  // Fly to new member on main map
  setTimeout(() => {
    MAP.flyTo([pickedLat, pickedLng], 15, {animate:true, duration:1});
    setTimeout(() => markers[newId].openPopup(), 1100);
    selectMember(newId);
  }, 300);
}

// ═══════════════════════════════════════════════════════ ACTIONS
function sendCheckin() {
  showToast('✅ Check-in request sent to all members!', 'green');
}

function triggerSOS() {
  document.getElementById('m-sos').textContent = '1';
  showToast('🚨 SOS Alert sent to all family members!', 'red');
  setTimeout(() => document.getElementById('m-sos').textContent = '0', 4000);
}

function refreshAll() {
  const btn = document.querySelector('.panel-head-action');
  btn.textContent = '↺ …';
  setTimeout(() => { btn.textContent = '↺ Refresh'; renderMembers(); updateMetrics(); }, 800);
}

function showToast(msg, type) {
  const colors = {
    green:  {bg:'rgba(0,230,118,.15)',  border:'rgba(0,230,118,.35)',  text:'#00e676'},
    blue:   {bg:'rgba(79,140,255,.15)', border:'rgba(79,140,255,.35)', text:'#4f8cff'},
    red:    {bg:'rgba(255,92,92,.15)',  border:'rgba(255,92,92,.35)',  text:'#ff5c5c'},
  };
  const c = colors[type] || colors.green;
  const t = document.createElement('div');
  t.className = 'toast';
  t.style.cssText = `background:${c.bg};border:1px solid ${c.border};color:${c.text};`;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => { t.style.opacity='0'; setTimeout(()=>t.remove(),600); }, 3000);
}

// ═══════════════════════════════════════════════════════ INIT
renderMembers();
renderAlerts();
renderTimeline(0);
updateMetrics();
</script>
</body>
</html>
""", height=820, scrolling=False)
