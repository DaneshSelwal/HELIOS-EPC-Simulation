# HELIOS EPC — Permit to Work (PTW), Stop-Work Order (SWO) & HSE Register

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Bukhara, Uzbekistan  
**Custodian:** AEGIS (EHS Manager, EH-01)  
**Field Officers:** GUARDIAN (Civil/Structural Safety), WARDEN (Electrical/Substation Safety & LOTO), VERDANT (Environmental & Social)  
**Last Updated:** 2026-10-06 (Sim Day 001, Month 1, Week 1 — LNTP Start Position)

## 1. Cumulative Project HSE Statistics (As of Sim Day 005)
| KPI Metric | Day 005 Daily | Cumulative (Days 001–005) | Target / Threshold | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Fatalities / Lost Time Injuries (LTI)** | 0 | **0** | 0 (Zero Harm) | **GREEN** |
| **Restricted Work / Medical Treatment Cases (MTC)** | 0 | **0** | 0 | **GREEN** |
| **First Aid Cases (FAC)** | 0 | **0** | 0 | **GREEN** |
| **Near Misses / Safety Observations Logged** | 1 | **2** | Proactive reporting | **GREEN** |
| **Safe Man-Hours Worked** | 1,120 hrs | **5,480 hrs** | Continuous LTI-free | **GREEN** |
| **Active Stop-Work Orders (SWO / Technical Holds)** | 1 (Block 6 Piling Hold) | **1** | Enforced on Block 6 (`EVT-001`) | **ACTIVE HOLD** |

## 2. Active Permit to Work (PTW) & Operational Hold Log

| PTW / Hold ID | Sim Day Issued | Permit Type | Location / Work Package | Issued To (Sub / Lead) | Authorized By | Mandatory Safety Controls & SanPiN Conditions | Validity Window | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PTW-GEN-001` | Day 001 | General Civil & Perimeter Mobilization | Site Perimeter & Camp (`WP-CON-MOB`) | `GROUNDWORK` / `BASTION` | `AEGIS` / `GUARDIAN` | PPE compliance, banksman for plant reversing, 20 km/h site speed limit, dust suppression water tanker active. | Days 001–014 | **ACTIVE** |
| `PTW-EXC-002` | Day 005 | Geotechnical Core Drilling & Trial Pit | Array Block 6 (`WP-ENG-CIV` / `EVT-001`) | `MERIDIAN` / `BASTION` | `GUARDIAN` | Underground service scan cleared, rotating auger guards installed, whip-checks on high-pressure air hoses, hearing protection. | Days 005–010 | **ACTIVE** |
| `HOLD-CIV-B6` | Day 005 | **Technical & Safety Piling Hold (`EVT-001`)** | Array Block 6 (`WP-CON-CIV-PIL`) | `GROUNDWORK` / `BASTION` | `BASTION` / `TERRA` (cc: `AEGIS`) | **PROHIBITED**: Direct hydraulic ramming on shallow 0.80m rock stratum (risk of steel pile shaft buckling & flying metal shrapnel). Locked until `FDC-CIV-001` DTH pre-drilling rig & PTW are cleared. | Until `FDC-CIV-001` Trial Piles Passed | **ENFORCED HOLD** |
