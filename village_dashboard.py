"""
JalRakshak — Village Officer / Sarpanch Dashboard
Dashboard 2: Village-Level Monitoring & Request Portal
"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

AMBER = "#D4820A"; TERRA = "#C1440E"; SAND = "#F5ECD7"
SAND_DARK = "#EAD9B8"; CREAM = "#FDFAF4"; BROWN = "#5C3317"
MUTED = "#8B6F47"; WHITE = "#FFFFFF"; GREEN_OK = "#2E7D32"
RED_CRIT = "#B71C1C"; ORANGE_W = "#E65100"; YELLOW_W = "#F57F17"

VILLAGE_DATA = {
    "name": "Kurkheda", "district": "Gadchiroli", "state": "Maharashtra",
    "population": 4820, "households": 964, "wsi": 72, "alert_level": "Warning",
    "days_since_rain": 18, "last_rain_date": "Feb 05, 2026",
    "rainfall_normal": 12.4, "rainfall_actual": 4.1, "rainfall_deviation": -67,
    "groundwater_level": 8.3, "groundwater_trend": -2.1, "water_availability_days": 6,
    "borewells_functional": 3, "borewells_total": 5,
    "last_tanker_date": "Feb 20, 2026", "last_tanker_litres": 12000,
    "officer_name": "Sarpanch Ramrao Bhoyar", "field_officer": "Suresh Deshmukh",
}

TANKERS = [
    {"id":"TK-04","capacity":"12,000 L","status":"In Transit","departure":"09:15 AM","eta":"11:30 AM",
     "depot":"Gadchiroli Depot","distance_km":38,"driver":"Raju Meshram","phone":"9876543210","progress":65},
    {"id":"TK-11","capacity":"10,000 L","status":"Scheduled","departure":"02:00 PM","eta":"04:20 PM",
     "depot":"Armori Sub-Depot","distance_km":24,"driver":"Dilip Pawar","phone":"9823412345","progress":0},
]

SUPPLY_HISTORY = [
    {"date":"Feb 20, 2026","tanker":"TK-09","litres":12000,"status":"Delivered","hh":280},
    {"date":"Feb 16, 2026","tanker":"TK-03","litres":10000,"status":"Delivered","hh":240},
    {"date":"Feb 11, 2026","tanker":"TK-07","litres":12000,"status":"Delivered","hh":280},
    {"date":"Feb 06, 2026","tanker":"TK-12","litres": 8000,"status":"Delivered","hh":190},
    {"date":"Jan 31, 2026","tanker":"TK-03","litres":10000,"status":"Delivered","hh":240},
    {"date":"Jan 26, 2026","tanker":"TK-09","litres": 6000,"status":"Partial",  "hh":140},
    {"date":"Jan 20, 2026","tanker":"TK-02","litres":12000,"status":"Delivered","hh":280},
]

NOTIFICATIONS = [
    {"icon":"🚛","time":"Today 9:15 AM","msg":"Tanker TK-04 dispatched from Gadchiroli Depot. ETA 11:30 AM.","type":"info"},
    {"icon":"🌡️","time":"Today 8:00 AM","msg":"Drought Warning active. WSI score crossed 70. Reduce water usage.","type":"warning"},
    {"icon":"✅","time":"Feb 20, 3:45 PM","msg":"Tanker TK-09 delivery confirmed. 12,000 L supplied to 280 households.","type":"success"},
    {"icon":"📋","time":"Feb 19, 11:00 AM","msg":"Tanker Request #TR-2026-0219 approved by Field Officer Suresh Deshmukh.","type":"success"},
    {"icon":"🌧️","time":"Feb 05, 6:00 AM","msg":"Last rainfall recorded: 4.1mm. Next expected: Low probability in 10 days.","type":"info"},
    {"icon":"⚠️","time":"Feb 04, 9:00 AM","msg":"Groundwater dropped 2.1m in 30 days. Borewell #2 reported dry.","type":"warning"},
]

SOS_LOG = [
    {"id":"SOS-2026-003","date":"Feb 10, 2026","reason":"Borewell #4 failure, 1200 people without water","status":"Resolved","hrs":4},
    {"id":"SOS-2026-001","date":"Jan 22, 2026","reason":"Acute drought — 3 consecutive tanker delays","status":"Resolved","hrs":6},
]

WSI_TREND = {"dates":["Jan 10","Jan 17","Jan 24","Feb 01","Feb 08","Feb 15","Feb 23"],"wsi":[41,48,54,60,65,69,72]}
RAINFALL_TREND = {"months":["Sep'25","Oct'25","Nov'25","Dec'25","Jan'26","Feb'26"],"normal":[180,42,8,4,6,12],"actual":[165,38,2,0,1,4]}

def wsi_badge(wsi):
    if wsi<=30: return "🟢","Normal","#2E7D32","#E8F5E9"
    elif wsi<=60: return "🟡","Watch","#F57F17","#FFF8E1"
    elif wsi<=80: return "🟠","Warning","#E65100","#FBE9E7"
    else: return "🔴","Critical","#B71C1C","#FFEBEE"

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
    .tanker-card{{background:{WHITE};border:2px solid {SAND_DARK};border-radius:14px;padding:1.2rem;margin-bottom:0.8rem;border-left:5px solid {AMBER};}}
    .notif-card{{display:flex;gap:1rem;align-items:flex-start;background:{WHITE};border:1.5px solid {SAND_DARK};border-radius:10px;padding:0.9rem 1.1rem;margin-bottom:0.7rem;}}
    .jal-divider{{height:2px;background:linear-gradient(90deg,{AMBER},{SAND_DARK},transparent);border:none;margin:1.2rem 0;border-radius:2px;}}
    .supply-row{{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:0.5rem;padding:0.7rem 0.5rem;border-bottom:1px solid {SAND};font-size:0.88rem;align-items:center;}}
    #MainMenu{{visibility:hidden;}}footer{{visibility:hidden;}}
    </style>""", unsafe_allow_html=True)

def render_sidebar(v):
    icon, level, color, bg = wsi_badge(v["wsi"])
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:1rem 0;'>
            <div style='font-size:2.4rem;'>🏘️</div>
            <div style='font-size:1.1rem;font-weight:700;color:{BROWN};'>{v['name']} Village</div>
            <div style='font-size:0.82rem;color:{MUTED};margin-top:0.2rem;'>📍 {v['district']}, {v['state']}</div>
            <div style='font-size:0.8rem;color:{MUTED};'>👤 {v['officer_name']}</div>
        </div>
        <hr style='border:1px solid {SAND_DARK};'>
        <div style='background:{WHITE};border:2px solid {color};border-radius:12px;padding:1rem;text-align:center;margin-bottom:1rem;'>
            <div style='font-size:0.75rem;font-weight:600;color:{MUTED};text-transform:uppercase;letter-spacing:0.06em;'>Water Stress Index</div>
            <div style='font-size:2.8rem;font-weight:800;color:{color};line-height:1;'>{v['wsi']}</div>
            <div style='font-size:0.8rem;margin-top:0.2rem;background:{bg};color:{color};border:1px solid {color};border-radius:20px;padding:0.2rem 0.75rem;display:inline-block;font-weight:600;'>{icon} {level}</div>
        </div>
        <div style='font-size:0.82rem;color:{MUTED};line-height:2.2;'>
            🌧️ Last Rain: <b style='color:{BROWN};'>{v['last_rain_date']}</b><br>
            📅 Days Without Rain: <b style='color:{TERRA};'>{v['days_since_rain']} days</b><br>
            👥 Population: <b style='color:{BROWN};'>{v['population']:,}</b><br>
            🏚️ Households: <b style='color:{BROWN};'>{v['households']:,}</b><br>
            ⛏️ Borewells OK: <b style='color:{GREEN_OK};'>{v['borewells_functional']}/{v['borewells_total']}</b>
        </div>
        <hr style='border:1px solid {SAND_DARK};'>
        <div style='background:#FFEBEE;border:1px solid #EF9A9A;border-radius:8px;padding:0.7rem;font-size:0.8rem;color:{RED_CRIT};margin-bottom:0.7rem;'>
            ⚠️ <b>Drought Warning Active</b><br>Est. {v['water_availability_days']} days water remaining
        </div>
        <div style='font-size:0.78rem;color:{MUTED};text-align:center;'>
            Field Officer: <b style='color:{BROWN};'>{v['field_officer']}</b>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

def tab_village_status(v):
    icon, level, color, bg = wsi_badge(v["wsi"])
    st.markdown(f"""<div class='alert-warning'>
        🌵 <b>Drought {level} Active</b> — WSI: <b>{v['wsi']}/100</b> &nbsp;|&nbsp;
        <b>{v['days_since_rain']} days</b> without rain &nbsp;|&nbsp;
        Est. <b>{v['water_availability_days']} days</b> of water remaining
    </div>""", unsafe_allow_html=True)

    metrics = [("💧",f"{v['wsi']}/100","Water Stress Index",color),("🌧️",f"{v['days_since_rain']}d","Days No Rainfall",TERRA),
               ("📉",f"{v['rainfall_deviation']}%","Rainfall vs Normal",ORANGE_W),("⛏️",f"{v['groundwater_level']}m","Groundwater Depth",MUTED)]
    cols = st.columns(4)
    for col,(em,val,lab,c) in zip(cols,metrics):
        with col: st.markdown(f"<div class='metric-card'><div style='font-size:1.6rem;'>{em}</div><div class='metric-val' style='color:{c};'>{val}</div><div class='metric-label'>{lab}</div></div>",unsafe_allow_html=True)

    st.markdown("<div class='jal-divider'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='jal-card-title'>📊 WSI Trend (6 Weeks)</div>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=WSI_TREND["dates"],y=WSI_TREND["wsi"],mode="lines+markers",
            line=dict(color=AMBER,width=3),marker=dict(size=7,color=AMBER),fill="tozeroy",fillcolor="rgba(212,130,10,0.1)"))
        fig.add_hline(y=60,line_dash="dot",line_color=ORANGE_W,annotation_text="Warning",annotation_font_color=ORANGE_W)
        fig.add_hline(y=80,line_dash="dot",line_color=RED_CRIT,annotation_text="Critical",annotation_font_color=RED_CRIT)
        fig.update_layout(paper_bgcolor="white",plot_bgcolor="white",margin=dict(t=20,b=20,l=10,r=10),height=220,
            xaxis=dict(showgrid=False),yaxis=dict(range=[0,100],showgrid=True,gridcolor=SAND),showlegend=False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with col2:
        st.markdown("<div class='jal-card-title'>🌧️ Rainfall vs Normal (mm)</div>", unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=RAINFALL_TREND["months"],y=RAINFALL_TREND["normal"],name="Normal",marker_color=SAND_DARK))
        fig2.add_trace(go.Bar(x=RAINFALL_TREND["months"],y=RAINFALL_TREND["actual"],name="Actual",marker_color=TERRA))
        fig2.update_layout(paper_bgcolor="white",plot_bgcolor="white",barmode="group",
            margin=dict(t=20,b=20,l=10,r=10),height=220,yaxis=dict(showgrid=True,gridcolor=SAND),
            legend=dict(orientation="h",yanchor="bottom",y=1,font=dict(size=10)))
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<div class='jal-card-title'>🎯 Current WSI Gauge</div>", unsafe_allow_html=True)
        fig3 = go.Figure(go.Indicator(mode="gauge+number",value=v["wsi"],
            number={"suffix":"/100","font":{"size":28,"color":color,"family":"Sora"}},
            gauge={"axis":{"range":[0,100]},"bar":{"color":color,"thickness":0.28},"bgcolor":"white",
                   "steps":[{"range":[0,30],"color":"#E8F5E9"},{"range":[30,60],"color":"#FFF8E1"},
                             {"range":[60,80],"color":"#FBE9E7"},{"range":[80,100],"color":"#FFEBEE"}],
                   "threshold":{"line":{"color":RED_CRIT,"width":3},"thickness":0.8,"value":80}}))
        fig3.update_layout(paper_bgcolor="white",margin=dict(t=20,b=10,l=20,r=20),height=200)
        st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

    with col4:
        st.markdown("<div class='jal-card-title'>📋 Village Vitals</div>", unsafe_allow_html=True)
        vitals = [("🌧️","Last Rainfall",v["last_rain_date"],"info"),
                  ("📏","Actual vs Normal",f"{v['rainfall_actual']}mm vs {v['rainfall_normal']}mm","warning"),
                  ("⛏️","Groundwater",f"{v['groundwater_level']}m depth (↓{abs(v['groundwater_trend'])}m/mo)","warning"),
                  ("🚛","Last Tanker",f"{v['last_tanker_date']} — {v['last_tanker_litres']:,}L","info"),
                  ("⚙️","Borewells",f"{v['borewells_functional']}/{v['borewells_total']} functional","info")]
        for em,lab,val,typ in vitals:
            cls = "alert-warning" if typ=="warning" else "alert-info"
            st.markdown(f"<div class='{cls}' style='padding:0.5rem 0.9rem;margin-bottom:0.45rem;font-size:0.85rem;'>{em} <b>{lab}:</b> {val}</div>",unsafe_allow_html=True)

def tab_tanker_request(v):
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown("<div class='jal-card-title'>📝 Submit Water Tanker Request</div>", unsafe_allow_html=True)
        with st.form("tanker_req"):
            urgency = st.selectbox("🚨 Urgency Level",["Critical — People without water NOW","High — Will run out in 1–2 days","Medium — Supplies running low","Low — Routine replenishment"])
            pop_aff = st.number_input("👥 Population Affected",0,v["population"],min(1200,v["population"]),50)
            litres  = st.number_input("💧 Litres Required",1000,50000,12000,1000)
            pref_date = st.date_input("📅 Preferred Delivery Date",datetime.now().date()+timedelta(days=1))
            pref_time = st.selectbox("⏰ Preferred Time Slot",["Morning (6–10 AM)","Midday (10 AM–2 PM)","Afternoon (2–6 PM)"])
            issue   = st.selectbox("🔧 Primary Water Issue",["Borewells Dry/Low","Canal/Nala Dry","Pipeline Broken","No Other Source Available","Other"])
            remarks = st.text_area("📌 Additional Remarks",placeholder="Describe the situation...",height=90)
            submit  = st.form_submit_button("📨 Submit Tanker Request",use_container_width=True)
        if submit:
            rid = f"TR-{datetime.now().strftime('%Y%m%d-%H%M')}"
            priority = "High" if "Critical" in urgency or "High" in urgency else "Medium"
            st.markdown(f"<div class='alert-success'>✅ <b>Request Submitted!</b> ID: <code>{rid}</code><br>Priority: <b>{priority}</b> — Routing to Field Officer {v['field_officer']}</div>",unsafe_allow_html=True)

    with col2:
        _, level, color, bg = wsi_badge(v["wsi"])
        st.markdown(f"""<div class='jal-card' style='border-color:{color};'>
            <div class='jal-card-title'>📊 System Validation</div>
            <div style='font-size:0.82rem;color:{MUTED};margin-bottom:0.8rem;'>
                System cross-checks your request against live WSI data to prevent misuse.
            </div>""", unsafe_allow_html=True)
        checks = [("WSI Score",f"{v['wsi']}/100 — {level}",v['wsi']>40),("Days Without Rain",f"{v['days_since_rain']} days",v['days_since_rain']>7),
                  ("Groundwater",f"{v['groundwater_level']}m depth",v['groundwater_level']>7),("Last Supply",v["last_tanker_date"],True),("Borewells",f"{v['borewells_functional']}/{v['borewells_total']} OK",v['borewells_functional']<v['borewells_total'])]
        for lab,val,flag in checks:
            dot = "🔴" if flag and v["wsi"]>60 else "🟡" if flag else "🟢"
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid {SAND};font-size:0.83rem;'><span style='color:{MUTED};'>{dot} {lab}</span><span style='font-weight:600;color:{BROWN};'>{val}</span></div>",unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='jal-card'><div class='jal-card-title'>📋 Recent Requests</div>",unsafe_allow_html=True)
        for rid,date,status,icon_r in [("TR-20260219-1412","Feb 19","Approved","✅"),("TR-20260211-0830","Feb 11","Approved","✅"),("TR-20260203-1100","Feb 03","Resolved","✅"),("TR-20260126-0900","Jan 26","Partial","🟡")]:
            c = GREEN_OK if status in ["Approved","Resolved"] else YELLOW_W
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid {SAND};font-size:0.82rem;'><span style='font-family:monospace;color:{AMBER};'>{rid}</span><span style='color:{MUTED};'>{date}</span><span style='color:{c};font-weight:600;'>{icon_r} {status}</span></div>",unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def tab_arrival_tracker():
    for tk in TANKERS:
        sc = AMBER if tk["status"]=="In Transit" else MUTED
        si = "🚛" if tk["status"]=="In Transit" else "⏳"
        st.markdown(f"""<div class='tanker-card'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                    <div style='font-size:1.1rem;font-weight:700;color:{BROWN};'>{si} Tanker {tk['id']}</div>
                    <div style='font-size:0.82rem;color:{MUTED};margin-top:0.2rem;'>Capacity: {tk['capacity']} | From: {tk['depot']}</div>
                    <div style='font-size:0.82rem;color:{MUTED};'>Driver: {tk['driver']} 📞 {tk['phone']}</div>
                </div>
                <div style='text-align:right;'>
                    <span style='background:{sc}22;color:{sc};border:1px solid {sc};border-radius:20px;padding:0.25rem 0.85rem;font-size:0.8rem;font-weight:600;'>{tk['status']}</span>
                    <div style='font-size:1.1rem;font-weight:700;color:{TERRA};margin-top:0.4rem;'>ETA: {tk['eta']}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        if tk["status"]=="In Transit":
            p = tk["progress"]
            st.markdown(f"""<div style='margin-top:0.8rem;'>
                <div style='display:flex;justify-content:space-between;font-size:0.78rem;color:{MUTED};margin-bottom:4px;'>
                    <span>🏭 Departed {tk['departure']}</span><span>{p}% of route</span><span>🏘️ ETA {tk['eta']}</span>
                </div>
                <div style='background:{SAND_DARK};border-radius:20px;height:10px;overflow:hidden;'>
                    <div style='background:linear-gradient(90deg,{AMBER},{TERRA});width:{p}%;height:100%;border-radius:20px;'></div>
                </div>
                <div style='font-size:0.77rem;color:{MUTED};margin-top:4px;'>🛣️ {int(tk['distance_km']*p/100)} km covered of {tk['distance_km']} km total</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='margin-top:0.7rem;background:{SAND};border-radius:8px;padding:0.5rem 0.8rem;font-size:0.82rem;color:{MUTED};'>⏳ Scheduled departure at {tk['departure']} — {tk['distance_km']} km from depot</div>",unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='jal-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='jal-card'><div class='jal-card-title'>🗺️ Today's Delivery Timeline</div>",unsafe_allow_html=True)
    timeline = [("09:15 AM","TK-04 departed Gadchiroli Depot",True),("09:48 AM","TK-04 reached Armori checkpoint",True),
                ("10:15 AM","TK-04 currently en route — 35% remaining",True),("11:30 AM","TK-04 expected arrival at village point",False),
                ("02:00 PM","TK-11 scheduled departure from Armori Sub-Depot",False),("04:20 PM","TK-11 expected arrival at village point",False)]
    for t,ev,done in timeline:
        dot_bg = GREEN_OK if done else SAND_DARK
        tc = BROWN if done else MUTED
        st.markdown(f"""<div style='display:flex;gap:1rem;align-items:flex-start;margin-bottom:0.7rem;'>
            <div style='width:12px;height:12px;border-radius:50%;background:{dot_bg};margin-top:5px;flex-shrink:0;border:2px solid white;box-shadow:0 0 0 2px {dot_bg};'></div>
            <div><div style='font-size:0.78rem;font-weight:600;color:{AMBER};'>{t}</div>
            <div style='font-size:0.87rem;color:{tc};'>{ev}</div></div></div>""",unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def tab_supply_history():
    total_l = sum(s["litres"] for s in SUPPLY_HISTORY)
    delivered = len([s for s in SUPPLY_HISTORY if s["status"]=="Delivered"])
    cols = st.columns(3)
    for col,(em,val,lab) in zip(cols,[("📦",f"{len(SUPPLY_HISTORY)}","Total Deliveries"),("💧",f"{total_l:,}L","Total Litres"),("📊",f"{total_l//len(SUPPLY_HISTORY):,}L","Avg Per Delivery")]):
        with col: st.markdown(f"<div class='metric-card'><div style='font-size:1.5rem;'>{em}</div><div class='metric-val'>{val}</div><div class='metric-label'>{lab}</div></div>",unsafe_allow_html=True)

    st.markdown("<div class='jal-divider'></div>",unsafe_allow_html=True)
    dates_r = [s["date"] for s in SUPPLY_HISTORY][::-1]; litres_r = [s["litres"] for s in SUPPLY_HISTORY][::-1]
    fig = go.Figure(go.Bar(x=dates_r,y=litres_r,marker_color=AMBER,text=[f"{l//1000}kL" for l in litres_r],textposition="outside"))
    fig.update_layout(paper_bgcolor="white",plot_bgcolor="white",margin=dict(t=20,b=20,l=30,r=10),height=240,
        xaxis=dict(showgrid=False),yaxis=dict(showgrid=True,gridcolor=SAND,title="Litres"),font=dict(family="Sora"))
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    st.markdown(f"<div class='jal-card'><div class='jal-card-title'>📋 Delivery Log</div><div class='supply-row' style='background:{SAND};border-radius:8px;font-weight:700;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em;color:{MUTED};'><span>Date</span><span>Tanker</span><span>Litres</span><span>Status</span></div>",unsafe_allow_html=True)
    for s in SUPPLY_HISTORY:
        sc = GREEN_OK if s["status"]=="Delivered" else YELLOW_W
        si = "✅" if s["status"]=="Delivered" else "🟡"
        st.markdown(f"<div class='supply-row'><span style='color:{BROWN};'>{s['date']}</span><span style='font-family:monospace;color:{AMBER};'>{s['tanker']}</span><span style='color:{BROWN};font-weight:600;'>{s['litres']:,} L</span><span style='color:{sc};font-weight:600;'>{si} {s['status']}</span></div>",unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)

def tab_community_board(v):
    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.markdown(f"<div class='jal-card'><div class='jal-card-title'>📣 Community Notification Board</div>",unsafe_allow_html=True)
        type_colors = {"info":AMBER,"warning":ORANGE_W,"success":GREEN_OK}
        for n in NOTIFICATIONS:
            bc = type_colors.get(n["type"],AMBER)
            st.markdown(f"""<div class='notif-card' style='border-left:4px solid {bc};'>
                <div style='font-size:1.5rem;flex-shrink:0;'>{n['icon']}</div>
                <div><div style='font-size:0.85rem;color:{BROWN};'>{n['msg']}</div>
                <div style='font-size:0.75rem;color:{MUTED};margin-top:0.25rem;'>🕐 {n['time']}</div></div>
            </div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class='jal-card' style='border:2px solid {RED_CRIT};'>
            <div class='jal-card-title' style='color:{RED_CRIT};'>🆘 Emergency SOS Alert</div>
            <div style='font-size:0.85rem;color:{MUTED};margin-bottom:1rem;'>
                Use ONLY in water emergencies. Instantly alerts the Field Officer <b>AND</b> District Collector.
            </div>""",unsafe_allow_html=True)

        sos_reason = st.selectbox("Emergency Type",["Select type...","Borewell failure — village without water","Tanker not arrived — 48+ hours overdue","Water source contaminated / toxic","Flood / pipeline burst / damage","Mass illness linked to water quality","Other critical emergency"],key="sos_type")
        sos_people = st.number_input("People directly affected",0,v["population"],500,50,key="sos_people")
        sos_detail = st.text_area("Brief description",key="sos_detail",height=65,placeholder="Describe the emergency clearly...")

        if st.button("🆘 SEND SOS ALERT — ESCALATE NOW",use_container_width=True,type="primary"):
            if sos_reason=="Select type...": st.error("Please select an emergency type first.")
            else:
                sid = f"SOS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                st.markdown(f"<div class='alert-critical'>🆘 <b>SOS SENT — {sid}</b><br>Notified: Field Officer {v['field_officer']} + District Collector<br>People affected: {sos_people} | Response expected: <b>2–4 hours</b></div>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

        st.markdown(f"<div class='jal-card'><div class='jal-card-title'>📜 SOS History</div>",unsafe_allow_html=True)
        for s in SOS_LOG:
            st.markdown(f"""<div style='padding:0.5rem 0;border-bottom:1px solid {SAND};font-size:0.82rem;'>
                <div style='display:flex;justify-content:space-between;'>
                    <b style='font-family:monospace;color:{AMBER};'>{s['id']}</b>
                    <span style='color:{GREEN_OK};'>✅ {s['status']}</span>
                </div>
                <div style='color:{MUTED};margin-top:0.2rem;'>{s['reason']}</div>
                <div style='color:{MUTED};font-size:0.77rem;'>📅 {s['date']} | ⚡ {s['hrs']}hrs response</div>
            </div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

def show():
    st.set_page_config(page_title="JalRakshak — Village Officer",page_icon="💧",layout="wide",initial_sidebar_state="expanded")
    inject_css()
    v = VILLAGE_DATA
    render_sidebar(v)
    _, level, color, _ = wsi_badge(v["wsi"])

    st.markdown(f"""<div style='background:linear-gradient(135deg,{AMBER} 0%,{TERRA} 100%);border-radius:14px;padding:1.4rem 2rem;margin-bottom:1.5rem;display:flex;align-items:center;justify-content:space-between;box-shadow:0 4px 18px rgba(212,130,10,0.25);'>
        <div>
            <div style='color:white;font-size:1.6rem;font-weight:800;letter-spacing:-0.02em;'>💧 JalRakshak — Village Dashboard</div>
            <div style='color:rgba(255,255,255,0.85);font-size:0.85rem;margin-top:0.2rem;'>🏘️ {v['name']} Village &nbsp;|&nbsp; 📍 {v['district']}, {v['state']}</div>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:0.78rem;color:rgba(255,255,255,0.8);'>Water Stress Index</div>
            <div style='font-size:2.2rem;font-weight:800;color:white;line-height:1.1;'>{v['wsi']}</div>
            <div style='font-size:0.82rem;color:rgba(255,255,255,0.9);'>⚠️ {level}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    nav_items = [("🌡️ Village Status","status"),("📋 Tanker Request","request"),("🚛 Arrival Tracker","tracker"),("📦 Supply History","history"),("📣 Community Board","board")]
    if "village_tab" not in st.session_state: st.session_state.village_tab = "status"

    cols = st.columns(len(nav_items))
    for col,(label,key) in zip(cols,nav_items):
        with col:
            if st.button(label,key=f"vnav_{key}",use_container_width=True):
                st.session_state.village_tab = key; st.rerun()

    st.markdown(f"<div style='height:2px;background:linear-gradient(90deg,{AMBER},{SAND_DARK},transparent);margin:1rem 0;'></div>",unsafe_allow_html=True)

    active = st.session_state.village_tab
    if active=="status": tab_village_status(v)
    elif active=="request": tab_tanker_request(v)
    elif active=="tracker": tab_arrival_tracker()
    elif active=="history": tab_supply_history()
    elif active=="board": tab_community_board(v)

if __name__=="__main__":
    show()
