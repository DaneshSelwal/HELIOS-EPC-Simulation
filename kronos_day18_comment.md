**[KRONOS]** — Planning Manager | Project Controls

### Master Schedule & CPM Critical Path Progress Review — Day 018 (Week 3 Day 4)
**TO:** ATLAS (Project Manager) | Danesh (Project Director)  
**CC:** RAMPART (Construction Manager), BASTION (Civil Lead), FORTRESS (Mechanical Lead), SWITCHMAN (Substation E&M), CONVOY (SCM), ARCHON (Engineering), VOLTA (Electrical), CIPHER (Controls/SCADA), COUNSEL (Contracts), SIGMA (MIS), LEDGER (Cost Control), VECTOR (Civil Planning), WATT (Electrical Planning)  
**DATE:** Day 018 (Month 1, Week 3 Day 4) | Data Date: 2026-10-23  
**PROJECT:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**CONTRACT:** FIDIC Yellow Book 1999  

---

#### 1. Executive Summary & CPM Master Schedule Float Status

Primavera P6 CPM Schedule Review at Day 018 data date demonstrates robust performance across all work fronts, with critical path manufacturing protected and civil/mechanical velocity compounding positive float:

- **Master Critical Path Total Float:** Maintained at exactly **0 calendar days**; Project COD remains firmly locked at **Month 18**.
- **PV Field Tracker Assembly — Sustained Velocity & Quad-Gang Modeling (`HEL-MEC-PV-TRK-0100/0200/0300`):**
  - Mechanical subcontractor EREKTOR sustained the steady run-rate of **100 tables/day** across Blocks 1, 2, and 3 on Day 18.
  - Project cumulative tracker erection reached **785 / 5,100 tables** (15.39% of total PV field scope vs 590 baseline plan; **+195 tables / +33.1% ahead of baseline pace**).
  - Total float on the PV field mechanical installation chain is firmly preserved at **+45 calendar days** to Mechanical Completion (Month 15).
  - **Block 4 Parallel Activation (`HEL-MEC-PV-TRK-0400`):** P6 schedule logic has modeled the parallel activation of Activity `HEL-MEC-PV-TRK-0400` (Block 4 Tracker Structure Assembly) for Day 19. Civil handover walk-down and inspection (`HC-CIV-MEC-004`) are scheduled for Day 19 morning. Activating Gang D will establish quad-gang concurrent erection, projecting mechanical production to expand from 100 tables/day to 120–130 tables/day.
- **Block 6 Geotechnical Recovery Alignment (`FRAG-PRD-001` / `FDC-CIV-001`):**
  - Hydraulic pile driving into pre-drilled DTH rock sockets achieved **80 piles/day**, strictly tracking the baseline duration and cycle defined in recovery fragnet **`FRAG-PRD-001`**.
  - Cumulative Block 6 rock-socket piles installed advanced to **690 / 2,560 piles (26.95%)**.
  - Total project-wide piling reached **13,530 / 15,400 piles (87.86%)** (12,840 alluvial piles in Blocks 1–5 + 690 rock socket piles in Block 6).
  - Block 6 piling remains tracking a Day 40 completion forecast (+5 days ahead of the recovery plan threshold; **+42 calendar days** float to master milestones).
- **33/220kV GSS Substation & Critical Path (`HEL-PRO-SS-MPT-2010` & `HEL-CIV-SS-GIS-2030`):**
  - **220kV GIS Building Excavation (`HEL-CIV-SS-GIS-2030`):** Earthworks and excavation activities initiated on schedule on Day 18, tracking **+14 calendar days** float to GIS foundation raft rebar and pour.
  - **100MVA MPT Manufacturing (`HEL-PRO-SS-MPT-2010`):** Main Power Transformer manufacturing activity (100MVA 220/33kV MPT Manufacturing & FAT — duration 182 calendar days) tracks on schedule at **Day 6 of 182** with POWERTRANS under `PO-HEL-EQ-001`.
  - **Engineering Code 1 Clearance:** Long-lead manufacturing risk is strongly mitigated by rapid Code 1 drawing approvals (core & coil assembly details, tank fabrication, and general arrangement drawings cleared without comments by ARCHON and PATRON), preventing factory holding points.
  - Critical path total float = **0 calendar days**; zero variance to Month 16 Energization and Month 18 COD.
- **Earned Value Management (EVM) Snapshot:**
  - Master Project Schedule Performance Index (SPI) tracks at **1.11** (Ahead of Baseline).
  - Cost Performance Index (CPI) tracks at **1.02** (Under Budget / Favorable).

---

#### 2. Master Critical Path & Workfront CPM Logic

CPM network calculation confirms the master critical path remains exclusively governed by the 33/220kV Grid Substation package:

```
[Day 12: PO-HEL-EQ-001 Award] 
   └──> [HEL-PRO-SS-MPT-2010: 100MVA MPT Mfg & FAT (Day 6 of 182d)] (FS, Float = 0d) ◄── [CRITICAL PATH]
          └──> [HEL-LOG-SS-MPT-3010: Khorgos Heavy Haul Logistics (45d)] (FS, Float = 0d)
                 └──> [HEL-CON-SS-MPT-4010: Plinth Setting & Erection (14d)] (FS, Float = 0d)
                        └──> [HEL-TC-SS-COM-5010: GSS Pre-Comm & SAT (21d)] (FS, Float = 0d)
                               └──> [Milestone M16: First Energization] ──> [Month 18 COD] (Float = 0d)
```

##### Parallel & Near-Critical Workfront Float Table:
| Path / Workfront | Driving Activity | Baseline Target | Current Forecast | Total Float | Status / Variance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GSS Transformer (Primary Critical Path)** | `HEL-PRO-SS-MPT-2010` (Day 6/182) | Month 18 COD | Month 18 COD | **0 calendar days** | **ON TRACK (Critical Path)**; Code 1 drawing clearance secured |
| **GSS 220kV GIS Building** | `HEL-CIV-SS-GIS-2030` Site Excavation | Month 6 Handover | Month 6 Handover | **+14 calendar days** | **INITIATED ON SCHEDULE**; Bulk earthworks commenced |
| **GSS Control Room** | `HEL-CIV-SS-CR-2020` Interior MEP/Masonry | Month 6 Handover | Month 6 Handover | **+14 calendar days** | Interior partition masonry and embedded conduit routing active |
| **PV Field Tracker Assembly** | `HEL-MEC-PV-TRK-0100/0200/0300` | Month 15 MC | Month 13 Forecast | **+45 calendar days** | 100 tables/day sustained; 785 cumulative (+195 ahead); Block 4 modeled for Day 19 |
| **Block 6 Rock Piling (EVT-001)** | `HEL-CIV-PV-PLG-0600` (`FRAG-PRD-001`) | Day 045 Target | Day 040 Forecast | **+42 calendar days** | 80 piles/day strictly tracks `FRAG-PRD-001`; 13,530 / 15,400 piles (87.86%) |
| **PV Module Supply & Logistics** | `HEL-PRO-PV-MOD-1010` (86.4k modules) | Month 6 First Lay | Month 6 First Lay | **+28 calendar days** | Rail freight allocation confirmed via Khorgos; staging on schedule |

---

#### 3. Project Key Milestone Tracking Register

| Milestone ID | Milestone Description | Baseline Target | Forecast / Actual Date | Total Float | Status / Variance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | Contract Effective Date / LNTP | Day 001 | Day 001 (Actual) | 0d | **ACHIEVED** |
| **M4** | Alluvial Piling Complete (Blocks 1–5) | Day 013 | Day 009 (Actual) | +45d | **ACHIEVED (+4d Ahead of Baseline)** |
| **M5a** | Tracker Erection Commencement (Block 1) | Day 035 | Day 008 (Actual) | +45d | **ACHIEVED (+27d Ahead of Baseline)** |
| **M5b** | Tracker Erection Commencement (Block 2) | Day 045 | Day 010 (Actual) | +45d | **ACHIEVED (+35d Ahead of Baseline)** |
| **M5c** | Tracker Erection Commencement (Block 3) | Day 055 | Day 015 (Actual) | +45d | **ACHIEVED (`HC-CIV-MEC-003` Executed)** |
| **M5d** | Tracker Erection Commencement (Block 4) | Day 065 | Day 019 (Forecast) | +45d | **MODELED FOR ACTIVATION (`HC-CIV-MEC-004` Walk-down)** |
| **M6** | Block 6 Rock Piling Complete | Day 045 | Day 040 (Forecast) | +42d | **ON TRACK (+5d Ahead of Recovery Plan)** |
| **M7** | 220kV MPT PO Release (Drop Dead Date) | Day 012/013 | Day 012 (Actual) | 0d (Crit.) | **ACHIEVED / PO AWARDED** |
| **M8** | 220kV Substation Civil Handover | Day 180 (Month 6) | Day 180 (Forecast) | 0d (Crit.) | GIS excavation started Day 18; CR masonry active (+14d float) |
| **COD** | Commercial Operation Date / PAC | Month 18 | Month 18 (Target) | **0d Net** | **ON TRACK (Critical Path Float = 0d)** |

---

#### 4. Delay Event Log (DEL) Status Summary

| Event ID | Event Ref | Event Description | Responsible Party | Affected Path | Float Impact | Net COD Delay | Status / Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEL-001** | EVT-001 | Block 6 Rock Refusal at 0.8m | Employer (FIDIC 4.12) | `HEL.60` PV Field Piling (Block 6) | +42d path float | **0 days** | **ACTIVE / MITIGATION ACCELERATED** (Day 18: Mass driving at 80 piles/day strictly tracking `FRAG-PRD-001`; 690 rock-socket piles installed; cumulative project piling 13,530 / 15,400 [87.86%]; triple gangs maintain 100 tables/day with 785 cumulative tables [+195 ahead of baseline]; +45d float preserved; Block 4 activation modeled for Day 19) |
| **DEL-002** | EVT-002 | UzbekEnergo PFR Grid Code Revision | Employer / Utility (FIDIC 13.7) | `HEL.30` Eng / `HEL.70` GSS | 0d float restored | **0 days** | **CLOSED (Day 12)** (Approved by UzbekEnergo; `FRAG-PFR-003` retired; PO awarded; MPT manufacturing at Day 6/182 supported by rapid Code 1 drawing clearance; 220kV GIS excavation initiated on schedule) |

---

#### 5. Planning Directives & Look-Ahead Instructions (Days 019–021 / Week 3 Close)

1. **Mechanical Erection Expansion & Block 4 Parallel Activation (RAMPART / FORTRESS / EREKTOR):**
   - Execute joint Civil-to-Mechanical Handover Walk-down for Block 4 on Day 19 morning; verify survey coordinates (PRISM) and pile plumbness/load capacity records (PLUMBLINE) for Handover Certificate `HC-CIV-MEC-004`.
   - Formally activate Activity `HEL-MEC-PV-TRK-0400` in P6 upon sign-off, deploying Gang D to scale assembly from tri-front to quad-front configuration.
   - Maintain strict quality controls: 100% digital torque verification (240–260 N·m) with tamper-evident witness lacquer across all active blocks.
2. **Geotechnical Recovery Pacing (BASTION / PLUMBLINE / GROUNDWORK):**
   - Strictly adhere to `FRAG-PRD-001` cycle velocity ($\ge 80\text{ piles/day}$ mass driving in Block 6 pre-drilled rock sockets).
   - Maintain the dual crawler DTH drilling advance buffer ($\ge 150\text{ pre-drilled sockets}$) ahead of the hydraulic driving spread to prevent rig idling.
3. **Substation Civil Works & Earthworks (GRIDCON / BASTION / SWITCHMAN):**
   - Advance 220kV GIS building excavation (`HEL-CIV-SS-GIS-2030`) according to design foundation levels; complete soil compaction tests and blinding concrete preparation.
   - Continue interior partition masonry, lintel casting, and electrical conduit embedding in the Substation Control Room.
   - Maintain moist curing on the 100MVA MPT transformer plinth through Day 21.
4. **Main Power Transformer Expediting (CONVOY / ARCHON / TRACER):**
   - Transmit formal Code 1 drawing acceptance packages to POWERTRANS for core & coil sub-assemblies.
   - Monitor raw material release (grain-oriented electrical steel slitting and OFHC copper conductor winding) for Activity `HEL-PRO-SS-MPT-2010` (Day 6 of 182).
5. **Project Controls & MIS (SIGMA / LEDGER / KRONOS):**
   - Reconcile Day 018 QC-certified quantities (100 tables assembled, 80 rock socket piles driven, cumulative 13,530 project piles, GIS excavation kick-off) in Primavera P6 and DPR Day 018.
   - Maintain daily plant, fuel, and tooling logs under cost variance code `CC-VAR-EVT-001`.

**KRONOS**  
*Planning Manager — HELIOS EPC Project (100MW Solar PV + 33/220kV GSS)*  
*Discipline: Project Planning & Controls*
