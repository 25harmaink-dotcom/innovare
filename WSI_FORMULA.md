# 💧 Water Stress Index (WSI) — Technical Documentation

## Formula

```
WSI = (rain_deficit × 0.30) +
      (gw_drop_normalized × 0.25) +
      (hist_freq_normalized × 0.20) +
      (pop_density_normalized × 0.15) +
      (days_no_rain_normalized × 0.10)
```

## Parameters

| Parameter | Weight | Source | Description |
|-----------|--------|--------|-------------|
| `rain_deficit` | 30% | Open-Meteo API / IMD | % deviation of actual rainfall from long-period average (LPA). 0–100 scale. |
| `gw_drop` | 25% | CGWB / ISRO sensors | Groundwater level drop in meters per month. Normalized to 0–100 scale. |
| `hist_freq` | 20% | District drought records | Historical drought frequency score for the village's block (0–100). |
| `pop_density` | 15% | Census data | Population density × water access vulnerability score (0–100). |
| `days_no_rain` | 10% | Calculated from API | Days since last measurable rainfall, capped at 38 days → normalized to 100. |

## Risk Bands

| WSI Score | Status | Color | Action |
|-----------|--------|-------|--------|
| 0–30 | 🟢 Normal | Green `#2E7D32` | Continue monitoring |
| 31–60 | 🟡 Watch | Yellow `#F9A825` | Prepare tankers, alert officers |
| 61–80 | 🟠 Warning | Orange `#E65100` | Mobilize fleet, contact Sarpanch |
| 81–100 | 🔴 Critical | Red `#C62828` | Emergency allocation, SOS protocol |

## Tanker Allocation Priority Score

Used for sorting villages when allocating limited tankers:

```
priority = (wsi × 0.50) +
           (vulnerable_pop_pct × 0.20) +
           (days_without_supply × 0.20) +
           (distance_from_depot_score × 0.10)
```

Where:
- `vulnerable_pop_pct` = (children < 12 + elderly > 60) / total population × 100
- `days_without_supply` = days since last tanker delivery (0–20 scale)
- `distance_from_depot_score` = inverse of Haversine distance (closer = higher priority)

## Tanker Demand Formula

```
demand_liters = population × lpd × days_ahead × wsi_multiplier × seasonal_factor
```

| Factor | Value |
|--------|-------|
| `lpd` | Litres per person per day (default: 50L; minimum standard: 30L) |
| WSI Normal (0–30) | multiplier = 0.0 |
| WSI Watch (31–60) | multiplier = 0.5 |
| WSI Warning (61–80) | multiplier = 1.0 |
| WSI Critical (81–100) | multiplier = 2.0 |
| Summer (Apr–Jun) | seasonal = 1.5× |
| Monsoon (Jul–Sep) | seasonal = 0.3× |
| Winter / Other | seasonal = 1.0× |

## Digital Twin Simulation

The Digital Twin modifies the WSI in real time using user-controlled parameters:

```python
def simulate_wsi(base_wsi, rainfall_reduction_pct, days_ahead, temp_anomaly_c):
    rain_mod = rainfall_reduction_pct * 0.30 * 0.5
    temp_mod = temp_anomaly_c * 4 * 0.3
    days_mod = (days_ahead / 30) * 10 * 0.2
    return min(100, round(base_wsi + rain_mod + temp_mod + days_mod))
```

## Route Optimization Algorithm

JalRakshak uses the **Greedy Nearest Neighbor** algorithm (TSP approximation):

```
1. Start at depot
2. Find the unvisited village closest to current location
3. Visit it, mark as visited
4. Repeat from step 2 until all villages visited
5. Return to depot
```

Distance is calculated using the **Haversine formula** (great-circle distance):

```javascript
function haversine(lat1, lng1, lat2, lng2) {
    const R = 6371; // Earth radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = Math.sin(dLat/2)**2 +
              Math.cos(lat1 * Math.PI/180) * Math.cos(lat2 * Math.PI/180) *
              Math.sin(dLng/2)**2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}
```

**Accuracy note:** Greedy nearest-neighbor produces routes ~20–25% longer than optimal (Christofides bound). For production, upgrade to Google Distance Matrix API or OR-Tools for exact routing.

## Data Sources

| Data | Source | Frequency |
|------|--------|-----------|
| Rainfall (actual) | [Open-Meteo API](https://open-meteo.com/) | Hourly |
| Rainfall (LPA) | [IMD](https://mausam.imd.gov.in/) | Annual baseline |
| Groundwater levels | CGWB borewell sensors / ISRO trend data | Monthly |
| Population | Census 2011 / 2021 projected | Annual update |
| Historical drought | District collectorate records | Static seeded |
