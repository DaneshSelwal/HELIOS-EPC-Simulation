# HELIOS EPC — Planning & Controls Department Delay Event Log

**Department:** 01 Planning & Controls  
**Custodian:** KRONOS (Planning Manager)  
**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**Contract Baseline:** FIDIC Yellow Book 1999  
**Data Date:** 2026-10-06 (Day 2, Month 1)

---

## 1. Master Register of Delay Events

| Delay ID | Event Ref | Date Occurred | Event Description | Responsible Party | Affected Path / WBS | Critical Path? | Local Delay | Master COD Delay | Notice 20.1 Deadline | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEL-001** | EVT-001 | 2026-10-06 | Geotechnical Anomaly — Competent Rock at 0.80m in Block 6 vs 1.50m design embedment depth causing pile refusal. | Employer (FIDIC Sub-Clause 4.12 Unforeseeable Physical Condition) | `HEL.60` PV Field Piling (Block 6) / `HEL-CIV-PV-PLG-0600` | No (Total Float = +45d) | +24 calendar days (Block 6 local path) | **0 days** (Absorbed by re-sequencing Blocks 1–5 first & float) | 2026-11-03 (28 days) | ACTIVE / MITIGATION IMPLEMENTED |

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
- **Workfront Re-sequencing Decision:**
  - Piling sequence modified: Deploy all hydraulic ramming rigs to **Blocks 1 through 5 first** upon Month 4 mobilization.
  - Re-allocate Block 6 to the rear position (Campaign Step 6, projected start Month 6–7).
  - Result: 10–12 weeks of lead time created; DTH mobilization and test pile qualification occur entirely during pre-construction window; net impact on Project COD = **0 days**.
- **Contractual & Commercial Actions:**
  - Instructed COUNSEL to serve FIDIC Sub-Clause 4.12 / 20.1 Reservation Notice of Claim within statutory 28-day window (deadline: 2026-11-03).
  - Cost tracking established with LEDGER under code `CC-VAR-EVT-001` to capture equipment mobilization, tooling wear, and grouting costs.
