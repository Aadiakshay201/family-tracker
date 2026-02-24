import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FamilyTrack", page_icon="📡", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="collapsedControl"]{display:none!important;}
[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#060818!important;}
.block-container{padding:0!important;max-width:100%!important;}
iframe{border:none!important;display:block!important;}
</style>""", unsafe_allow_html=True)

components.html("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:#060818;
  --s1:#0c0f24;
  --s2:#10142e;
  --s3:#161b38;
  --border:rgba(255,255,255,0.06);
  --border2:rgba(255,255,255,0.10);
  --blue:#3b82f6;
  --violet:#7c3aed;
  --cyan:#06b6d4;
  --green:#10b981;
  --amber:#f59e0b;
  --red:#ef4444;
  --pink:#ec4899;
  --text:#f0f4ff;
  --muted:rgba(240,244,255,0.45);
  --dim:rgba(240,244,255,0.20);
  --glow-blue:rgba(59,130,246,0.35);
  --glow-green:rgba(16,185,129,0.35);
}
html,body{height:100%;width:100%;background:var(--bg);color:var(--text);font-family:'Plus Jakarta Sans',sans-serif;overflow:hidden;font-size:14px;}

/* scrollbars */
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:4px;}

/* ══════════ TOPBAR ══════════ */
#topbar{
  position:fixed;top:0;left:0;right:0;z-index:1000;
  height:54px;
  background:rgba(6,8,24,0.85);
  backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 18px;
  gap:12px;
}
.brand{display:flex;align-items:center;gap:10px;flex-shrink:0;}
.brand-logo{
  width:32px;height:32px;border-radius:9px;
  background:linear-gradient(135deg,var(--blue),var(--violet));
  display:flex;align-items:center;justify-content:center;
  font-size:15px;box-shadow:0 0 20px var(--glow-blue);
}
.brand-text{font-size:1rem;font-weight:800;letter-spacing:-.03em;
  background:linear-gradient(135deg,#fff 30%,var(--cyan));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.brand-sub{font-size:.6rem;color:var(--dim);font-weight:500;letter-spacing:.05em;text-transform:uppercase;margin-top:-2px;}

.live-badge{
  display:flex;align-items:center;gap:6px;
  background:rgba(16,185,129,0.10);border:1px solid rgba(16,185,129,0.22);
  border-radius:100px;padding:3px 10px;
  font-size:.65rem;font-weight:700;color:var(--green);
  letter-spacing:.08em;text-transform:uppercase;
}
.pulse{width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:p 1.4s ease-in-out infinite;}
@keyframes p{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.3;transform:scale(.6);}}

.tb-center{display:flex;align-items:center;gap:6px;flex:1;justify-content:center;}
.circle-btn{
  display:flex;align-items:center;gap:6px;
  background:var(--s2);border:1px solid var(--border2);
  border-radius:9px;padding:5px 12px;cursor:pointer;
  font-family:'Plus Jakarta Sans',sans-serif;font-size:.75rem;font-weight:600;color:var(--muted);
  transition:all .2s;
}
.circle-btn:hover,.circle-btn.active{background:rgba(59,130,246,.12);border-color:rgba(59,130,246,.3);color:var(--text);}

.tb-right{display:flex;align-items:center;gap:8px;flex-shrink:0;}
.btn{border:none;border-radius:9px;padding:6px 13px;font-family:'Plus Jakarta Sans',sans-serif;font-size:.75rem;font-weight:700;cursor:pointer;transition:all .2s;display:flex;align-items:center;gap:5px;white-space:nowrap;}
.btn-ghost{background:var(--s2);border:1px solid var(--border2);color:var(--muted);}
.btn-ghost:hover{background:var(--s3);color:var(--text);}
.btn-primary{background:linear-gradient(135deg,var(--blue),var(--violet));color:#fff;box-shadow:0 4px 16px var(--glow-blue);}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 24px var(--glow-blue);}
.btn-sos{background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.25);color:var(--red);}
.btn-sos:hover{background:rgba(239,68,68,.22);}
.btn-checkin{background:rgba(16,185,129,.10);border:1px solid rgba(16,185,129,.22);color:var(--green);}
.btn-checkin:hover{background:rgba(16,185,129,.20);}

/* ══════════ LAYOUT ══════════ */
#app{position:fixed;top:54px;left:0;right:0;bottom:0;display:flex;}
#sidebar{width:300px;flex-shrink:0;background:var(--s1);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;}
#map-area{flex:1;position:relative;overflow:hidden;}
#panel{width:272px;flex-shrink:0;background:var(--s1);border-left:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;}

/* ══════════ SIDEBAR ══════════ */
.sec-head{padding:12px 14px 8px;font-size:.6rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border);}
.sec-action{background:rgba(59,130,246,.10);border:1px solid rgba(59,130,246,.2);color:var(--blue);border-radius:6px;padding:2px 8px;font-size:.62rem;font-weight:700;cursor:pointer;font-family:'Plus Jakarta Sans',sans-serif;transition:all .2s;text-transform:none;letter-spacing:0;}
.sec-action:hover{background:rgba(59,130,246,.2);}

/* Stats strip */
.stats-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:10px 10px 6px;}
.stat-box{background:var(--s2);border:1px solid var(--border);border-radius:10px;padding:8px 6px;text-align:center;}
.stat-n{font-family:'Space Mono',monospace;font-size:1.3rem;font-weight:700;line-height:1;}
.stat-l{font-size:.58rem;color:var(--dim);text-transform:uppercase;letter-spacing:.07em;margin-top:3px;}
.c-blue{color:var(--blue);} .c-green{color:var(--green);} .c-amber{color:var(--amber);} .c-red{color:var(--red);}

/* Search */
.search-wrap{padding:8px 10px;}
.search-box{display:flex;align-items:center;gap:8px;background:var(--s2);border:1px solid var(--border2);border-radius:10px;padding:7px 11px;}
.search-box input{background:none;border:none;outline:none;color:var(--text);font-family:'Plus Jakarta Sans',sans-serif;font-size:.78rem;flex:1;}
.search-box input::placeholder{color:var(--dim);}

/* Member cards */
.members-list{flex:1;overflow-y:auto;padding:4px 8px 8px;}
.m-card{
  display:flex;align-items:center;gap:10px;
  padding:9px 10px;border-radius:12px;
  cursor:pointer;transition:all .2s;
  border:1px solid transparent;margin-bottom:4px;
  position:relative;overflow:hidden;
}
.m-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;border-radius:3px 0 0 3px;opacity:0;transition:opacity .2s;}
.m-card:hover{background:rgba(255,255,255,.03);border-color:var(--border);}
.m-card:hover::before{opacity:1;}
.m-card.sel{background:rgba(59,130,246,.07);border-color:rgba(59,130,246,.22);}
.m-card.sel::before{opacity:1;background:var(--blue);}

.ava{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.25rem;flex-shrink:0;position:relative;border:2px solid transparent;transition:all .2s;}
.ava.on{border-color:var(--green);box-shadow:0 0 12px rgba(16,185,129,.3);}
.ava.idle{border-color:var(--amber);box-shadow:0 0 12px rgba(245,158,11,.2);}
.ava.off{border-color:#333;}
.ava-ring{position:absolute;bottom:-1px;right:-1px;width:11px;height:11px;border-radius:50%;border:2px solid var(--s1);}
.r-on{background:var(--green);} .r-idle{background:var(--amber);} .r-off{background:#444;}

.m-info{flex:1;min-width:0;}
.m-name{font-weight:700;font-size:.85rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.m-loc{font-size:.7rem;color:var(--muted);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.m-ago{font-size:.62rem;color:var(--dim);margin-top:2px;}
.m-tag{font-size:.6rem;font-weight:800;padding:2px 7px;border-radius:100px;white-space:nowrap;flex-shrink:0;}
.t-on{background:rgba(16,185,129,.12);color:var(--green);}
.t-idle{background:rgba(245,158,11,.12);color:var(--amber);}
.t-off{background:rgba(80,80,80,.2);color:#666;}

/* Activity feed */
.feed{border-top:1px solid var(--border);padding:6px 8px 8px;max-height:175px;overflow-y:auto;}
.feed-item{display:flex;gap:8px;align-items:flex-start;padding:6px 8px;border-radius:9px;margin-bottom:3px;font-size:.73rem;cursor:pointer;transition:all .15s;}
.feed-item:hover{filter:brightness(1.3);}
.fi-b{background:rgba(59,130,246,.07);border:1px solid rgba(59,130,246,.13);}
.fi-g{background:rgba(16,185,129,.07);border:1px solid rgba(16,185,129,.13);}
.fi-a{background:rgba(245,158,11,.07);border:1px solid rgba(245,158,11,.13);}
.fi-r{background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.13);}
.feed-txt{color:var(--text);line-height:1.35;flex:1;}
.feed-t{font-size:.61rem;color:var(--dim);margin-top:2px;}

/* ══════════ MAP ══════════ */
#map{width:100%;height:100%;}
.leaflet-tile-pane{filter:brightness(.7) contrast(1.15) saturate(.75) hue-rotate(200deg);}
.leaflet-popup-content-wrapper{background:rgba(12,15,36,.96)!important;backdrop-filter:blur(16px);border:1px solid rgba(59,130,246,.2)!important;border-radius:14px!important;color:var(--text)!important;font-family:'Plus Jakarta Sans',sans-serif!important;box-shadow:0 12px 40px rgba(0,0,0,.6)!important;}
.leaflet-popup-tip{background:rgba(12,15,36,.96)!important;}
.leaflet-popup-content{margin:12px 16px!important;font-size:.8rem!important;}
.leaflet-popup-close-button{color:var(--muted)!important;font-size:16px!important;}

/* Map overlays */
.map-tl{position:absolute;top:12px;left:12px;z-index:500;display:flex;align-items:center;gap:7px;}
.map-search{background:rgba(6,8,24,.88);backdrop-filter:blur(16px);border:1px solid var(--border2);border-radius:10px;padding:7px 12px;display:flex;align-items:center;gap:7px;font-size:.75rem;color:var(--dim);min-width:200px;box-shadow:0 4px 24px rgba(0,0,0,.4);}
.map-search input{background:none;border:none;outline:none;color:var(--text);font-family:'Plus Jakarta Sans',sans-serif;font-size:.75rem;flex:1;}
.map-search input::placeholder{color:var(--dim);}
.map-pill{background:rgba(6,8,24,.88);backdrop-filter:blur(16px);border:1px solid var(--border2);border-radius:9px;padding:6px 11px;font-size:.7rem;font-weight:700;color:var(--muted);cursor:pointer;font-family:'Plus Jakarta Sans',sans-serif;transition:all .2s;white-space:nowrap;}
.map-pill:hover{border-color:rgba(59,130,246,.35);color:var(--blue);}
.map-pill.ap{background:rgba(59,130,246,.12);border-color:rgba(59,130,246,.3);color:var(--blue);}

.map-br{position:absolute;bottom:12px;right:12px;z-index:500;display:flex;flex-direction:column;gap:5px;}
.map-ic{width:32px;height:32px;background:rgba(6,8,24,.88);backdrop-filter:blur(16px);border:1px solid var(--border2);border-radius:8px;color:var(--text);font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;box-shadow:0 4px 14px rgba(0,0,0,.3);}
.map-ic:hover{background:rgba(59,130,246,.15);border-color:rgba(59,130,246,.35);}

.map-leg{position:absolute;bottom:12px;left:12px;z-index:500;background:rgba(6,8,24,.88);backdrop-filter:blur(16px);border:1px solid var(--border);border-radius:11px;padding:9px 12px;font-size:.68rem;}
.leg-r{display:flex;align-items:center;gap:6px;color:var(--muted);margin-bottom:4px;}
.leg-r:last-child{margin-bottom:0;}
.leg-d{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.leg-z{width:14px;height:8px;border-radius:3px;flex-shrink:0;opacity:.65;}

/* Custom markers */
.mk{display:flex;flex-direction:column;align-items:center;cursor:pointer;}
.mk-bub{background:rgba(6,8,24,.92);backdrop-filter:blur(10px);border:2px solid;border-radius:10px;padding:3px 8px;display:flex;align-items:center;gap:4px;white-space:nowrap;font-family:'Plus Jakarta Sans',sans-serif;box-shadow:0 4px 20px rgba(0,0,0,.5);}
.mk-em{font-size:1rem;}
.mk-nm{font-size:.68rem;font-weight:700;color:#fff;}
.mk-ln{width:2px;height:8px;}
.mk-dt{width:9px;height:9px;border-radius:50%;}

/* ══════════ RIGHT PANEL ══════════ */
.detail-wrap{padding:12px;border-bottom:1px solid var(--border);}
.detail-card{
  background:linear-gradient(135deg,rgba(59,130,246,.10),rgba(124,58,237,.07));
  border:1px solid rgba(59,130,246,.18);
  border-radius:14px;padding:14px;text-align:center;margin-bottom:10px;
}
.d-ava{font-size:2.4rem;margin-bottom:5px;}
.d-name{font-size:.95rem;font-weight:800;letter-spacing:-.02em;}
.d-loc{font-size:.7rem;color:var(--muted);margin-top:3px;}
.d-status{display:flex;align-items:center;justify-content:center;gap:5px;font-size:.68rem;font-weight:700;color:var(--green);margin-top:5px;}
.d-stats{display:grid;grid-template-columns:1fr 1fr;gap:5px;}
.d-stat{background:var(--s2);border:1px solid var(--border);border-radius:9px;padding:7px 8px;text-align:center;}
.ds-n{font-family:'Space Mono',monospace;font-size:.95rem;font-weight:700;color:#fff;}
.ds-l{font-size:.58rem;color:var(--dim);text-transform:uppercase;letter-spacing:.06em;margin-top:2px;}
.d-acts{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:8px;}
.d-btn{border:1px solid var(--border2);background:var(--s2);color:var(--text);border-radius:9px;padding:7px;font-family:'Plus Jakarta Sans',sans-serif;font-size:.72rem;font-weight:700;cursor:pointer;transition:all .2s;display:flex;align-items:center;justify-content:center;gap:4px;}
.d-btn:hover{background:var(--s3);border-color:var(--border2);}
.d-btn-p{background:linear-gradient(135deg,var(--blue),var(--violet));border-color:transparent;color:#fff;}
.d-btn-p:hover{transform:translateY(-1px);box-shadow:0 4px 16px var(--glow-blue);}

.tl-wrap{flex:1;overflow-y:auto;padding:8px 12px;}
.tl{position:relative;padding-left:20px;}
.tl-i{position:relative;padding-bottom:12px;}
.tl-i::before{content:'';position:absolute;left:-14px;top:10px;bottom:0;width:1px;background:var(--border);}
.tl-i:last-child::before{display:none;}
.tl-d{position:absolute;left:-20px;top:4px;width:11px;height:11px;border-radius:50%;border:2px solid var(--s1);}
.tl-txt{font-size:.72rem;color:rgba(240,244,255,.6);line-height:1.4;}
.tl-txt strong{color:var(--text);}
.tl-t{font-size:.61rem;color:var(--dim);margin-top:2px;}

.zones-wrap{border-top:1px solid var(--border);padding:8px 10px;}
.z-item{display:flex;align-items:center;gap:8px;background:var(--s2);border:1px solid var(--border);border-radius:9px;padding:7px 9px;margin-bottom:4px;cursor:pointer;transition:all .2s;}
.z-item:hover{border-color:rgba(59,130,246,.25);}
.z-ic{width:26px;height:26px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:.85rem;flex-shrink:0;}
.z-info{flex:1;}
.z-name{font-weight:700;font-size:.75rem;}
.z-addr{font-size:.62rem;color:var(--muted);}
.z-tag{font-size:.6rem;font-weight:800;padding:2px 7px;border-radius:100px;background:rgba(16,185,129,.12);color:var(--green);}
.add-z{width:100%;border:1px dashed rgba(59,130,246,.2);background:transparent;color:var(--blue);border-radius:9px;padding:6px;font-family:'Plus Jakarta Sans',sans-serif;font-size:.7rem;font-weight:700;cursor:pointer;transition:all .2s;margin-top:3px;}
.add-z:hover{background:rgba(59,130,246,.07);}

/* ══════════ MODAL ══════════ */
#overlay{display:none;position:fixed;inset:0;z-index:2000;background:rgba(4,6,18,.82);backdrop-filter:blur(10px);align-items:center;justify-content:center;}
#overlay.open{display:flex;}
#modal{background:var(--s1);border:1px solid rgba(59,130,246,.2);border-radius:20px;width:540px;max-width:96vw;max-height:92vh;display:flex;flex-direction:column;box-shadow:0 30px 100px rgba(0,0,0,.8);animation:mi .22s ease;}
@keyframes mi{from{transform:scale(.93) translateY(18px);opacity:0;}to{transform:scale(1) translateY(0);opacity:1;}}
.m-hd{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid var(--border);}
.m-title{font-size:.95rem;font-weight:800;letter-spacing:-.02em;}
.m-close{background:rgba(255,255,255,.05);border:1px solid var(--border2);border-radius:7px;width:28px;height:28px;cursor:pointer;color:var(--muted);font-size:.95rem;display:flex;align-items:center;justify-content:center;transition:all .2s;}
.m-close:hover{background:rgba(239,68,68,.15);color:var(--red);}
.m-body{padding:18px 20px;overflow-y:auto;flex:1;}
.f-row{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-bottom:13px;}
.f-grp{display:flex;flex-direction:column;gap:5px;margin-bottom:13px;}
.f-grp.half{margin-bottom:0;}
label{font-size:.62rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);}
input[type=text],input[type=tel],select{background:var(--s2);border:1px solid var(--border2);border-radius:9px;padding:8px 11px;color:var(--text);font-family:'Plus Jakarta Sans',sans-serif;font-size:.8rem;outline:none;transition:all .2s;width:100%;}
input:focus,select:focus{border-color:rgba(59,130,246,.45);box-shadow:0 0 0 3px rgba(59,130,246,.08);}
input::placeholder{color:var(--dim);}
select option{background:var(--s2);}
.e-row{display:flex;gap:6px;flex-wrap:wrap;}
.e-opt{width:36px;height:36px;border-radius:8px;border:2px solid var(--border2);background:var(--s2);font-size:1.1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;}
.e-opt:hover{border-color:rgba(59,130,246,.35);}
.e-opt.sel{border-color:var(--blue);background:rgba(59,130,246,.12);box-shadow:0 0 0 3px rgba(59,130,246,.10);}
.pick-lbl{font-size:.62rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);margin-bottom:5px;display:block;}
#mmap{height:185px;border-radius:11px;border:1px solid var(--border2);overflow:hidden;margin-bottom:5px;}
.pick-hint{font-size:.66rem;color:var(--dim);display:flex;align-items:center;gap:5px;margin-bottom:13px;}
#p-coords{font-family:'Space Mono',monospace;font-size:.65rem;color:var(--blue);}
.err{font-size:.65rem;color:var(--red);margin-top:3px;}
.input-err{border-color:rgba(239,68,68,.4)!important;}
.m-ft{padding:12px 20px;border-top:1px solid var(--border);display:flex;gap:8px;justify-content:flex-end;}
.btn-cancel{background:transparent;border:1px solid var(--border2);color:var(--muted);border-radius:9px;padding:7px 18px;font-family:'Plus Jakarta Sans',sans-serif;font-size:.78rem;font-weight:700;cursor:pointer;transition:all .2s;}
.btn-cancel:hover{border-color:var(--border2);color:var(--text);}
.btn-confirm{background:linear-gradient(135deg,var(--blue),var(--violet));border:none;color:#fff;border-radius:9px;padding:7px 22px;font-family:'Plus Jakarta Sans',sans-serif;font-size:.78rem;font-weight:800;cursor:pointer;box-shadow:0 4px 18px var(--glow-blue);transition:all .2s;}
.btn-confirm:hover{transform:translateY(-1px);box-shadow:0 6px 26px var(--glow-blue);}

/* ══════════ TOAST ══════════ */
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);border-radius:11px;padding:9px 20px;font-family:'Plus Jakarta Sans',sans-serif;font-size:.8rem;font-weight:700;z-index:9999;pointer-events:none;transition:opacity .5s;backdrop-filter:blur(14px);white-space:nowrap;}
</style>
</head>
<body>

<!-- ════════════════ TOPBAR ════════════════ -->
<div id="topbar">
  <div class="brand">
    <div class="brand-logo">📡</div>
    <div>
      <div class="brand-text">FamilyTrack</div>
      <div class="brand-sub">Live Location</div>
    </div>
  </div>

  <div class="tb-center">
    <button class="circle-btn active" onclick="setCircle(this,'family')">👨‍👩‍👧 Johnson Family</button>
    <button class="circle-btn" onclick="setCircle(this,'extended')">👴 Extended</button>
    <button class="circle-btn" onclick="setCircle(this,'work')">🏢 Work</button>
  </div>

  <div class="tb-right">
    <div class="live-badge"><span class="pulse"></span>Live</div>
    <button class="btn btn-checkin" onclick="sendCheckin()">📲 Check-In</button>
    <button class="btn btn-sos" onclick="triggerSOS()">🚨 SOS</button>
    <button class="btn btn-primary" onclick="openModal()">＋ Add Member</button>
  </div>
</div>

<!-- ════════════════ APP ════════════════ -->
<div id="app">

  <!-- SIDEBAR -->
  <div id="sidebar">
    <div class="sec-head">Overview <button class="sec-action" onclick="refreshAll()">↺ Refresh</button></div>
    <div class="stats-strip">
      <div class="stat-box"><div class="stat-n c-blue" id="s-total">4</div><div class="stat-l">Total</div></div>
      <div class="stat-box"><div class="stat-n c-green" id="s-online">3</div><div class="stat-l">Online</div></div>
      <div class="stat-box"><div class="stat-n c-amber" id="s-away">1</div><div class="stat-l">Away</div></div>
      <div class="stat-box"><div class="stat-n c-red" id="s-sos">0</div><div class="stat-l">SOS</div></div>
    </div>

    <div class="search-wrap">
      <div class="search-box">
        <span style="color:var(--dim)">🔍</span>
        <input type="text" placeholder="Search members…" oninput="filterMembers(this.value)"/>
      </div>
    </div>

    <div class="sec-head">Members</div>
    <div class="members-list" id="members-list"></div>

    <div class="sec-head" style="border-top:1px solid var(--border)">Activity</div>
    <div class="feed" id="feed-list"></div>
  </div>

  <!-- MAP -->
  <div id="map-area">
    <div id="map"></div>

    <div class="map-tl">
      <div class="map-search"><span>🔍</span><input type="text" placeholder="Search location…"/></div>
      <button class="map-pill ap" onclick="setPill(this,'all')">All</button>
      <button class="map-pill" onclick="setPill(this,'zones')">Zones</button>
      <button class="map-pill" onclick="setPill(this,'routes')">Routes</button>
      <button class="map-pill" onclick="fitAll()">⊙ Fit All</button>
    </div>

    <div class="map-br">
      <button class="map-ic" onclick="MAP.zoomIn()">＋</button>
      <button class="map-ic" onclick="MAP.zoomOut()">－</button>
      <button class="map-ic" onclick="fitAll()" title="Fit all members">⊙</button>
      <button class="map-ic" onclick="toggleSat()" title="Satellite">🛰</button>
    </div>

    <div class="map-leg">
      <div class="leg-r"><div class="leg-d" style="background:var(--green)"></div>Online</div>
      <div class="leg-r"><div class="leg-d" style="background:var(--amber)"></div>Away</div>
      <div class="leg-r"><div class="leg-d" style="background:#555"></div>Offline</div>
      <div class="leg-r"><div class="leg-z" style="background:var(--blue)"></div>Safe Zone</div>
    </div>
  </div>

  <!-- RIGHT PANEL -->
  <div id="panel">
    <div class="detail-wrap">
      <div class="sec-head" style="padding:0 0 8px;border-bottom:none;">Selected Member</div>
      <div class="detail-card">
        <div class="d-ava" id="d-ava">👩</div>
        <div class="d-name" id="d-name">Mom</div>
        <div class="d-loc" id="d-loc">📍 Home · Banjara Hills</div>
        <div class="d-status">
          <span style="width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block;box-shadow:0 0 6px var(--green);"></span>
          Online · Active
        </div>
      </div>
      <div class="d-stats">
        <div class="d-stat"><div class="ds-n" id="d-spd">0.0</div><div class="ds-l">km/h</div></div>
        <div class="d-stat"><div class="ds-n" id="d-bat">97%</div><div class="ds-l">Battery</div></div>
        <div class="d-stat"><div class="ds-n" id="d-acc">±2m</div><div class="ds-l">Accuracy</div></div>
        <div class="d-stat"><div class="ds-n" id="d-chk">5</div><div class="ds-l">Check-ins</div></div>
      </div>
      <div class="d-acts">
        <button class="d-btn" onclick="toast('📞 Calling…','blue')">📞 Call</button>
        <button class="d-btn d-btn-p" onclick="toast('💬 Message sent!','green')">💬 Message</button>
      </div>
    </div>

    <div class="sec-head">Timeline</div>
    <div class="tl-wrap"><div class="tl" id="tl"></div></div>

    <div class="zones-wrap">
      <div class="sec-head" style="padding:0 0 8px;border-bottom:none;">Safe Zones</div>
      <div class="z-item"><div class="z-ic" style="background:rgba(16,185,129,.12)">🏠</div><div class="z-info"><div class="z-name">Home</div><div class="z-addr">Banjara Hills, Hyd</div></div><span class="z-tag">Active</span></div>
      <div class="z-item"><div class="z-ic" style="background:rgba(59,130,246,.12)">🏫</div><div class="z-info"><div class="z-name">School</div><div class="z-addr">DPS, Secunderabad</div></div><span class="z-tag">Active</span></div>
      <div class="z-item"><div class="z-ic" style="background:rgba(124,58,237,.12)">🏢</div><div class="z-info"><div class="z-name">Work</div><div class="z-addr">HITEC City, Hyd</div></div><span class="z-tag">Active</span></div>
      <button class="add-z" onclick="toast('Safe zone creator coming soon!','blue')">＋ Add Safe Zone</button>
    </div>
  </div>
</div>

<!-- ════════════════ ADD MEMBER MODAL ════════════════ -->
<div id="overlay" onclick="overlayClick(event)">
  <div id="modal">
    <div class="m-hd">
      <div class="m-title">➕ Add Family Member</div>
      <button class="m-close" onclick="closeModal()">✕</button>
    </div>
    <div class="m-body">
      <div class="f-row">
        <div class="f-grp half">
          <label>Full Name *</label>
          <input id="f-name" type="text" placeholder="e.g. Priya Sharma"/>
          <div class="err" id="e-name"></div>
        </div>
        <div class="f-grp half">
          <label>Relation</label>
          <select id="f-rel">
            <option>👩 Mom</option><option>👨 Dad</option>
            <option>🧒 Son</option><option>👧 Daughter</option>
            <option>👴 Grandpa</option><option>👵 Grandma</option>
            <option>👦 Brother</option><option>👩 Sister</option>
            <option>🧑 Other</option>
          </select>
        </div>
      </div>
      <div class="f-row">
        <div class="f-grp half">
          <label>Phone Number</label>
          <input id="f-phone" type="tel" placeholder="+91 98765 43210"/>
        </div>
        <div class="f-grp half">
          <label>Initial Status</label>
          <select id="f-status">
            <option value="on">🟢 Online</option>
            <option value="idle">🟡 Away</option>
            <option value="off">⚫ Offline</option>
          </select>
        </div>
      </div>
      <div class="f-grp">
        <label>Choose Avatar</label>
        <div class="e-row" id="e-row"></div>
      </div>
      <span class="pick-lbl">📍 Pin Location on Map *</span>
      <div id="mmap"></div>
      <div class="pick-hint">🖱 Click on the map to set location · <span id="p-coords">Not selected yet</span></div>
      <div class="err" id="e-loc"></div>
    </div>
    <div class="m-ft">
      <button class="btn-cancel" onclick="closeModal()">Cancel</button>
      <button class="btn-confirm" onclick="confirmAdd()">Add Member</button>
    </div>
  </div>
</div>

<script>
// ═══════════════════════════════ DATA
const MEMBERS = [
  {id:1,emoji:'👩',name:'Mom',  status:'on',  lat:17.4126,lng:78.4482,place:'Home · Banjara Hills',  ago:'Just now', spd:0,bat:'97%',acc:'±2m',chk:5,color:'#10b981',
   tl:[{c:'#10b981',t:'Arrived at <strong>Home</strong>',time:'10:45 AM'},{c:'#3b82f6',t:'Left <strong>Grocery Store</strong>',time:'10:18 AM'},{c:'#3b82f6',t:'Left <strong>Home</strong>',time:'9:30 AM'},{c:'#10b981',t:'Device <strong>online</strong>',time:'7:05 AM'}]},
  {id:2,emoji:'👨',name:'Dad',  status:'on',  lat:17.4435,lng:78.3772,place:'Work · HITEC City',     ago:'2 min ago',spd:0,bat:'62%',acc:'±4m',chk:3,color:'#3b82f6',
   tl:[{c:'#3b82f6',t:'Arrived at <strong>HITEC City</strong>',time:'9:10 AM'},{c:'#3b82f6',t:'Left <strong>Home</strong>',time:'8:35 AM'},{c:'#10b981',t:'Device <strong>online</strong>',time:'7:00 AM'}]},
  {id:3,emoji:'🧒',name:'Jake', status:'on',  lat:17.4399,lng:78.4983,place:'School · DPS Sec\'bad', ago:'5 min ago',spd:0,bat:'81%',acc:'±3m',chk:2,color:'#06b6d4',
   tl:[{c:'#06b6d4',t:'Arrived at <strong>DPS School</strong>',time:'8:20 AM'},{c:'#3b82f6',t:'Left <strong>Home</strong>',time:'7:55 AM'},{c:'#10b981',t:'Device <strong>online</strong>',time:'7:10 AM'}]},
  {id:4,emoji:'👧',name:'Lily', status:'idle',lat:17.4320,lng:78.4510,place:'Jubilee Hills (last seen)',ago:'41 min ago',spd:0,bat:'34%',acc:'±8m',chk:1,color:'#f59e0b',
   tl:[{c:'#f59e0b',t:'Last seen near <strong>Jubilee Hills</strong>',time:'10:02 AM'},{c:'#3b82f6',t:'Left <strong>Home</strong>',time:'9:15 AM'},{c:'#10b981',t:'Device <strong>online</strong>',time:'7:22 AM'}]},
];

const ZONES = [
  {lat:17.4126,lng:78.4482,r:400,label:'Home',  color:'#10b981'},
  {lat:17.4399,lng:78.4983,r:350,label:'School',color:'#3b82f6'},
  {lat:17.4435,lng:78.3772,r:350,label:'Work',  color:'#7c3aed'},
];

const FEED = [
  {cls:'fi-g',ic:'✅',msg:'Jake arrived at DPS School',      t:'8 min ago'},
  {cls:'fi-b',ic:'🏠',msg:'Mom arrived home',                t:'45 min ago'},
  {cls:'fi-a',ic:'⚠️',msg:'Lily left safe zone',             t:'1 hr ago'},
  {cls:'fi-b',ic:'📍',msg:'Dad checked in at Work',          t:'2 hrs ago'},
  {cls:'fi-g',ic:'🔋',msg:'Jake battery charged to 81%',     t:'3 hrs ago'},
];

const PALETTE = ['#ec4899','#a78bfa','#34d399','#fb923c','#f472b6','#38bdf8'];
const EMOJIS  = ['👩','👨','🧒','👧','👴','👵','👦','🧑','🧔','👩‍🦱','👨‍🦳','🧓'];

// ═══════════════════════════════ MAP INIT
const MAP = L.map('map',{center:[17.4262,78.4462],zoom:13,zoomControl:false,attributionControl:true});
const TILE_STREET = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap',maxZoom:19});
const TILE_SAT    = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{attribution:'© Esri',maxZoom:19});
TILE_STREET.addTo(MAP);
let satMode = false;
function toggleSat(){satMode=!satMode;if(satMode){MAP.removeLayer(TILE_STREET);TILE_SAT.addTo(MAP);}else{MAP.removeLayer(TILE_SAT);TILE_STREET.addTo(MAP);}}

// ═══════════════════════════════ MARKERS — keyed by member id, never by index
const MK = {}; // marker store
const ZC = []; // zone circles
let selId = MEMBERS[0].id;

function mkHTML(m){
  return `<div class="mk"><div class="mk-bub" style="border-color:${m.color}99;"><span class="mk-em">${m.emoji}</span><span class="mk-nm">${m.name}</span></div><div class="mk-ln" style="background:${m.color};margin:0 auto;"></div><div class="mk-dt" style="background:${m.color};margin:0 auto;box-shadow:0 0 10px ${m.color};"></div></div>`;
}
function mkPopup(m){
  return `<div><div style="font-weight:800;font-size:.88rem;margin-bottom:5px;">${m.emoji} ${m.name}</div><div style="color:rgba(240,244,255,.5);font-size:.73rem;">📍 ${m.place}</div><div style="color:rgba(240,244,255,.3);font-size:.65rem;margin-top:3px;">Updated ${m.ago}</div><div style="display:flex;gap:7px;margin-top:8px;font-size:.68rem;"><span style="background:rgba(59,130,246,.15);padding:2px 8px;border-radius:6px;color:#3b82f6;">🔋 ${m.bat}</span><span style="background:rgba(16,185,129,.1);padding:2px 8px;border-radius:6px;color:#10b981;">${m.status==='on'?'Online':m.status==='idle'?'Away':'Offline'}</span></div></div>`;
}
function addMarker(m){
  const icon = L.divIcon({html:mkHTML(m),className:'',iconAnchor:[38,50],iconSize:[76,50]});
  const mk = L.marker([m.lat,m.lng],{icon}).addTo(MAP).bindPopup(mkPopup(m));
  mk.on('click',()=>selectMember(m.id));
  MK[m.id] = mk;
}

// Create markers ONCE
MEMBERS.forEach(m=>addMarker(m));

// Safe zone circles ONCE
ZONES.forEach(z=>{
  const c = L.circle([z.lat,z.lng],{radius:z.r,color:z.color,fillColor:z.color,fillOpacity:.06,weight:1.5,dashArray:'5 5'}).addTo(MAP);
  const l = L.marker([z.lat,z.lng],{icon:L.divIcon({html:`<div style="background:rgba(6,8,24,.85);border:1px solid ${z.color}44;border-radius:7px;padding:2px 8px;font-family:'Plus Jakarta Sans',sans-serif;font-size:.62rem;font-weight:800;color:${z.color};white-space:nowrap;">${z.label}</div>`,className:'',iconAnchor:[28,7],iconSize:[56,14]})}).addTo(MAP);
  ZC.push(c,l);
});

// ═══════════════════════════════ RENDER MEMBERS LIST
let filterQ = '';
function renderMembers(){
  const q = filterQ.toLowerCase();
  const list = MEMBERS.filter(m=>m.name.toLowerCase().includes(q));
  document.getElementById('members-list').innerHTML = list.map(m=>`
  <div class="m-card ${m.id===selId?'sel':''}" onclick="selectMember(${m.id})" style="--ac:${m.color}">
    <div class="ava ${m.status}" style="--c:${m.color}">
      ${m.emoji}
      <div class="ava-ring r-${m.status}"></div>
    </div>
    <div class="m-info">
      <div class="m-name">${m.name}</div>
      <div class="m-loc">📍 ${m.place}</div>
      <div class="m-ago">${m.ago}</div>
    </div>
    <span class="m-tag t-${m.status}">${m.status==='on'?'Live':m.status==='idle'?'Away':'Offline'}</span>
  </div>`).join('');
  // colour the active card left border via inline style
  document.querySelectorAll('.m-card.sel').forEach(el=>{
    const m = MEMBERS.find(x=>x.id===selId);
    if(m) el.style.setProperty('--ac',m.color);
    el.querySelectorAll('::before');
  });
}
function filterMembers(v){filterQ=v;renderMembers();}

// ═══════════════════════════════ RENDER FEED
function renderFeed(){
  document.getElementById('feed-list').innerHTML = FEED.map(f=>`
  <div class="feed-item ${f.cls}">
    <span style="font-size:.9rem;flex-shrink:0;">${f.ic}</span>
    <div><div class="feed-txt">${f.msg}</div><div class="feed-t">${f.t}</div></div>
  </div>`).join('');
}

// ═══════════════════════════════ RENDER TIMELINE
function renderTL(id){
  const m = MEMBERS.find(x=>x.id===id);
  document.getElementById('tl').innerHTML = (m?m.tl:[]).map(t=>`
  <div class="tl-i">
    <div class="tl-d" style="background:${t.c};box-shadow:0 0 6px ${t.c}55;"></div>
    <div class="tl-txt">${t.t}</div>
    <div class="tl-t">${t.time}</div>
  </div>`).join('');
}

// ═══════════════════════════════ UPDATE STATS
function updateStats(){
  document.getElementById('s-total').textContent  = MEMBERS.length;
  document.getElementById('s-online').textContent = MEMBERS.filter(m=>m.status==='on').length;
  document.getElementById('s-away').textContent   = MEMBERS.filter(m=>m.status==='idle').length;
}

// ═══════════════════════════════ SELECT MEMBER
function selectMember(id){
  selId = id;
  const m = MEMBERS.find(x=>x.id===id);
  if(!m) return;
  document.getElementById('d-ava').textContent  = m.emoji;
  document.getElementById('d-name').textContent = m.name;
  document.getElementById('d-loc').textContent  = '📍 '+m.place;
  document.getElementById('d-spd').textContent  = m.spd.toFixed(1);
  document.getElementById('d-bat').textContent  = m.bat;
  document.getElementById('d-acc').textContent  = m.acc;
  document.getElementById('d-chk').textContent  = m.chk;
  MAP.flyTo([m.lat,m.lng],15,{animate:true,duration:.8});
  setTimeout(()=>MK[id]&&MK[id].openPopup(),900);
  renderMembers();
  renderTL(id);
}

// ═══════════════════════════════ FIT ALL
function fitAll(){
  const b = L.latLngBounds(MEMBERS.map(m=>[m.lat,m.lng]));
  MAP.flyToBounds(b.pad(.25),{animate:true,duration:1});
}

// ═══════════════════════════════ FILTER PILLS
function setPill(btn,type){
  document.querySelectorAll('.map-pill').forEach(b=>b.classList.remove('ap'));
  btn.classList.add('ap');
  const sm = type!=='routes', mm = type!=='zones';
  ZC.forEach(c=>sm?MAP.addLayer(c):MAP.removeLayer(c));
  Object.values(MK).forEach(mk=>mm?MAP.addLayer(mk):MAP.removeLayer(mk));
  if(type==='all') fitAll();
}

// ═══════════════════════════════ CIRCLE SELECTOR
function setCircle(btn,c){document.querySelectorAll('.circle-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active');}

// ═══════════════════════════════ LIVE SIMULATION — always uses MK[m.id], never index
let tick=0;
setInterval(()=>{
  tick++;
  MEMBERS.forEach(m=>{
    if(m.status!=='on') return;
    m.lat += (Math.random()-.5)*0.00007;
    m.lng += (Math.random()-.5)*0.00007;
    if(MK[m.id]) MK[m.id].setLatLng([m.lat,m.lng]);
    if(tick%7===m.id%7) m.spd = parseFloat((Math.random()*3).toFixed(1));
  });
  const s = MEMBERS.find(x=>x.id===selId);
  if(s) document.getElementById('d-spd').textContent = s.spd.toFixed(1);
},2000);

// ═══════════════════════════════ ADD MEMBER MODAL
let picLat=null, picLng=null, mmap=null, pickMk=null, selEmoji='👩';

function openModal(){
  // Reset
  ['f-name','f-phone'].forEach(id=>{document.getElementById(id).value='';document.getElementById(id).classList.remove('input-err');});
  document.getElementById('f-rel').selectedIndex=0;
  document.getElementById('f-status').selectedIndex=0;
  document.getElementById('e-name').textContent='';
  document.getElementById('e-loc').textContent='';
  picLat=null; picLng=null;
  document.getElementById('p-coords').textContent='Not selected yet';
  selEmoji='👩';

  // Emoji picker
  document.getElementById('e-row').innerHTML = EMOJIS.map(e=>
    `<button class="e-opt${e===selEmoji?' sel':''}" onclick="pickEmoji(this,'${e}')">${e}</button>`
  ).join('');

  document.getElementById('overlay').classList.add('open');

  if(!mmap){
    mmap = L.map('mmap',{center:[17.4262,78.4462],zoom:11,zoomControl:true,attributionControl:false});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(mmap);
    mmap.on('click',e=>{
      picLat=e.latlng.lat; picLng=e.latlng.lng;
      document.getElementById('p-coords').textContent=`${picLat.toFixed(5)}, ${picLng.toFixed(5)}`;
      document.getElementById('e-loc').textContent='';
      if(pickMk) mmap.removeLayer(pickMk);
      pickMk = L.circleMarker([picLat,picLng],{radius:8,color:'#3b82f6',fillColor:'#3b82f6',fillOpacity:.85,weight:2}).addTo(mmap);
    });
  } else {
    mmap.setView([17.4262,78.4462],11);
    if(pickMk){mmap.removeLayer(pickMk);pickMk=null;}
    setTimeout(()=>mmap.invalidateSize(),50);
  }
  setTimeout(()=>mmap.invalidateSize(),120);
}

function closeModal(){document.getElementById('overlay').classList.remove('open');}
function overlayClick(e){if(e.target===document.getElementById('overlay'))closeModal();}
function pickEmoji(btn,em){document.querySelectorAll('.e-opt').forEach(b=>b.classList.remove('sel'));btn.classList.add('sel');selEmoji=em;}

function confirmAdd(){
  const name = document.getElementById('f-name').value.trim();
  let ok=true;
  document.getElementById('e-name').textContent='';
  document.getElementById('f-name').classList.remove('input-err');
  document.getElementById('e-loc').textContent='';
  if(!name){document.getElementById('e-name').textContent='Name is required.';document.getElementById('f-name').classList.add('input-err');ok=false;}
  if(picLat===null){document.getElementById('e-loc').textContent='Click the map to set a location.';ok=false;}
  if(!ok) return;

  const color = PALETTE[MEMBERS.length % PALETTE.length];
  const rel   = document.getElementById('f-rel').value.split(' ').slice(1).join(' ');
  const st    = document.getElementById('f-status').value;
  const newM  = {
    id:Date.now(), emoji:selEmoji, name, status:st,
    lat:picLat, lng:picLng,
    place:`${rel} · Added now`, ago:'Just now',
    spd:0, bat:'100%', acc:'±5m', chk:0,
    color,
    tl:[{c:color,t:`<strong>${name}</strong> joined FamilyTrack`,time:'Just now'}]
  };

  MEMBERS.push(newM);
  addMarker(newM);   // create ONE marker with correct id key
  updateStats();
  renderMembers();
  FEED.unshift({cls:'fi-g',ic:'👤',msg:`${selEmoji} ${name} added to family circle`,t:'Just now'});
  renderFeed();
  closeModal();
  toast(`✅ ${name} added!`,'green');
  setTimeout(()=>{MAP.flyTo([picLat,picLng],15,{animate:true,duration:1});setTimeout(()=>MK[newM.id]&&MK[newM.id].openPopup(),1100);selectMember(newM.id);},300);
}

// ═══════════════════════════════ ACTIONS
function sendCheckin(){toast('✅ Check-in request sent to all members!','green');}
function triggerSOS(){
  document.getElementById('s-sos').textContent='1';
  toast('🚨 SOS Alert sent to all family members!','red');
  FEED.unshift({cls:'fi-r',ic:'🚨',msg:'SOS alert triggered',t:'Just now'});
  renderFeed();
  setTimeout(()=>document.getElementById('s-sos').textContent='0',5000);
}
function refreshAll(){
  const btn=document.querySelector('.sec-action');
  btn.textContent='…';
  setTimeout(()=>{btn.textContent='↺ Refresh';renderMembers();updateStats();},700);
}

// ═══════════════════════════════ TOAST
function toast(msg,type){
  const c={green:{bg:'rgba(16,185,129,.14)',b:'rgba(16,185,129,.3)',t:'#10b981'},blue:{bg:'rgba(59,130,246,.14)',b:'rgba(59,130,246,.3)',t:'#3b82f6'},red:{bg:'rgba(239,68,68,.14)',b:'rgba(239,68,68,.3)',t:'#ef4444'}}[type]||{bg:'rgba(59,130,246,.14)',b:'rgba(59,130,246,.3)',t:'#3b82f6'};
  const el=document.createElement('div');
  el.className='toast';
  el.style.cssText=`background:${c.bg};border:1px solid ${c.b};color:${c.t};`;
  el.textContent=msg;
  document.body.appendChild(el);
  setTimeout(()=>{el.style.opacity='0';setTimeout(()=>el.remove(),600);},3000);
}

// ═══════════════════════════════ INIT
renderMembers();
renderFeed();
renderTL(MEMBERS[0].id);
updateStats();
</script>
</body>
</html>
""", height=820, scrolling=False)