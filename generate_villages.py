#!/usr/bin/env python3
"""
JalRakshak — Demo Village Data Generator
Generates realistic village data for any district.

Usage:
    python3 generate_villages.py --district gadchiroli --state MH --count 20 --output villages.csv
    python3 generate_villages.py --district jaipur --state RJ --lat 26.9124 --lng 75.7873
"""

import csv
import random
import argparse
import math

# District centers (lat, lng)
DISTRICT_CENTERS = {
    "gadchiroli": (20.1809, 80.0016),
    "nagpur": (21.1458, 79.0882),
    "pune": (18.5204, 73.8567),
    "nashik": (19.9975, 73.7898),
    "jaipur": (26.9124, 75.7873),
    "jodhpur": (26.2389, 73.0243),
    "lucknow": (26.8467, 80.9462),
    "ranchi": (23.3441, 85.3096),
}

# Village name components by region
PREFIXES = {
    "MH": ["Kurkheda", "Chamorshi", "Mul", "Bhamragad", "Sironcha", "Etapalli", "Aheri", "Dhanora",
           "Wadsa", "Nagbhid", "Bramhapuri", "Sindewahi", "Gondpipri", "Rajura", "Chimur", "Warora"],
    "RJ": ["Sawai", "Churu", "Sikar", "Jhunjhunu", "Nagaur", "Barmer", "Bikaner", "Jaisalmer",
           "Pali", "Sirohi", "Ajmer", "Tonk", "Bundi", "Kota", "Baran", "Jhalawar"],
    "UP": ["Varanasi", "Ballia", "Ghazipur", "Jaunpur", "Azamgarh", "Mau", "Deoria", "Gorakhpur",
           "Kushinagar", "Maharajganj", "Siddharth", "Basti", "Sant", "Ambedkar"],
    "DEFAULT": ["Nandura", "Shegaon", "Khamgaon", "Buldana", "Akola", "Washim", "Hingoli", "Nanded",
                "Latur", "Osmanabad", "Solapur", "Sangli", "Kolhapur", "Ratnagiri", "Sindhudurg"],
}

SUFFIXES = ["pur", "wadi", "gaon", "khurd", "budruk", "nagar", "peth", "tanda", "pada", "vasti"]


def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def calculate_wsi(rain_deficit, gw_drop, hist_freq, pop_density, days_no_rain):
    # Normalize gw_drop (0–4m → 0–100)
    gw_norm = min(100, gw_drop * 25)
    # Normalize days_no_rain (0–38 days → 0–100)
    days_norm = min(100, (days_no_rain / 38) * 100)

    score = (
        rain_deficit * 0.30 +
        gw_norm * 0.25 +
        hist_freq * 0.20 +
        pop_density * 0.15 +
        days_norm * 0.10
    )
    return round(min(100, score), 1)


def generate_village(name, lat, lng, district_lat, district_lng):
    pop = random.randint(600, 8000)
    rain_deficit = random.randint(10, 85)
    gw_drop = round(random.uniform(0.2, 3.8), 1)
    hist_freq = random.randint(10, 80)
    pop_density = random.randint(10, 80)
    days_no_rain = random.randint(0, 35)
    wsi = calculate_wsi(rain_deficit, gw_drop, hist_freq, pop_density, days_no_rain)
    dist_km = round(haversine(lat, lng, district_lat, district_lng), 1)

    return {
        "name": name,
        "lat": round(lat, 5),
        "lon": round(lng, 5),
        "pop": pop,
        "rain_deficit": rain_deficit,
        "gw_drop": gw_drop,
        "hist_freq": hist_freq / 100,  # Normalize to 0-1 for compatibility
        "pop_density": pop_density,
        "days_no_rain": days_no_rain,
        "wsi": wsi,
        "borewells_ok": random.randint(1, 4),
        "borewells_total": random.randint(3, 6),
        "dist_from_depot_km": dist_km,
    }


def generate_villages(district, state, lat, lng, count):
    prefixes = PREFIXES.get(state, PREFIXES["DEFAULT"])
    random.shuffle(prefixes)

    villages = []
    used_names = set()

    for i in range(count):
        # Generate unique name
        for _ in range(100):
            prefix = random.choice(prefixes)
            suffix = random.choice(SUFFIXES)
            name = f"{prefix}{suffix}" if random.random() > 0.5 else prefix
            if name not in used_names:
                used_names.add(name)
                break

        # Random offset from district center (±0.7 degrees)
        v_lat = lat + random.uniform(-0.7, 0.7)
        v_lng = lng + random.uniform(-0.7, 0.7)

        village = generate_village(name, v_lat, v_lng, lat, lng)
        villages.append(village)

    # Sort by WSI descending
    villages.sort(key=lambda v: v["wsi"], reverse=True)
    return villages


def main():
    parser = argparse.ArgumentParser(description="JalRakshak Demo Village Data Generator")
    parser.add_argument("--district", default="gadchiroli", help="District name (lowercase)")
    parser.add_argument("--state", default="MH", help="State code (MH, RJ, UP, JH, KA)")
    parser.add_argument("--lat", type=float, default=None, help="District center latitude")
    parser.add_argument("--lng", type=float, default=None, help="District center longitude")
    parser.add_argument("--count", type=int, default=16, help="Number of villages")
    parser.add_argument("--output", default="villages.csv", help="Output CSV filename")
    args = parser.parse_args()

    # Get center coordinates
    if args.lat and args.lng:
        lat, lng = args.lat, args.lng
    elif args.district.lower() in DISTRICT_CENTERS:
        lat, lng = DISTRICT_CENTERS[args.district.lower()]
    else:
        print(f"Unknown district '{args.district}'. Please provide --lat and --lng.")
        return

    print(f"Generating {args.count} villages for {args.district.title()} district...")
    villages = generate_villages(args.district, args.state, lat, lng, args.count)

    # Write CSV
    fieldnames = ["name", "lat", "lon", "pop", "rain_deficit", "gw_drop", "hist_freq",
                  "pop_density", "days_no_rain", "wsi", "borewells_ok", "borewells_total", "dist_from_depot_km"]

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(villages)

    print(f"✅ Generated {len(villages)} villages → {args.output}")
    print(f"\nWSI Distribution:")
    critical = sum(1 for v in villages if v["wsi"] >= 80)
    warning = sum(1 for v in villages if 60 <= v["wsi"] < 80)
    watch = sum(1 for v in villages if 30 <= v["wsi"] < 60)
    normal = sum(1 for v in villages if v["wsi"] < 30)
    print(f"  🔴 Critical (80–100): {critical}")
    print(f"  🟠 Warning  (60–79):  {warning}")
    print(f"  🟡 Watch    (30–59):  {watch}")
    print(f"  🟢 Normal   (0–29):   {normal}")


if __name__ == "__main__":
    main()
