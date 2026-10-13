#!/usr/bin/env python3
"""
Generate state/baseline.json for HELIOS EPC Simulation.
Implements Rev 0 Baseline milestones using 28-day months and standard S-curve.
"""

import json
import math
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(REPO_ROOT, "state", "baseline.json")

def generate_baseline():
    total_days = 504  # 18 months * 28 days
    contract_price = 85000000.0  # USD 85,000,000

    # Key milestone anchors (day -> planned progress %)
    # Day 0: 0.0%
    # M2 (Day 56): 4.5% (mobilization complete, engineering ramping)
    # M4 (Day 112): 12.0% (first pile start, engineering nearing completion, initial procurement)
    # M6 (Day 168): 28.0% (first module delivery, peak civil piling)
    # M10 (Day 280): 62.0% (peak construction and deliveries)
    # M15 (Day 420): 92.0% (mechanical completion)
    # M16 (Day 448): 96.5% (first energization, cold commissioning)
    # M18 (Day 504): 100.0% (COD, performance tests completed)
    anchors = [
        (0, 0.0),
        (56, 0.045),
        (112, 0.120),
        (168, 0.280),
        (280, 0.620),
        (420, 0.920),
        (448, 0.965),
        (504, 1.000)
    ]

    # Monotonic cubic hermite / smooth interpolation between anchors
    daily_progress = {}
    daily_bcws = {}

    for i in range(len(anchors) - 1):
        d0, p0 = anchors[i]
        d1, p1 = anchors[i+1]
        span = d1 - d0
        for d in range(d0 + 1, d1 + 1):
            t = (d - d0) / span
            # Smoothstep interpolation s(t) = 3t^2 - 2t^3
            # or cosine interpolation (1 - cos(pi*t))/2
            smooth_t = (1.0 - math.cos(math.pi * t)) / 2.0
            p = p0 + (p1 - p0) * smooth_t
            daily_progress[str(d)] = round(p, 6)
            daily_bcws[str(d)] = round(p * contract_price, 2)

    baseline_data = {
        "project": {
            "name": "HELIOS 100MW Solar PV + 33/220kV GSS",
            "location": "Bukhara Region, Uzbekistan",
            "contract_form": "FIDIC Yellow Book 1999 (Plant and Design-Build)",
            "contract_price_usd": contract_price,
            "bac_usd": contract_price,
            "month_convention_days": 28,
            "total_duration_months": 18,
            "total_duration_days": total_days
        },
        "progress_weights": {
            "engineering": 0.05,
            "procurement": 0.60,
            "construction": 0.30,
            "tnc": 0.05
        },
        "discipline_budgets_usd": {
            "engineering": 4250000.0,
            "procurement": 51000000.0,
            "construction": 25500000.0,
            "tnc": 4250000.0
        },
        "milestones_rev0": [
            {
                "code": "HEL.00",
                "month": 0,
                "day": 1,
                "name": "Project Commencement / LNTP",
                "critical_path": True,
                "planned_date": "2026-10-06"
            },
            {
                "code": "HEL.20",
                "month": 2,
                "day": 56,
                "name": "Site Mobilization Complete",
                "critical_path": False,
                "planned_date": "2026-11-30"
            },
            {
                "code": "HEL.20.CIV",
                "month": 4,
                "day": 112,
                "name": "First Piling Start",
                "critical_path": True,
                "planned_date": "2027-01-25"
            },
            {
                "code": "HEL.SCM.MOD",
                "month": 6,
                "day": 168,
                "name": "First PV Module Delivery",
                "critical_path": False,
                "planned_date": "2027-03-22"
            },
            {
                "code": "HEL.15",
                "month": 15,
                "day": 420,
                "name": "Mechanical Completion",
                "critical_path": True,
                "planned_date": "2027-11-29"
            },
            {
                "code": "HEL.TNC.ENG",
                "month": 16,
                "day": 448,
                "name": "First Energization",
                "critical_path": True,
                "planned_date": "2027-12-27"
            },
            {
                "code": "HEL.10",
                "month": 18,
                "day": 504,
                "name": "Commercial Operation Date (COD)",
                "critical_path": True,
                "planned_date": "2028-02-21"
            }
        ],
        "daily_planned_progress_pct": daily_progress,
        "daily_bcws": daily_bcws
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(baseline_data, f, indent=2)

    print(f"Generated baseline.json at {OUTPUT_PATH}")
    print(f"Day 4 BCWS: ${daily_bcws['4']:,.2f} ({daily_progress['4']*100:.3f}%)")
    print(f"Day 14 BCWS: ${daily_bcws['14']:,.2f} ({daily_progress['14']*100:.3f}%)")
    print(f"Day 56 BCWS: ${daily_bcws['56']:,.2f} ({daily_progress['56']*100:.3f}%)")
    print(f"Day 504 BCWS: ${daily_bcws['504']:,.2f} ({daily_progress['504']*100:.3f}%)")

if __name__ == "__main__":
    generate_baseline()
