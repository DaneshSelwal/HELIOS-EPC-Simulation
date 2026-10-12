# HELIOS EPC — Planning & Controls Department Delay Event Log

**Department:** 01 Planning & Controls  
**Custodian:** KRONOS (Planning Manager)  
**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**Contract Baseline:** FIDIC Yellow Book 1999  
**Data Date:** 2026-10-13 (Day 8, Month 1)

---

## 1. Master Register of Delay Events

| Delay ID | Event Ref | Date Occurred | Event Description | Responsible Party | Affected Path / WBS | Critical Path? | Local Delay | Master COD Delay | Notice 20.1 Deadline | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEL-001** | EVT-001 | 2026-10-06 | Geotechnical Anomaly — Competent Rock at 0.80m in Block 6 vs 1.50m design embedment depth causing pile refusal. | Employer (FIDIC Sub-Clause 4.12 Unforeseeable Physical Condition) | `HEL.60` PV Field Piling (Block 6) / `HEL-CIV-PV-PLG-0600` | No (Total Float = +42d to +45d) | +24 calendar days (Block 6 local path) | **0 days** (Absorbed by re-sequencing Blocks 1–5 first & float) | 2026-11-03 (28 days) | **ACTIVE / MITIGATION VALIDATED (Day 8: Piling at 82.7%, alluvial completion in 3 days; DTH pre-drilling ongoing)** |
| **DEL-002** | EVT-002 | 2026-10-06 | UzbekEnergo Grid Code Revision — Primary Frequency Response (PFR) capability mandated; redesign of Protection Philosophy (`HEL-PR-PHL-0200`). | Employer / Utility (FIDIC Sub-Clause 13.7 & Sub-Clause 13.1) | `HEL.30` Engineering / `HEL.70` 33/220kV GSS Substation (`HEL-ENG-SS-PRT-1010`) | **YES (Critical Path: 0d Float)** | +7 calendar days (Software/PPC revision) | **+7 calendar days** (Critical path exposure; 7d review fragnet running) | 2026-11-03 (28 days) | **ACTIVE / PFR UTILITY REVIEW (Day 3 of 7 on expedited review fragnet FRAG-PFR-003; 0d Float)** |

---

## 2. Comprehensive Event Analysis & Fragnet Documentation

### Event Record: DEL-001 (EVT-001)
- **Activity Affected:** `HEL-CIV-PV-PLG-0600` (PV Field Block 6 Piling Installation)
- **Predecessor:** `HEL-CIV-PV-GRD-0600` (Block 6 Civil Grading & Layout)
- **Successor:** `HEL-MEC-PV-TRK-0600` (Block 6 Tracker Structure Assembly)
- **Discovery Date:** 2026-10-06 (Project Day 2, Month 1 from LNTP)
- **Baseline Schedule Context:**
  - Today: Day 2, Month 1
  - Site Mobilization (`HEL.20`): Month 2
  - Engineering Freeze: Month 3
  - First Pile Driven Milestone (`HEL.10`): Month 4 (~Day 90–120)
  - Lead Time Buffer Available: **10 to 12 weeks (~70 to 88 calendar days)** prior to commencement of field piling operations.
- **CPM Float Status:**
  - Total Float (PV Field Array): **+45 to +52 calendar days** to Mechanical Completion (Month 15).
  - True Master Critical Path: Runs through 220kV GSS Detailed Design -> NEGU Review -> 220kV MPT & GIS Manufacturing (24–30 wks) -> Logistics via Khorgos -> MPT Erection -> Energization (Month 16) -> COD (Month 18). Total Float on Critical Path = **0 days**.
- **Fragnet Structure (`FRAG-EVT-001`):**
  1. `FRAG-GEO-001`: Confirmatory Diamond Core Drilling (6–8 boreholes) & UCS/RQD Laboratory Testing (MERIDIAN) — 5 days
  2. `FRAG-ENG-001`: Engineering Design Revision FDC-CIV-001 & Updated Geotech Calculations Rev 1 (TERRA / ARCHON) — 4 days
  3. `FRAG-PRO-001`: Crawler DTH Drill Rig & High-Pressure Compressor Mobilization (CONVOY / GROUNDWORK) — 12 days
  4. `FRAG-CAL-001`: Trial Test Pile Drilling, Socketing & Annular Grouting (GROUNDWORK / BASTION) — 1 day install + 7 days grout cure (8 days total)
  5. `FRAG-TST-001`: Static Compression, Uplift & Lateral Load Tests (ASTM D1143/D3689/D3966) (MERIDIAN / PLUMBLINE) — 3 days
  6. `FRAG-APP-001`: Load Test Report Approval & Engineer Sign-Off (ARCHON / TERRA / PATRON) — 4 days
  7. `FRAG-PRD-001`: Block 6 DTH Pre-drilling & Pile Driving Execution (GROUNDWORK) — 35–40 piles/day/rig across ~2,800 piles with 2 rigs = 35–40 working days (vs baseline 12 days at 120 piles/day). Net variance: +24 days.
- **Day 6 Performance Validation (2026-10-10):**
  - DTH pilot pre-drilling commenced in Block 6 following PTW issuance; recorded productivity is **35 holes/day**, directly validating FDC-CIV-001 and Technical Memorandum `HEL-CV-MEM-0001` assumptions (35–40 holes/day).
  - Main ramming campaign across alluvial Blocks 1–5 reached **71.2% physical completion** (10,965 / 15,400 total piles driven) with **SPI = 1.03** (ahead of baseline schedule).
  - Total float on PV field works remains **+42 to +45 calendar days**; net impact on Project COD remains **0 days**.
- **Day 8 Performance Validation (2026-10-13):**
  - Cumulative piling reached **12,740 / 15,400 piles (82.7%)**, with alluvial Blocks 1–5 tracking 100% completion within 3 days (by Day 011).
  - Block 1 handed over; Milestone M5 activated with 25 tracker tables installed on Day 1 of assembly (`HEL-MEC-PV-TRK-0100`).
  - Total float on PV field works remains intact at **+45 calendar days** to Mechanical Completion; COD impact remains **0 days**.
- **Workfront Re-sequencing Decision:**
  - Piling sequence modified: Deploy all hydraulic ramming rigs to **Blocks 1 through 5 first** upon Month 4 mobilization.
  - Re-allocate Block 6 to the rear position (Campaign Step 6, projected start Month 6–7).
  - Result: 10–12 weeks of lead time created; DTH mobilization and test pile qualification occur entirely during pre-construction window; net impact on Project COD = **0 days**.
- **Contractual & Commercial Actions:**
  - Notice Served: COUNSEL served formal FIDIC Sub-Clause 4.12 / 20.1 Notice of Claim HELIOS-NTC-001 on 2026-10-06 (Claim Ref CLM-001, 26 days ahead of 2026-11-03 statutory deadline).
  - Cost tracking established with LEDGER under code `CC-VAR-EVT-001` to capture equipment mobilization, tooling wear, and grouting costs.

---

### Event Record: DEL-002 (EVT-002)
- **Activity Affected:** `HEL-ENG-SS-PRT-1010` (Rework of Substation Protection & Control Philosophy)
- **Predecessor:** `HEL-ENG-SS-PRT-1000` (Receipt of Revised UzbekEnergo Grid Code & Issue MOC-002)
- **Successor:** `HEL-ENG-SS-PRT-1020` (UzbekEnergo / NEGU Formal Review & Approval Cycle) -> `HEL-PRO-SS-MPT-2010` (MPT & High Voltage Equipment Manufacturing Release)
- **Discovery Date:** 2026-10-06 (Project Day 2, Month 1 from LNTP; Formally logged Day 4: 2026-10-08)
- **Baseline Schedule Context:**
  - Today: Day 6, Month 1
  - Site Mobilization (`HEL.20`): Month 2
  - Engineering Freeze Milestone: Month 3
  - First Energization (Back-feed from NEGU): Month 16
  - Grid Synchronization / COD (`HEL.10`): Month 18
  - Total Float on Substation Path: **0 calendar days (True Master Critical Path)**.
- **CPM Float Status & Critical Path Impact:**
  - Unlike PV field works (which possess +42d to +45d float), the 33/220kV GSS electrical engineering path dictates the project completion date.
  - Zero float available: any extension to `HEL-ENG-SS-PRT-1010` or the subsequent utility review cycle impacts COD directly day-for-day.
  - Critical Path status: **CRITICAL PATH ACTIVE MONITORING (Amber / High Priority)**.
- **Fragnet Structure (`FRAG-EVT-002`):**
  1. `FRAG-PFR-001`: Joint Protection & Automation Technical Feasibility Review (VOLTA / CIPHER) — Completed Day 5.
  2. `FRAG-PFR-002`: Protection Philosophy Revision `HEL-PR-PHL-0200 Rev 1` & SLD `HEL-HV-SLD-0101` Update (ARCHON / CIPHER) — Completed Day 6. Software/PPC droop logic route confirmed (no CT/PT hardware resizing needed).
  3. `FRAG-PFR-003`: Formal Submission to UzbekEnergo / NEGU and Contractual Review (ARCHON / GRIDMASTER) — **ACTIVE (Day 8: Day 3 of 7 elapsed)**: Grid Code PFR software revision actively under expedited review; critical path float remains 0 days. MPT PO release Drop Dead Date is Day 12/13.
  4. `FRAG-PFR-004`: Baseline Schedule Recalculation & Time Impact Analysis (TIA) Finalization (KRONOS) — 2 calendar days upon approval.
- **Mitigation & Recovery Actions:**
  - PO releases for 220kV CT/PT cleared from hardware modification risk; PPC software configuration baseline confirmed.
  - Expedited 7-day review fragnet actively tracked with UzbekEnergo / NEGU grid compliance engineers to prevent day-for-day slippage against MPT release Drop Dead Date.
- **Contractual & Commercial Actions:**
  - Notice Served: Formal FIDIC Sub-Clause 13.7 / 13.1 / 20.1 Notice of Claim `HELIOS-NTC-002` drafted/issued by COUNSEL on 2026-10-06 (Claim Ref `CLM-002`).
  - Statutory 28-day time-bar deadline: 2026-11-03 preserved.
  - Full detailed claim under Sub-Clause 20.1 due within 42 days (2026-11-17).
  - Cost code `CC-VAR-EVT-002` assigned by LEDGER for engineering rework and potential vendor variation costs.
