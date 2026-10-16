# HELIOS EPC — Master Delay Event Log (DEL)

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Bukhara, Uzbekistan  
**Contract:** FIDIC Yellow Book 1999 (Sub-Clause 8.4 EOT & Sub-Clause 20.1 28-Day Notice Bar)  
**Custodians:** KRONOS (Planning Manager) & COUNSEL (Contracts Manager)  
**Data Date / Last Updated:** 2026-10-06 (Sim Day 001, Month 1, Week 1 — LNTP Start Position)

## 1. Master Register of Delay Events

| Delay ID | Event Ref | Date Occurred | Event Description | Responsible Party | Affected Path / WBS | Critical Path? | Unmitigated Delay | Net COD Delay | Notice 20.1 Deadline | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| *None Active at Day 001* | — | — | *Project reset to Clean Start Position (Sim Day 001 — 2026-10-06 LNTP Issued). Pre-planted simulation events (`EVT-001` through `EVT-017` in `engine/events.json`) will trigger dynamically as the simulation clock advances (starting with `EVT-001` at Day 004).* | — | — | Master Critical Path: 220kV GSS & MPT (`0d Float`) | `0 days` | **`0 days`** | — | **CLEAN BASELINE** |

## 2. Daily Gate (i) Validation & Time Impact Review Log (`KRONOS`)

| Sim Day | Sim Date | Reviewed By | Active Delay Events | Master Critical Path Float (220kV GSS / MPT) | PV Field Float | Gate (i) Verification Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Day 001** | 2026-10-06 | `KRONOS` | None (`0 Active`) | `0 days` | `+45 days` | **Day 1 Validated (`HEL-D001-PLN-PLN-MOB-RPT-0002`)**: Rev 0 Baseline Schedule (`HEL.00` LNTP) active; `SPI = 0.9304`, `CPI = 0.9330`; zero delay events at Start Position. |
