#!/usr/bin/env python3
"""
HELIOS EPC Action Validation and Application Engine.
Validates agent proposed actions against authority_matrix.json and physical state rules.
Accepted actions are applied to state registers.
Rejected actions are logged with reasons and queued to the agent's inbox for next day.
Python Standard Library only.
"""

import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

AUTHORITY_PATH = os.path.join(REPO_ROOT, "engine", "authority_matrix.json")
STATE_PATH = os.path.join(REPO_ROOT, "state", "project_state.json")
NEXT_INBOX_DIR = os.path.join(REPO_ROOT, "state", "inbox_queue")

class ActionValidator:
    def __init__(self, authority_matrix_path=AUTHORITY_PATH):
        with open(authority_matrix_path, "r", encoding="utf-8") as f:
            self.matrix = json.load(f)

    def validate_action(self, agent, action, current_state):
        """
        Validates a single action against authority matrix and project rules.
        Returns (is_accepted: bool, reason: str).
        """
        auth = self.matrix.get(agent)
        if not auth:
            return False, f"Unknown agent '{agent}' has no authority matrix record."

        act_type = action.get("type", "").lower()
        params = action.get("params", {})
        fin_limit = auth.get("financial_limit", "ESCALATE")
        esc_target = auth.get("escalation_target", "ATLAS")

        # 1. Financial Authority Check
        cost_impact = params.get("cost_usd", params.get("value_usd", 0.0))
        if cost_impact > 0.0:
            if fin_limit == "ESCALATE":
                return False, f"Agent {agent} has zero standalone financial authority (limit is ESCALATE). Must escalate to {esc_target} for approval of ${cost_impact:,.2f}."
            elif isinstance(fin_limit, (int, float)) and cost_impact > fin_limit:
                return False, f"Cost ${cost_impact:,.2f} exceeds {agent}'s financial authority limit of ${fin_limit:,.2f}. Must escalate to {esc_target}."

        # 2. Check Prohibitions
        prohibitions = " ".join(auth.get("prohibitions", [])).lower()
        if "without atlas" in prohibitions and act_type in ["settle_claim", "alter_programme", "approve_baseline"]:
            return False, f"Action '{act_type}' requires prior ATLAS/PD approval per persona limits."

        # 3. Physical State & Discipline Rules
        if act_type in ["claim_installed", "certify_progress"]:
            wp_id = params.get("wp_id", "")
            qty = params.get("quantity", 0.0)
            wp = current_state.get("work_packages", {}).get(wp_id)
            if wp:
                if not wp.get("ifc_released", False) and "PIL" in wp_id:
                    return False, f"Cannot claim installation for {wp_id}: IFC drawings not released."
                if wp.get("delivered", 0.0) < (wp.get("installed", 0.0) + qty):
                    return False, f"Cannot install {qty} units of {wp_id}: material delivered ({wp.get('delivered')}) is insufficient."

        # 4. Known Allowed Action Patterns
        allowed_patterns = [a.lower() for a in auth.get("allowed_actions", [])]
        allowed_str = " ".join(allowed_patterns)

        # Standard accepted action types for project agents:
        valid_types = {
            "TERRA": ["issue_fdc", "respond_rfi", "request_geotech", "issue_tq", "put_hold"],
            "MERIDIAN": ["conduct_survey", "drill_borehole", "issue_geotech_report"],
            "BASTION": ["put_hold", "site_inspection", "witness_hold_point", "instruct_subcontractor"],
            "KRONOS": ["log_delay_event", "update_schedule", "run_tia", "flag_critical_path"],
            "COUNSEL": ["issue_notice", "log_claim", "review_contract", "instruct_hold"],
            "ATLAS": ["issue_instruction", "approve_plan", "escalate_to_pd", "chair_meeting"],
            "SIGMA": ["compile_dpr", "reconcile_quantities", "publish_mpr"]
        }

        agent_valid_types = valid_types.get(agent, [])
        if act_type in agent_valid_types or any(act_type in p for p in allowed_patterns):
            return True, f"Action '{act_type}' permitted under {agent}'s delegated authority."

        # If general match in allowed descriptions
        for p in allowed_patterns:
            if any(w in p for w in act_type.split("_")):
                return True, f"Action '{act_type}' matches permitted scope: {p[:50]}..."

        # Default fallback: check if action type is reasonable coordination
        if act_type in ["send_memo", "request_information", "hold_review", "log_observation"]:
            return True, f"Administrative coordination action '{act_type}' accepted."

        return False, f"Action '{act_type}' is outside {agent}'s defined authority scope. Escalate to {esc_target}."

def process_agent_actions(sim_day, agent, actions_list, current_state):
    """
    Validates a list of actions from an agent.
    Returns (accepted_list, rejected_list).
    Queues rejected actions to next day inbox.
    """
    validator = ActionValidator()
    accepted = []
    rejected = []

    os.makedirs(NEXT_INBOX_DIR, exist_ok=True)
    next_day_inbox_file = os.path.join(NEXT_INBOX_DIR, f"inbox_day_{sim_day+1:03d}_{agent}.json")
    next_day_items = []
    if os.path.exists(next_day_inbox_file):
        with open(next_day_inbox_file, "r", encoding="utf-8") as f:
            next_day_items = json.load(f)

    for act in actions_list:
        is_ok, reason = validator.validate_action(agent, act, current_state)
        act_record = {
            "action": act,
            "status": "ACCEPTED" if is_ok else "REJECTED",
            "reason": reason
        }
        if is_ok:
            accepted.append(act_record)
        else:
            rejected.append(act_record)
            next_day_items.append({
                "type": "ACTION_REJECTED",
                "sim_day": sim_day + 1,
                "from_agent": "GOVERNANCE_ENGINE",
                "topic": f"Rejected action: {act.get('type')}",
                "reason": reason,
                "original_action": act
            })

    if next_day_items:
        with open(next_day_inbox_file, "w", encoding="utf-8") as f:
            json.dump(next_day_items, f, indent=2)

    return accepted, rejected

if __name__ == "__main__":
    test_agent = "TERRA"
    test_act = {"type": "issue_fdc", "params": {"fdc_no": "FDC-CIV-001", "scope": "Block 6 pre-drilling"}}
    with open(STATE_PATH, "r") as f:
        st = json.load(f)
    val = ActionValidator()
    ok, msg = val.validate_action(test_agent, test_act, st)
    print(f"Test Action validation: {test_agent} {test_act['type']} -> {ok} ({msg})")
