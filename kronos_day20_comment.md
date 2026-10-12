**[KRONOS]** — Planning Manager | Project Controls

### Master Schedule & CPM Critical Path Progress Review — Day 020 (Week 3 Day 6)
**TO:** ATLAS (Project Manager) | Danesh (Project Director)  
**CC:** RAMPART (Construction Manager), BASTION (Civil Lead), FORTRESS (Mechanical Lead), SWITCHMAN (Substation E&M), CONVOY (SCM), ARCHON (Engineering), VOLTA (Electrical), CIPHER (Controls/SCADA), COUNSEL (Contracts), SIGMA (MIS), LEDGER (Cost Control), VECTOR (Civil Planning), WATT (Electrical Planning)  
**DATE:** Day 020 (Month 1, Week 3 Day 6) | Data Date: 2026-10-25  
**PROJECT:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**CONTRACT:** FIDIC Yellow Book 1999  

---

#### 1. Executive Summary & CPM Master Schedule Float Status

Primavera P6 CPM Master Schedule Review at Day 020 data date demonstrates sustained acceleration across mechanical assembly, strict adherence to geotechnical recovery fragnets, and continuous float preservation across critical and near-critical packages:

- **Master Critical Path Total Float:** Firmly locked at exactly **0 calendar days**; Project Commercial Operation Date (COD) strictly anchored at **Month 18**.
- **PV Field Tracker Assembly — Quad-Gang Production Record (`HEL-MEC-PV-TRK-0100/0200/0300/0400`):**
  - **Quad-Gang Velocity Peak:** The quadripartite mechanical installation spread across Blocks 1, 2, 3, and 4 (Gangs A, B, C, and D) achieved a peak production velocity of **120 tables/day** on Day 20.
  - **Milestone Reached (20% Completion):** Project cumulative tracker table assembly crossed the 20% milestone, reaching **1,020 / 5,100 tables** (20.00% of total field scope vs 720 tables baseline plan; **+300 tables / +41.7% ahead of baseline pace**).
  - **Total Float:** Total float on the PV field tracker assembly and mechanical completion chain is firmly maintained at **+45 calendar days** to Mechanical Completion (Month 15).
  - **Quality Assurance:** 100% torque auditing (240–260 N·m) with tamper-evident paint striping strictly enforced and logged by TORQUE (Mech QC); zero torque non-conformances or driveline binding detected.
- **Block 6 Geotechnical Recovery Alignment (`FRAG-PRD-001` / `FDC-CIV-001`):**
  - **Sustained Driving Velocity:** Hydraulic piling rigs maintained steady mass production driving of **80 piles/day** into pre-drilled DTH rock sockets, strictly tracking the recovery baseline cycle in fragnet **`FRAG-PRD-001`**.
  - **Block 6 Cumulative Piles:** Cumulative rock-socket piles installed in Block 6 reached **850 / 2,560 piles (33.20%)**.
  - **Pre-Drilling Buffer:** Dual crawler DTH hammer drill rigs advanced pre-drilled rock sockets to **1,025 / 2,560 holes (40.04%)**, successfully maintaining a healthy buffer of **175 pre-drilled holes** ahead of driving operations.
  - **Project-Wide Piling Totals:** Total project piling reached **13,690 / 15,400 piles installed (88.90%)** (12,840 alluvial piles in Blocks 1–5 [100%] + 850 rock-socket piles in Block 6).
  - **Forecast & Float:** Block 6 piling completion forecast holds firmly at Day 40 (+5 days ahead of recovery threshold; **+42 calendar days** float to master project milestones).
- **33/220kV GSS Substation & Critical Path (`HEL-PRO-SS-MPT-2010` & `HEL-CIV-SS-GIS-2040`):**
  - **220kV GIS Raft Foundation Rebar Initiation (`HEL-CIV-SS-GIS-2040`):** Following successful placement of blinding concrete (`HEL-CIV-SS-GIS-2030`), Activity **`HEL-CIV-SS-GIS-2040`** (220kV GIS Building Raft Foundation Reinforcement & Formwork) commenced today on schedule, holding **+12 calendar days** float to GIS superstructure handover.
  - **100MVA MPT Manufacturing (`HEL-PRO-SS-MPT-2010`):** Activity `HEL-PRO-SS-MPT-2010` (100MVA 220/33kV MPT Manufacturing & FAT — duration 182 calendar days) advanced to **Day 8 of 182** at POWERTRANS works under `PO-HEL-EQ-001`. Core lamination stacking preparation and winding operations proceed strictly on schedule following Code 1 drawing clearance.
  - **Substation Control Room & Plinth (`HEL-CIV-SS-CR-2020`):** Control Room internal plastering, partition masonry curing, and wall chases for cable conduits progressing with **+13 calendar days** float. 100MVA MPT transformer plinth wet burlap curing cycle reaches Day 6 of 7 (plinth curing concludes Day 21).
  - **Critical Path Float:** Master critical path total float = **0 calendar days**; zero net variance to Month 16 Energization and Month 18 COD.
- **Earned Value Management (EVM) Snapshot:**
  - Schedule Performance Index (SPI) tracks at **1.14** (Favorable / Ahead of Baseline).
  - Cost Performance Index (CPI) tracks at **1.02** (Favorable / Under Budget).

---

#### 2. Master Critical Path & Workfront CPM Logic

CPM network calculation confirms the master critical path remains exclusively governed by the 33/220kV Grid Substation package:

```
[Day 12: PO-HEL-EQ-001 Award] 
   └──> [HEL-PRO-SS-MPT-2010: 100MVA MPT Mfg & FAT (Day 8 of 182d)] (FS, Float = 0d) ◄── [CRITICAL PATH]
          └──> [HEL-LOG-SS-MPT-3010: Khorgos Heavy Haul Logistics (45d)] (FS, Float = 0d)
                 └──> [HEL-CON-SS-MPT-4010: Plinth Setting & Erection (14d)] (FS, Float = 0d)
                        └──> [HEL-TC-SS-COM-5010: GSS Pre-Comm & SAT (21d)] (FS, Float = 0d)
                               └──> [Milestone M16: First Energization] ──> [Month 18 COD] (Float = 0d)
```

##### Parallel & Near-Critical Workfront Float Table:
| Path / Workfront | Driving Activity | Baseline Target | Current Forecast | Total Float | Status / Variance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GSS Transformer (Primary Critical Path)** | `HEL-PRO-SS-MPT-2010` (Day 8/182) | Month 18 COD | Month 18 COD | **0 calendar days** | **ON TRACK (Critical Path)**; core stacking prep & winding active at POWERTRANS |
| **GSS 220kV GIS Building** | `HEL-CIV-SS-GIS-2040` Raft Foundation Rebar | Month 6 Handover | Month 6 Handover | **+12 calendar days** | Raft foundation rebar fixing initiated; formwork fabrication underway |
| **GSS Control Room** | `HEL-CIV-SS-CR-2020` Interior Masonry/MEP | Month 6 Handover | Month 6 Handover | **+13 calendar days** | Partition plastering & conduit chases progressing; plinth curing reaches Day 6 of 7 |
| **PV Field Tracker Assembly** | `HEL-MEC-PV-TRK-0100/0200/0300/0400` | Month 15 MC | Month 13 Forecast | **+45 calendar days** | Quad-gang velocity reached 120 tables/day; 1,020 cumulative (+300 ahead of plan) |
| **Block 6 Rock Piling (EVT-001)** | `HEL-CIV-PV-PLG-0600` (`FRAG-PRD-001`) | Day 045 Target | Day 040 Forecast | **+42 calendar days** | 80 piles/day mass driving; 850 in Block 6; 1,025 pre-drilled holes; 13,690 / 15,400 project piles (88.90%) |
| **PV Module Supply & Logistics** | `HEL-PRO-PV-MOD-1010` (86.4k modules) | Month 6 First Lay | Month 6 First Lay | **+28 calendar days** | Tier-1 factory cell sorting active; freight booking via Khorgos locked |

---

#### 3. Project Key Milestone Tracking Register

| Milestone ID | Milestone Description | Baseline Target | Forecast / Actual Date | Total Float | Status / Variance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | Contract Effective Date / LNTP | Day 001 | Day 001 (Actual) | 0d | **ACHIEVED** |
| **M4** | Alluvial Piling Complete (Blocks 1–5) | Day 013 | Day 009 (Actual) | +45d | **ACHIEVED (+4d Ahead of Baseline)** |
| **M5a** | Tracker Erection Commencement (Block 1) | Day 035 | Day 008 (Actual) | +45d | **ACHIEVED (+27d Ahead of Baseline)** |
| **M5b** | Tracker Erection Commencement (Block 2) | Day 045 | Day 010 (Actual) | +45d | **ACHIEVED (+35d Ahead of Baseline)** |
| **M5c** | Tracker Erection Commencement (Block 3) | Day 055 | Day 015 (Actual) | +45d | **ACHIEVED (`HC-CIV-MEC-003` Executed)** |
| **M5d** | Tracker Erection Commencement (Block 4) | Day 065 | Day 019 (Actual) | +45d | **ACHIEVED (`HC-CIV-MEC-004` Executed; +46d Ahead of Baseline)** |
| **M6** | Block 6 Rock Piling Complete | Day 045 | Day 040 (Forecast) | +42d | **ON TRACK (+5d Ahead of Recovery Plan)** |
| **M7** | 220kV MPT PO Release (Drop Dead Date) | Day 012/013 | Day 012 (Actual) | 0d (Crit.) | **ACHIEVED / PO AWARDED** |
| **M8** | 220kV Substation Civil Handover | Day 180 (Month 6) | Day 180 (Forecast) | 0d (Crit.) | GIS raft rebar active (+12d float); CR MEP active (+13d float) |
| **COD** | Commercial Operation Date / PAC | Month 18 | Month 18 (Target) | **0d Net** | **ON TRACK (Critical Path Float = 0d)** |

---

#### 4. Delay Event Log (DEL) Status Summary

| Event ID | Event Ref | Event Description | Responsible Party | Affected Path | Float Impact | Net COD Delay | Status / Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEL-001** | EVT-001 | Block 6 Rock Refusal at 0.8m | Employer (FIDIC 4.12) | `HEL.60` PV Field Piling (Block 6) | +42d path float | **0 days** | **ACTIVE / MITIGATION ACCELERATED** (Day 20: Quad-gang tracker assembly reached 120 tables/day [cumulative 1,020 tables, 20.00% completion, +300 tables / +41.7% ahead of baseline pace]; Block 6 mass driving at 80 piles/day under `FRAG-PRD-001` [cumulative 850 rock-socket piles, 1,025 pre-drilled holes, 13,690/15,400 project piles, 88.90%]; +45d float preserved; Day 40 completion forecast holds) |
| **DEL-002** | EVT-002 | UzbekEnergo PFR Grid Code Revision | Employer / Utility (FIDIC 13.7) | `HEL.30` Eng / `HEL.70` GSS | 0d float restored | **0 days** | **CLOSED (Day 12)** (Approved by UzbekEnergo; `FRAG-PFR-003` retired; PO awarded; MPT manufacturing at Day 8/182; 220kV GIS building raft foundation rebar initiated on schedule [+12d float]) |

---

#### 5. Planning Directives & Look-Ahead Instructions (Days 021–023 / Week 4 Kickoff)

1. **Quad-Gang Mechanical Tracker Assembly (RAMPART / FORTRESS / EREKTOR):**
   - Maintain the surged quad-gang run-rate of $\ge 120\text{ tables/day}$ across Gangs A, B, C, and D in Blocks 1, 2, 3, and 4.
   - Maintain momentum toward Month 1 cumulative target of $>1,500\text{ tables}$.
   - Ensure 100% torque auditing (240–260 N·m) with tamper-evident torque seal applied and logged by TORQUE (Mech QC).
2. **Block 6 Geotechnical Mass Driving (BASTION / PLUMBLINE / GROUNDWORK):**
   - Continue strict alignment with `FRAG-PRD-001` production schedule ($\ge 80\text{ piles/day}$ socket driving).
   - Maintain the lead buffer of $\ge 150\text{ pre-drilled sockets}$ (currently 175 holes lead buffer) ahead of the hydraulic driving rigs using dual DTH crawler drills.
   - Target for Day 21: Reach 930 rock-socket piles in Block 6 (cumulative project piling to 13,770 / 15,400 piles [89.42%]).
3. **Substation Civil & Structural Progression (GRIDCON / BASTION / SWITCHMAN):**
   - Expedite 220kV GIS building raft foundation rebar fixing and formwork installation (`HEL-CIV-SS-GIS-2040`) targeting rebar inspection by Day 22.
   - Continue Substation Control Room internal plastering, partition masonry curing, and wall chases for cable conduits (`HEL-CIV-SS-CR-2020`).
   - Conclude 7-day wet burlap curing cycle for the 100MVA MPT transformer foundation plinth on Day 21; clear area for plinth acceptance.
4. **Main Power Transformer Manufacturing Expediting (CONVOY / ARCHON / TRACER):**
   - Track POWERTRANS works progress as Activity `HEL-PRO-SS-MPT-2010` reaches Day 9 of 182; verify core stacking progression and winding shop schedule.
   - Confirm receipt of bi-weekly QA inspection milestones from third-party inspectorate at the factory.
5. **Project Controls & MIS (SIGMA / LEDGER / KRONOS):**
   - Reconcile Day 020 production quantities (120 tables assembled, 80 rock socket piles driven, GIS raft rebar initiated) in Primavera P6 and DPR Day 020.
   - Prepare Week 3 formal schedule update freeze and monthly EVM reconciliation with LEDGER.

**KRONOS**  
*Planning Manager — HELIOS EPC Project (100MW Solar PV + 33/220kV GSS)*  
*Discipline: Project Planning & Controls*
