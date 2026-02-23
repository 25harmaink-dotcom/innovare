# JalRakshak — Feature Documentation

## Feature Matrix

| # | Feature | Status | Demo Impact | Tab/Location |
|---|---------|--------|-------------|--------------|
| 1 | Village WSI Engine | ✅ Built | Core | All dashboards |
| 2 | Drought Heatmap (Leaflet) | ✅ Built | High | Collector → Risk Map |
| 3 | Smart Tanker Allocation | ✅ Built | High | Collector → Tanker Allocation |
| 4 | Digital Twin Slider | ✅ Built | ⭐ EXTREME | Collector → Digital Twin |
| 5 | Route Optimizer + Map | ✅ Built | High | Officer → Route Optimizer |
| 6 | Predictive Demand Forecast | ✅ Built | High | Collector → Demand Forecast |
| 7 | Farmer Drought Advisory | ✅ Built | Medium | Sarpanch → Village Status |
| 8 | OTP Delivery Verification | ✅ Built | Medium | Officer → Delivery OTP |
| 9 | Multi-language (11 langs) | ✅ Built | Medium | Header dropdown |
| 10 | SOS Emergency Alert | ✅ Built | High | Sarpanch → Community Board |
| 11 | Escalation Management | ✅ Built | Medium | Officer → Escalation |
| 12 | Budget & Fleet Overview | ✅ Built | Low | Collector → Budget |
| 13 | Groundwater Trend Chart | ✅ Built | Medium | Collector → Policy Alerts |
| 14 | Ground Truth Entry | ✅ Built | Low | Officer → Ground Truth |
| 15 | Tanker Arrival Tracker | ✅ Built | Medium | Sarpanch → Arrival Tracker |

## Feature Details

### Feature 4: Digital Twin Simulator

**What it does:**
Allows district planners to simulate future drought scenarios by adjusting four parameters in real time. The Leaflet map updates immediately, showing how red zones expand as stress increases.

**Parameters:**
- Rainfall Reduction (0–80%): Simulates monsoon failure
- Days Ahead (7–30): Time horizon for planning
- Temperature Anomaly (+0–5°C): Heat wave simulation
- Litres/Person/Day (30–70L): Demand sensitivity

**WSI Simulation Formula:**
```
simulated_wsi = min(100, base_wsi + rain_mod + temp_mod + days_mod)
rain_mod = rainfall_reduction × 0.30 × 0.5
temp_mod = temperature_anomaly × 4 × 0.3
days_mod = (days_ahead / 30) × 10 × 0.2
```

**Tanker Demand Calculation:**
Uses the feature sheet's exact formula:
```
demand_L = population × lpd × days × wsi_multiplier × seasonal_factor
```

### Feature 5: Route Optimizer

**Algorithm:** Greedy Nearest Neighbor (TSP Approximation)
**Distance:** Haversine formula (great-circle, no API needed)
**Visualization:** Leaflet polylines connecting depot → village 1 → village 2 → depot

**Output:**
- Ordered stop sequence with cumulative distances
- Estimated arrival times (assuming 40 km/h avg speed)
- "Dispatch" button to send route to driver

**Upgrade path:** OR-Tools or Google Distance Matrix API for production

### Feature 9: Multi-Language Support

Languages supported:
- English (en)
- Hindi - हिंदी (hi)
- Marathi - मराठी (mr)
- Telugu - తెలుగు (te)
- Tamil - தமிழ் (ta)
- Kannada - ಕನ್ನಡ (kn)
- Gujarati - ગુજરાતી (gu)
- Bengali - বাংলা (bn)
- Malayalam - മലയാളം (ml)
- Odia - ଓଡ଼ିଆ (or)
- Punjabi - ਪੰਜਾਬੀ (pa)

### Feature 8: OTP Delivery Verification

**Purpose:** Prevents fake delivery reporting.

**Flow:**
1. Field Officer generates 6-digit OTP before delivery
2. Reads it verbally to Sarpanch on arrival
3. Officer enters OTP confirmed by Sarpanch
4. System logs delivery only if OTP matches
5. Anti-fraud measure for government tanker programs

## Skipped Features (as per feature sheet)

| Feature | Reason Skipped |
|---------|----------------|
| LSTM/Prophet ML Forecasting | 2+ day build, high failure risk for hackathon |
| Live SMS via Twilio | Low ROI, easy to mock |
| Google Maps Distance Matrix | Paid API, greedy is sufficient |
| Real IMD API Integration | API key needed, mock data works for demo |
