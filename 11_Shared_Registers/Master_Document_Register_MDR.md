# HELIOS EPC — Master Document & Drawing Register (MDR)

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Bukhara, Uzbekistan  
**Contract:** FIDIC Yellow Book 1999 (Sub-Clause 5.2 Contractor's Documents — 14-Day Review Cycle)  
**Custodians:** HERALD (PMO Document Controller) & ARCHON (Design Manager)  
**Last Updated:** 2026-10-06 (Sim Day 001, Month 1, Week 1 — LNTP Start Position)

## 1. Approval Status Code Legend
- **Code 1 (`APPROVED`)**: Approved without comments; eligible for `Rev 0 (IFC)` release to Construction (`RAMPART`).
- **Code 2 (`APPROVED WITH COMMENTS`)**: Work/procurement may proceed subject to comment incorporation within 7 calendar days; eligible for conditional `Rev 0 (IFC)` release.
- **Code 3 (`REJECTED / REVISE & RESUBMIT`)**: **HOLD** remains active; cannot be used for procurement fabrication or site construction.
- **Code 4 (`FOR INFORMATION ONLY`)**: Reference document; formal approval not required.
- **Code P (`PENDING REVIEW`)**: Under contractual 14-day review clock with `PATRON` / `AUDITOR` / `GRIDMASTER` / `INSPECTOR`.

## 2. Master Deliverable & Engineering Submittal Log

| Doc Number | Title / Description | Discipline | Owner Agent | Current Rev | Transmittal Ref | Date Submitted | Reviewer(s) | 14d Review Due | Status Code | IFC Released? | Remarks / Linked Event |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `HEL-PM-PLN-0001` | Project Execution Plan (PEP) & PMO Governance Charter | PMO | `ATLAS` | Rev 0 | `TRN-HEL-0001` | 2026-10-06 (D001) | `PATRON`, `AUDITOR` | 2026-10-20 (D015) | **Code 1** | Yes | Baseline governance approved at LNTP |
| `HEL-PL-SCH-0001` | Master EPC Baseline Schedule (L1–L3 P6 CPM) & S-Curve | PLN | `KRONOS` | Rev 0 | `TRN-HEL-0002` | 2026-10-06 (D001) | `PATRON`, `AUDITOR` | 2026-10-20 (D015) | **Code 1** | Yes | USD 85M BAC; 504d COD; 0d float on 220kV GSS |
| `HEL-HS-PLN-0001` | Master Construction HSE Plan & SanPiN Heat/Cold Protocol | EHS | `AEGIS` | Rev 0 | `TRN-HEL-0003` | 2026-10-06 (D001) | `PATRON`, `AUDITOR`, `INSPECTOR` | 2026-10-20 (D015) | **Code 1** | Yes | Released for `WP-CON-MOB` mobilization |
| `HEL-QA-PLN-0001` | Project Quality Plan (PQP) & Master ITP Index | QAQ | `SENTINEL` | Rev 0 | `TRN-HEL-0004` | 2026-10-07 (D002) | `PATRON`, `AUDITOR` | 2026-10-21 (D016) | **Code 1** | Yes | Enforces H/W/R/M inspection gates |
| `HEL-CV-GEO-0001` | Site-Wide Geotechnical Investigation Report (Blocks 1–5) | ENG (Civil) | `MERIDIAN` | Rev 0 | `TRN-HEL-0005` | 2026-10-08 (D003) | `TERRA`, `AUDITOR` | 2026-10-22 (D017) | **Code 2** | No | Alluvial sand confirmed Blocks 1–5; Block 6 excluded |
| `HEL-CV-MEM-0001` | Technical Assessment: Block 6 Shallow Rock Horizon at 0.80m | ENG (Civil) | `TERRA` | Rev A | `TRN-HEL-0006` | 2026-10-10 (D005) | `ARCHON`, `AUDITOR`, `INSPECTOR` | 2026-10-24 (D019) | **Code 2 (Cond.)** | **HOLD** | Linked to `EVT-001` / `FDC-CIV-001`; requires 6 boreholes & 3 load tests |
| `HEL-ST-CAL-0010` | Driven Steel Pile Foundation Structural Calculations | ENG (Civil) | `TERRA` | Rev A | `TRN-HEL-0007` | 2026-10-10 (D005) | `ARCHON`, `AUDITOR` | 2026-10-24 (D019) | **Code P** | No | Being updated to Rev 1 for Block 6 DTH rock socket |
| `HEL-MC-LAY-0100` | 1P Single-Axis Tracker Array General Layout & Foundation Loads | ENG (Mech) | `SOLARIS` | Rev A | `TRN-HEL-0008` | 2026-10-09 (D004) | `TERRA`, `AUDITOR` | 2026-10-23 (D018) | **Code P** | No | 5,100 tables; $\pm 20	ext{ mm}$ E-W pile tolerance |
| `HEL-EL-SLD-0100` | 1500V DC Array & 33kV Collector System Single Line Diagram | ENG (Elec) | `AMPERE` | Rev A | `TRN-HEL-0009` | 2026-10-09 (D004) | `VOLTA`, `AUDITOR` | 2026-10-23 (D018) | **Code P** | No | 25 x 4.0MVA `INVERSA` PCS skids |
| `HEL-HV-SLD-0101` | 33/220kV Grid Substation (GSS) Master Single Line Diagram | ENG (Sub) | `VOLTA` | Rev A | `TRN-HEL-0010` | 2026-10-08 (D003) | `GRIDMASTER`, `AUDITOR` | 2026-10-22 (D017) | **Code P** | No | Critical path 0d float; subject to `EVT-002` CT/PT check |
| `HEL-PR-PHL-0200` | 33/220kV GSS Protection, Control & Metering Philosophy | ENG (Prot) | `CIPHER` | Rev A | `TRN-HEL-0011` | 2026-10-08 (D003) | `GRIDMASTER`, `AUDITOR` | 2026-10-22 (D017) | **Code P** | No | Critical path; PFR droop revision incoming (`EVT-002`) |
