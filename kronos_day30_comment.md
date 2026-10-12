**[KRONOS]** — Planning Manager | Project Controls

### Master Schedule & CPM Critical Path Progress Review — Day 030 (Month 2 / Week 5 Day 2)
**TO:** ATLAS (Project Manager) | Danesh (Project Director)  
**CC:** RAMPART (Construction Manager), BASTION (Civil Lead), FORTRESS (Substation Civil Lead), STRATUM (MMS/Tracker Lead), SWITCHMAN (Substation E&M Lead), CONVOY (SCM Lead), ARCHON (Engineering Lead), VOLTA (Electrical Lead), ELECTRA (Electrical Construction Lead), CIPHER (Controls/SCADA), COUNSEL (Contracts Lead), SIGMA (MIS Lead), LEDGER (Cost Control Lead), VECTOR (Civil Planning), WATT (Electrical Planning)  
**DATE:** Day 030 (Month 2 / Week 5 Day 2) | Data Date: 2026-10-31  
**PROJECT:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**CONTRACT:** FIDIC Yellow Book 1999  

---

#### 1. Executive Summary & Day 30 CPM Master Schedule Review

The Day 030 Primavera P6 CPM master schedule network recalculation confirms sustained physical momentum across all active civil, structural, mechanical, and electrical work packages. Earned Value Management (EVM) indices for Day 030 remain firmly favorable at **SPI = 1.14** (+14% ahead of baseline schedule plan) and **CPI = 1.02** (+2% under baseline budget envelope).

Key operational milestones achieved on Day 030:
1. **Substation Civil & Structural Milestone (`HEL-CIV-SS-GIS-2060`):** Activity `HEL-CIV-SS-GIS-2060` (220kV GIS Building Superstructure Steel Erection) has officially initiated in Primavera P6 holding **+12 calendar days float**. The monolithic foundation raft passed its 7-day concrete compressive strength milestone (>70% design strength achieved per C30/37 laboratory cylinder break tests). Heavy crane spreads, spreader bars, and rigging crews commenced structural column positioning and anchor bolt alignment.
2. **PV Field Module Mounting Acceleration (`HEL-ELC-PV-MOD-0100`):** Electrical Subcontractor ELECTRA accelerated installation to **1,500 modules/day**, bringing cumulative module mounting to **2,700 modules (1.57 MWp)** across released Block 1 tracker tables. The activity is progressing **+35 calendar days ahead of baseline schedule**. 100% torque clamp verification (8–10 N·m) and pre-string insulation resistance megger testing (>1000 MΩ at 1,500V DC) confirmed zero defects.
3. **PV Field Tracker Assembly Velocity (`HEL-MEC-PV-TRK-0100/0200/0300/0400`):** EREKTOR sustained quad-gang assembly velocity at **120 tables/day** across Gangs A, B, C, and D in Blocks 1, 2, 3, and 4. Cumulative tracker table assembly reached **2,220 / 5,100 tables (43.53% completion)** against the 1,320-table baseline plan, establishing a net positive variance of **+900 tables (+68.2% ahead of baseline pace)**. Total float on the PV mechanical installation path to Mechanical Completion (Month 15) remains firmly locked at **+45 calendar days**.
4. **Block 6 Geotechnical Recovery Final Lap (`FRAG-PRD-001` / `EVT-001` / `FDC-CIV-001`):** Mass pile driving strictly tracked recovery fragnet `FRAG-PRD-001` at **80 piles/day**, advancing cumulative rock-socket piles to **1,650 / 2,560 piles (64.45%)**. Dual crawler DTH hammer pre-drilling reached **1,825 / 2,560 holes (71.29%)**, sustaining an unhindered **175-socket advance buffer**. Total project piling reached **14,490 / 15,400 piles (94.09%)**, leaving **only 910 piles remaining across the entire 100MW solar park footprint**. Final substructure completion forecast is firmly locked at **Day 040 (+42 calendar days float)**.
5. **33/220kV GSS Substation Critical Path (`HEL-PRO-SS-MPT-2010`):** Main Power Transformer manufacturing activity `HEL-PRO-SS-MPT-2010` advanced to **Day 18 of 182 calendar days** strictly on schedule at POWERTRANS works under PO-HEL-EQ-001. Critical path total float holds at **0 calendar days**, with Commercial Operation Date (COD) firmly locked at **Month 18**.

---

#### 2. Earned Value Management (EVM) Dashboard (Data Date: Day 030)

| Metric | Baseline Target (PV) | Earned Value (EV) | Actual Cost (AC) | Index / Variance | Schedule Status | Cost Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Project Master EVM** | BCWS | BCWP | ACWP | **SPI = 1.14** / **CPI = 1.02** | **AHEAD OF SCHEDULE** (+14%) | **UNDER BUDGET** (+2%) |
| *PV Field Civil (Piling)* | 87.5% Scope | 94.09% Scope (14,490 / 15,400) | Reconciled | SPI = 1.08 | Ahead of Plan (Blocks 1–5 100%; Block 6 at 64.45%) | On Budget (`FDC-CIV-001` / `CC-VAR-EVT-001`) |
| *PV Field Mechanical (Trackers)* | 25.88% (1,320 tbl) | 43.53% (2,220 tbl) | Reconciled | SPI = 1.68 | Ahead of Plan (+900 tables / +68.2%) | On Budget (Quad-gang cadence: 120 tbl/d) |
| *PV Field Electrical (Modules)* | Month 2 Baseline | 2,700 Modules (1.57 MWp) | Reconciled | SPI = 1.25 | Fast-Track Activated (+35d ahead of baseline) | On Budget (`HC-MEC-ELC-001` / ELECTRA) |
| *Substation Civil & Structural* | Foundation Cure | Superstructure Steel Initiated | Reconciled | SPI = 1.15 | Ahead of Plan (+12 calendar days float) | On Budget (`HEL-CIV-SS-GIS-2060`) |
| *Substation Electrical (MPT)* | Day 18 / 182d | Day 18 / 182d | Reconciled | SPI = 1.00 | On Track (Critical Path, 0d float) | On Budget (POWERTRANS PO-HEL-EQ-001) |

---

#### 3. Master Critical Path & Workfront CPM Float Register

Primavera P6 CPM network time analysis confirms that the primary critical path remains exclusively governed by the 33/220kV Grid Substation MPT procurement, logistics, installation, and energization sequence:

```
[Day 12: PO-HEL-EQ-001 Awarded] 
   └──> [HEL-PRO-SS-MPT-2010: 100MVA MPT Mfg & FAT (Day 18 of 182d)] (FS, Float = 0d) ◄── [CRITICAL PATH]
          └──> [HEL-LOG-SS-MPT-3010: Khorgos Heavy Haul Logistics (45d)] (FS, Float = 0d)
                 └──> [HEL-CON-SS-MPT-4010: Plinth Setting & Erection (14d)] (FS, Float = 0d)
                        └──> [HEL-TC-SS-COM-5010: GSS Pre-Comm & SAT (21d)] (FS, Float = 0d)
                               └──> [Milestone M16: First Energization] ──> [Month 18 COD] (Float = 0d)
```

##### Parallel & Near-Critical Workfront Float Register:
| Path / Workfront | Driving Activity | Baseline Target | Current Forecast | Total Float | Status / Variance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GSS Transformer (Primary Critical Path)** | `HEL-PRO-SS-MPT-2010` (Day 18/182) | Month 18 COD | Month 18 COD | **0 calendar days** | **ON TRACK (Critical Path)**; core assembly complete, winding active at POWERTRANS works |
| **GSS 220kV GIS Superstructure** | `HEL-CIV-SS-GIS-2060` Steel Erection | Month 6 Handover | Month 6 Handover | **+12 calendar days** | **INITIATED TODAY**; 7-day raft strength passed; crane rigging & column alignment active |
| **GSS Control Room** | `HEL-CIV-SS-CR-2020` Interior / MEP | Month 6 Handover | Month 6 Handover | **+13 calendar days** | HVAC ducting ongoing; electrical panel room prepped for switchgear and cable trays |
| **PV Field Tracker Assembly** | `HEL-MEC-PV-TRK-0100/0200/0300/0400` | Month 15 MC | Month 13 Forecast | **+45 calendar days** | Quad-gang 120 tbl/d sustained; cumulative 2,220 tbl (+900 tables / +68.2% ahead of baseline) |
| **PV Field Module Installation Block 1** | `HEL-ELC-PV-MOD-0100` | Month 2 Target | Day 028 (Actual) | **+35 calendar days** | 1,500 modules/day; cumulative 2,700 modules (1.57 MWp); 100% torque and megger sign-off |
| **Block 6 Rock Piling (EVT-001)** | `HEL-CIV-PV-PLG-0600` (`FRAG-PRD-001`) | Day 045 Target | Day 040 Forecast | **+42 calendar days** | 80 piles/day mass driving; 1,650 socket piles (64.45%); 1,825 holes (71.29%); only 910 piles remain |
| **PV Module Supply & Logistics** | `HEL-PRO-PV-MOD-1010` (86.4k modules) | Month 6 First Lay | Month 6 First Lay | **+28 calendar days** | Staged line-haul deliveries feeding accelerated Block 1 installation buffer |

---

#### 4. Project Key Milestone Tracking Register

| Milestone ID | Milestone Description | Baseline Target | Forecast / Actual Date | Total Float | Status / Variance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | Contract Effective Date / LNTP | Day 001 | Day 001 (Actual) | 0d | **ACHIEVED** |
| **M4** | Alluvial Piling Complete (Blocks 1–5) | Day 013 | Day 009 (Actual) | +45d | **ACHIEVED (+4d Ahead of Baseline)** |
| **M5a** | Tracker Erection Commencement (Block 1) | Day 035 | Day 008 (Actual) | +45d | **ACHIEVED (+27d Ahead of Baseline)** |
| **M5b** | Tracker Erection Commencement (Block 2) | Day 045 | Day 010 (Actual) | +45d | **ACHIEVED (+35d Ahead of Baseline)** |
| **M5c** | Tracker Erection Commencement (Block 3) | Day 055 | Day 015 (Actual) | +45d | **ACHIEVED (`HC-CIV-MEC-003` Executed)** |
| **M5d** | Tracker Erection Commencement (Block 4) | Day 065 | Day 019 (Actual) | +45d | **ACHIEVED (`HC-CIV-MEC-004` Executed; +46d Ahead of Baseline)** |
| **M6** | Block 6 Rock Piling Complete | Day 045 | Day 040 (Forecast) | +42d | **ON TRACK (+5d Ahead of Recovery Plan; 94.09% Total Piling; 910 Piles Remaining)** |
| **M7** | 220kV MPT PO Release (Drop Dead Date) | Day 012/013 | Day 012 (Actual) | 0d (Crit.) | **ACHIEVED / PO AWARDED** |
| **M8** | 220kV Substation Civil Handover | Day 180 (Month 6) | Day 180 (Forecast) | 0d (Crit.) | GIS steel erection initiated (`HEL-CIV-SS-GIS-2060`) holding +12d float |
| **M9 (Early)** | Block 1 Mech-to-Elec Handover (`HC-MEC-ELC-001`) | Month 2 | Day 028 (Actual) | +35d | **ACHIEVED (`HEL-ELC-PV-MOD-0100` Active; 2,700 Modules Mounted)** |
| **COD** | Commercial Operation Date / PAC | Month 18 | Month 18 (Target) | **0d Net** | **ON TRACK (Critical Path Float = 0d)** |

---

#### 5. Delay Event Log (DEL) Status Summary

| Event ID | Event Ref | Event Description | Responsible Party | Affected Path | Float Impact | Net COD Delay | Status / Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEL-001** | EVT-001 | Block 6 Rock Refusal at 0.8m | Employer (FIDIC 4.12) | `HEL.60` PV Field Piling (Block 6) | +42d path float | **0 days** | **ACTIVE / MITIGATION ACCELERATED** (Day 30 Review: Block 6 rock-socket piling at 1,650 / 2,560 piles [64.45%]; DTH pre-drilling at 1,825 / 2,560 holes [71.29%]; 175-socket advance buffer maintained; Total project piling at 14,490 / 15,400 piles [94.09%]; only 910 piles remaining; Quad-gang tracker assembly at 2,220 / 5,100 tables [43.53%, +900 tables / +68.2% ahead of baseline]; Day 40 finish locked; +42d float preserved) |
| **DEL-002** | EVT-002 | UzbekEnergo PFR Grid Code Revision | Employer / Utility (FIDIC 13.7) | `HEL.30` Eng / `HEL.70` GSS | 0d float restored | **0 days** | **CLOSED (Day 12)** (Approved by UzbekEnergo; `FRAG-PFR-003` retired; PO awarded; MPT manufacturing at Day 18 of 182; 220kV GIS superstructure steel erection initiated [`HEL-CIV-SS-GIS-2060`] holding +12d float) |

---

#### 6. Look-Ahead Planning Directives & Execution Instructions

1. **Substation Civil & Superstructure Steel Erection (GRIDCON / FORTRESS / SWITCHMAN / AEGIS):**
   - Execute column erection and horizontal tie-beam placement for Activity **`HEL-CIV-SS-GIS-2060`** (220kV GIS Building Superstructure Steel Erection).
   - Enforce strict rigging safety zones and overhead crane lift permits under AEGIS supervision; ensure 100% torque auditing and plumbness survey checks on column baseplates.
   - Maintain MEP HVAC and cable tray progress inside the Control Room building (`HEL-CIV-SS-CR-2020`).
2. **PV Module Mounting & String Cabling (RAMPART / ELECTRA / CONDUIT / SENTINEL):**
   - Sustain module mounting velocity at **1,500 modules/day** along Block 1 string tables under Activity **`HEL-ELC-PV-MOD-0100`**.
   - Enforce 100% torque audits (8–10 N·m) with calibrated digital wrenches and witness marking. Ensure MC4-EVO2 harness clips maintain bend radius without frame pinch.
   - Prepare mechanical-to-electrical joint inspection protocol (`HC-MEC-ELC-002`) for Block 2 handover as tracker assembly reaches completion.
3. **PV Field Quad-Gang Tracker Assembly (RAMPART / STRATUM / EREKTOR):**
   - Maintain sustained quad-gang velocity of **120 tables/day** across Gangs A, B, C, and D in Blocks 1, 2, 3, and 4.
   - Target crossing the 2,500-table milestone (49.02% of total plant scope) by Day 033, expanding net float beyond +45 calendar days.
   - Maintain 100% torque audit sign-off (240–260 N·m) on all driveline joints, slewing drives, and purlin fasteners.
4. **Block 6 Geotechnical Mass Driving Final Run-Down (BASTION / PLUMBLINE / GROUNDWORK):**
   - Maintain production under `FRAG-PRD-001` at **80 piles/day** socket driving and **80 holes/day** DTH pre-drilling.
   - Maintain dual crawler DTH pre-drilling advance buffer at $\ge 175$ sockets ahead of hydraulic driving rigs.
   - Lock substructure completion: with only 910 piles remaining project-wide, 100% foundation completion will be achieved on **Day 040 (+42 calendar days float preserved)**.
5. **Main Power Transformer Manufacturing Expediting (CONVOY / ARCHON / TRACER):**
   - Monitor POWERTRANS manufacturing progress as Activity `HEL-PRO-SS-MPT-2010` advances through Day 18 of 182; review coil winding inspection logs and tank fabrication milestones.
   - Verify Khorgos border customs clearance readiness and logistics route permits.
6. **Project Controls & EVM Governance (SIGMA / LEDGER / KRONOS):**
   - Maintain daily EVM monitoring (**SPI = 1.14**, **CPI = 1.02**) and ensure full reconciliation with DPR Day 030.
   - Progress is earned strictly upon QC acceptance under the Rule of Credit.

**KRONOS**  
*Planning Manager — HELIOS EPC Project (100MW Solar PV + 33/220kV GSS)*  
*Discipline: Project Planning & Controls*
