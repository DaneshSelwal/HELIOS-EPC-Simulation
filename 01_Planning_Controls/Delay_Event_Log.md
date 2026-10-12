# HELIOS EPC — Planning & Controls Department Delay Event Log

**Department:** 01 Planning & Controls  
**Custodian:** KRONOS (Planning Manager)  
**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**Contract Baseline:** FIDIC Yellow Book 1999  
**Data Date:** Day 18, Month 1 (2026-10-23)

---

## 1. Master Register of Delay Events

| Delay ID | Event Ref | Date Occurred | Event Description | Responsible Party | Affected Path / WBS | Critical Path? | Local Delay | Master COD Delay | Notice 20.1 Deadline | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEL-001** | EVT-001 | 2026-10-06 | Geotechnical Anomaly — Competent Rock at 0.80m in Block 6 vs 1.50m design embedment depth causing pile refusal. | Employer (FIDIC Sub-Clause 4.12 Unforeseeable Physical Condition) | `HEL.60` PV Field Piling (Block 6) / `HEL-CIV-PV-PLG-0600` | No (Total Float = +42d to +45d) | +24 calendar days (Block 6 local path) | **0 days** (Absorbed by re-sequencing Blocks 1–5 first & float) | 2026-11-03 (28 days) | **ACTIVE / MITIGATION ACCELERATED (Day 18: Mass driving at 80 piles/day in pre-drilled sockets under FDC-CIV-001 / FRAG-PRD-001; 690 rock socket piles installed, 13,530/15,400 project piles [87.86%]; triple gangs maintain 100 tables/day with 785 cumulative tables [+195 ahead of baseline]; +45d float preserved; Block 4 activation modeled for Day 19)** |
| **DEL-002** | EVT-002 | 2026-10-06 | UzbekEnergo Grid Code Revision — Primary Frequency Response (PFR) capability mandated; redesign of Protection Philosophy (`HEL-PR-PHL-0200`). | Employer / Utility (FIDIC Sub-Clause 13.7 & Sub-Clause 13.1) | `HEL.30` Engineering / `HEL.70` 33/220kV GSS Substation (`HEL-ENG-SS-PRT-1010`) | **YES (Critical Path: 0d Float)** | 0 calendar days (Software/PPC revision approved) | **0 days** (Critical path float restored to 0d; zero net delay to Project COD) | 2026-11-03 (28 days) | **CLOSED / MITIGATED (Net Delay: 0 Days)** (Day 12: UzbekEnergo approval letter received; Fragnet FRAG-PFR-003 retired; 33/220kV GSS CP float restored to 0d; PO-HEL-EQ-001 awarded to POWERTRANS linking to HEL-PRO-SS-MPT-2010 at Day 6 of 182 supported by rapid Code 1 drawing clearance; 220kV GIS excavation initiated on schedule) |

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
- **Day 9 Performance Validation (2026-10-14):**
  - Activity `HEL-CIV-PV-PLG-0105` (Blocks 1–5 Alluvial Piling) achieved **100% completion (12,840 / 12,840 piles)**.
  - Milestone M4 closed out **+4 days ahead of baseline schedule**, fully preserving **+45 calendar days** total float to Mechanical Completion.
  - Tracker table installation (`HEL-MEC-PV-TRK-0100`) accelerated to **35 tables/day** (surpassing 30 tables/day baseline target; cumulative 60 tables). Net impact on Project COD remains **0 days**.
- **Day 10 Performance Validation (2026-10-15):**
  - Formal handover of Block 2 following civil QC signoff triggers concurrent activity `HEL-MEC-PV-TRK-0200` (Block 2 Tracker Structure Assembly), running in parallel with `HEL-MEC-PV-TRK-0100` (Block 1). Combined mechanical tracker installation run-rate projected to ramp to **60 tables/day**.
  - Second crawler DTH drill rig and 21-bar high-pressure compressor fully deployed and operational in Block 6 (`HEL-CIV-PV-PLG-0600` under `FRAG-EVT-001` / `FRAG-PRD-001`), doubling drilling production to 80 holes/day and accelerating remaining recovery duration by **50%**.
  - Total float on PV field works remains intact at **+45 calendar days**; net impact on Project COD remains **0 days**.
- **Day 11 Performance Validation (2026-10-16):**
  - Dual crawler DTH hammer drill rigs reached planned full production of **80 holes/day** (cumulative 305 holes pre-drilled in Block 6).
  - Parallel tracker assembly across Blocks 1 & 2 hit planned target run-rate of **60 tables/day** (cumulative 175 tables).
  - Total float preserved at **+45 calendar days**; COD impact remains **0 days**.
- **Day 12 Performance Validation (2026-10-17):**
  - Dual DTH rigs drilled **80 holes today** (cumulative 385 / 2,560 holes, 15.04%). Ramming teams installed 80 piles in rock sockets (cumulative 270 in Block 6; overall project piling at 13,110 / 15,400 piles, 85.13%).
  - Parallel tracker table assembly accelerated to **65 tables/day** across Gang A (Block 1: 40 tables) and Gang B (Block 2: 25 tables), reaching cumulative 240 tables (4.71%).
  - Total float on PV field works fully intact at **+45 calendar days**; net Project COD impact = **0 days**.
- **Day 13 Performance Validation (2026-10-18):**
  - Dual crawler DTH rigs drilled **80 holes today** (cumulative 465 / 2,560 holes, 18.16%). 80 piles driven into pre-drilled sockets (cumulative 350 in Block 6; overall project piling at 13,190 / 15,400 piles, 85.65%).
  - Parallel tracker assembly across Blocks 1 & 2 hit **70 tables/day** (cumulative 310 tables).
  - PV field total float preserved at **+45 calendar days**; net COD impact remains **0 days**.
- **Day 14 Performance Validation (2026-10-19 / Week 2 Close):**
  - Pilot Test Pile Dynamic Load Campaign: 20 test piles driven into pre-drilled rock sockets and 100% passed High-Strain Dynamic Load Testing (PDA/CAPWAP per ASTM D4945; axial capacity 125 kN vs 75 kN design, FS = 1.66; uplift 52 kN; lateral deflection 4.2 mm). Formal clearance granted under `FDC-CIV-001` for mass pile driving into pre-drilled sockets.
  - Dual DTH rigs drilled **80 holes** (cumulative 545 / 2,560 holes, 21.29%). Overall project piling reached **13,210 / 15,400 piles (85.78%)**.
  - Tracker assembly across Blocks 1 & 2 reached peak run-rate of **80 tables/day** (cumulative 390 tables). Total float remains **+45 calendar days**; net COD impact = **0 days**.
- **Day 15 Performance Validation (2026-10-20 / Week 3 Kickoff):**
  - Formal execution of Handover Certificate `HC-CIV-MEC-003` (RAMPART to EREKTOR) triggers activity `HEL-MEC-PV-TRK-0300` (Block 3 Tracker Assembly) running concurrently with Blocks 1 and 2.
  - Tri-front tracker assembly run-rate surges to **95 tables/day** (cumulative 485 tables project-wide). Total float on PV field works firmly preserved at **+45 calendar days**.
  - Block 6 Geotechnical Mass Driving: 80 piles driven/day into pre-drilled sockets under `FDC-CIV-001`, bringing cumulative Block 6 rock-socket piles to **450** and project-wide piling to **13,290 / 15,400 piles (86.30%)**. Progress strictly aligns with recovery fragnet `FRAG-PRD-001` schedule duration.
  - Master critical path: MPT manufacturing activity `HEL-PRO-SS-MPT-2010` (Day 3 of 182) progressing on schedule with POWERTRANS; Critical path total float = **0 calendar days**; Project COD locked at **Month 18**.
- **Day 16 Performance Validation (2026-10-21 / Week 3 Day 2):**
  - Substation Civil Superstructure: Control Room superstructure structural concrete (`HEL-CIV-SS-CR-2020`) 100% completed (+14 calendar days float). Successful pour secures predecessor milestone for indoor electrical cable tray and switchgear room preparation (`HEL-ELE-SS-SWG-3010`).
  - PV Field Tracker Assembly: Triple gangs (Gangs A, B, and C across Blocks 1, 2, and 3) achieved record installation run-rate of **100 tables/day**, reaching cumulative **585 / 5,100 tables** project-wide (**+175 tables ahead of baseline pace**). Total float on PV field works firmly preserved at **+45 calendar days** to Mechanical Completion (Month 15).
  - Block 6 Geotechnical Mass Driving: Maintained sustained production velocity of **80 piles/day** driven into pre-drilled rock sockets under `FDC-CIV-001` / `FRAG-PRD-001`, bringing cumulative Block 6 rock-socket piles to **530** and project-wide piling to **13,370 / 15,400 piles (86.82%)**. Progress strictly aligns with recovery fragnet `FRAG-PRD-001` schedule duration.
  - Master Critical Path: MPT manufacturing activity `HEL-PRO-SS-MPT-2010` (100MVA 220/33kV MPT Manufacturing & FAT) tracks at **Day 4 of 182** on schedule with POWERTRANS under `PO-HEL-EQ-001`. Critical path total float = **0 calendar days**; Project COD locked at **Month 18**.
  - Net Project COD impact remains **0 days**.
- **Day 17 Performance Validation (2026-10-22 / Week 3 Day 3):**
  - Substation Civil & MEP Fitout: Control Room interior partition masonry and embedded electrical conduit installations commenced; 100MVA MPT foundation plinth formwork cleanly stripped, wet burlap curing ongoing.
  - PV Field Tracker Assembly: Maintained 100 tables/day run-rate across Blocks 1, 2, and 3, reaching cumulative 685 / 5,100 tables (13.43%). Total float preserved at **+45 calendar days**.
  - Block 6 Geotechnical Mass Driving: 80 piles/day driven into pre-drilled rock sockets (cumulative 610 rock-socket piles; cumulative project piling at 13,450 / 15,400 piles [87.34%]). Dual DTH pre-drilling advanced to 785 holes (30.66%) maintaining 175-hole lead buffer.
  - Master Critical Path: MPT manufacturing `HEL-PRO-SS-MPT-2010` tracks at Day 5 of 182 on schedule. Critical path total float = **0 calendar days**.
- **Day 18 Performance Validation (2026-10-23 / Week 3 Day 4):**
  - 33/220kV GSS Substation: 220kV GIS building excavation activity initiated on schedule (`HEL-CIV-SS-GIS-2030`). 100MVA MPT manufacturing activity `HEL-PRO-SS-MPT-2010` (Day 6 of 182) supported by rapid Code 1 drawing clearance (core/coil assembly & GA drawings approved without comments by ARCHON/PATRON). Master critical path total float = **0 calendar days**; Project COD locked at **Month 18**.
  - PV Field Tracker Assembly: Sustained steady 100 tables/day run-rate, bringing project cumulative tracker assembly to **785 / 5,100 tables** (**+195 tables ahead of baseline pace**). Total float firmly preserved at **+45 calendar days**. Parallel activation of Activity `HEL-MEC-PV-TRK-0400` (Block 4) modeled in P6 for Day 19 following planned execution of Handover Certificate `HC-CIV-MEC-004`.
  - Block 6 Geotechnical Recovery: 80 piles/day mass driving strictly tracking `FRAG-PRD-001` / `FDC-CIV-001`, bringing cumulative Block 6 rock-socket piles to **690 / 2,560** and total project piling to **13,530 / 15,400 piles (87.86%)**. Piling completion tracks Day 40 forecast (+5 days ahead of recovery target; +42 calendar days float).
  - Net Project COD impact remains **0 days**.
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
  - Today: Day 12, Month 1
  - Site Mobilization (`HEL.20`): Month 2
  - Engineering Freeze Milestone: Month 3
  - First Energization (Back-feed from NEGU): Month 16
  - Grid Synchronization / COD (`HEL.10`): Month 18
  - Total Float on Substation Path: **0 calendar days (True Master Critical Path, Fully Restored)**.
- **CPM Float Status & Critical Path Impact:**
  - The 33/220kV GSS electrical engineering path dictates the project completion date.
  - Following receipt of UzbekEnergo approval on Day 12, Total Float on the 33/220kV GSS critical path is restored to **0 calendar days** with zero net delay to Project COD.
  - Status: **CLOSED / MITIGATED (Net Delay: 0 Days)**.
- **Fragnet Structure (`FRAG-EVT-002`):**
  1. `FRAG-PFR-001`: Joint Protection & Automation Technical Feasibility Review (VOLTA / CIPHER) — Completed Day 5.
  2. `FRAG-PFR-002`: Protection Philosophy Revision `HEL-PR-PHL-0200 Rev 1` & SLD `HEL-HV-SLD-0101` Update (ARCHON / CIPHER) — Completed Day 6. Software/PPC droop logic route confirmed (no CT/PT hardware resizing needed).
  3. `FRAG-PFR-003`: Formal Submission to UzbekEnergo / NEGU and Contractual Review (ARCHON / GRIDMASTER) — **CLOSED / RETIRED (Day 12)**: Receipt of UzbekEnergo approval letter on Day 12 formally retires Fragnet `FRAG-PFR-003`.
  4. `FRAG-PFR-004`: Downstream Logic Linkage & P6 Master Schedule Realignment (KRONOS) — **EXECUTED (Day 12)**: PO-HEL-EQ-001 award links directly into manufacturing activity `HEL-PRO-SS-MPT-2010` (duration 182 calendar days / 26 weeks).
- **Mitigation & Recovery Actions:**
  - PO releases for 220kV CT/PT cleared from hardware modification risk; PPC software configuration baseline confirmed.
  - PO-HEL-EQ-001 awarded to POWERTRANS on Day 12 for $850,000 DDP site on schedule, meeting the Drop Dead Date and locking the factory manufacturing queue.
  - Total Float on the 33/220kV GSS critical path restored to 0 calendar days with zero net delay to Project COD.
- **Contractual & Commercial Actions & Formal Closeout:**
  - Closure Trigger: Receipt of UzbekEnergo approval letter on Day 12 endorsing PPC firmware compliance (`TRN-EPC-CLI-0012`).
  - Log Status: **CLOSED / MITIGATED (Net Delay: 0 Days)**.
  - Notice Served: Formal FIDIC Sub-Clause 13.7 / 13.1 / 20.1 Notice of Claim `HELIOS-NTC-002` drafted/issued by COUNSEL on 2026-10-06 (Claim Ref `CLM-002`).
  - Commercial Resolution: Engineering rework completed within budgeted overhead with no contractor cost claim; cost code `CC-VAR-EVT-002` closed; Claim `CLM-002` / Notice `HELIOS-NTC-002` closed as fully resolved with zero EOT and zero cost impact.
