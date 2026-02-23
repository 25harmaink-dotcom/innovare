# 💧 JalRakshak — Integrated Drought Warning & Smart Tanker Management System

> **Shifting water governance from crisis management → preventive planning**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Leaflet](https://img.shields.io/badge/Leaflet-199900?logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)

---

## 🎯 Problem Statement

Districts respond to drought **after** it hits. JalRakshak predicts emerging drought stress using rainfall and groundwater trends, enabling district authorities to **proactively** plan and optimize water tanker allocation — saving lives and ₹ crores in reactive crisis spending.

---

## ✨ Core Features

### 📊 Village-Level Water Stress Index (WSI)
A composite 0–100 score per village calculated in real time from:
- Rainfall deviation from normal (30%)
- Groundwater level drop (25%)
- Historical drought frequency (20%)
- Population density / water access (15%)
- Days since last rainfall (10%)

| Range | Status | Action |
|-------|--------|--------|
| 🟢 0–30 | Normal | Monitor |
| 🟡 31–60 | Watch | Prepare |
| 🟠 61–80 | Warning | Mobilize |
| 🔴 81–100 | Critical | Emergency |

### 🗺️ Drought Early Warning Heatmap
Live Leaflet.js map with color-coded village markers. Click any marker to see WSI breakdown, population, tanker status, and groundwater data.

### 🎛️ Digital Twin Simulator ⭐ WOW Feature
The **hackathon hero feature**. Drag four sliders to simulate future drought scenarios in real time:
- Rainfall reduction (0–80%)
- Days ahead (7–30)
- Temperature anomaly (+0–5°C)
- Litres per person per day (30–70L)

Watch the map turn red and tanker demand spike — judges gasp.

### 🚛 Priority-Based Smart Tanker Allocation
One-click "Auto-Allocate" assigns available tankers to highest-need villages first based on WSI, population vulnerability, days without supply, and distance from depot.

### 🗺️ Greedy Route Optimizer
Nearest-neighbor TSP algorithm calculates the most efficient visit order for each tanker. Draws polylines on Leaflet map with numbered stops, cumulative distances, and ETAs.

### 🔮 Predictive Tanker Demand Forecast
7/14/30 day demand forecasting:
```
demand_liters = population × lpd × days × wsi_multiplier × seasonal_factor
```
Seasonal multipliers: Summer 1.5x | Winter 1.0x | Monsoon 0.3x

### 🌾 Farmer Drought Advisory
When village WSI crosses 60, farmer dashboard auto-activates drought mode with adjusted irrigation plans and water-saving scheme recommendations.

---

## 👥 User Roles

| Role | Interface | Key Features |
|------|-----------|--------------|
| 🏛️ **District Collector** | Web Dashboard | Command overview, Risk map, Tanker allocation, Digital Twin, Policy alerts |
| 👷 **Field Officer** | Web Dashboard | Priority queue, Fleet status, OTP verification, Route optimizer, Ground truth |
| 🏘️ **Sarpanch** | Web Dashboard | Village status, Tanker requests, Arrival tracker, Community board, SOS |

---

## 🌐 Multi-Language Support

JalRakshak supports 11 Indian languages:

| Code | Language | Code | Language |
|------|----------|------|----------|
| en | English | te | Telugu |
| hi | हिंदी | kn | ಕನ್ನಡ |
| mr | मराठी | gu | ગુજરાતી |
| ta | தமிழ் | bn | বাংলা |
| ml | മലയാളം | or | ଓଡ଼ିଆ |
| pa | ਪੰਜਾਬੀ | | |

---

## 🛠️ Tech Stack

This is a **zero-dependency, single-file frontend prototype** designed for hackathon speed and demo reliability.

| Layer | Technology |
|-------|-----------|
| UI Framework | Vanilla HTML5 + CSS3 + JavaScript ES6 |
| Maps | [Leaflet.js](https://leafletjs.com/) v1.9.4 via CDN |
| Charts | [Chart.js](https://www.chartjs.org/) v4.4 via CDN |
| Fonts | Google Fonts (Rajdhani, Noto Sans Devanagari, IBM Plex Mono) |
| Tile Provider | OpenStreetMap (free, no API key) |
| Hosting | Any static file server or GitHub Pages |

**Production stack** (recommended upgrade path):
- React.js + Tailwind CSS → Dashboards
- React Native → Driver Mobile App
- Node.js + Express → REST API
- Python FastAPI → ML microservice
- PostgreSQL → Primary database
- Redis → Caching

---

## 🚀 Quick Start

### Option 1: Direct Open (Simplest)
```bash
# Clone the repo
git clone https://github.com/your-org/jalrakshak.git
cd jalrakshak

# Open directly in browser
open jalrakshak_portal.html
# or on Linux:
xdg-open jalrakshak_portal.html
```

### Option 2: Local HTTP Server
```bash
# Python 3
python3 -m http.server 8080

# Node.js
npx serve .

# Then open: http://localhost:8080/jalrakshak_portal.html
```

### Option 3: GitHub Pages
1. Fork this repository
2. Go to Settings → Pages
3. Set source to main branch, root directory
4. Access at `https://yourusername.github.io/jalrakshak/jalrakshak_portal.html`

---

## 📁 Project Structure

```
jalrakshak/
├── jalrakshak_portal.html    # Complete single-file app (main file)
├── data/
│   └── villages.csv          # Sample village data (Gadchiroli district, MH)
├── docs/
│   ├── FEATURES.md           # Detailed feature documentation
│   ├── WSI_FORMULA.md        # Water Stress Index calculation guide
│   └── DEMO_SCRIPT.md        # Hackathon demo walkthrough
├── scripts/
│   └── generate_villages.py  # Script to generate demo village data
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🎮 Demo Walkthrough

### Best Demo Flow (5 minutes):

**1. Login as Collector (District)**
- Select Maharashtra → Gadchiroli → any district
- Enter any 10-digit number, copy OTP shown, verify

**2. Command Overview** → Show metrics, rainfall chart, policy alerts

**3. Risk Map** → Zoom into colored markers, click a village for popup

**4. 🎛️ Digital Twin (WOW MOMENT)**
- Slide "Rainfall Reduction" from 0% to 60%
- Watch red zones expand on map in real time
- Show tanker demand jump from 50 → 180
- "This is the climate simulation that no other team has"

**5. Tanker Allocation** → Auto-allocate with one click

**6. Route Optimizer** → Show polyline connecting depot → villages → depot

**7. Switch to Sarpanch role** → Show village-level WSI gauge, tanker request

---

## 📊 Data Flow

```
Open-Meteo API (Rainfall)  +  ISRO/CGWB (Groundwater)
                 ↓
        WSI Engine (Python / JS)
                 ↓
    Collector Dashboard (Approve Allocation)
                 ↓
    Field Officer Dashboard (Assign & Route Tankers)
                 ↓
    Driver Mobile App (Navigate & Deliver)
                 ↓
    Sarpanch Dashboard (Confirm Receipt via OTP)
```

---

## 🗺️ Roadmap

- [x] Phase 1 — Core dashboards (Collector, Sarpanch, Officer)
- [x] Phase 2 — WSI Engine + Digital Twin Simulator
- [x] Phase 3 — Route Optimizer + Fleet Tracker
- [x] Phase 4 — Multi-language support (11 languages)
- [ ] Phase 5 — ML prediction engine (Prophet/ARIMA)
- [ ] Phase 6 — Driver Mobile App (React Native)
- [ ] Phase 7 — Real sensor integration (IMD, CGWB APIs)
- [ ] Phase 8 — State-level scaling

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'feat: add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

> **Mission:** Every village gets water **before** the crisis, not after.  
> **"Water Today. Tomorrow Lives."** 💧
