# 💧 Drought Stress Prediction & Water Tanker Allocation Platform

> Shifting water governance from **crisis management → preventive planning**

---

## 🎯 Problem Statement

Districts respond to drought **after** it hits. This platform predicts emerging drought stress using rainfall and groundwater trends, enabling district authorities to **proactively** plan and optimize water tanker allocation.

---

## 🏗️ Platform Architecture

```
┌─────────────────────────────────────────────────────┐
│              INTEGRATED DIGITAL PLATFORM             │
├──────────────┬──────────────┬───────────┬───────────┤
│  Collector   │   Sarpanch   │  Officer  │  Driver   │
│  Dashboard   │  Dashboard   │ Dashboard │  Mobile   │
│  (District)  │  (Village)   │  (Zone)   │   App     │
└──────────────┴──────────────┴───────────┴───────────┘
```

### 👥 User Roles

| Role | Interface | Responsibility |
|------|-----------|----------------|
| 🏛️ Collector | Web Dashboard | Predict, Plan, Approve, Govern |
| 🏘️ Sarpanch | Web Dashboard | Monitor village, Request tankers |
| 👷 Field Officer | Web Dashboard | Coordinate zone, Track delivery |
| 🚛 Driver | Mobile App | Navigate route, Confirm delivery |

---

## ✨ Core Features

### 1. 🌧️ Rainfall Deviation & Groundwater Trend Analysis
- Historical vs actual rainfall comparison
- Groundwater level monitoring (borewell sensors)
- Anomaly detection & trend forecasting

### 2. 📊 Village-Level Water Stress Index (WSI)
- Composite scoring per village
- Factors: rainfall deficit + groundwater depletion + population
- Auto-ranked priority list

### 3. 🔮 Predictive Tanker Demand Estimation
- 7 / 14 / 30 day demand forecasting
- ML-based prediction using historical patterns
- Zone-wise demand aggregation

### 4. 🎯 Priority-Based Allocation
- Population × Severity scoring matrix
- Auto-allocation engine
- Collector approval workflow

### 5. 🗺️ Route Optimization for Tanker Dispatch
- Shortest path with priority weighting
- Multi-tanker fleet optimization
- Real-time rerouting

### 6. 📡 Real-Time Monitoring
- Live tanker GPS tracking
- Delivery confirmation
- Alert escalation system

---

## 🛠️ Tech Stack

### Frontend
- **React.js** — Dashboards (Collector, Sarpanch, Officer)
- **React Native** — Driver Mobile App
- **Tailwind CSS** — Styling
- **Recharts / Leaflet.js** — Charts & Maps
- **Socket.io Client** — Real-time updates

### Backend
- **Node.js + Express** — REST API
- **Python (FastAPI)** — ML prediction microservice
- **PostgreSQL** — Primary database
- **Redis** — Caching & real-time pub/sub
- **Socket.io** — WebSocket server

### ML / Analytics
- **Prophet / ARIMA** — Time series rainfall forecasting
- **Scikit-learn** — Water Stress Index model
- **Pandas / NumPy** — Data processing

### Infrastructure
- **Docker + Docker Compose** — Containerization
- **GitHub Actions** — CI/CD pipeline

---

## 📁 Project Structure

```
drought-platform/
├── frontend/                  # React Web Dashboards
│   └── src/
│       ├── components/
│       │   ├── collector/     # Collector Dashboard components
│       │   ├── sarpanch/      # Sarpanch Dashboard components
│       │   ├── officer/       # Field Officer Dashboard components
│       │   └── driver/        # Driver Mobile App components
│       ├── pages/
│       ├── hooks/
│       ├── context/
│       └── utils/
├── backend/                   # Node.js API Server
│   ├── routes/
│   ├── models/
│   ├── controllers/
│   ├── middleware/
│   └── utils/
├── ml-service/                # Python ML Microservice
│   ├── models/
│   ├── data/
│   └── api/
├── docs/                      # Documentation
│   ├── architecture.md
│   ├── api-spec.md
│   └── data-dictionary.md
├── scripts/                   # Utility scripts
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js >= 18
- Python >= 3.10
- PostgreSQL >= 14
- Docker & Docker Compose

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/drought-platform.git
cd drought-platform

# Install frontend dependencies
cd frontend && npm install

# Install backend dependencies
cd ../backend && npm install

# Install ML service dependencies
cd ../ml-service && pip install -r requirements.txt

# Start all services
cd .. && docker-compose up
```

---

## 🗺️ Data Flow

```
Sensor Data (Rainfall + Groundwater)
        ↓
ML Service (Predict Stress Index)
        ↓
Collector Dashboard (Approve Allocation)
        ↓
Field Officer Dashboard (Assign Tankers)
        ↓
Driver Mobile App (Execute Delivery)
        ↓
Sarpanch Dashboard (Confirm Receipt)
```

---

## 📌 Roadmap

- [ ] Phase 1 — Core dashboards (Collector + Sarpanch)
- [ ] Phase 2 — ML prediction engine
- [ ] Phase 3 — Field Officer + Driver app
- [ ] Phase 4 — Route optimization
- [ ] Phase 5 — State-level scaling

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/collector-dashboard`)
3. Commit changes (`git commit -m 'feat: add collector dashboard'`)
4. Push to branch (`git push origin feature/collector-dashboard`)
5. Open Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details

---

> **Mission:** Every village gets water **before** the crisis, not after.
