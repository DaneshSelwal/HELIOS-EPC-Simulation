#!/usr/bin/env python3
"""
Deterministic Earned Value Management (EVM) Calculation Engine.
Calculates BCWS, BCWP, ACWP, SPI, CPI from project state and baseline S-curve.
Enforces hard anti-freeze integrity assertion: fails loudly if SPI or CPI
remains unchanged for 5+ consecutive days while physical progress changed.
Python Standard Library only.
"""

import json
import os

class EVMEngine:
    def __init__(self, baseline_path=None):
        if baseline_path is None:
            repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            baseline_path = os.path.join(repo_root, "state", "baseline.json")
        with open(baseline_path, "r", encoding="utf-8") as f:
            self.baseline = json.load(f)

    def calculate_evm(self, project_state, history=None):
        """
        Calculates EVM metrics for the given project state:
        - BCWS from baseline.json
        - BCWP from QC-accepted progress weighted by budget
        - ACWP from sum of actual costs
        - SPI = BCWP / BCWS
        - CPI = BCWP / ACWP
        - Runs freeze detection check if history is provided.
        """
        sim_day = project_state["day"]
        day_str = str(sim_day)

        # 1. BCWS from baseline S-curve
        daily_bcws_table = self.baseline.get("daily_bcws", {})
        bcws = daily_bcws_table.get(day_str)
        if bcws is None:
            # Fallback if beyond curve
            bcws = self.baseline["project"]["bac_usd"]

        # 2. BCWP (Earned Value)
        # Sum of earned value per package = budget * (qc_accepted / total_qty)
        # Also track by discipline
        discipline_totals = {
            "engineering": {"budget": 0.0, "earned": 0.0, "actual": 0.0},
            "procurement": {"budget": 0.0, "earned": 0.0, "actual": 0.0},
            "construction": {"budget": 0.0, "earned": 0.0, "actual": 0.0},
            "tnc": {"budget": 0.0, "earned": 0.0, "actual": 0.0}
        }

        total_bcwp = 0.0
        total_acwp = 0.0

        for wp_id, wp in project_state["work_packages"].items():
            b = wp.get("budget", 0.0)
            t_qty = wp.get("total_qty", 100.0)
            qc_qty = wp.get("qc_accepted", 0.0)
            act_cost = wp.get("actual_cost", 0.0)
            disc = wp.get("discipline", "construction")

            earned_fraction = min(1.0, qc_qty / t_qty) if t_qty > 0 else 0.0
            earned_val = b * earned_fraction

            total_bcwp += earned_val
            total_acwp += act_cost

            if disc in discipline_totals:
                discipline_totals[disc]["budget"] += b
                discipline_totals[disc]["earned"] += earned_val
                discipline_totals[disc]["actual"] += act_cost

        total_bcwp = round(total_bcwp, 2)
        total_acwp = round(total_acwp, 2)
        bcws = round(float(bcws), 2)

        # 3. Schedule and Cost Indices
        spi = round(total_bcwp / bcws, 4) if bcws > 0 else 1.0000
        cpi = round(total_bcwp / total_acwp, 4) if total_acwp > 0 else 1.0000
        sv = round(total_bcwp - bcws, 2)
        cv = round(total_bcwp - total_acwp, 2)

        evm_metrics = {
            "day": sim_day,
            "bac": self.baseline["project"]["bac_usd"],
            "bcws": bcws,
            "bcwp": total_bcwp,
            "acwp": total_acwp,
            "sv": sv,
            "cv": cv,
            "spi": spi,
            "cpi": cpi,
            "progress_pct": round((total_bcwp / self.baseline["project"]["bac_usd"]) * 100, 4),
            "discipline_performance": {
                disc: {
                    "progress_pct": round((data["earned"] / data["budget"]) * 100, 2) if data["budget"] > 0 else 0.0,
                    "earned_usd": round(data["earned"], 2),
                    "actual_usd": round(data["actual"], 2)
                }
                for disc, data in discipline_totals.items()
            }
        }

        # 4. Anti-Freeze Assertion Check
        # Fail loudly if SPI or CPI is unchanged for 5+ consecutive days while progress changed
        if history and len(history) >= 4:
            current_entry = {
                "day": sim_day,
                "bcwp": total_bcwp,
                "spi": spi,
                "cpi": cpi
            }
            # Combine history with current
            full_window = history[-4:] + [current_entry]
            if len(full_window) >= 5:
                self.assert_no_evm_constancy(full_window)

        return evm_metrics

    @staticmethod
    def assert_no_evm_constancy(window):
        """
        Raises RuntimeError if SPI or CPI remained unchanged for 5+ days
        while physical progress (BCWP) changed.
        """
        assert len(window) >= 5, "Window must contain at least 5 days"
        first_day = window[0]["day"]
        last_day = window[-1]["day"]

        bcwp_values = [r["bcwp"] for r in window]
        spi_values = [r["spi"] for r in window]
        cpi_values = [r["cpi"] for r in window]

        # Check if progress actually changed
        progress_changed = (max(bcwp_values) - min(bcwp_values)) > 1.0  # more than $1 variance

        if progress_changed:
            # Check SPI constancy
            if len(set(spi_values)) == 1:
                raise RuntimeError(
                    f"CRITICAL EVM FAILURE: Synthetic EVM constancy detected! "
                    f"SPI remained completely frozen at {spi_values[0]} across {len(window)} "
                    f"consecutive days (Day {first_day} to Day {last_day}) while physical earned value "
                    f"changed by ${max(bcwp_values) - min(bcwp_values):,.2f}."
                )

            # Check CPI constancy
            if len(set(cpi_values)) == 1:
                raise RuntimeError(
                    f"CRITICAL EVM FAILURE: Synthetic EVM constancy detected! "
                    f"CPI remained completely frozen at {cpi_values[0]} across {len(window)} "
                    f"consecutive days (Day {first_day} to Day {last_day}) while physical earned value "
                    f"changed by ${max(bcwp_values) - min(bcwp_values):,.2f}."
                )
