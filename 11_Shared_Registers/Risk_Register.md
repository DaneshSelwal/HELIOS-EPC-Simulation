# HELIOS EPC — Project Risk & Opportunity Register

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Bukhara, Uzbekistan  
**Custodians:** ATLAS (Project Manager), KRONOS (Planning Manager) & COUNSEL (Contracts Manager)  
**Last Updated:** 2026-10-06 (Sim Day 001, Month 1, Week 1 — LNTP Start Position)

## 1. Active Project Risk Matrix

| Risk ID | Category | Risk Description & Cause | Affected WBS / Path | Prob. (1-5) | Impact (1-5) | Score | Financial Exposure (USD) | Schedule Exposure (Days) | Mitigation & Response Strategy | Risk Owner | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `RSK-001` | Geotechnical | Shallow bedrock refusal at 0.80m in Array Block 6 (`EVT-001`) preventing standard hydraulic ramming (1.50m design). | `WP-ENG-CIV` / `WP-CON-CIV-PIL` | 5 (Realized) | 3 | **15 (HIGH)** | $185,000 (Recoverable under 4.12) | +24d local / **0d COD** (45d float) | Issued `FDC-CIV-001` (DTH pre-drilling + M15 grout); re-sequenced Blocks 1–5 first; served Sub-Clause 20.1 Notice `HELIOS-NTC-001`. | `TERRA` / `COUNSEL` | **REALIZED — MITIGATING** |
| `RSK-002` | Grid / Regulatory | UzbekEnergo / NEGU National Grid Code revision mandating Primary Frequency Response (PFR) & FRT resubmission (`EVT-002`). | `WP-ENG-SUB` / `WP-PROC-TRA` (0d Float) | 4 | 5 | **20 (CRITICAL)** | $65,000 | **+7 to +14d COD** (Critical Path) | Fast-track PPC firmware solution with `INVERSA`; joint workshop with `GRIDMASTER` to compress 14d review to 7d; Sub-Clause 13.7/20.1 notice. | `VOLTA` / `CIPHER` | **ACTIVE WATCH** |
| `RSK-003` | Supply Chain | Tier-1 TOPCon wafer/cell shortage delaying `LUMINOS` PV module deliveries (`EVT-003`). | `WP-PROC-MOD` (Near-Critical) | 3 | 4 | **12 (MED-HIGH)** | $350,000 (LD offset) | +14 to +56d local | Enforce 0.5%/wk LD clause; negotiate split-shipment block-trains via Khorgos to protect Month 6 First Module Delivery. | `CONVOY` / `FORGE` | **MONITORING** |
| `RSK-004` | Customs / Logistics | 220kV 100MVA MPT border detention at Khorgos due to missing `GOST-UZ` conformity certificate or bridge permits (`EVT-009`) or rail transit shock $>4.0g$ (`EVT-010`). | `WP-PROC-TRA` (0d Float) | 3 | 5 | **15 (HIGH)** | $220,000 | **+10 to +21d COD** | Retain licensed Tashkent customs broker (`ROUTE`); audit `GOST-UZ` passport 30d pre-shipment; fit dual 3-axis impact recorders & marine cargo/DSU insurance (`LEDGE`). | `ROUTE` / `TRACER` | **PREVENTIVE** |
| `RSK-005` | Climatic / HSE | Kyzylkum desert dust storms (>20 m/s winds, `EVT-004`) and severe Siberian winter ground freeze (<-15°C, `EVT-012`). | `WP-CON-CIV-PIL` / `WP-CON-MEC-MOD` | 4 | 3 | **12 (MED-HIGH)** | $120,000 (Standby) | +3 to +18d | Built 6-day weather-adjusted calendar into P6 baseline; enforce `AEGIS` wind/freeze stop-work protocols and `SHNK` winter concrete curing. | `AEGIS` / `KRONOS` | **MITIGATED IN BASELINE** |
