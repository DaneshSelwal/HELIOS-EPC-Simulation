# HELIOS EPC — Delay Event Log (DEL)

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**Contract:** FIDIC Yellow Book 1999  
**Custodians:** KRONOS (Planning Manager) & COUNSEL (Contracts Manager)  
**Last Updated:** Day 15, Month 1 (2026-10-20)

---

## 1. Summary of Logged Events

| Delay ID | Event Ref | Date Occurred | Event Description | Responsible Party | Affected Path / WBS | Critical Path? | Unmitigated Delay | Net Project Delay | Notice 20.1 Deadline | Notice 20.1 Status | Log Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEL-001** | EVT-001 | 2026-10-06 | Geotechnical Anomaly — Competent Rock Layer encountered at 0.80m in PV Block 6 vs 1.50m design embedment depth causing pile refusal. | Employer (FIDIC Sub-Clause 4.12 Unforeseeable Physical Condition) | `HEL.60` PV Field Piling (Block 6) / `HEL-CIV-PV-PLG-0600` | No (Float: +42d to +45d) | +24 calendar days (Block 6 local path) | **0 days** (Absorbed by re-sequencing Blocks 1–5 first & float) | 2026-11-03 (28 days) | Issued: HELIOS-NTC-001 (2026-10-06) | **ACTIVE / MITIGATION ACCELERATED (Day 15: Mass driving at 80 piles/day in pre-drilled sockets under FDC-CIV-001 / FRAG-PRD-001; 450 rock socket piles installed, 13,290/15,400 project piles; tri-front tracker assembly at 95 tables/day across Blocks 1, 2 & 3; +45d float preserved)** |
| **DEL-002** | EVT-002 | 2026-10-06 | UzbekEnergo Grid Code Revision — Primary Frequency Response (PFR) capability mandated; redesign of Protection Philosophy (`HEL-PR-PHL-0200`) and Substation SLD (`HEL-HV-SLD-0101`). | Employer / Utility (FIDIC Sub-Clause 13.7 Changes in Legislation & Sub-Clause 13.1 Right to Vary) | `HEL.30` Engineering / `HEL.70` 33/220kV GSS Substation (`HEL-ENG-SS-PRT-1010`) | **YES (Critical Path: 0d Float)** | 0 calendar days (Software/PPC revision approved) | **0 days** (Critical path float restored to 0d; zero net delay to Project COD) | 2026-11-03 (28 days) | Issued: HELIOS-NTC-002 (2026-10-06); Closed Day 12 | **CLOSED / MITIGATED (Net Delay: 0 Days)** (Day 12: UzbekEnergo approval letter received; Fragnet FRAG-PFR-003 retired; 33/220kV GSS CP float restored to 0d; PO-HEL-EQ-001 awarded to POWERTRANS linking to HEL-PRO-SS-MPT-2010 at Day 3 of 182) |

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
- **Day 8 Performance Validation (2026-10-13):** Cumulative piling reached **12,740 / 15,400 piles (82.7%)**, with alluvial Blocks 1–5 tracking 100% completion within 3 days (by Day 011). Block 1 handed over; Milestone M5 activated with 25 tracker tables installed on Day 1 (`HEL-MEC-PV-TRK-0100`). Total float on PV field works remains intact at **+45 calendar days**; net COD impact remains **0 days**.
- **Day 9 Performance Validation (2026-10-14):** Activity `HEL-CIV-PV-PLG-0105` (Blocks 1–5 Alluvial Piling) achieved **100% completion (12,840 / 12,840 piles)**. Milestone M4 closed out **+4 days ahead of baseline schedule**, fully preserving **+45 calendar days** total float to Mechanical Completion. Tracker table installation (`HEL-MEC-PV-TRK-0100`) accelerated to **35 tables/day** (surpassing 30 tables/day baseline target; cumulative 60 tables). Net impact on Project COD remains **0 days**.
- **Day 10 Performance Validation (2026-10-15):** Handover of Block 2 following civil QC signoff triggers concurrent activity `HEL-MEC-PV-TRK-0200` (Block 2 Tracker Assembly) running parallel with `HEL-MEC-PV-TRK-0100` (Block 1). Combined tracker assembly rate projected to ramp to **60 tables/day**. Second crawler DTH drill rig deployed in Block 6 (`HEL-CIV-PV-PLG-0600` / `FRAG-EVT-001`), doubling drilling production to 80 holes/day and accelerating remaining recovery duration by **50%**. Total float on PV field works preserved at **+45 calendar days**; master COD impact = **0 days**.
- **Day 11 Performance Validation (2026-10-16):** Dual crawler DTH drill rigs achieved planned full production of **80 holes/day** (cumulative 305 holes pre-drilled). Parallel tracker assembly across Blocks 1 & 2 reached target run-rate of **60 tables/day** (cumulative 175 tables). Total float preserved at **+45 calendar days**; net COD impact remains **0 days**.
- **Day 12 Performance Validation (2026-10-17):** Dual DTH rigs drilled **80 holes today** (cumulative 385 / 2,560 holes, 15.04%). Hydraulic ramming teams installed 80 piles in rock sockets (cumulative 270 in Block 6; overall project piling at 13,110 / 15,400 piles, 85.13%). Parallel tracker table assembly accelerated to **65 tables/day** across Gang A (Block 1: 40 tables) and Gang B (Block 2: 25 tables), reaching cumulative 240 tables (4.71%). Total float on PV field works intact at **+45 calendar days**; net Project COD impact = **0 days**.
- **Day 13 Performance Validation (2026-10-18):** Dual crawler DTH rigs drilled **80 holes today** (cumulative 465 / 2,560 holes, 18.16%). 80 piles driven into pre-drilled sockets (cumulative 350 in Block 6; overall project piling at 13,190 / 15,400 piles, 85.65%). Parallel tracker assembly across Blocks 1 & 2 hit **70 tables/day** (cumulative 310 tables). PV field total float preserved at **+45 calendar days**; net COD impact remains **0 days**.
- **Day 14 Performance Validation (2026-10-19 / Week 2 Close):** Block 6 Pilot Test Pile Campaign successfully achieved 100% PDA/CAPWAP pass rate across 20 test piles (axial compressive capacity 125 kN vs 75 kN design threshold, FS = 1.66; uplift 52 kN; lateral deflection 4.2 mm). Formal clearance granted under `FDC-CIV-001` for mass pile driving into pre-drilled DTH rock sockets. Dual DTH rigs drilled 80 holes (cumulative 545 / 2,560 holes, 21.29%). Overall project piling reached **13,210 / 15,400 piles (85.78%)**. Parallel tracker assembly reached peak run-rate of **80 tables/day** (cumulative 390 tables). Total float remains **+45 calendar days**; net COD impact = **0 days**.
- **Day 15 Performance Validation (2026-10-20 / Week 3 Kickoff):** Handover Certificate `HC-CIV-MEC-003` formally executed (RAMPART to EREKTOR), triggering activity `HEL-MEC-PV-TRK-0300` (Block 3 Tracker Assembly) running concurrently with Blocks 1 and 2. Tri-front tracker assembly run-rate surged to **95 tables/day** (cumulative 485 tables total). Total float on PV field works preserved at **+45 calendar days**. Block 6 mass driving underway at **80 piles/day** into pre-drilled rock sockets under `FDC-CIV-001`, bringing Block 6 rock-socket piles to **450** and project-wide piling to **13,290 / 15,400 piles (86.30%)**, strictly aligning with recovery fragnet `FRAG-PRD-001` schedule duration. Master critical path: MPT manufacturing activity `HEL-PRO-SS-MPT-2010` (Day 3 of 182) progressing on schedule with POWERTRANS; Critical path total float = **0 calendar days**; Project COD locked at **Month 18**.
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
  - Critical Path Float: **0 calendar days (Fully Restored)**.
  - Unmitigated Path Impact: Initial exposure of +7 calendar days during expedited review.
  - Net Project Delay: **0 calendar days** — Project COD remains strictly on baseline schedule (Month 18); zero day-for-day slippage realized.
- **Mitigation & Fragnet Plan:**
  1. **Fragnet Insertion & Retirement (`FRAG-EVT-002`):** Inserted into master CPM network between baseline activity `HEL-ENG-SS-PRT-1000` (Grid Code Receipt) and `HEL-ENG-SS-PRT-1020` (Utility Review):
     - `FRAG-PFR-001`: Joint CIPHER/VOLTA Technical Assessment & Instrument Burden Verification (Completed Day 5).
     - `FRAG-PFR-002`: Protection Philosophy Rework `HEL-ENG-SS-PRT-1010` & PPC Droop Logic Redraft (Completed Day 6; Software/droop curve revision finalized).
     - `FRAG-PFR-003`: UzbekEnergo / GRIDMASTER Expedited Review & Formal Approval — **CLOSED / RETIRED (Day 12)**: Receipt of formal UzbekEnergo approval letter on Day 12 endorsing PPC firmware-based Primary Frequency Response compliance without hardware alteration formally retires Fragnet `FRAG-PFR-003`.
     - `FRAG-PFR-004`: Downstream Logic Linkage & P6 Re-alignment — **EXECUTED (Day 12)**: Award of Purchase Order `PO-HEL-EQ-001` ($850,000 DDP Site to POWERTRANS) executed on Day 12 on schedule, linking directly as Finish-to-Start predecessor into 100MVA transformer manufacturing activity `HEL-PRO-SS-MPT-2010` (duration 182 calendar days / 26 weeks).
  2. **Inter-Discipline Coordination:** SCM hold on 220kV CT/PT released; PPC software configuration baseline confirmed; factory production slot locked with POWERTRANS.
  3. **Schedule Acceleration & Float Recovery:** Total float on the 33/220kV GSS critical path restored to 0 calendar days with zero net delay to Project COD.
- **Day 12 Formal Closeout Record (2026-10-17):**
  - **Closure Trigger:** Formal UzbekEnergo approval letter received on Day 12 validating transmittal `TRN-EPC-CLI-0012`.
  - **Status:** **CLOSED / MITIGATED (Net Delay: 0 Days)**.
  - **Fragnet Retired:** `FRAG-PFR-003` retired; Primavera P6 master schedule updated.
  - **Critical Path Impact:** 0 calendar days net variance to COD; float restored to 0 calendar days.
  - **Manufacturing Milestone:** PO-HEL-EQ-001 awarded to POWERTRANS on Day 12 drop-dead date; successor activity `HEL-PRO-SS-MPT-2010` (182 calendar days) activated.
  - **Cost & Commercial Implications:** Engineering rework absorbed within existing engineering overhead; zero variation cost claimed against Employer; cost code `CC-VAR-EVT-002` closed; Claim `CLM-002` / Notice `HELIOS-NTC-002` closed as fully resolved with zero time extension and zero cost adjustment.
