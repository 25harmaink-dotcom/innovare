"""
JalRakshak — Field Officer / Supervisor Dashboard
Dashboard 3: Operational Monitoring & Ground Coordination
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

AMBER="#D4820A"; TERRA="#C1440E"; SAND="#F5ECD7"; SAND_DARK="#EAD9B8"
CREAM="#FDFAF4"; BROWN="#5C3317"; MUTED="#8B6F47"; WHITE="#FFFFFF"
GREEN_OK="#2E7D32"; RED_CRIT="#B71C1C"; ORANGE_W="#E65100"; YELLOW_W="#F57F17"
BLUE_INFO="#0277BD"

# ── MOCK DATA ──────────────────────────────────────────────────────────────────

OFFICER = {"name":"Suresh Deshmukh","zone":"Gadchiroli East Zone","district":"Gadchiroli","villages_under":12,"phone":"9812345678"}

VILLAGES_QUEUE = [
    {"rank":1,"name":"Kurkheda",    "wsi":72,"days_no_supply":3,"pop":4820,"severity":"Warning", "tanker_assigned":"TK-04","last_supply":"Feb 20"},
    {"rank":2,"name":"Chamorshi",   "wsi":68,"days_no_supply":5,"pop":3210,"severity":"Warning", "tanker_assigned":"TK-11","last_supply":"Feb 18"},
    {"rank":3,"name":"Mul",         "wsi":61,"days_no_supply":2,"pop":5400,"severity":"Warning", "tanker_assigned":"Pending","last_supply":"Feb 21"},
    {"rank":4,"name":"Bhamragad",   "wsi":55,"days_no_supply":4,"pop":1890,"severity":"Watch",   "tanker_assigned":"Pending","last_supply":"Feb 19"},
    {"rank":5,"name":"Sironcha",    "wsi":48,"days_no_supply":1,"pop":2340,"severity":"Watch",   "tanker_assigned":"TK-07","last_supply":"Feb 22"},
    {"rank":6,"name":"Etapalli",    "wsi":41,"days_no_supply":2,"pop":2100,"severity":"Watch",   "tanker_assigned":"TK-03","last_supply":"Feb 21"},
    {"rank":7,"name":"Aheri",       "wsi":35,"days_no_supply":1,"pop":3780,"severity":"Normal",  "tanker_assigned":"TK-08","last_supply":"Feb 22"},
    {"rank":8,"name":"Dhanora",     "wsi":29,"days_no_supply":0,"pop":2650,"severity":"Normal",  "tanker_assigned":"TK-02","last_supply":"Feb 23"},
]

FLEET = [
    {"id":"TK-04","cap":"12,000L","status":"In Transit",  "driver":"Raju Meshram",  "village":"Kurkheda",  "eta":"11:30 AM","km_left":14,"fuel":68},
    {"id":"TK-11","cap":"10,000L","status":"Scheduled",   "driver":"Dilip Pawar",   "village":"Chamorshi", "eta":"04:20 PM","km_left":24,"fuel":82},
    {"id":"TK-07","cap":"12,000L","status":"Delivered",   "driver":"Anil Koreti",   "village":"Sironcha",  "eta":"Done",    "km_left":0, "fuel":45},
    {"id":"TK-03","cap":"10,000L","status":"In Transit",  "driver":"Santosh Yadav", "village":"Etapalli",  "eta":"01:15 PM","km_left":31,"fuel":71},
    {"id":"TK-08","cap":"10,000L","status":"Available",   "driver":"Manoj Shinde",  "village":"—",         "eta":"—",       "km_left":0, "fuel":91},
    {"id":"TK-02","cap":"12,000L","status":"Under Maint.","driver":"Pravin Gore",   "village":"—",         "eta":"Feb 25",  "km_left":0, "fuel":0},
]

DELIVERIES_TODAY = [
    {"id":"DEL-2026-047","village":"Sironcha",  "tanker":"TK-07","litres":12000,"time":"08:45 AM","status":"Confirmed","otp":"✅ Verified","sarpanch":"Lalita Naitam"},
    {"id":"DEL-2026-046","village":"Dhanora",   "tanker":"TK-02","litres":10000,"time":"07:30 AM","status":"Confirmed","otp":"✅ Verified","sarpanch":"Govinda Tekam"},
]

PENDING_DELIVERIES = [
    {"id":"DEL-2026-048","village":"Kurkheda",  "tanker":"TK-04","litres":12000,"eta":"11:30 AM","priority":"High"},
    {"id":"DEL-2026-049","village":"Chamorshi", "tanker":"TK-11","litres":10000,"eta":"04:20 PM","priority":"High"},
    {"id":"DEL-2026-050","village":"Etapalli",  "tanker":"TK-03","litres":10000,"eta":"01:15 PM","priority":"Medium"},
]

ESCALATIONS = [
    {"id":"ESC-2026-012","village":"Kurkheda", "type":"SOS Alert","msg":"Borewell #2 dry, 1200 people critical","time":"Feb 10, 9:02 AM","status":"Resolved","priority":"High"},
    {"id":"ESC-2026-011","village":"Chamorshi","type":"Route Blocked","msg":"NH-136 flooded near Armori bridge","time":"Feb 09, 2:15 PM","status":"Resolved","priority":"Medium"},
    {"id":"ESC-2026-009","village":"Mul",      "type":"Tanker Delay","msg":"TK-06 breakdown — 3hr delay expected","time":"Feb 07, 11:00 AM","status":"Resolved","priority":"Medium"},
]

BOREWELL_DATA = [
    {"village":"Kurkheda",  "borewell":"BW-KU-2","level_m":8.3,"change":"-2.1m/mo","condition":"Low",  "status":"Functional"},
    {"village":"Kurkheda",  "borewell":"BW-KU-4","level_m":None,"change":"N/A",     "condition":"Dry",  "status":"Failed"},
    {"village":"Chamorshi", "borewell":"BW-CH-1","level_m":6.1, "change":"-1.8m/mo","condition":"Low",  "status":"Functional"},
    {"village":"Mul",       "borewell":"BW-MU-3","level_m":4.2, "change":"-0.9m/mo","condition":"Good", "status":"Functional"},
    {"village":"Sironcha",  "borewell":"BW-SI-1","level_m":3.8, "change":"-0.5m/mo","condition":"Good", "status":"Functional"},
]

# OTP session store
if "otp_store" not in st.session_state:
    st.session_state.otp_store = {}

def wsi_badge(wsi):
    if wsi<=30:  return "🟢","Normal", GREEN_OK,"#E8F5E9"
    elif wsi<=60:return "🟡","Watch",  YELLOW_W,"#FFF8E1"
    elif wsi<=80:return "🟠","Warning",ORANGE_W,"#FBE9E7"
    else:        return "🔴","Critical",RED_CRIT,"#FFEBEE"

def fleet_color(status):
    return {
        "In Transit":AMBER,"Delivered":GREEN_OK,"Available":BLUE_INFO,
        "Scheduled":MUTED,"Under Maint.":RED_CRIT
    }.get(status, MUTED)

def inject_css():
    st.markdown(f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');
    html,body,[class*="css"]{{font-family:'Sora',sans-serif;background:{CREAM};color:{BROWN};}}
    .stApp{{background:{CREAM};}}
    [data-testid="stSidebar"]{{background:linear-gradient(180deg,{SAND} 0%,{SAND_DARK} 100%);border-right:2px solid {AMBER};}}
    .metric-card{{background:{WHITE};border:1.5px solid {SAND_DARK};border-radius:12px;padding:1.1rem 1rem;text-align:center;box-shadow:0 2px 8px rgba(92,51,23,0.07);}}
    .metric-val{{font-size:1.9rem;font-weight:800;color:{AMBER};line-height:1.1;}}
    .metric-label{{font-size:0.75rem;color:{MUTED};margin-top:0.3rem;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;}}
    .jal-card{{background:{WHITE};border:1.5px solid {SAND_DARK};border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:1rem;box-shadow:0 2px 8px rgba(92,51,23,0.06);}}
    .jal-card-title{{font-size:1rem;font-weight:700;color:{BROWN};margin-bottom:0.8rem;border-bottom:2px solid {SAND};padding-bottom:0.4rem;}}
    .alert-critical{{background:linear-gradient(135deg,#FFEBEE,#FFCDD2);border:2px solid {RED_CRIT};border-left:6px solid {RED_CRIT};border-radius:10px;padding:1rem 1.2rem;margin-bottom:1rem;color:{RED_CRIT};font-weight:600;}}
    .alert-warning{{background:linear-gradient(135deg,#FBE9E7,#FFCCBC);border:2px solid {ORANGE_W};border-left:6px solid {ORANGE_W};border-radius:10px;padding:1rem 1.2rem;margin-bottom:1rem;color:{ORANGE_W};font-weight:600;}}
    .alert-info{{background:{SAND};border:1.5px solid {AMBER};border-left:5px solid {AMBER};border-radius:10px;padding:0.9rem 1.2rem;margin-bottom:0.8rem;color:{BROWN};}}
    .alert-success{{background:#E8F5E9;border:1.5px solid {GREEN_OK};border-left:5px solid {GREEN_OK};border-radius:10px;padding:0.9rem 1.2rem;margin-bottom:0.8rem;color:{GREEN_OK};font-weight:600;}}
    .village-row{{display:grid;grid-template-columns:0.4fr 1.4fr 0.7fr 0.7fr 0.9fr 1.1fr 1fr;gap:0.5rem;padding:0.7rem 0.6rem;border-bottom:1px solid {SAND};font-size:0.85rem;align-items:center;}}
    .row-header{{font-weight:700;color:{MUTED};font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;background:{SAND};border-radius:8px;padding:0.5rem 0.6rem;}}
    .fleet-card{{background:{WHITE};border:1.5px solid {SAND_DARK};border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.8rem;border-left:5px solid {AMBER};}}
    .otp-box{{background:linear-gradient(135deg,#E8F5E9,#C8E6C9);border:2px solid {GREEN_OK};border-radius:12px;padding:1rem;text-align:center;}}
    .otp-code{{font-size:3rem;font-weight:800;color:{GREEN_OK};letter-spacing:0.3em;font-family:'IBM Plex Mono',monospace;}}
    .esc-card{{background:{WHITE};border:1.5px solid {SAND_DARK};border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.7rem;}}
    .jal-divider{{height:2px;background:linear-gradient(90deg,{AMBER},{SAND_DARK},transparent);border:none;margin:1.2rem 0;border-radius:2px;}}
    #MainMenu{{visibility:hidden;}}footer{{visibility:hidden;}}
    </style>""", unsafe_allow_html=True)

def render_sidebar(o):
    in_transit = len([f for f in FLEET if f["status"]=="In Transit"])
    avail = len([f for f in FLEET if f["status"]=="Available"])
    critical_vils = len([v for v in VILLAGES_QUEUE if v["wsi"]>60])
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:1rem 0;'>
            <div style='font-size:2.4rem;'>👷</div>
            <div style='font-size:1.1rem;font-weight:700;color:{BROWN};'>{o['name']}</div>
            <div style='font-size:0.82rem;color:{MUTED};margin-top:0.2rem;'>📍 {o['zone']}</div>
            <div style='font-size:0.8rem;color:{MUTED};'>📍 {o['district']} District</div>
        </div>
        <hr style='border:1px solid {SAND_DARK};'>
        <div style='font-size:0.82rem;color:{MUTED};line-height:2.2;'>
            🏘️ Villages Under: <b style='color:{BROWN};'>{o['villages_under']}</b><br>
            🚛 Tankers In Transit: <b style='color:{AMBER};'>{in_transit}</b><br>
            ✅ Tankers Available: <b style='color:{GREEN_OK};'>{avail}</b><br>
            🔴 Critical Villages: <b style='color:{RED_CRIT};'>{critical_vils}</b>
        </div>
        <hr style='border:1px solid {SAND_DARK};'>
        """, unsafe_allow_html=True)

        open_esc = len([e for e in ESCALATIONS if e["status"]!="Resolved"])
        if open_esc > 0:
            st.markdown(f"<div style='background:#FFEBEE;border:1px solid #EF9A9A;border-radius:8px;padding:0.7rem;font-size:0.8rem;color:{RED_CRIT};margin-bottom:0.7rem;'>⚠️ <b>{open_esc} Open Escalation(s)</b><br>Requires immediate attention</div>",unsafe_allow_html=True)

        st.markdown(f"<div style='font-size:0.78rem;color:{MUTED};text-align:center;'>📞 {o['phone']}</div>",unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout",use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

# ── TAB 1: VILLAGE PRIORITY QUEUE ────────────────────────────────────────────

def tab_priority_queue():
    critical_v = [v for v in VILLAGES_QUEUE if v["wsi"]>60]
    if critical_v:
        st.markdown(f"<div class='alert-warning'>⚡ <b>{len(critical_v)} villages</b> are currently in Warning/Critical zone. Prioritize tanker dispatch immediately.</div>",unsafe_allow_html=True)

    # Summary metrics
    total_pop = sum(v["pop"] for v in VILLAGES_QUEUE)
    warning_v = len([v for v in VILLAGES_QUEUE if v["wsi"]>60])
    pending_t = len([v for v in VILLAGES_QUEUE if v["tanker_assigned"]=="Pending"])
    avg_wsi   = int(sum(v["wsi"] for v in VILLAGES_QUEUE)/len(VILLAGES_QUEUE))

    cols = st.columns(4)
    for col,(em,val,lab,c) in zip(cols,[("🏘️",str(len(VILLAGES_QUEUE)),"Villages in Zone",BROWN),
            ("⚠️",str(warning_v),"In Warning/Critical",ORANGE_W),
            ("⏳",str(pending_t),"Pending Assignment",TERRA),
            ("📊",str(avg_wsi),"Avg Zone WSI",AMBER)]):
        with col: st.markdown(f"<div class='metric-card'><div style='font-size:1.5rem;'>{em}</div><div class='metric-val' style='color:{c};'>{val}</div><div class='metric-label'>{lab}</div></div>",unsafe_allow_html=True)

    st.markdown("<div class='jal-divider'></div>",unsafe_allow_html=True)

    # WSI bar chart
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("<div class='jal-card-title'>📊 Village WSI Rankings</div>",unsafe_allow_html=True)
        names = [v["name"] for v in VILLAGES_QUEUE]
        wsis  = [v["wsi"]  for v in VILLAGES_QUEUE]
        bar_colors = [wsi_badge(w)[2] for w in wsis]
        fig = go.Figure(go.Bar(y=names,x=wsis,orientation="h",
            marker_color=bar_colors,text=[f"{w}" for w in wsis],textposition="outside"))
        fig.add_vline(x=60,line_dash="dot",line_color=ORANGE_W)
        fig.add_vline(x=80,line_dash="dot",line_color=RED_CRIT)
        fig.update_layout(paper_bgcolor="white",plot_bgcolor="white",
            margin=dict(t=10,b=10,l=10,r=40),height=280,
            xaxis=dict(range=[0,100],showgrid=True,gridcolor=SAND),
            yaxis=dict(showgrid=False,categoryorder="array",categoryarray=names[::-1]),
            font=dict(family="Sora",size=11))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with col2:
        st.markdown("<div class='jal-card-title'>🗂️ Priority Breakdown</div>",unsafe_allow_html=True)
        counts = {"Normal":len([v for v in VILLAGES_QUEUE if v["wsi"]<=30]),
                  "Watch":  len([v for v in VILLAGES_QUEUE if 30<v["wsi"]<=60]),
                  "Warning":len([v for v in VILLAGES_QUEUE if 60<v["wsi"]<=80]),
                  "Critical":len([v for v in VILLAGES_QUEUE if v["wsi"]>80])}
        fig2 = go.Figure(go.Pie(
            labels=list(counts.keys()), values=list(counts.values()),
            marker_colors=[GREEN_OK,YELLOW_W,ORANGE_W,RED_CRIT],
            hole=0.55, textinfo="label+value",
            textfont=dict(family="Sora",size=11)))
        fig2.update_layout(paper_bgcolor="white",margin=dict(t=10,b=10,l=10,r=10),height=280,showlegend=False)
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

    # Priority table
    st.markdown("<div class='jal-divider'></div>",unsafe_allow_html=True)
    st.markdown("<div class='jal-card'>",unsafe_allow_html=True)
    st.markdown("""<div class='village-row row-header'>
        <span>#</span><span>Village</span><span>WSI</span><span>Days w/o Supply</span>
        <span>Population</span><span>Tanker</span><span>Severity</span>
    </div>""",unsafe_allow_html=True)

    for v in VILLAGES_QUEUE:
        _, level, color, bg = wsi_badge(v["wsi"])
        t_color = GREEN_OK if v["tanker_assigned"]!="Pending" else RED_CRIT
        days_color = RED_CRIT if v["days_no_supply"]>=3 else ORANGE_W if v["days_no_supply"]>=2 else BROWN
        st.markdown(f"""<div class='village-row'>
            <span style='font-weight:700;color:{MUTED};'>#{v['rank']}</span>
            <span style='font-weight:600;color:{BROWN};'>{v['name']}</span>
            <span style='font-weight:700;color:{color};'>{v['wsi']}</span>
            <span style='font-weight:600;color:{days_color};'>{v['days_no_supply']}d</span>
            <span style='color:{BROWN};'>{v['pop']:,}</span>
            <span style='font-family:monospace;font-weight:600;color:{t_color};'>{v['tanker_assigned']}</span>
            <span style='background:{bg};color:{color};border:1px solid {color};border-radius:20px;padding:0.15rem 0.6rem;font-size:0.78rem;font-weight:600;'>{level}</span>
        </div>""",unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)

# ── TAB 2: FLEET STATUS ───────────────────────────────────────────────────────

def tab_fleet_status():
    status_counts = {}
    for f in FLEET:
        status_counts[f["status"]] = status_counts.get(f["status"],0)+1

    cols = st.columns(4)
    summary = [("🚛",status_counts.get("In Transit",0),"In Transit",AMBER),
               ("✅",status_counts.get("Delivered",0),"Delivered Today",GREEN_OK),
               ("🔵",status_counts.get("Available",0),"Available",BLUE_INFO),
               ("🔴",status_counts.get("Under Maint.",0),"Under Maintenance",RED_CRIT)]
    for col,(em,val,lab,c) in zip(cols,summary):
        with col: st.markdown(f"<div class='metric-card'><div style='font-size:1.5rem;'>{em}</div><div class='metric-val' style='color:{c};'>{val}</div><div class='metric-label'>{lab}</div></div>",unsafe_allow_html=True)

    st.markdown("<div class='jal-divider'></div>",unsafe_allow_html=True)

    for tk in FLEET:
        sc         = fleet_color(tk["status"])
        fuel_color = RED_CRIT if tk["fuel"]<30 else YELLOW_W if tk["fuel"]<60 else GREEN_OK

        # Build assignment line
        if tk["village"] != "—":
            assign_html = f"<div style='font-size:0.82rem;color:{BROWN};margin-top:0.2rem;'>📍 Assigned: {tk['village']} &nbsp;|&nbsp; ETA: {tk['eta']}</div>"
        else:
            assign_html = ""

        # Build fuel gauge OR workshop notice (no nested ternary in f-string)
        if tk["fuel"] > 0:
            right_html = f"""<div style='font-size:0.78rem;color:{MUTED};margin-bottom:3px;'>Fuel</div>
                <div style='background:{SAND_DARK};border-radius:20px;height:8px;width:80px;overflow:hidden;'>
                    <div style='background:{fuel_color};width:{tk["fuel"]}%;height:100%;border-radius:20px;'></div>
                </div>
                <div style='font-size:0.75rem;color:{MUTED};text-align:right;'>{tk["fuel"]}%</div>"""
        else:
            right_html = f"<div style='font-size:0.78rem;color:{RED_CRIT};font-weight:600;'>🔧 In Workshop</div>"

        # Build journey progress bar (only for In Transit)
        if tk["status"] == "In Transit":
            progress_pct  = max(0, 100 - int(tk["km_left"] / 0.38))
            progress_html = f"""<div style='margin-top:0.8rem;'>
                <div style='background:{SAND_DARK};border-radius:20px;height:8px;overflow:hidden;'>
                    <div style='background:linear-gradient(90deg,{AMBER},{TERRA});width:{progress_pct}%;height:100%;border-radius:20px;'></div>
                </div>
                <div style='font-size:0.77rem;color:{MUTED};margin-top:3px;'>{tk["km_left"]} km remaining to destination</div>
            </div>"""
        else:
            progress_html = ""

        card_html = (
            f"<div class='fleet-card' style='border-left-color:{sc};'>"
            f"<div style='display:flex;justify-content:space-between;align-items:flex-start;'>"
            f"<div>"
            f"<div style='font-size:1.05rem;font-weight:700;color:{BROWN};'>🚛 Tanker {tk['id']} <span style='background:{sc}22;color:{sc};border:1px solid {sc};border-radius:20px;padding:0.15rem 0.6rem;font-size:0.78rem;font-weight:600;margin-left:0.5rem;'>{tk['status']}</span></div>"
            f"<div style='font-size:0.82rem;color:{MUTED};margin-top:0.3rem;'>Capacity: {tk['cap']} &nbsp;|&nbsp; Driver: {tk['driver']}</div>"
            f"{assign_html}"
            f"</div>"
            f"<div style='text-align:right;'>{right_html}</div>"
            f"</div>"
            f"{progress_html}"
            f"</div>"
        )
        st.markdown(card_html, unsafe_allow_html=True)

# ── TAB 3: DELIVERY OTP ───────────────────────────────────────────────────────

def tab_delivery_otp():
    st.markdown(f"""<div class='alert-info'>
        🔐 <b>Delivery OTP Verification</b> — Generate a 4-digit OTP before delivery. 
        The Sarpanch confirms receipt by reading back the OTP. This prevents fake delivery reporting.
    </div>""",unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("<div class='jal-card'><div class='jal-card-title'>🔑 Generate Delivery OTP</div>",unsafe_allow_html=True)

        delivery_id = st.selectbox("Select Pending Delivery",
            [f"{d['id']} — {d['village']} ({d['tanker']}, ETA {d['eta']})" for d in PENDING_DELIVERIES],
            key="otp_delivery_select")
        selected_del = PENDING_DELIVERIES[[f"{d['id']} — {d['village']} ({d['tanker']}, ETA {d['eta']})" for d in PENDING_DELIVERIES].index(delivery_id)]

        if st.button("🔑 Generate OTP for This Delivery",use_container_width=True):
            otp = str(random.randint(1000,9999))
            st.session_state.otp_store[selected_del["id"]] = {"otp":otp,"generated":datetime.now().strftime("%H:%M:%S"),"village":selected_del["village"]}
            st.markdown(f"""<div class='otp-box'>
                <div style='font-size:0.85rem;color:{GREEN_OK};font-weight:600;margin-bottom:0.3rem;'>OTP for {selected_del['village']}</div>
                <div class='otp-code'>{otp}</div>
                <div style='font-size:0.78rem;color:{MUTED};margin-top:0.5rem;'>Share verbally with Sarpanch. Valid for this delivery only.</div>
            </div>""",unsafe_allow_html=True)
        elif selected_del["id"] in st.session_state.otp_store:
            otp_data = st.session_state.otp_store[selected_del["id"]]
            st.markdown(f"""<div class='otp-box'>
                <div style='font-size:0.85rem;color:{GREEN_OK};font-weight:600;margin-bottom:0.3rem;'>OTP for {otp_data['village']} (Generated {otp_data['generated']})</div>
                <div class='otp-code'>{otp_data['otp']}</div>
                <div style='font-size:0.78rem;color:{MUTED};margin-top:0.5rem;'>Share verbally with Sarpanch. Valid for this delivery only.</div>
            </div>""",unsafe_allow_html=True)

        st.markdown("</div>",unsafe_allow_html=True)

        # Confirm delivery form
        st.markdown("<div class='jal-card'><div class='jal-card-title'>✅ Confirm Delivery</div>",unsafe_allow_html=True)
        with st.form("confirm_delivery"):
            confirm_del = st.selectbox("Delivery ID",[(f"{d['id']} — {d['village']}") for d in PENDING_DELIVERIES])
            otp_entered = st.text_input("Enter OTP confirmed by Sarpanch",max_chars=4,placeholder="4-digit OTP")
            actual_litres = st.number_input("Actual Litres Delivered",1000,15000,12000,500)
            timestamp = st.text_input("Delivery Timestamp",value=datetime.now().strftime("%H:%M, %b %d"))
            remarks = st.text_area("Field Remarks",height=70,placeholder="Any observations, issues, or notes...")
            submitted = st.form_submit_button("✅ Confirm & Submit",use_container_width=True)

        if submitted:
            del_id = confirm_del.split(" — ")[0]
            stored = st.session_state.otp_store.get(del_id,{})
            if stored and otp_entered == stored.get("otp",""):
                st.markdown(f"<div class='alert-success'>✅ <b>OTP Verified!</b> Delivery for {stored['village']} confirmed — {actual_litres:,}L at {timestamp}</div>",unsafe_allow_html=True)
            elif otp_entered:
                st.markdown(f"<div class='alert-critical'>❌ <b>OTP Mismatch.</b> Please verify with Sarpanch and re-enter.</div>",unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='alert-warning'>⚠️ Please enter the OTP provided by the Sarpanch.</div>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='jal-card'><div class='jal-card-title'>📋 Pending Deliveries</div>",unsafe_allow_html=True)
        for d in PENDING_DELIVERIES:
            pc = RED_CRIT if d["priority"]=="High" else ORANGE_W
            st.markdown(f"""<div style='background:{SAND};border-radius:10px;padding:0.8rem 1rem;margin-bottom:0.7rem;border-left:4px solid {pc};'>
                <div style='display:flex;justify-content:space-between;'>
                    <b style='font-family:monospace;color:{AMBER};font-size:0.82rem;'>{d['id']}</b>
                    <span style='background:{pc}22;color:{pc};border:1px solid {pc};border-radius:20px;padding:0.1rem 0.5rem;font-size:0.75rem;font-weight:600;'>{d['priority']}</span>
                </div>
                <div style='font-size:0.9rem;font-weight:700;color:{BROWN};margin-top:0.3rem;'>{d['village']}</div>
                <div style='font-size:0.82rem;color:{MUTED};'>🚛 {d['tanker']} &nbsp;|&nbsp; {d['litres']:,}L &nbsp;|&nbsp; ETA {d['eta']}</div>
            </div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

        st.markdown("<div class='jal-card'><div class='jal-card-title'>✅ Confirmed Today</div>",unsafe_allow_html=True)
        for d in DELIVERIES_TODAY:
            st.markdown(f"""<div style='padding:0.6rem 0;border-bottom:1px solid {SAND};font-size:0.83rem;'>
                <div style='display:flex;justify-content:space-between;'>
                    <b style='font-family:monospace;color:{AMBER};'>{d['id']}</b>
                    <span style='color:{GREEN_OK};font-weight:600;'>{d['otp']}</span>
                </div>
                <div style='color:{BROWN};font-weight:600;'>{d['village']} — {d['litres']:,}L</div>
                <div style='color:{MUTED};'>🚛 {d['tanker']} &nbsp;|&nbsp; 🕐 {d['time']} &nbsp;|&nbsp; 👤 {d['sarpanch']}</div>
            </div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

# ── TAB 4: ESCALATION REPORTING ───────────────────────────────────────────────

def tab_escalation():
    open_esc = [e for e in ESCALATIONS if e["status"]!="Resolved"]
    if open_esc:
        st.markdown(f"<div class='alert-critical'>⚠️ <b>{len(open_esc)} open escalation(s)</b> require your attention.</div>",unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='alert-success'>✅ All escalations resolved. No open issues.</div>",unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("<div class='jal-card'><div class='jal-card-title'>⚡ Log New Escalation / Exception</div>",unsafe_allow_html=True)
        with st.form("escalation_form"):
            esc_type  = st.selectbox("Issue Type",["Tanker Delayed","Route Blocked","Water Quantity Insufficient","Borewell Failed","Village Access Problem","Driver Issue","SOS Alert Received","Other"])
            esc_vil   = st.selectbox("Village Affected",[v["name"] for v in VILLAGES_QUEUE])
            esc_tank  = st.text_input("Tanker ID (if relevant)",placeholder="e.g. TK-04")
            esc_pri   = st.selectbox("Priority",["High","Medium","Low"])
            esc_msg   = st.text_area("Describe the issue",height=100,placeholder="Clearly describe what happened and what action is needed...")
            notify_co = st.checkbox("📤 Also notify District Collector",value=esc_pri=="High")
            submitted = st.form_submit_button("⚡ Submit Escalation",use_container_width=True)

        if submitted and esc_msg:
            eid = f"ESC-{datetime.now().strftime('%Y%m%d-%H%M')}"
            notified = "Field Officer + Collector" if notify_co else "Field Officer only"
            st.markdown(f"<div class='alert-success'>✅ <b>Escalation Logged: {eid}</b><br>Type: {esc_type} | Village: {esc_vil} | Priority: {esc_pri}<br>Notified: {notified}</div>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='jal-card'><div class='jal-card-title'>📋 Escalation History</div>",unsafe_allow_html=True)
        for e in ESCALATIONS:
            pc = RED_CRIT if e["priority"]=="High" else ORANGE_W
            sc = GREEN_OK if e["status"]=="Resolved" else RED_CRIT
            si = "✅" if e["status"]=="Resolved" else "🔴"
            st.markdown(f"""<div class='esc-card' style='border-left:4px solid {pc};'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                        <b style='font-family:monospace;font-size:0.8rem;color:{AMBER};'>{e['id']}</b>
                        <span style='background:{pc}22;color:{pc};border:1px solid {pc};border-radius:20px;padding:0.1rem 0.5rem;font-size:0.75rem;font-weight:600;margin-left:0.5rem;'>{e['type']}</span>
                    </div>
                    <span style='color:{sc};font-weight:600;font-size:0.82rem;'>{si} {e['status']}</span>
                </div>
                <div style='font-weight:600;color:{BROWN};margin:0.3rem 0;font-size:0.9rem;'>📍 {e['village']}</div>
                <div style='font-size:0.83rem;color:{MUTED};'>{e['msg']}</div>
                <div style='font-size:0.77rem;color:{MUTED};margin-top:0.3rem;'>🕐 {e['time']}</div>
            </div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

# ── TAB 5: GROUND TRUTH DATA ENTRY ────────────────────────────────────────────

def tab_ground_truth():
    st.markdown(f"""<div class='alert-info'>
        📡 <b>Ground Truth Entry</b> — Update field observations to improve WSI accuracy. 
        Your data directly feeds into the drought forecasting model.
    </div>""",unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("<div class='jal-card'><div class='jal-card-title'>📝 Submit Field Observations</div>",unsafe_allow_html=True)
        with st.form("ground_truth_form"):
            gt_village  = st.selectbox("Village",     [v["name"] for v in VILLAGES_QUEUE])
            gt_date     = st.date_input("Observation Date",datetime.now().date())
            st.markdown(f"<div style='font-size:0.85rem;font-weight:600;color:{MUTED};margin:0.6rem 0 0.3rem;'>💧 Water Source Conditions</div>",unsafe_allow_html=True)
            bw_level    = st.slider("Borewell Water Level (m below surface)",0.0,20.0,8.0,0.1)
            bw_cond     = st.selectbox("Borewell Condition",["Good","Low","Very Low","Dry","Unknown"])
            canal_level = st.selectbox("Canal/Nala Status",["Flowing","Reduced Flow","Trickle","Completely Dry","N/A"])
            st.markdown(f"<div style='font-size:0.85rem;font-weight:600;color:{MUTED};margin:0.6rem 0 0.3rem;'>🌿 Ground Conditions</div>",unsafe_allow_html=True)
            soil_moisture = st.select_slider("Soil Moisture",["Bone Dry","Very Dry","Dry","Slightly Moist","Moist","Wet"])
            vegetation    = st.select_slider("Vegetation Health",["Dead/Wilting","Very Stressed","Stressed","Moderate","Healthy"])
            emergency     = st.checkbox("🚨 Flag as Emergency — Immediate Response Needed")
            notes         = st.text_area("Field Notes",height=80,placeholder="Any other observations...")
            submitted = st.form_submit_button("📡 Submit Ground Truth",use_container_width=True)

        if submitted:
            wsi_impact = 0
            if bw_cond in ["Very Low","Dry"]: wsi_impact += 8
            if canal_level in ["Completely Dry","Trickle"]: wsi_impact += 5
            if soil_moisture in ["Bone Dry","Very Dry"]: wsi_impact += 4
            if emergency: wsi_impact += 10
            st.markdown(f"""<div class='alert-success'>
                ✅ <b>Ground Truth Submitted!</b><br>
                Village: {gt_village} | Date: {gt_date}<br>
                Estimated WSI impact: <b>+{wsi_impact} pts</b> (model will recalculate)
                {'<br>🚨 <b>Emergency flag raised — Collector notified</b>' if emergency else ''}
            </div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    with col2:
        # Borewell status table
        st.markdown("<div class='jal-card'><div class='jal-card-title'>⛏️ Borewell Status Dashboard</div>",unsafe_allow_html=True)
        for bw in BOREWELL_DATA:
            cond_color = {"Good":GREEN_OK,"Low":YELLOW_W,"Very Low":ORANGE_W,"Dry":RED_CRIT}.get(bw["condition"],MUTED)
            st.markdown(f"""<div style='display:flex;justify-content:space-between;align-items:center;
                padding:0.55rem 0;border-bottom:1px solid {SAND};font-size:0.83rem;'>
                <div>
                    <div style='font-weight:600;color:{BROWN};'>{bw['village']}</div>
                    <div style='font-family:monospace;font-size:0.77rem;color:{AMBER};'>{bw['borewell']}</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:0.75rem;color:{MUTED};'>Depth</div>
                    <div style='font-weight:700;color:{BROWN};'>{str(bw['level_m'])+'m' if bw['level_m'] else 'Dry'}</div>
                    <div style='font-size:0.72rem;color:{ORANGE_W};'>{bw['change']}</div>
                </div>
                <div>
                    <span style='background:{cond_color}22;color:{cond_color};border:1px solid {cond_color};
                        border-radius:20px;padding:0.15rem 0.6rem;font-size:0.78rem;font-weight:600;'>
                        {bw['condition']}
                    </span>
                </div>
            </div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

        # Recent observations
        st.markdown("<div class='jal-card'><div class='jal-card-title'>📋 Recent Field Submissions</div>",unsafe_allow_html=True)
        recent_obs = [
            ("Feb 22","Chamorshi","BW low, soil very dry","⚡ WSI +6"),
            ("Feb 21","Mul","Canal trickle, veg stressed","⚡ WSI +3"),
            ("Feb 20","Sironcha","Good conditions, borewell stable","✅ No change"),
            ("Feb 19","Bhamragad","BW level dropped 1.2m","⚡ WSI +4"),
        ]
        for date,vil,obs,impact in recent_obs:
            ic = GREEN_OK if "No change" in impact else ORANGE_W
            st.markdown(f"""<div style='padding:0.45rem 0;border-bottom:1px solid {SAND};font-size:0.82rem;'>
                <div style='display:flex;justify-content:space-between;'>
                    <b style='color:{BROWN};'>{vil}</b>
                    <span style='color:{ic};font-size:0.78rem;font-weight:600;'>{impact}</span>
                </div>
                <div style='color:{MUTED};font-size:0.77rem;'>📅 {date} — {obs}</div>
            </div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

# ── MAIN ──────────────────────────────────────────────────────────────────────

def show():
    st.set_page_config(page_title="JalRakshak — Field Officer",page_icon="🚛",layout="wide",initial_sidebar_state="expanded")
    inject_css()
    o = OFFICER

    render_sidebar(o)

    in_transit = len([f for f in FLEET if f["status"]=="In Transit"])
    critical_v = len([v for v in VILLAGES_QUEUE if v["wsi"]>60])

    st.markdown(f"""<div style='background:linear-gradient(135deg,{TERRA} 0%,{BROWN} 100%);border-radius:14px;padding:1.4rem 2rem;margin-bottom:1.5rem;display:flex;align-items:center;justify-content:space-between;box-shadow:0 4px 18px rgba(193,68,14,0.25);'>
        <div>
            <div style='color:white;font-size:1.6rem;font-weight:800;letter-spacing:-0.02em;'>🚛 JalRakshak — Field Officer Dashboard</div>
            <div style='color:rgba(255,255,255,0.85);font-size:0.85rem;margin-top:0.2rem;'>👷 {o['name']} &nbsp;|&nbsp; 📍 {o['zone']}</div>
        </div>
        <div style='display:flex;gap:1.5rem;'>
            <div style='text-align:center;'>
                <div style='font-size:0.72rem;color:rgba(255,255,255,0.75);'>In Transit</div>
                <div style='font-size:1.8rem;font-weight:800;color:white;'>{in_transit}</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:0.72rem;color:rgba(255,255,255,0.75);'>Critical Villages</div>
                <div style='font-size:1.8rem;font-weight:800;color:#FFCCBC;'>{critical_v}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    nav_items = [("🗂️ Priority Queue","queue"),("🚛 Fleet Status","fleet"),("🔑 Delivery OTP","otp"),("⚡ Escalation","esc"),("📡 Ground Truth","ground")]
    if "field_tab" not in st.session_state: st.session_state.field_tab = "queue"

    cols = st.columns(len(nav_items))
    for col,(label,key) in zip(cols,nav_items):
        with col:
            if st.button(label,key=f"fnav_{key}",use_container_width=True):
                st.session_state.field_tab = key; st.rerun()

    st.markdown(f"<div style='height:2px;background:linear-gradient(90deg,{TERRA},{SAND_DARK},transparent);margin:1rem 0;'></div>",unsafe_allow_html=True)

    active = st.session_state.field_tab
    if active=="queue":  tab_priority_queue()
    elif active=="fleet":  tab_fleet_status()
    elif active=="otp":    tab_delivery_otp()
    elif active=="esc":    tab_escalation()
    elif active=="ground": tab_ground_truth()

if __name__=="__main__":
    show()
