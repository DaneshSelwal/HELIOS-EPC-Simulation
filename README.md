# HELIOS 100MW Solar PV + 33/220kV GSS EPC Simulation (`FIDIC Yellow Book 1999`)

**Project Location**: Bukhara Region, Republic of Uzbekistan  
**Contract Price (BAC)**: USD 85,000,000 (Fixed Lump Sum Turnkey EPC)  
**Baseline Schedule (`HEL.00`)**: 18 Months (`504` Simulation Days at `28` days/month)  
**Current Simulation Clock**: **Day `001` (`2026-10-06`, Month 1 / Week 1 / Day 1 — LNTP Start Position)**  
**Project Director (Human-in-the-Loop)**: **Danesh** (`PD`)  
**Lead EPC Project Manager**: **`ATLAS`** (`PMO`)  

---

## 1. Canonical Repository Architecture

Every file in `/Users/danesh/Desktop/HELIOS_EPC` (synced 1:1 with `DaneshSelwal/HELIOS-EPC-Simulation`) follows a strict, deterministic directory architecture. Any file added, modified, or deleted locally is tracked by Git ownership rules ([`scripts/path_owners.json`](scripts/path_owners.json)) and synced directly with GitHub.

```text
HELIOS_EPC/
├── README.md                                      # Master Repository Architecture & Governance Specification
├── 00_Project_Overview/                           # [DEPT: PMO] Project Management Office & Executive Command
│   ├── ATLAS_ProjectManagement/                   # PMO Agent Personas: ATLAS, NEXUS, HERALD
│   ├── 01_Executive_Command_Suite/                # Executive PPTX Deck, Master Excel Workbook & Master Prompt
│   ├── 02_Department_Research_Briefs/             # Reference Department Research PDFs (DEPT01–DEPT10)
│   ├── HELIOS_EPC_Workforce.xlsx                  # 64-Agent Master Workforce Roster & Activity Windows
│   └── Communications_PMO.md                      # PMO Coded Mail Mirror (CH-01 & CH-02)
├── 01_Planning_Controls/                          # [DEPT: PLN] Planning, Schedule & Cost Controls (KRONOS, SIGMA, VECTOR, WATT, LEDGER)
│   ├── Delay_Event_Log.md                         # Master Delay Event & Daily Gate (i) Validation Register
│   └── Communications_PLN.md                      # PLN Coded Mail Mirror (CH-02)
├── 02_Engineering_Design/                         # [DEPT: ENG] Engineering & Design (ARCHON, NEXGEN, CIPHER, TERRA, MERIDIAN, AMPERE, VOLTA, SOLARIS)
│   └── Communications_ENG.md                      # ENG Coded Mail Mirror (CH-03)
├── 03_SCM/                                        # [DEPT: SCM] Supply Chain, Procurement & Logistics (CONVOY, FORGE, VENDOR, TRACER, ROUTE, VAULT, DEPOT)
│   └── Communications_SCM.md                      # SCM Coded Mail Mirror (CH-04)
├── 04_Construction/                               # [DEPT: CON] Site Construction Execution (RAMPART, BASTION, SWITCHMAN, ARCLINE, FORTRESS, CONDUIT, STRATUM, PRISM)
│   └── Communications_CON.md                      # CON Coded Mail Mirror (CH-05 & CH-06)
├── 05_Quality/                                    # [DEPT: QAQ] QA/QC & ITP Hold Points (SENTINEL, PLUMBLINE, OHMMETER, TORQUE, DOSSIER)
│   └── Communications_QAQ.md                      # QAQ Coded Mail Mirror (CH-07)
├── 06_EHS/                                        # [DEPT: EHS] Health, Safety, Environment & SanPiN (AEGIS, GUARDIAN, WARDEN, VERDANT)
│   └── Communications_EHS.md                      # EHS Coded Mail Mirror (CH-08)
├── 07_Contracts/                                  # [DEPT: COM] FIDIC Contracts, Claims & Billing (COUNSEL, CLAIMS, INVOICE, LEDGE, CHECKER)
│   ├── Claims_Register.md                         # Master FIDIC Claims Register
│   ├── FIDIC_Notice_Log.md                        # Statutory 28-Day Sub-Clause 20.1 Notice Log
│   └── Communications_COM.md                      # COM Coded Mail Mirror (CH-09)
├── 08_TC/                                         # [DEPT: TNC] Testing, Commissioning & Grid (IGNITE, SPARK, GRIDLOCK, RELAY)
│   └── Communications_TNC.md                      # TNC Coded Mail Mirror (CH-10)
├── 09_Admin/                                      # [DEPT: ADM] Site Administration, Permits & Finance (SUMMIT, PERMIT, LEDGER2)
│   └── Communications_ADM.md                      # ADM Coded Mail Mirror (CH-08)
├── 10_Subcontractors/                             # [DEPT: SUB] Turnkey Subcontractors (GROUNDWORK, EREKTOR, ELECTRA, GRIDCON)
│   └── Communications_SUB.md                      # SUB Coded Mail Mirror (CH-05 & CH-06)
├── 11_Shared_Registers/                           # [ENGINE / ALL] Single Source-of-Truth Project Registers & Mail Archive
│   ├── Communication_Log.csv                      # Master Coded Communication Log (Gate ii & iii enforced)
│   ├── COMM_MATRIX.md                             # Auto-generated Inter-Department Communication Matrix
│   ├── Communications_Archive/Day_NNN/            # Daily Coded Mail Archive & Digest (.md)
│   ├── Action_Tracker.md                          # Cross-Department Open Action Tracker
│   ├── Billing_Register.md                        # Employer IPC & Subcontractor Billing Register
│   ├── Cost_Control_EVM_Ledger.md                 # Earned Value Management (BCWS/BCWP/ACWP/SPI/CPI) Ledger
│   ├── Delay_Event_Log.md                         # Shared Mirror of Master Delay Event Log
│   ├── HELIOS_EPC_Master_Control_Workbook.xlsx    # 7-Tab Advanced Excel Master Control Workbook
│   ├── ITP_Hold_Point_Register.md                 # Inspection & Test Plan (ITP) Hold/Witness Point Register
│   ├── Master_Document_Register_MDR.md            # Engineering Submittal & IFC Transmittal Register
│   ├── Material_Receipt_Quarantine_Log_MIRN.md    # Site Warehouse Material Inspection & Quarantine Log
│   ├── NCR_Register.md                            # Quality Non-Conformance Report Register
│   ├── Procurement_Tracker.md                     # Long-Lead Equipment & BOP Procurement Tracker
│   ├── PTW_Log.md                                 # EHS Permit-to-Work & Stop-Work Register
│   ├── RFI_TQ_FDC_Register.md                     # Technical Queries, RFIs & Field Design Changes Register
│   ├── Risk_Register.md                           # Project Risk & Mitigation Register
│   └── Statutory_Permits_Tracker.md               # Uzbek Regulatory & Construction Permits Tracker
├── 12_Daily_Reports/DPR/                          # [SIGMA] Daily Progress Reports (DPR_Day001.md ...)
├── 13_Weekly_Reports/                             # [SIGMA] Weekly Progress Reports (WPR)
├── 14_Monthly_Reports/                            # [KRONOS] Monthly Progress Reports (MPR)
├── 15_Event_Engine/                               # [ENGINE] Pre-Planted Risk & Event Seed Specifications
├── 16_External_Parties/                           # [DEPT: EXT] External Counterparties (PATRON, AUDITOR, GRIDMASTER, LUMINOS, INVERSA, POWERTRANS, INSPECTOR, CERTIFIER)
│   └── Communications_EXT.md                      # EXT Coded Mail Mirror
├── engine/                                        # Deterministic Python Simulation & Governance Engine
│   ├── agent_orchestrator.py                      # Daily closed-loop multi-agent orchestrator (max 8 agents/day)
│   ├── apply_actions.py                           # Authority validation & automatic Markdown register mutation
│   ├── authority_matrix.json                      # Extracted 64-agent financial limits, allowed actions & prohibitions
│   ├── events.json                                # Deterministic event trigger definitions (EVT-001..EVT-017)
│   ├── evm.py                                     # Earned Value Management calculator
│   ├── git_identity.py                            # Per-agent Git author/committer identity enforcement
│   ├── run_day.py                                 # Daily state advancer
│   ├── site_reality.py                            # Weather, manpower & physical workfront progression model
│   └── triggers.py                                # Priority-scored agent invocation trigger engine
├── scripts/                                       # Operational & Sync Scripts
│   ├── advance_day.py                             # Gate (i), (ii), (iii) verifier & simulation clock advancer
│   ├── audit_state.py                             # State-to-register integrity auditor
│   ├── build_authority_matrix.py                  # Persona authority parser (64 agents)
│   ├── comm_log.py                                # Communication_Log.csv manager
│   ├── comm_report.py                             # COMM_MATRIX.md generator
│   ├── path_owners.json                           # Strict file-to-agent Git ownership rules
│   ├── pd_inbox.py                                # Danesh (PD) command reader on Channel CH-01
│   ├── post_messages.py                           # 10-Channel GitHub Issue router & dual .md mailbox writer
│   ├── pre_push_hook.py                           # Git pre-push hook verifying commit identity & path ownership
│   └── sim_clock.json                             # Master simulation clock
└── state/                                         # Machine-Readable State Snapshots
    ├── baseline.json                              # Rev 0 Baseline milestones & work package weights
    ├── project_state.json                         # Live cumulative project state
    ├── day_001_state.json                         # Daily immutable state snapshot
    ├── STATE_BRIEF.md                             # Human-readable daily state summary
    └── thread_issues.json                         # Live mapping of Channels CH-01..CH-10 to GitHub Issue numbers
```

---

## 2. 10-Channel Coded Mail & GitHub Issue Architecture

All agent communications use the standardized **Coded Mail ID**:
`HEL-D{DDD}-{FROM_DEPT}-{TO_DEPT}-{WORK_CODE}-{TYPE}-{NNNN}`

Every message is automatically logged to [`11_Shared_Registers/Communication_Log.csv`](11_Shared_Registers/Communication_Log.csv), mirrored to its departmental `.md` mailbox, archived in `11_Shared_Registers/Communications_Archive/Day_NNN/`, and posted to its dedicated GitHub Issue Channel (`CH-01` through `CH-10`, tracked in [`state/thread_issues.json`](state/thread_issues.json)).

---

## 3. Historical Archives
- All legacy pre-reset simulation branches are preserved on GitHub under `archive/drifted-day079` and `archive/pilot-day005-history`.
- All local pre-simulation draft/research folders are stored outside this repository in `/Users/danesh/Desktop/HELIOS_EPC_Legacy_Archive`.
