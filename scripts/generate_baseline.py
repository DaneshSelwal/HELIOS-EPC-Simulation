#!/usr/bin/env python3
"""
Generate state/baseline.json for HELIOS EPC Simulation.
Implements Rev 0 Baseline milestones using 28-day months and standard S-curve.
Includes procurement milestone weights (Rule of Credit):
PO issued: 10%, Drawings approved: 15%, FAT cleared: 25%, Shipped: 25%, Delivered: 25%.
"""

import json
import math
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(REPO_ROOT, "state", "baseline.json")

def generate_baseline():
    total_days = 504  # 18 months * 28 days
    contract_price = 85000000.0  # USD 85,000,000

    anchors = [
        (28, 1667500.0),   # Month 1 (Day 28): Design + Mob + MPT PO ($180k)
        (56, 3825000.0),   # Month 2 (Day 56): 4.5% (Mob complete, engineering ramping)
        (112, 10200000.0), # Month 4 (Day 112): 12.0% (Piling start)
        (168, 23800000.0), # Month 6 (Day 168): 28.0% (Module deliveries)
        (280, 52700000.0), # Month 10 (Day 280): 62.0% (Peak construction)
        (420, 78200000.0), # Month 15 (Day 420): 92.0% (Mechanical completion)
        (448, 82025000.0), # Month 16 (Day 448): 96.5% (Energization)
        (504, 85000000.0)  # Month 18 (Day 504): 100.0% (COD)
    ]

    daily_progress = {}
    daily_bcws = {}

    # Month 1 (Days 1 to 28)
    for d in range(1, 29):
        if d < 12:
            bcws = d * 53125.0
        else:
            bcws = d * 53125.0 + 180000.0  # MPT PO award milestone planned on Day 12
        daily_bcws[str(d)] = round(bcws, 2)
        daily_progress[str(d)] = round(bcws / contract_price, 6)

    # Subsequent months: smooth interpolation between milestone anchors
    prev_d = 28
    prev_bcws = 1667500.0

    for d_anchor, bcws_anchor in anchors[1:]:
        span = d_anchor - prev_d
        diff = bcws_anchor - prev_bcws
        for d in range(prev_d + 1, d_anchor + 1):
            t = (d - prev_d) / span
            smooth_t = (1.0 - math.cos(math.pi * t)) / 2.0
            bcws = prev_bcws + diff * smooth_t
            daily_bcws[str(d)] = round(bcws, 2)
            daily_progress[str(d)] = round(bcws / contract_price, 6)
        prev_d = d_anchor
        prev_bcws = bcws_anchor

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
        "procurement_milestone_weights": {
            "po_issued": 0.10,
            "drawings_approved": 0.15,
            "fat_cleared": 0.25,
            "shipped": 0.25,
            "delivered": 0.25
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
    print(f"Day 12 BCWS: ${daily_bcws['12']:,.2f} ({daily_progress['12']*100:.3f}%)")
    print(f"Day 14 BCWS: ${daily_bcws['14']:,.2f} ({daily_progress['14']*100:.3f}%)")

if __name__ == "__main__":
    generate_baseline()
