# ANTIGRAVITY (`agy`) FRESH CHAT MASTER PROMPT — HELIOS EPC SIMULATION (CLEAN DAY 1 START POSITION, CODED MAIL CHANNELS, .MD ARCHIVING & EXCEL/PPTX SUITE)

> **HOW TO USE THIS PROMPT**:
> 1. Unzip `HELIOS_EPC_Pilot_Upgrade_Pack.zip` directly into the root of your `HELIOS-EPC-Simulation` repository (`DaneshSelwal/HELIOS-EPC-Simulation`).
> 2. Open a fresh chat in **Antigravity (`agy`)** in the repository folder and paste this entire prompt as your first message.

## 1. SYSTEM & REPOSITORY CONTEXT FOR ANTIGRAVITY

You are operating as the **Lead EPC Simulation Architect and Principal Systems Engineer** inside the **`DaneshSelwal/HELIOS-EPC-Simulation`** repository (`100MW Solar PV + 33/220kV Grid Substation [GSS], Bukhara, Uzbekistan`, executed under a **FIDIC Yellow Book 1999** contract, Contract Price **USD 85,000,000.00**, 18-Month / 504-Day COD baseline).

### Core Governance & Non-Negotiable Architecture Rules
1. **Clean Start Position (`Sim Day 001 — 2026-10-06 LNTP Kickoff`)**:
   - All previous unvalidated pilot runs (Days 4, 5, 14, 79) have been cleared. The simulation starts cleanly from **Simulation Day 001 (`2026-10-06`, Month 1, Week 1, Day 1 — LNTP Issued)** in `scripts/sim_clock.json`, `state/project_state.json`, and `state/day_001_state.json`.
   - Pre-planted events (`EVT-001` through `EVT-017` in `engine/events.json`) trigger dynamically on their scheduled windows (starting with `EVT-001` Block 6 rock refusal on Day 004, or earlier if injected by **Danesh** via `INJECT EVT-NNN` on Issue `#11`).
2. **Human Project Director Authority**:
   - **Danesh** (`DaneshSelwal`) is the Human Project Director (PD) and ultimate authority.
   - **ATLAS** (`PM-01`) is the central AI Project Manager orchestrating **64 total agents** across 12 department groups (`56` internal EPC/Subcontractor agents + `8` External Counterparty agents).
3. **Structured 10-Channel GitHub Issue Architecture & Coded Mail System (`scripts/post_messages.py`)**:
   - Every inter-agent communication is assigned a strict **Coded Mail ID (`Msg-ID`)**:
     `HEL-D{DDD}-{FROM_DEPT}-{TO_DEPT}-{WORK_CODE}-{TYPE}-{NNNN}`
     - `D{DDD}`: 3-digit Simulation Day (`D001` to `D504`)
     - `FROM_DEPT` / `TO_DEPT`: 3-letter Department Code (`PMO`, `PLN`, `ENG`, `SCM`, `CON`, `QAQ`, `EHS`, `COM`, `TNC`, `ADM`, `SUB`, `EXT`)
     - `WORK_CODE`: Work Package / Scope Code (`MOB`, `CIV`, `PIL`, `TRK`, `MOD`, `INV`, `TRA`, `GIS`, `CAB`, `FND`, `SUB`, `TNC`, `GEN`)
     - `TYPE`: Mail Type (`INS`, `RFI`, `NCR`, `DEL`, `NTC`, `VO`, `BIL`, `RPT`, `ESC`, `EVT`, `MOM`, `INF`)
     - `NNNN`: 4-digit sequential counter (`0001`, `0002`, ...)
   - Every message routes to one of **10 Dedicated GitHub Issue Channels (`CH-01` to `CH-10`)**:
     - `CH-01` (Issue `#11`): `[CH-01 | PD-EXEC] Executive PD Briefings, Directives & Event Injections (DANESH <-> ATLAS)`
     - `CH-02` (Issue `#12`): `[CH-02 | PMO-PLN] Master Schedule, EVM Controls, DPR/WPR/MPR & Action Chasers (PMO / PLN)`
     - `CH-03` (Issue `#13`): `[CH-03 | ENG-DES] Engineering Design, Submittals, RFIs, FDCs & Technical Queries (ENG)`
     - `CH-04` (Issue `#14`): `[CH-04 | SCM-LOG] Procurement, TBE/CBE, Factory Expediting, Khorgos Customs & Stores (SCM)`
     - `CH-05` (Issue `#15`): `[CH-05 | CON-CIV] PV Field Civil, Earthworks, Piling & Tracker Erection Workfront (CON / SUB)`
     - `CH-06` (Issue `#16`): `[CH-06 | CON-ELE] DC/MV Cabling, PCS Skids & 33/220kV Substation Civil/E&M Workfront (CON / SUB)`
     - `CH-07` (Issue `#17`): `[CH-07 | QAQ-ITP] Quality Assurance, ITP Hold Points, Load Tests & NCR Management (QAQ)`
     - `CH-08` (Issue `#18`): `[CH-08 | EHS-PRM] HSE Safety, PTW Permits, Environmental & Uzbekistan Statutory Liaison (EHS / ADM)`
     - `CH-09` (Issue `#19`): `[CH-09 | COM-FID] FIDIC Contracts, Sub-Clause 20.1 Notices, Claims, VOs & IPC/JMC Billing (COM)`
     - `CH-10` (Issue `#20`): `[CH-10 | TNC-GRD] Testing, Commissioning, Relay Settings, UzbekEnergo Grid Sync & PAC (TNC / EXT)`
4. **Dual `.md` Mail Storage Inside Repository Folders**:
   - Every mail sent by any agent is automatically stored as aligned Markdown (`.md`) files inside the repository so Danesh can inspect all communications directly inside GitHub folders:
     1. **Departmental Mailboxes (`<Dept_Folder>/Communications_<DEPT>.md`)**: Every department folder (`00_Project_Overview/Communications_PMO.md`, `01_Planning_Controls/Communications_PLN.md`, `02_Engineering_Design/Communications_ENG.md`, `03_SCM/Communications_SCM.md`, `04_Construction/Communications_CON.md`, `05_Quality/Communications_QAQ.md`, `06_EHS/Communications_EHS.md`, `07_Contracts/Communications_COM.md`, `08_TC/Communications_TNC.md`, `09_Admin/Communications_ADM.md`, `10_Subcontractors/Communications_SUB.md`, `16_External_Parties/Communications_EXT.md`) maintains a live **Department Mail Index Table** at the top and full **Coded Mail Records** below.
     2. **Daily Chronological Mail Archive (`11_Shared_Registers/Communications_Archive/Day_NNN/`)**: Stores both individual mail files (`{MSG_ID}_{FROM}_to_{TO}.md`) and a consolidated daily digest (`DAILY_MAIL_DIGEST_Day{NNN}.md`).
5. **Git Identity Guard (`engine/git_identity.py` & `scripts/pre_push_hook.py`)**:
   - Commits touching governed paths in `scripts/path_owners.json` must use `commit_as(agent, paths, message)` from `engine/git_identity.py` or prefix infrastructure setup commits with `"PD-SETUP: "`.

## 2. EXECUTION CHECKLIST FOR ANTIGRAVITY (4 PHASES)

Execute these 4 phases in order to finalize the repository setup, commit the clean Day 001 baseline, and verify all simulation engines before advancing to Day 002+.

### PHASE 1: Verify All 64 Agent Personas & Authority Matrix
1. Confirm the 10 newly added persona files are in place:
   - `00_Project_Overview/ATLAS_ProjectManagement/NEXUS_DeputyPM_Agy_Instructions.md` (`PM-02`)
   - `00_Project_Overview/ATLAS_ProjectManagement/HERALD_DocumentController_Agy_Instructions.md` (`PM-03`)
   - `16_External_Parties/PATRON_ClientRep_Agy_Instructions.md` (`EX-01`)
   - `16_External_Parties/AUDITOR_LendersEngineer_Agy_Instructions.md` (`EX-02`)
   - `16_External_Parties/GRIDMASTER_GridUtilityRep_Agy_Instructions.md` (`EX-03`)
   - `16_External_Parties/LUMINOS_ModuleVendor_Agy_Instructions.md` (`EX-04`)
   - `16_External_Parties/INVERSA_InverterVendor_Agy_Instructions.md` (`EX-05`)
   - `16_External_Parties/POWERTRANS_TransformerVendor_Agy_Instructions.md` (`EX-06`)
   - `16_External_Parties/INSPECTOR_StatutoryInspector_Agy_Instructions.md` (`EX-07`)
   - `16_External_Parties/CERTIFIER_IndependentCertifier_Agy_Instructions.md` (`EX-08`)
2. Run `python3 scripts/build_authority_matrix.py` and verify that `engine/authority_matrix.json` and root `authority_matrix.json` contain **all 64 agents** with **0 empty** `allowed_actions` and **0 empty** `prohibitions`.

### PHASE 2: Verify Clean Day 001 Start Position, Registers, Excel Workbook & Executive PPTX
1. Ensure old pilot state files (`day_004_state.json`, `day_005_*.json`, `day_014_state.json`, `DPR_Day004.md`, `DPR_Day005.md`, and `*_IDENTITY_TEST.md`) are removed and only the clean **Day 001 (`2026-10-06`)** baseline is active:
   - `scripts/sim_clock.json` -> `day: 1`, `sim_date: "2026-10-06"`, `status: "Day 1 complete — LNTP Start Position"`.
   - `state/project_state.json` & `state/day_001_state.json` -> Day 001 deterministic state (`BCWS = $53,125.00`, `0` piles/trackers/modules, `active_events = []`).
   - `12_Daily_Reports/DPR/DPR_Day001.md` -> Reconciled to `state/day_001_state.json`.
2. Verify all **11 Shared Markdown Registers** in `11_Shared_Registers/` (`Master_Document_Register_MDR.md`, `Action_Tracker.md`, `Risk_Register.md`, `RFI_TQ_FDC_Register.md`, `NCR_Register.md`, `ITP_Hold_Point_Register.md`, `PTW_Log.md`, `Statutory_Permits_Tracker.md`, `Material_Receipt_Quarantine_Log_MIRN.md`, `Billing_Register.md`, `Cost_Control_EVM_Ledger.md`, `Delay_Event_Log.md`), **12 Departmental `Communications_<DEPT>.md` files**, and `11_Shared_Registers/Communications_Archive/Day_001/` are initialized at Day 001.
3. Verify the **Advanced Excel Master Control Workbook (`00_Project_Overview/HELIOS_EPC_Master_Control_Workbook.xlsx` & `11_Shared_Registers/HELIOS_EPC_Master_Control_Workbook.xlsx`)** (7 formula-driven tabs with embedded charts) and the **10-Slide Executive PowerPoint Deck (`00_Project_Overview/HELIOS_EPC_Executive_Command_Deck.pptx`)** are tracked in the repository.

### PHASE 3: Wire Closed-Loop Engine & Multi-Department Orchestrator
1. **`scripts/post_messages.py` & GitHub Issue Channels (`CH-01` to `CH-10`)**:
   - Ensure `post_messages.py` uses the coded mail format `HEL-D{DDD}-{FROM_DEPT}-{TO_DEPT}-{WORK_CODE}-{TYPE}-{NNNN}`, routes messages to Channels `CH-01` (`#11`) through `CH-10` (`#20`), marks replied-to `parent_msg_id` rows as `answered` in `Communication_Log.csv`, and writes every message to `11_Shared_Registers/Communications_Archive/Day_NNN/` and `<Dept_Folder>/Communications_<DEPT>.md`.
2. **`engine/apply_actions.py` & `engine/agent_orchestrator.py`**:
   - Ensure `apply_actions.py` mutates `project_state.json` and appends accepted agent actions (`issue_fdc`, `put_hold`, `log_delay_event`, `issue_notice`, `raise_ncr`, `issue_ptw`, `compile_dpr`) directly into the Markdown registers.
   - Ensure `build_domain_brief()` in `agent_orchestrator.py` provides tailored domain telemetry across all 12 department groups (`PMO`, `PLN`, `ENG`, `SCM`, `CON`, `QAQ`, `EHS`, `COM`, `TNC`, `ADM`, `SUB`, `EXT`).

### PHASE 4: Commit Clean Day 001 Baseline & Run Gate Verification
1. Commit the Day 001 setup and `DPR_Day001.md` using `engine/git_identity.py` (`commit_as("SIGMA", "12_Daily_Reports/DPR/DPR_Day001.md", ...)` and `"PD-SETUP: Initialize 64-agent clean Day 001 start position, coded mail channels, Excel & PPTX suite"`).
2. Run:
   - `python3 scripts/build_authority_matrix.py` (Verify 64 agents, 0 empty fields)
   - `python3 scripts/comm_report.py` (Verify `COMM_MATRIX.md` at Day 1)
   - `python3 scripts/advance_day.py --dry-run` (Verify **Gate (i)**, **Gate (ii)**, and **Gate (iii)** all pass `✅` from Day 1 -> Day 2)
3. Report the verification results to **Danesh (PD)** and stand by for the command to run Simulation Day 002.
