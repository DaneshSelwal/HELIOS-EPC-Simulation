#!/usr/bin/env python3
"""
Deterministic Site Reality Engine for HELIOS EPC Simulation.
Implements physical constraints, seeded RNG, weather calendar,
and productivity rates from project research baselines.
Python Standard Library only (no LLM, no external libraries).
"""

import math
import random
from datetime import datetime, timedelta

DEFAULT_SEED = 20261006
PROJECT_START_DATE = datetime(2026, 10, 6)

MATERIAL_MAPPING = {
    "WP-CON-CIV-PIL": "WP-PROC-PIL",
    "WP-CON-MEC-TRK": "WP-PROC-TRK",
    "WP-CON-MEC-MOD": "WP-PROC-MOD",
    "WP-CON-ELE-DC": "WP-PROC-CAB-DC",
    "WP-CON-ELE-MV": "WP-PROC-CAB-MV",
    "WP-CON-SUB-ERE": "WP-PROC-TRA"
}

class SiteRealityEngine:
    def __init__(self, seed=DEFAULT_SEED):
        self.base_seed = seed

    def get_weather(self, sim_day):
        """
        Deterministic weather calendar based on Bukhara, Uzbekistan climate.
        - Winter: Dec (Day 57) to Feb (Day 145) -> 0.7x productivity, sub-zero days
        - Spring/Autumn: Oct-Nov, Mar-May -> optimal conditions
        - Summer: Jun-Aug -> extreme heat protocols
        - Dust storms: Kyzylkum desert winds
        - High wind: >12 m/s halts module lifting
        """
        rng = random.Random(self.base_seed + sim_day * 101)
        sim_date = PROJECT_START_DATE + timedelta(days=sim_day - 1)
        cal_month = sim_date.month

        # Base temperature curves for Bukhara
        # Month: [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]
        monthly_avg_temp = {
            1: 0.5, 2: 3.8, 3: 10.2, 4: 17.5, 5: 23.8, 6: 28.7,
            7: 30.5, 8: 28.1, 9: 21.6, 10: 14.2, 11: 7.5, 12: 2.1
        }
        base_t = monthly_avg_temp.get(cal_month, 15.0)
        temp_c = round(base_t + rng.uniform(-6.0, 6.0), 1)

        # Wind speed (m/s)
        # Average 4-7 m/s, occasional gusty days
        wind_speed_ms = round(rng.weibullvariate(5.5, 2.0), 1)

        # Precipitation (Uzbekistan arid region: rare rain/snow)
        has_precip = rng.random() < 0.08
        precip_mm = round(rng.uniform(1.0, 12.0), 1) if has_precip else 0.0

        # Dust storm check (more common in spring/summer dry winds, or triggered events)
        dust_storm = (rng.random() < 0.02) and (wind_speed_ms > 10.0)

        # Winter factor
        is_winter = cal_month in [12, 1, 2]
        is_frozen_ground = temp_c < -5.0

        # Productivity multipliers
        productivity_factor = 1.0
        weather_notes = []

        if dust_storm:
            productivity_factor = 0.0
            weather_notes.append("Dust storm active: outdoor operations halted")
        elif is_winter:
            if is_frozen_ground:
                productivity_factor = 0.2
                weather_notes.append("Severe freeze (temp < -5°C): concrete & earthworks restricted")
            else:
                productivity_factor = 0.70
                weather_notes.append("Winter season: 0.70x productivity factor applied")

        # Wind threshold for module lifting
        module_lifting_allowed = (wind_speed_ms <= 12.0) and (not dust_storm)
        if not module_lifting_allowed and not dust_storm:
            weather_notes.append(f"Wind speed {wind_speed_ms} m/s > 12.0 m/s: module crane lifting suspended")

        return {
            "sim_day": sim_day,
            "sim_date": sim_date.strftime("%Y-%m-%d"),
            "cal_month": cal_month,
            "temp_c": temp_c,
            "wind_speed_ms": wind_speed_ms,
            "precip_mm": precip_mm,
            "dust_storm": dust_storm,
            "is_winter": is_winter,
            "is_frozen_ground": is_frozen_ground,
            "module_lifting_allowed": module_lifting_allowed,
            "productivity_factor": round(productivity_factor, 2),
            "summary": f"{temp_c}°C, Wind {wind_speed_ms} m/s" + (f", {', '.join(weather_notes)}" if weather_notes else ", Clear")
        }

    def evaluate_installation_rules(self, wp_id, project_state):
        """
        Hard rules:
        Nothing is installed unless:
        1. IFC is released (ifc_released == True)
        2. Material is delivered (material delivered >= installed + production)
        3. Predecessor is accepted (predecessors qc_accepted meets constraint)
        4. Crews are mobilised (crews_mobilised > 0)
        """
        wp = project_state["work_packages"].get(wp_id)
        if not wp:
            return False, f"Unknown work package {wp_id}", 0.0

        # Rule 1: IFC Released
        if not wp.get("ifc_released", False):
            return False, f"Rule 1 Violated: IFC drawing not released for {wp_id}", 0.0

        # Rule 4: Crews Mobilised
        crews = wp.get("crews_mobilised", 0)
        if crews <= 0:
            return False, f"Rule 4 Violated: Zero crews mobilised for {wp_id}", 0.0

        # Rule 2: Material Delivered
        mat_wp_id = MATERIAL_MAPPING.get(wp_id)
        max_material_avail = float("inf")
        if mat_wp_id:
            mat_wp = project_state["work_packages"].get(mat_wp_id)
            if mat_wp:
                delivered = mat_wp.get("delivered", 0.0)
                installed = wp.get("installed", 0.0)
                max_material_avail = max(0.0, delivered - installed)
                if max_material_avail <= 0.0:
                    return False, f"Rule 2 Violated: No delivered material available ({mat_wp_id} delivered={delivered}, installed={installed})", 0.0

        # Rule 3: Predecessor Accepted
        predecessors = wp.get("predecessors", [])
        for pred_id in predecessors:
            pred_wp = project_state["work_packages"].get(pred_id)
            if not pred_wp:
                continue

            # Engineering predecessors
            if pred_wp["discipline"] == "engineering":
                if pred_wp.get("qc_accepted", 0.0) < 100.0 and not pred_wp.get("ifc_released", False):
                    return False, f"Rule 3 Violated: Engineering predecessor {pred_id} incomplete ({pred_wp.get('qc_accepted')}%)", 0.0

            # Construction predecessor dependencies
            if wp_id == "WP-CON-CIV-PIL":
                # Piling requires grading ready
                grd = project_state["work_packages"].get("WP-CON-CIV-GRD", {})
                if grd.get("qc_accepted", 0.0) < 15.0:
                    return False, f"Rule 3 Violated: Site grading {grd.get('qc_accepted', 0.0)}% < 15.0% threshold for piling start", 0.0

            elif wp_id == "WP-CON-MEC-TRK":
                # Tracker assembly requires accepted piles (~3 piles per table)
                pil = project_state["work_packages"].get("WP-CON-CIV-PIL", {})
                piles_accepted = pil.get("qc_accepted", 0.0)
                tables_installed = wp.get("installed", 0.0)
                if piles_accepted < (tables_installed + 1) * 3:
                    return False, f"Rule 3 Violated: Insufficient accepted piles ({piles_accepted} piles < {(tables_installed+1)*3} required)", 0.0

            elif wp_id == "WP-CON-MEC-MOD":
                # Module mounting requires accepted tracker tables (~34 modules per table)
                trk = project_state["work_packages"].get("WP-CON-MEC-TRK", {})
                trackers_accepted = trk.get("qc_accepted", 0.0)
                modules_installed = wp.get("installed", 0.0)
                if trackers_accepted < (modules_installed + 1) / 33.88:
                    return False, f"Rule 3 Violated: Insufficient accepted tracker tables ({trackers_accepted} tables < {(modules_installed+1)/33.88:.1f} required)", 0.0

        return True, "All physical preconditions satisfied", max_material_avail

    def compute_daily_production(self, wp_id, project_state, weather, active_events=None):
        """
        Computes physical production for one day using research baseline rates:
        - Piles: 80-120/rig/day (20-30 in rock / EVT-001)
        - Modules: 1,000-1,500/day per 60-person crew (0 if wind > 12m/s)
        - DC Cable: 2,000-3,000 m/day
        - MV Cable: 800-1,200 m/day
        - Concrete: 40-60 m3/day (0 if frozen)
        """
        can_run, reason, max_mat = self.evaluate_installation_rules(wp_id, project_state)
        if not can_run:
            return 0.0, reason

        sim_day = weather["sim_day"]
        rng = random.Random(self.base_seed + sim_day * 997 + hash(wp_id) % 10000)
        wp = project_state["work_packages"][wp_id]
        crews = wp.get("crews_mobilised", 0)
        w_factor = weather["productivity_factor"]

        # Check for event modifiers
        is_rock_condition = False
        if active_events:
            for ev in active_events:
                if ev.get("event_id") == "EVT-001" and wp_id == "WP-CON-CIV-PIL":
                    is_rock_condition = True

        daily_qty = 0.0

        if wp_id == "WP-CON-CIV-PIL":
            # Piles: 80-120 / rig / day (20-30 in rock)
            base_rate = rng.uniform(20.0, 30.0) if is_rock_condition else rng.uniform(80.0, 120.0)
            daily_qty = crews * base_rate * w_factor

        elif wp_id == "WP-CON-MEC-MOD":
            # Modules: 1,000-1,500 / day per crew
            if not weather["module_lifting_allowed"]:
                return 0.0, f"Module lifting halted: wind {weather['wind_speed_ms']} m/s > 12 m/s"
            base_rate = rng.uniform(1000.0, 1500.0)
            daily_qty = crews * base_rate * w_factor

        elif wp_id == "WP-CON-ELE-DC":
            # DC cable: 2,000-3,000 m / day
            base_rate = rng.uniform(2000.0, 3000.0)
            daily_qty = crews * base_rate * w_factor

        elif wp_id == "WP-CON-ELE-MV":
            # MV cable: 800-1,200 m / day
            base_rate = rng.uniform(800.0, 1200.0)
            daily_qty = crews * base_rate * w_factor

        elif wp_id == "WP-CON-CIV-FND":
            # Concrete: 40-60 m3 / day
            if weather["is_frozen_ground"]:
                return 0.0, "Concrete batching suspended: ground frozen"
            base_rate = rng.uniform(40.0, 60.0)
            daily_qty = crews * base_rate * w_factor

        elif wp_id == "WP-CON-MEC-TRK":
            # Tracker assembly: 30-50 tables / day per crew
            base_rate = rng.uniform(30.0, 50.0)
            daily_qty = crews * base_rate * w_factor

        elif wp_id == "WP-CON-CIV-GRD":
            # Site grading: 1.0% - 2.5% per day
            base_rate = rng.uniform(1.0, 2.5)
            daily_qty = crews * base_rate * w_factor

        elif wp_id == "WP-CON-MOB":
            # Mobilization: 0.6% - 0.9% per crew per day (1.2% - 1.8% total with 2 crews)
            base_rate = rng.uniform(0.6, 0.9)
            daily_qty = crews * base_rate * w_factor

        else:
            daily_qty = crews * 1.0 * w_factor

        # Bound by material available and remaining scope
        remaining_scope = max(0.0, wp["total_qty"] - wp["installed"])
        actual_qty = min(daily_qty, max_mat, remaining_scope)
        return round(actual_qty, 2), "Success"
