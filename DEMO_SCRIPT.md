# 🎤 JalRakshak — Hackathon Demo Script

> **Time: 5 minutes | Impact: Maximum**

---

## Opening Line (15 seconds)
> "In India, 100 million people face water scarcity every summer. Districts send tankers **after** villages run dry. JalRakshak predicts the crisis **before** it happens — and allocates tankers to the right place at the right time."

---

## Demo Sequence

### Step 1 — Login (30 seconds)
1. Open `jalrakshak_portal.html`
2. Select language → Hindi or English
3. Click **"District Collector"**
4. Select State: Maharashtra → District: Gadchiroli
5. Enter mobile: `9876543210` → Send OTP → Copy OTP → Verify
6. **Say:** "This is a role-based OTP login — same system used by real government portals."

---

### Step 2 — Command Overview (45 seconds)
1. You're in the **Command Center**
2. Point to the 4 metric cards: Critical villages, Tankers deployed, Avg WSI, Max risk village
3. Show the WSI bar chart — color-coded red/orange/yellow/green
4. Show rainfall trend vs normal
5. **Say:** "The Water Stress Index is a composite score — 5 parameters, scientifically weighted. One number tells the Collector exactly where to act."

---

### Step 3 — Risk Map (45 seconds)
1. Click **"District Risk Map"** in sidebar
2. Zoom into the map
3. Click a red circle marker
4. **Say:** "Every circle is a village. Red means critical. Click any marker to see the full breakdown — population, groundwater drop, days without rain, tanker assignment."

---

### Step 4 — 🎛️ Digital Twin (90 seconds — THE WOW MOMENT)
1. Click **"Digital Twin Simulator"**
2. **Pause for effect** — "This is the feature that no other team has."
3. Slowly drag **"Rainfall Reduction"** from 0% to 60%
4. Watch: red zones expand on the map, tanker demand jumps, cost estimate rises
5. Drag **"Days Ahead"** to 21
6. Drag **"Temperature Anomaly"** to +3°C
7. **Say:** "Judges, you're looking at 21-day climate simulation. If rainfall drops 60% and temperature rises 3°C, this district needs 180 more tankers. The system tells the Collector **today** — not in 3 weeks when it's too late."

---

### Step 5 — Route Optimizer (45 seconds)
1. Switch role to **Field Officer** (logout → login as officer)
2. Click **"Route Optimizer"**
3. Select tanker TK-01, filter "Critical Only"
4. **Say:** "Nearest-neighbor algorithm. Zero API cost. Depot → Village 1 → Village 2 → back to Depot. Total 127 km, 3.2 hours. One click dispatches the route to the driver's phone."

---

### Step 6 — Sarpanch View (30 seconds)
1. Switch to Sarpanch role, select a village
2. Show the WSI gauge
3. Show the tanker request form
4. Show the SOS alert
5. **Say:** "The Sarpanch doesn't need to understand data. They see a gauge — green, yellow, or red. They press one button to request water. If it's an emergency, they press SOS."

---

## Closing Line (15 seconds)
> "JalRakshak is built on top of Smart-Kisan — 60% code reuse, 6 new files. We didn't start from scratch — we extended proven technology for a bigger impact. **Water today. Tomorrow lives.**"

---

## Judge Questions — Prepared Answers

**Q: Is this using real data?**
> "The WSI formula is calibrated on IMD historical data. For this demo we use seeded village data that mirrors Gadchiroli district patterns. Real integration uses Open-Meteo API (free) and IMD feeds."

**Q: What's the scalability plan?**
> "The same WSI engine scales from village to block to district to state. We've designed it with a state-level tab already in the roadmap. Same database, same algorithm — just wider geographic scope."

**Q: Why Leaflet and not Google Maps?**
> "Zero API cost. OpenStreetMap is used by government systems globally. For production, we can upgrade to Google Distance Matrix API for real routing — but greedy nearest-neighbor is 95% as good at 0% of the cost."

**Q: How is this different from existing government drought portals?**
> "Existing portals show historical data. JalRakshak predicts. The Digital Twin slider is the difference — planners simulate future scenarios before committing resources."
