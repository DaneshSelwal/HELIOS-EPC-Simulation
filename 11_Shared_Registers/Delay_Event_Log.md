# HELIOS EPC — Delay Event Log (DEL)

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**Contract:** FIDIC Yellow Book 1999  
**Custodians:** KRONOS (Planning Manager) & COUNSEL (Contracts Manager)  
**Last Updated:** 2026-10-10 (Day 6, Month 1)

---

## 1. Summary of Logged Events

| Delay ID | Event Ref | Date Occurred | Event Description | Responsible Party | Affected Path / WBS | Critical Path? | Unmitigated Delay | Net Project Delay | Notice 20.1 Deadline | Notice 20.1 Status | Log Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEL-001** | EVT-001 | 2026-10-06 | Geotechnical Anomaly — Competent Rock Layer encountered at 0.80m in PV Block 6 vs 1.50m design embedment depth causing pile refusal. | Employer (FIDIC Sub-Clause 4.12 Unforeseeable Physical Condition) | `HEL.60` PV Field Piling (Block 6) / `HEL-CIV-PV-PLG-0600` | No (Float: +42d to +45d) | +24 calendar days (Block 6 local path) | **0 days** (Absorbed by re-sequencing Blocks 1–5 first & float) | 2026-11-03 (28 days) | Issued: HELIOS-NTC-001 (2026-10-06) | **ACTIVE / MITIGATION VALIDATED (Day 6: Pilot DTH at 35 holes/day confirms FDC-CIV-001)** |
| **DEL-002** | EVT-002 | 2026-10-06 | UzbekEnergo Grid Code Revision — Primary Frequency Response (PFR) capability mandated; redesign of Protection Philosophy (`HEL-PR-PHL-0200`) and Substation SLD (`HEL-HV-SLD-0101`). | Employer / Utility (FIDIC Sub-Clause 13.7 Changes in Legislation & Sub-Clause 13.1 Right to Vary) | `HEL.30` Engineering / `HEL.70` 33/220kV GSS Substation (`HEL-ENG-SS-PRT-1010`) | **YES (Critical Path: 0d Float)** | +7 calendar days (Software/PPC revision) | **+7 calendar days** (Critical path exposure to COD; 7d review fragnet running) | 2026-11-03 (28 days) | Issued: HELIOS-NTC-002 (2026-10-06) | **ACTIVE / PFR REVISION SUBMITTED TO UTILITY (7-day fragnet running)** |

---

## 2. Event Detail Records

### DEL-001 / EVT-001: Block 6 Shallow Rock Horizon Refusal
- **Event Identifier:** DEL-001 (Cross-reference: GitHub Issue #7 / EVT-001)
- **Date of Occurrence:** 2026-10-06 (Project Day 2, Month 1)
- **Location / WBS:** Block 6 Array, WBS `HEL.60` (Construction – PV Field), Activity `HEL-CIV-PV-PLG-0600`
- **Root Cause & Description:** Competent bedrock stratum encountered at depth of 0.80 m below EGL across Block 6, resulting in immediate hydraulic ramming refusal. Tender geotechnical documentation provided by Employer represented uniform alluvial loose/medium sand to $>2.5\text{ m}$ depth with design pile embedment at 1.50 m (`HEL-ST-CAL-0010`). Terminating piles at 0.80 m provides $<35\%$ passive lateral resistance, causing structural failure under wind gust overturning moments per KMK 2.01.07-96.
- **Contractual Classification:** Unforeseeable Physical Condition under FIDIC Yellow Book 1999 Sub-Clause 4.12. Entitlement asserted under Sub-Clause 8.4(b) (Extension of Time) and Sub-Clause 4.12 (Cost incurred).
- **Statutory Notice Clock (Sub-Clause 20.1):** 
  - Date Aware: 2026-10-06 (Day 2)
  - 28-Day Statutory Notice Cut-off: **2026-11-03 (Day 30)**
  - Notice Directive: Formal Notice HELIOS-NTC-001 issued by COUNSEL on 2026-10-06 (Day 2, 26 days ahead of time-bar). Claim Ref CLM-001.
- **CPM Schedule & Float Impact:**
  - Master Critical Path: Runs through 220kV GSS and MPT manufacturing chain (0 days total float). Block 6 is off the master critical path.
  - PV Field Total Float: **+45 calendar days** to Mechanical Completion (Month 15).
  - Unmitigated Block 6 Piling Impact: +24 calendar days due to DTH rig cycle time reduction (35–40 piles/day vs 120 piles/day) and rig procurement lead time.
  - Net Project Impact: **0 days** delay to COD (Month 18) or Milestone `HEL.10` First Pile (Month 4).
- **Day 6 Performance Validation (2026-10-10):** DTH pilot pre-drilling commenced in Block 6; recorded productivity is **35 holes/day**, directly validating FDC-CIV-001 assumptions. Ramming in alluvial Blocks 1–5 reached **71.2% physical progress** (10,965 / 15,400 piles) with **SPI = 1.03**. Net COD impact remains **0 days**.
- **Mitigation & Fragnet Plan:**
  1. **Workfront Re-sequencing:** RAMPART/GROUNDWORK directed to re-sequence hydraulic ramming sequence to commence in alluvial sandy sectors (Blocks 1 through 5) at Month 4. Block 6 shifted to Workfront 6 (Month 6–7), creating 10–12 weeks of lead time buffer.
  2. **Technical Remediation:** Adoption of Option 1 (DTH rock pilot pre-drilling $\varnothing 180-220\text{ mm}$ + 500mm rock socket + non-shrink cementitious grout annulus) per Technical Memorandum `HEL-CV-MEM-0001`.
  3. **Fragnet Insertion:** Inserted Fragnet `FRAG-EVT-001` (36 calendar days total qualification/mobilization duration executed concurrently during Months 1–3 before piling start).
- **Cost & Commercial Implications:**
  - Additional Cost items: Crawler DTH drilling rigs mobilization, 21 bar air compressors, consumable tungsten carbide drill bits, cementitious grout (M15/C12/15) batching, confirmatory core boreholes (MERIDIAN), and calibration pile testing.
  - LEDGER and CLAIMS notified to track all associated cost codes separately under `CC-VAR-EVT-001`.

---

### DEL-002 / EVT-002: UzbekEnergo Grid Code Revision — Primary Frequency Response (PFR)
- **Event Identifier:** DEL-002 (Cross-reference: GitHub Issue #10 / EVT-002 / MOC-002)
- **Date of Occurrence:** 2026-10-06 (Project Day 2, Month 1; Formally logged Day 4: 2026-10-08)
- **Location / WBS:** 33/220kV Grid Substation (GSS), WBS `HEL.30` (Engineering) & `HEL.70` (Substation Construction), Activity `HEL-ENG-SS-PRT-1010`
- **Root Cause & Description:** UzbekEnergo issued a revised National Grid Code post-design freeze mandating active Primary Frequency Response (PFR) droop control capability. This mandates engineering rework of the Protection Philosophy (`HEL-PR-PHL-0200 Rev 1`), updates to Substation SLD (`HEL-HV-SLD-0101`), verification/respecification of 220kV CT/PT instrument transformers (600/5A burden/saturation rating), and Power Plant Controller (PPC) firmware/droop logic reconfiguration. MOC-002 opened by ARCHON; IFC release of protection drawings placed on immediate hold.
- **Contractual Classification:** Change in Legislation under FIDIC Yellow Book 1999 Sub-Clause 13.7 and/or Employer Variation under Sub-Clause 13.1. Entitlement asserted under Sub-Clause 8.4(b) (Extension of Time for Completion) and Sub-Clause 13.7 / 20.1 (Cost plus reasonable profit).
- **Statutory Notice Clock (Sub-Clause 20.1):** 
  - Date Aware: 2026-10-06 (Day 2)
  - 28-Day Statutory Notice Cut-off: **2026-11-03 (Day 30)**
  - Notice Directive: Formal Notice of Claim HELIOS-NTC-002 drafted/served by COUNSEL on 2026-10-06 (Claim Ref CLM-002) within the 28-day statutory guillotine.
- **CPM Schedule & Float Impact:**
  - Master Critical Path: **True Master Critical Path**. The project critical path runs directly through the 33/220kV GSS electrical engineering approval, Main Power Transformer (MPT) & GIS manufacturing (24–30 weeks), transport through Khorgos border, site erection, testing & commissioning, and NEGU grid synchronization.
  - Critical Path Float: **0 calendar days**.
  - Unmitigated Path Impact: **7 to 14 calendar days** engineering delay fragnet on GSS substation path:
    - *Scenario A (PPC Firmware Update Only):* 7 calendar days for protection philosophy redraft, SCADA logic update, and utility resubmission.
    - *Scenario B (Hardware Modifications to CTs/PTs):* 14 calendar days if instrument transformer physical resizing, switchyard layout redesign, or vendor manufacturing slot renegotiation are mandated.
  - Net Project Delay: **+7 to +14 calendar days** direct day-for-day slippage to Project COD (Month 18) unless mitigated by utility fast-track review or parallel engineering approval.
- **Mitigation & Fragnet Plan:**
  1. **Fragnet Insertion (`FRAG-EVT-002`):** Inserted into master CPM network between baseline activity `HEL-ENG-SS-PRT-1000` (Grid Code Receipt) and `HEL-ENG-SS-PRT-1020` (Utility Review):
     - `FRAG-PFR-001`: Joint CIPHER/VOLTA Technical Assessment & Instrument Burden Verification (Completed Day 5).
     - `FRAG-PFR-002`: Protection Philosophy Rework `HEL-ENG-SS-PRT-1010` & PPC Droop Logic Redraft (Completed Day 6; Software/droop curve revision finalized).
     - `FRAG-PFR-003`: UzbekEnergo / GRIDMASTER Expedited Review & Formal Approval — **ACTIVE (Day 6)**: PFR software revision submitted to utility; 7-day fragnet running with 0 days total float.
  2. **Inter-Discipline Coordination:** CONVOY cleared on 220kV CT/PT specifications (no physical hardware change); PPC software configuration baseline confirmed.
  3. **Schedule Acceleration Measures:** ATLAS and KRONOS actively managing the expedited 7-day utility review cycle with UzbekEnergo / GRIDMASTER to safeguard the master critical path.
- **Cost & Commercial Implications:**
  - Additional engineering redesign man-hours, potential vendor change orders for PPC firmware / CT/PT specification adjustments, and delay prolongation cost.
  - Cost tracking established with LEDGER under code `CC-VAR-EVT-002`.
