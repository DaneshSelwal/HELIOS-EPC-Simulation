# HELIOS EPC — Master Inspection & Test Plan (ITP) & Hold Point Register

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Bukhara, Uzbekistan  
**Custodians:** SENTINEL (QA/QC Manager) & DOSSIER (QA Document Coordinator)  
**Last Updated:** 2026-10-06 (Sim Day 001, Month 1, Week 1 — LNTP Start Position)

## 1. Inspection Point Definitions
- **H (`Hold Point`)**: Mandatory stop. Work **cannot proceed** beyond this step without physical attendance and signed release by EPC QC (`PLUMBLINE`/`TORQUE`/`OHMMETER`) and, where designated, `AUDITOR` (Lender's IE). Proceeding past an `H` point without release triggers an immediate Category A/B NCR.
- **W (`Witness Point`)**: 24-hour formal Inspection Request (`IR`) notification required. Work may proceed if inspector does not attend at the scheduled time, provided Subcontractor QC records are complete.
- **R (`Review`)**: Documentation review (Mill Test Certificates `MTC`, calibration certs, cube results).

## 2. Active ITP & Hold Point Schedule

| ITP / IR Ref | WBS / Work Package | Activity & Inspection Stage | Governing Standard / Criteria | Subcontractor | EPC QC Owner | External Witness | Point Type | Current Status (Day 005) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `HEL-IR-CIV-001` | `WP-CON-MOB` | Site Perimeter Fencing, Gates, Security & Temp Camp Setup (7.55% installed) | Project Spec / HSE Plan `HEL-HS-PLN-0001` | `GROUNDWORK` | `PLUMBLINE` | `AUDITOR` (M) | **W** | **7.20% Certified** (Ongoing daily checks) |
| `HEL-IR-CIV-002` | `WP-CON-CIV-GRD` | Mass Grading Cut/Fill & Internal Road Sub-Base Compaction | NDG $\ge 95\%$ MDD, CBR per KMK, N-S slope $<10\%$, $\pm 50	ext{ mm}$ | `GROUNDWORK` | `PLUMBLINE` | `AUDITOR` (W) | **H** | **Awaiting `WP-ENG-CIV` IFC Release** |
| `HEL-IR-CIV-003` | `WP-CON-CIV-PIL` (Block 6) | **Block 6 Calibration Pile Load Tests (3 No. Pre-Drilled & Grouted Piles per `FDC-CIV-001`)** | **ASTM D1143 (Compression), D3689 (Uplift $\ge 1.5	imes$ design), D3966 (Lateral $\le 6.0	ext{ mm}$), KMK 2.02.01-98** | `GROUNDWORK` | `PLUMBLINE` | **`AUDITOR` (H), `INSPECTOR` (R)** | **H (CRITICAL)** | **HOLD ACTIVE (`EVT-001` / `HEL-ENG-QAQ-INS-0004`)** |
| `HEL-IR-CIV-004` | `WP-CON-CIV-PIL` (Blocks 1–5) | Production Ramming Pile Acceptance (Depth, Plumbness, E-W Tolerance $\pm 20	ext{ mm}$, Head $\pm 6	ext{ mm}$) | `HEL-ST-CAL-0010` / `SOLARIS` Tracker Spec | `GROUNDWORK` | `PLUMBLINE` / `PRISM` | `AUDITOR` (W) | **H** | **Scheduled Month 4 (Day 112)** |
| `HEL-IR-MEC-001` | `WP-CON-MEC-TRK` | 1P Single-Axis Tracker Bearing, Torque Tube & Slew Drive Bolt Torque Verification | OEM Torque Spec + 100% Torque-Seal Witness Marks | `EREKTOR` | `TORQUE` | `AUDITOR` (W) | **H** | **Scheduled post-Piling Acceptance** |
| `HEL-IR-MEC-002` | `WP-CON-MEC-MOD` | 580W Bifacial PV Module Mounting, Clamp Zone & Torque ($14–20	ext{ Nm}$) | `LUMINOS` Installation Manual / IEC 62446-1 | `EREKTOR` | `TORQUE` | `AUDITOR` (W) | **H** | **Scheduled Month 6 (Day 168)** |
| `HEL-IR-ELE-001` | `WP-CON-ELE-DC` | DC Trench Sand Bedding, String Polarity, $V_{oc}$, $I_{sc}$, Insulation Resistance & IV Curve ($FF \ge 78\%$) | IEC 62446-1 / IEC 62930 | `ELECTRA` / `EREKTOR` | `OHMMETER` / `SPARK` | `AUDITOR` (W) | **H** | **Scheduled post-Module Mounting** |
| `HEL-IR-ELE-002` | `WP-CON-ELE-MV` | 33kV MV Cable Cold-Shrink Jointing (Tent Required) & 0.1Hz VLF Withstand Test ($3U_0$) | IEEE 400.2 / IEC 60502-2 | `ELECTRA` | `OHMMETER` | `AUDITOR` (H) | **H** | **Scheduled Month 7** |
| `HEL-IR-SUB-001` | `WP-CON-SUB-ERE` | 220kV 100MVA MPT Arrival Impact Recorder Check ($\le 4.0g$), Plinth Skidding, SFRA & Protection Injection | IEC 60076-18 / `POWERTRANS` Spec / `Uzenergoinspeksiya` | `ELECTRA` / `POWERTRANS` | `OHMMETER` / `RELAY` | `AUDITOR` (H), `GRIDMASTER` (H) | **H** | **Scheduled Month 10–16** |
