# HELIOS EPC — Master Commercial Billing Register (Client IPCs & Subcontractor JMCs)

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Bukhara, Uzbekistan  
**Contract:** FIDIC Yellow Book 1999 (Contract Price: USD 85,000,000.00)  
**Custodians:** INVOICE (Billing / QS Engineer, CC-03), CHECKER (Subcontractor Billing Verifier, CC-04) & LEDGER2 (Finance Controller, AD-02)  
**Approvers:** COUNSEL (Contracts Manager) & ATLAS (Project Manager)  
**Last Updated:** 2026-10-06 (Sim Day 001, Month 1, Week 1 — LNTP Start Position)

## 1. Commercial Rules of Credit & Payment Governance
1. **Strict Earned Value Alignment**: Client Interim Payment Certificates (`IPC` under FIDIC Sub-Clause 14.3) and Subcontractor Joint Measurement Certificates (`JMC`) are strictly capped at **QC-Accepted Quantities (`qc_accepted`)** verified in `state/project_state.json`. Unverified installed work, materials without a signed `MIRN`, or items under an open Category A/B NCR are excluded.
2. **Contractual Deductions**:
   - **Client IPCs (`PATRON`)**: 15% Advance Payment (`USD 12,750,000`) amortized pro-rata at 15% per IPC; 10% Retention Money deducted until Retention reaches 5% of Contract Price (`USD 4,250,000`). Payment due within 56 days of Engineer receipt under Sub-Clause 14.7.
   - **Subcontractor JMCs (`GROUNDWORK`, `EREKTOR`, `ELECTRA`, `GRIDCON`)**: 10% Retention deduction, 10% Advance amortization, plus deduction of verified EPC back-charges (e.g., `EVT-005` rig breakdown standby, `EVT-006` pile re-drive survey costs).

## 2. Part A — Employer / Client Interim Payment Certificate (IPC) Log

| IPC Ref | Billing Period | Sim Day Submitted | Cumulative BCWP Earned (USD) | This Period Gross Work (USD) | Advance Recovery (-15%) | Retention (-10%) | Net Certified by `PATRON`/`AUDITOR` (USD) | Payment Due Sim Day | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `IPC-ADV` | LNTP Mobilization | Day 001 | $0.00 | $12,750,000.00 (15% Advance) | $0.00 | $0.00 | **$12,750,000.00** | Day 014 | **CERTIFIED — APBG Delivered** |
| `IPC-001` (Accrual) | Month 1 (As of Day 005) | Due Day 028 | $261,978.75 (0.3082% of BAC) | $261,978.75 (Eng: $153,978.75 + Mob: $108,000.00) | -$39,296.81 | -$26,197.88 | **$196,484.06 (Accrued)** | Day 084 | **ACCRUING (Submits Day 028)** |

## 3. Part B — Subcontractor Progress & JMC Verification Log

| Subcontractor | Scope / Package | Contract Type | Installed Progress (Day 005) | QC-Accepted Progress (Day 005) | Cumulative Earned Value (USD) | Actual Cost Incurred ACWP (USD) | Disputed / Capped Overclaims (USD) | Back-Charges Applied (USD) | Status (Verified by `CHECKER`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GROUNDWORK** | `WP-CON-MOB` (Site Mobilization & Temp Facilities) | Lump Sum / Milestone ($1,500,000) | 7.55% | **7.20%** | $108,000.00 | $111,125.00 | $5,250.00 (0.35% unverified fencing capped) | $0.00 | **RECONCILED (JMC-GW-01 accruing)** |
| **GROUNDWORK** | `WP-CON-CIV-GRD` & `WP-CON-CIV-PIL` (Grading & 15,400 Piles) | Item-Rate BOQ ($4,700,000) | 0.00% (0 piles) | **0.00% (0 piles)** | $0.00 | $0.00 | $0.00 | $0.00 | **NOT STARTED (Block 6 Held under `EVT-001`; Piling starts M4)** |
| **EREKTOR** | `WP-CON-MEC-TRK` & `MOD` (Trackers & Modules) | Item-Rate BOQ ($9,300,000) | 0 tables / 0 mods | **0 tables / 0 mods** | $0.00 | $0.00 | $0.00 | $0.00 | **NOT MOBILISED (Starts post-Piling)** |
| **ELECTRA** | `WP-CON-ELE-DC`, `MV` & `SUB-ERE` (Electrical & GSS E&M) | Item-Rate + LS ($8,200,000) | 0.00% | **0.00%** | $0.00 | $0.00 | $0.00 | $0.00 | **NOT MOBILISED** |
| **GRIDCON** | `WP-CON-CIV-FND` (Substation & Inverter Concrete Foundations) | Item-Rate BOQ ($1,800,000) | 0.0 m³ | **0.0 m³** | $0.00 | $0.00 | $0.00 | $0.00 | **AWAITING `WP-ENG-CIV` IFC** |
