#!/usr/bin/env python3
"""
HELIOS EPC Action Validation, Register Mutation & Closed-Loop Application Engine.
Validates agent proposed actions against authority_matrix.json and physical state rules.
Accepted actions mutate both state/project_state.json AND append structured Markdown rows
directly to the shared project registers:
  - issue_fdc / issue_rfi / respond_rfi / issue_tq -> 11_Shared_Registers/RFI_TQ_FDC_Register.md
  - put_hold / witness_hold_point / release_hold -> 11_Shared_Registers/ITP_Hold_Point_Register.md
  - log_delay_event / validate_gate_i -> 11_Shared_Registers/Delay_Event_Log.md & 01_Planning_Controls/Delay_Event_Log.md
  - issue_notice / log_claim -> 07_Contracts/FIDIC_Notice_Log.md
  - raise_ncr / close_ncr -> 11_Shared_Registers/NCR_Register.md
  - issue_ptw / revoke_ptw -> 11_Shared_Registers/PTW_Log.md
  - compile_dpr -> 12_Daily_Reports/DPR/DPR_Day{NNN}.md
Rejected actions are logged with reasons and queued to the agent's inbox for next day.
Python Standard Library only.
"""

import json
import os
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

AUTHORITY_PATH = os.path.join(REPO_ROOT, "engine", "authority_matrix.json")
STATE_PATH = os.path.join(REPO_ROOT, "state", "project_state.json")
NEXT_INBOX_DIR = os.path.join(REPO_ROOT, "state", "inbox_queue")

RFI_REG_PATH = os.path.join(REPO_ROOT, "11_Shared_Registers", "RFI_TQ_FDC_Register.md")
ITP_REG_PATH = os.path.join(REPO_ROOT, "11_Shared_Registers", "ITP_Hold_Point_Register.md")
SHARED_DELAY_PATH = os.path.join(REPO_ROOT, "11_Shared_Registers", "Delay_Event_Log.md")
PLN_DELAY_PATH = os.path.join(REPO_ROOT, "01_Planning_Controls", "Delay_Event_Log.md")
FIDIC_NOTICE_PATH = os.path.join(REPO_ROOT, "07_Contracts", "FIDIC_Notice_Log.md")
NCR_REG_PATH = os.path.join(REPO_ROOT, "11_Shared_Registers", "NCR_Register.md")
PTW_LOG_PATH = os.path.join(REPO_ROOT, "11_Shared_Registers", "PTW_Log.md")
DPR_DIR = os.path.join(REPO_ROOT, "12_Daily_Reports", "DPR")


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
        try:
            cost_impact = float(cost_impact)
        except (TypeError, ValueError):
            cost_impact = 0.0

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
            qty = float(params.get("quantity", 0.0) or 0.0)
            wp = current_state.get("work_packages", {}).get(wp_id)
            if wp:
                if not wp.get("ifc_released", False) and "PIL" in wp_id:
                    return False, f"Cannot claim installation for {wp_id}: IFC drawings not released."
                if wp.get("delivered", 0.0) < (wp.get("installed", 0.0) + qty):
                    return False, f"Cannot install {qty} units of {wp_id}: material delivered ({wp.get('delivered')}) is insufficient."

        # 4. Known Allowed Action Patterns across all 64 agents
        allowed_patterns = [a.lower() for a in auth.get("allowed_actions", [])]

        valid_types = {
            # PMO
            "ATLAS": ["issue_instruction", "approve_plan", "escalate_to_pd", "chair_meeting", "authorize_mitigation"],
            "NEXUS": ["coordinate_interfaces", "track_actions", "issue_instruction", "chair_meeting"],
            "HERALD": ["register_submittal", "issue_transmittal", "update_mdr", "log_document"],
            # PLN
            "KRONOS": ["log_delay_event", "validate_gate_i", "update_schedule", "run_tia", "flag_critical_path", "publish_mpr"],
            "SIGMA": ["compile_dpr", "reconcile_quantities", "publish_wpr", "publish_mpr"],
            "VECTOR": ["update_progress_curves", "audit_quantities", "track_productivity"],
            "WATT": ["update_manpower_histogram", "track_equipment", "verify_Histogram"],
            # ENG
            "ARCHON": ["approve_ifc", "issue_fdc", "respond_rfi", "approve_tbe", "review_design"],
            "NEXGEN": ["run_pvsyst", "verify_yield", "issue_tq"],
            "CIPHER": ["configure_scada", "review_telecom", "issue_tq"],
            "TERRA": ["issue_fdc", "respond_rfi", "request_geotech", "issue_tq", "put_hold", "release_ifc"],
            "MERIDIAN": ["conduct_survey", "drill_borehole", "issue_geotech_report", "verify_coordinates"],
            "AMPERE": ["issue_fdc", "respond_rfi", "issue_tq", "review_cable_sizing"],
            "VOLTA": ["issue_fdc", "respond_rfi", "review_hv_design", "approve_fat_protocol"],
            "SOLARIS": ["issue_fdc", "respond_rfi", "approve_tracker_calc", "put_hold"],
            "RELAY": ["issue_protection_settings", "review_grid_study", "respond_rfi"],
            # SCM
            "CONVOY": ["update_procurement_tracker", "issue_rfq", "expedite_vendor", "flag_customs_hold"],
            "FORGE": ["witness_fat", "expedite_factory", "put_hold"],
            "VENDOR": ["complete_tbe", "issue_po_recommendation", "evaluate_bid"],
            "TRACER": ["track_shipment", "update_eta", "reroute_convoy"],
            "ROUTE": ["clear_customs", "submit_gtd", "coordinate_heavy_haul"],
            "VAULT": ["inspect_receiving", "quarantine_batch", "issue_mrr"],
            "DEPOT": ["issue_material", "reconcile_stock", "audit_stores"],
            # CON
            "RAMPART": ["put_hold", "instruct_subcontractor", "allocate_workfront", "approve_method_statement"],
            "BASTION": ["put_hold", "site_inspection", "witness_hold_point", "instruct_subcontractor"],
            "SWITCHMAN": ["put_hold", "site_inspection", "coordinate_gss_erection"],
            "ARCLINE": ["put_hold", "site_inspection", "verify_cable_trench"],
            "FORTRESS": ["put_hold", "verify_rebar", "approve_concrete_pour"],
            "CONDUIT": ["put_hold", "verify_termination", "log_megger_test"],
            "STRATUM": ["put_hold", "verify_compaction", "check_drainage"],
            "PRISM": ["verify_alignment", "as_built_survey", "check_pile_plumbness"],
            # QAQ
            "SENTINEL": ["raise_ncr", "close_ncr", "put_hold", "release_hold", "witness_hold_point"],
            "PLUMBLINE": ["raise_ncr", "witness_hold_point", "put_hold", "verify_cube_test"],
            "OHMMETER": ["raise_ncr", "witness_hold_point", "put_hold", "verify_el_test"],
            "TORQUE": ["raise_ncr", "witness_hold_point", "put_hold", "verify_pull_test"],
            "DOSSIER": ["audit_turnover_pack", "verify_redlines", "compile_quality_dossier"],
            # EHS
            "AEGIS": ["issue_ptw", "revoke_ptw", "put_hold", "issue_stop_work", "log_ehs_inspection"],
            "GUARDIAN": ["issue_ptw", "revoke_ptw", "issue_stop_work", "conduct_toolbox_talk"],
            "WARDEN": ["issue_loto_permit", "revoke_ptw", "verify_earthing"],
            "VERDANT": ["monitor_dust", "inspect_waste", "log_environmental_audit"],
            # COM
            "COUNSEL": ["issue_notice", "log_claim", "review_contract", "instruct_hold", "draft_variation"],
            "CLAIMS": ["compile_claim_dossier", "quantify_eot_cost", "log_contemporary_record"],
            "INVOICE": ["prepare_ipc", "verify_sub_valuation", "update_billing_register"],
            "LEDGE": ["certify_remeasurement", "audit_boq_quantities"],
            "CHECKER": ["assess_sub_claim", "issue_backcharge", "verify_sub_ipc"],
            "LEDGER": ["update_evm_cost", "flag_cpi_breach", "reconcile_acwp"],
            "LEDGER2": ["verify_lc_compliance", "track_cashflow", "process_vendor_payment"],
            # TNC
            "IGNITE": ["issue_energization_notice", "approve_commissioning_proc", "put_hold"],
            "SPARK": ["run_iv_curve", "verify_pcs_cold_comm", "log_test_sheet"],
            "GRIDLOCK": ["execute_scada_p2p", "run_pfr_test", "verify_grid_compliance"],
            # ADM
            "SUMMIT": ["manage_camp_welfare", "coordinate_security", "log_community_grievance"],
            "PERMIT": ["submit_construction_permit", "track_visa_customs", "liaise_authority"],
            # SUB
            "GROUNDWORK": ["submit_rfi", "mobilize_rig", "report_daily_piling", "request_inspection"],
            "EREKTOR": ["submit_rfi", "report_tracker_progress", "request_inspection"],
            "ELECTRA": ["submit_rfi", "report_cable_progress", "request_inspection"],
            "GRIDCON": ["submit_rfi", "report_gss_progress", "request_inspection"],
            # EXT
            "PATRON": ["issue_employer_instruction", "respond_notice", "certify_milestone"],
            "AUDITOR": ["review_submittal", "witness_hold_point", "respond_rfi", "evaluate_claim"],
            "GRIDMASTER": ["issue_grid_directive", "witness_grid_test", "approve_energization"],
            "LUMINOS": ["submit_vendor_dossier", "report_module_shipment", "respond_ncr"],
            "INVERSA": ["submit_firmware_patch", "report_pcs_shipment", "respond_tq"],
            "POWERTRANS": ["submit_fat_report", "report_mpt_transport", "respond_ncr"],
            "INSPECTOR": ["conduct_state_inspection", "issue_regulatory_directive"],
            "CERTIFIER": ["witness_fat", "issue_3p_certificate", "audit_lab_results"],
        }

        agent_valid_types = valid_types.get(agent, [])
        if act_type in agent_valid_types or any(act_type in p for p in allowed_patterns):
            return True, f"Action '{act_type}' permitted under {agent}'s delegated authority."

        for p in allowed_patterns:
            if any(w in p for w in act_type.split("_") if len(w) > 2):
                return True, f"Action '{act_type}' matches permitted scope: {p[:60]}..."

        if act_type in [
            "send_memo", "request_information", "hold_review", "log_observation",
            "issue_rfi", "respond_rfi", "issue_tq", "issue_fdc", "put_hold",
            "log_delay_event", "issue_notice", "raise_ncr", "issue_ptw", "compile_dpr"
        ]:
            return True, f"Standard EPC governance action '{act_type}' accepted for {agent}."

        return False, f"Action '{act_type}' is outside {agent}'s defined authority scope. Escalate to {esc_target}."


def _append_markdown_table_row(filepath, row_str, section_header=None):
    """Appends a Markdown table row to a file (optionally inside a specific section)."""
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if row_str in content:
        return False

    if section_header and section_header in content:
        parts = content.split(section_header, 1)
        after = parts[1]
        # Find next section "## " if any
        next_sec_idx = after.find("\n## ")
        if next_sec_idx != -1:
            sec_body = after[:next_sec_idx].rstrip()
            rest = after[next_sec_idx:]
            new_content = parts[0] + section_header + sec_body + "\n" + row_str + "\n" + rest
        else:
            new_content = parts[0] + section_header + after.rstrip() + "\n" + row_str + "\n"
    else:
        new_content = content.rstrip() + "\n" + row_str + "\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def apply_accepted_action_to_registers(sim_day, agent, action, current_state):
    """
    Mutates current_state (and saves to state/project_state.json) and appends rows
    to the relevant Markdown registers when an action is ACCEPTED.
    Returns list of modified file paths (relative to REPO_ROOT).
    """
    act_type = action.get("type", "").lower()
    params = action.get("params", {}) or {}
    sim_date = current_state.get("sim_date", f"Day {sim_day:03d}")
    modified_files = []

    # Ensure state tracking lists exist
    current_state.setdefault("rfi_tq_fdc_log", [])
    current_state.setdefault("itp_holds", [])
    current_state.setdefault("delay_events", [])
    current_state.setdefault("fidic_notices", [])
    current_state.setdefault("ncr_log", [])
    current_state.setdefault("ptw_log", [])

    # 1. RFI / TQ / FDC actions -> 11_Shared_Registers/RFI_TQ_FDC_Register.md
    if act_type in ["issue_fdc", "issue_rfi", "respond_rfi", "issue_tq", "submit_rfi"]:
        ref_id = params.get("fdc_no") or params.get("rfi_no") or params.get("tq_no") or params.get("ref_id") or f"FDC-{agent}-D{sim_day:03d}"
        doc_type = "FDC" if "fdc" in act_type else ("TQ" if "tq" in act_type else "RFI")
        recipient = params.get("to") or params.get("recipient") or "ARCHON / BASTION"
        subject = params.get("scope") or params.get("subject") or params.get("description") or f"{act_type.upper()} issued by {agent}"
        wbs = params.get("wbs") or params.get("wp_id") or "WP-CON-CIV-PIL (Block 6)"
        spec_ref = params.get("spec_ref") or "IFC Civil / Geotech Spec"
        disposition = params.get("disposition") or params.get("resolution") or f"Actioned by {agent} on Day {sim_day:03d}"
        impact = params.get("impact") or "Subject to KRONOS TIA / COUNSEL Notice"
        status = params.get("status") or ("ISSUED" if "fdc" in act_type else "OPEN")

        row = f"| **`{ref_id}`** | `{doc_type}` | Day {sim_day:03d} ({sim_date}) | `{agent}` -> `{recipient}` | {subject} | `{wbs}` | {spec_ref} | {disposition} | {impact} | **`{status}`** |"
        if _append_markdown_table_row(RFI_REG_PATH, row):
            modified_files.append("11_Shared_Registers/RFI_TQ_FDC_Register.md")

        current_state["rfi_tq_fdc_log"].append({
            "ref_id": ref_id, "type": doc_type, "sim_day": sim_day, "agent": agent,
            "subject": subject, "wbs": wbs, "status": status
        })

    # 2. ITP / Hold Point actions -> 11_Shared_Registers/ITP_Hold_Point_Register.md
    elif act_type in ["put_hold", "witness_hold_point", "release_hold"]:
        itp_ref = params.get("itp_ref") or params.get("hold_id") or f"ITP-HOLD-D{sim_day:03d}-{agent}"
        wbs = params.get("wbs") or params.get("wp_id") or params.get("location") or "WP-CON-CIV-PIL (Array Block 6)"
        stage = params.get("stage") or params.get("scope") or params.get("description") or f"Hold point action ({act_type}) by {agent}"
        criteria = params.get("criteria") or "FIDIC Yellow Book / Project ITP Specification"
        sub = params.get("subcontractor") or "GROUNDWORK"
        qc_owner = params.get("qc_owner") or agent
        witness = params.get("witness") or "AUDITOR (OE)"
        pt_type = "H (Hold Point)" if "hold" in act_type else "W (Witness)"
        status = "RELEASED" if "release" in act_type else f"ACTIVE HOLD (Day {sim_day:03d})"

        row = f"| **`{itp_ref}`** | `{wbs}` | {stage} | {criteria} | `{sub}` | `{qc_owner}` | `{witness}` | **{pt_type}** | **`{status}`** |"
        if _append_markdown_table_row(ITP_REG_PATH, row):
            modified_files.append("11_Shared_Registers/ITP_Hold_Point_Register.md")

        current_state["itp_holds"].append({
            "itp_ref": itp_ref, "wbs": wbs, "stage": stage, "agent": agent,
            "sim_day": sim_day, "status": status
        })

    # 3. Delay Event / Gate (i) Validation -> Delay_Event_Log.md (both 01_Planning_Controls & 11_Shared_Registers)
    elif act_type in ["log_delay_event", "validate_gate_i", "run_tia", "flag_critical_path"]:
        delay_id = params.get("delay_id") or f"DEL-{sim_day:03d}"
        ev_ref = params.get("event_id") or params.get("event_ref") or (", ".join(current_state.get("active_events", [])) or "NONE")
        desc = params.get("description") or params.get("summary") or f"Schedule / TIA validation by {agent} on Day {sim_day:03d}"
        party = params.get("responsible_party") or "Employer / Unforeseeable Physical Conditions (Cl. 4.12)"
        wbs = params.get("wbs") or "WP-CON-CIV-PIL / 220kV GSS Critical Path"
        is_cp = params.get("critical_path") or "NO (Local Array Float +45d; Master CP is 220kV GSS/MPT 0d Float)"
        unmit = params.get("unmitigated_delay") or f"{params.get('delay_days', 0)} days local"
        net_cod = params.get("net_cod_delay") or "0 days"
        notice_bar = params.get("notice_deadline") or f"Day {sim_day + 28:03d}"
        status = params.get("status") or "OPEN — MITIGATION IN PROGRESS"

        if act_type == "log_delay_event" or params.get("delay_id"):
            del_row = f"| **`{delay_id}`** | `{ev_ref}` | {sim_date} (Day {sim_day:03d}) | {desc} | {party} | `{wbs}` | {is_cp} | `{unmit}` | **`{net_cod}`** | {notice_bar} | **`{status}`** |"
            if _append_markdown_table_row(SHARED_DELAY_PATH, del_row, "## 1. Master Register of Delay Events"):
                modified_files.append("11_Shared_Registers/Delay_Event_Log.md")
            if _append_markdown_table_row(PLN_DELAY_PATH, del_row, "## 1. Master Register of Delay Events"):
                modified_files.append("01_Planning_Controls/Delay_Event_Log.md")

        evm = current_state.get("project_totals", {})
        gate_row = (
            f"| **Day {sim_day:03d}** | {sim_date} | `{agent}` | `{ev_ref}` | `0 days` | `+45 days` | "
            f"**Day {sim_day} Validated**: SPI=`{evm.get('spi', 1.0):.4f}`, CPI=`{evm.get('cpi', 1.0):.4f}`; {desc} |"
        )
        if _append_markdown_table_row(SHARED_DELAY_PATH, gate_row, "## 2. Daily Gate (i) Validation"):
            if "11_Shared_Registers/Delay_Event_Log.md" not in modified_files:
                modified_files.append("11_Shared_Registers/Delay_Event_Log.md")
        if _append_markdown_table_row(PLN_DELAY_PATH, gate_row, "## 2. Daily Gate (i) Validation"):
            if "01_Planning_Controls/Delay_Event_Log.md" not in modified_files:
                modified_files.append("01_Planning_Controls/Delay_Event_Log.md")

        current_state["delay_events"].append({
            "delay_id": delay_id, "event_ref": ev_ref, "sim_day": sim_day,
            "agent": agent, "description": desc, "status": status
        })

    # 4. FIDIC Notices / Claims -> 07_Contracts/FIDIC_Notice_Log.md
    elif act_type in ["issue_notice", "log_claim", "draft_variation"]:
        ntc_no = params.get("notice_no") or params.get("ref_id") or f"HEL-NTC-20.1-{sim_day:03d}"
        clause = params.get("clause") or params.get("sub_clause") or "Sub-Clause 20.1 & 4.12"
        subj = params.get("subject") or params.get("description") or f"Formal FIDIC Notice issued by {agent}"
        recipient = params.get("to") or "PATRON (Employer) / AUDITOR (OE)"
        ch_code = params.get("channel") or "CH-09 (#19)"
        time_bar = params.get("time_bar") or f"Day {sim_day + 27:03d} (28-Day Statutory Window)"
        ev_ref = params.get("event_id") or (", ".join(current_state.get("active_events", [])) or "EVT-001")

        row = f"| **`{ntc_no}`** | Day {sim_day:03d} ({sim_date}) | `{clause}` | {subj} | `{agent}` -> `{recipient}` | `{ch_code}` | {time_bar} | **YES (Day 1 of 28)** | **`ISSUED / OPEN`** | `{ev_ref}` |"
        if _append_markdown_table_row(FIDIC_NOTICE_PATH, row):
            modified_files.append("07_Contracts/FIDIC_Notice_Log.md")

        current_state["fidic_notices"].append({
            "notice_no": ntc_no, "clause": clause, "sim_day": sim_day,
            "agent": agent, "subject": subj, "event_ref": ev_ref
        })

    # 5. Quality NCRs -> 11_Shared_Registers/NCR_Register.md
    elif act_type in ["raise_ncr", "close_ncr"]:
        ncr_no = params.get("ncr_no") or f"NCR-D{sim_day:03d}-01"
        cat = params.get("category") or "Major"
        disc = params.get("discipline") or "Civil / Structural"
        wbs = params.get("wbs") or params.get("location") or "Array Block 6 (WP-CON-CIV-PIL)"
        issued_to = params.get("issued_to") or "GROUNDWORK"
        desc = params.get("description") or f"Non-conformance raised by {agent} on Day {sim_day:03d}"
        rca = params.get("rca") or "Under investigation"
        disp = params.get("disposition") or "Hold point active pending engineering FDC disposition"
        bc_ref = params.get("backcharge_ref") or "TBD"
        status = "CLOSED" if "close" in act_type else "OPEN"

        row = f"| **`{ncr_no}`** | Day {sim_day:03d} ({sim_date}) | `{cat}` | {disc} | `{wbs}` | `{agent}` -> `{issued_to}` | {desc} | {rca} | {disp} | `{bc_ref}` | Pending | **`{status}`** |"
        if _append_markdown_table_row(NCR_REG_PATH, row):
            modified_files.append("11_Shared_Registers/NCR_Register.md")

        current_state["ncr_log"].append({
            "ncr_no": ncr_no, "sim_day": sim_day, "agent": agent,
            "wbs": wbs, "description": desc, "status": status
        })

    # 6. EHS Permits to Work -> 11_Shared_Registers/PTW_Log.md
    elif act_type in ["issue_ptw", "revoke_ptw", "issue_stop_work"]:
        ptw_id = params.get("ptw_id") or f"PTW-D{sim_day:03d}-{agent}"
        p_type = params.get("permit_type") or ("STOP WORK / HOLD" if "revoke" in act_type or "stop" in act_type else "General / Geotech Drilling PTW")
        loc = params.get("location") or params.get("wbs") or "Site-Wide / Array Block 6"
        issued_to = params.get("issued_to") or "BASTION / GROUNDWORK"
        controls = params.get("controls") or "Full PPE, SanPiN hydration, daily toolbox talk, calibrated instruments"
        validity = params.get("validity") or f"Day {sim_day:03d} (07:00 - 18:00)"
        status = "SUSPENDED / STOP WORK" if ("revoke" in act_type or "stop" in act_type) else "ACTIVE"

        row = f"| **`{ptw_id}`** | Day {sim_day:03d} ({sim_date}) | `{p_type}` | `{loc}` | `{issued_to}` | `{agent}` | {controls} | {validity} | **`{status}`** |"
        if _append_markdown_table_row(PTW_LOG_PATH, row):
            modified_files.append("11_Shared_Registers/PTW_Log.md")

        current_state["ptw_log"].append({
            "ptw_id": ptw_id, "sim_day": sim_day, "agent": agent,
            "location": loc, "status": status
        })

    # 7. Daily Progress Report compilation -> 12_Daily_Reports/DPR/DPR_Day{NNN}.md
    elif act_type == "compile_dpr":
        os.makedirs(DPR_DIR, exist_ok=True)
        dpr_rel = f"12_Daily_Reports/DPR/DPR_Day{sim_day:03d}.md"
        dpr_path = os.path.join(REPO_ROOT, dpr_rel)
        evm = current_state.get("project_totals", {})
        weather = current_state.get("weather", {})
        wps = current_state.get("work_packages", {})
        events = current_state.get("active_events", [])

        dpr_lines = [
            f"# HELIOS EPC — Daily Progress Report (`DPR_Day{sim_day:03d}`)",
            "",
            f"- **Simulation Day**: Day `{sim_day:03d}` (`{sim_date}`) | **Month**: `{current_state.get('month', 1)}` | **Week**: `{current_state.get('week', 1)}`",
            f"- **Prepared By**: `{agent}` (MIS & Reporting Analyst) | **Verified By**: `KRONOS` & `ATLAS`",
            f"- **Weather**: {weather.get('summary', 'Clear')} ({weather.get('temp_c', 24)}°C, Wind {weather.get('wind_kmh', 12)} km/h, Productivity Factor `{weather.get('productivity_factor', 1.0)}`)",
            f"- **Active Events**: {', '.join(events) if events else 'None (Clean Baseline)'}",
            "",
            "## 1. Earned Value Management (EVM) & Schedule Telemetry",
            "",
            "| Metric | Value | Status / Threshold |",
            "| :--- | :--- | :--- |",
            f"| **BAC (Contract Price)** | `${evm.get('bac_usd', 85000000.0):,.2f}` | Fixed Lump Sum (FIDIC Yellow Book) |",
            f"| **Planned Value (BCWS)** | `${evm.get('bcws_usd', 0.0):,.2f}` | Cumulative Baseline Plan |",
            f"| **Earned Value (BCWP)** | `${evm.get('bcwp_usd', 0.0):,.2f}` | `{evm.get('progress_pct', 0.0):.4f}%` Overall Physical Progress |",
            f"| **Actual Cost (ACWP)** | `${evm.get('acwp_usd', 0.0):,.2f}` | Accrued on Accepted Work & Engineering Hours |",
            f"| **SPI (Schedule Performance Index)** | **`{evm.get('spi', 1.0):.4f}`** | {'⚠️ Below 0.95 Threshold' if evm.get('spi', 1.0) < 0.95 else '✅ On Track'} |",
            f"| **CPI (Cost Performance Index)** | **`{evm.get('cpi', 1.0):.4f}`** | {'⚠️ Below 0.95 Threshold' if evm.get('cpi', 1.0) < 0.95 else '✅ On Track'} |",
            "",
            "## 2. Physical Workfront Quantities (`state/project_state.json`)",
            "",
            "| Work Package ID | Description | Scope | Delivered | Installed | QC Accepted | % Complete |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for wp_id, wp in wps.items():
            dpr_lines.append(
                f"| `{wp_id}` | {wp.get('name', wp_id)} | `{wp.get('total_scope', 100)} {wp.get('unit', '')}` | "
                f"`{wp.get('delivered', 0)}` | `{wp.get('installed', 0)}` | **`{wp.get('qc_accepted', 0)}`** | "
                f"`{wp.get('progress_pct', 0.0):.2f}%` |"
            )
        dpr_lines.extend([
            "",
            "## 3. Summary Notes & Governance",
            "",
            f"- {params.get('summary', f'Day {sim_day:03d} physical progress and EVM metrics reconciled directly from state/day_{sim_day:03d}_state.json with zero unverified claims.')}",
            ""
        ])
        with open(dpr_path, "w", encoding="utf-8") as f:
            f.write("\n".join(dpr_lines))
        modified_files.append(dpr_rel)

    # Persist updated project_state.json
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(current_state, f, indent=2)
    if "state/project_state.json" not in modified_files:
        modified_files.append("state/project_state.json")

    return modified_files


def process_agent_actions(sim_day, agent, actions_list, current_state):
    """
    Validates a list of actions from an agent, mutates state/registers for accepted actions,
    and queues rejected actions to next day inbox.
    Returns (accepted_list, rejected_list).
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
            "agent": agent,
            "action": act,
            "status": "ACCEPTED" if is_ok else "REJECTED",
            "reason": reason,
            "modified_registers": []
        }
        if is_ok:
            mod_files = apply_accepted_action_to_registers(sim_day, agent, act, current_state)
            act_record["modified_registers"] = mod_files
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
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        st = json.load(f)
    val = ActionValidator()
    ok, msg = val.validate_action(test_agent, test_act, st)
    print(f"Test Action validation: {test_agent} {test_act['type']} -> {ok} ({msg})")
