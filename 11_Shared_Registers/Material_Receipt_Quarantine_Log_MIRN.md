# HELIOS EPC — Site Stores Material Receipt (MIRN), Inventory & Quarantine Register

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Bukhara, Uzbekistan  
**Custodian:** VAULT (Site Stores In-Charge, SC-07)  
**Interfaces:** TRACER (Expediter), ROUTE (Logistics/Customs), SENTINEL / TORQUE / OHMMETER (Receiving QC)  
**Last Updated:** 2026-10-06 (Sim Day 001, Month 1, Week 1 — LNTP Start Position)

## 1. Receiving & Quarantine Governance Rules
1. **Hard Physical Constraint (`engine/site_reality.py`)**: Zero permanent plant materials (piles, tracker tables, PV modules, DC/MV cables, inverter skids, 220kV MPT/GIS) can be installed by Construction unless they are physically delivered to site, cleared through Uzbekistan customs (`GTD`), inspected via a joint **Material Inspection & Receipt Note (`MIRN`)** by `VAULT` and `QUALITY`, and released to free stock.
2. **Quarantine Protocol**: Any shipment arriving with missing `GOST-UZ` certificates (`EVT-009`), shock impact recorder alarms $>4.0g$ (`EVT-010` 5.2g MPT shock), container transit damage, or batch microcrack failures (`EVT-015`) is immediately logged in the **Quarantine Bay** and locked from issue.

## 2. Master Material Receipt & Inventory Ledger (As of Sim Day 005)

| Work Package | Material Description | Unit | Total Contract Scope | PO Status | Delivered to Site | MIRN QC Accepted | Quarantined Qty | Issued to Construction | Free Stock Balance | Remarks / Next Delivery Milestone |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `WP-PROC-PIL` | Galvanized H-Piles ( PV Field Foundations) | piles | 15,400 | RFQ / Bidding | 0 | 0 | 0 | 0 | 0 | First batch delivery scheduled prior to Month 4 (Day 112) |
| `WP-PROC-TRK` | 1P Single-Axis Tracker Tables & Slew Drives | tables | 5,100 | MTO Alignment | 0 | 0 | 0 | 0 | 0 | Sequenced behind `WP-PROC-PIL` |
| `WP-PROC-MOD` | 580W N-Type TOPCon Bifacial PV Modules (`LUMINOS`) | modules | 172,800 | `RFQ-HEL-EQ-003` (Day 5) | 0 | 0 | 0 | 0 | 0 | Baseline ROSD Month 6 (Day 168); subject to `EVT-003` |
| `WP-PROC-INV` | 4.0MVA Central Inverter / MVS Turnkey Skids (`INVERSA`) | skids | 25 | `RFQ-HEL-EQ-004` | 0 | 0 | 0 | 0 | 0 | Baseline ROSD Month 7–8 |
| `WP-PROC-TRA` | 220kV/33kV 100MVA Main Power Transformer (`POWERTRANS`) | units | 1 | Award Target Day 012 | 0 | 0 | 0 | 0 | 0 | 182d lead time (ETA Day 194); critical path 0d float |
| `WP-PROC-GIS` | 220kV SF6 Gas Insulated Switchgear (`POWERTRANS`) | sets | 1 | `RFQ-HEL-EQ-002` (Day 4) | 0 | 0 | 0 | 0 | 0 | Baseline ROSD Month 11 |
| `WP-PROC-CAB-DC` | 1.5kV Solar DC String & Main Cables (IEC 62930) | meters | 1,300,000 | MTO Alignment | 0 | 0 | 0 | 0 | 0 | Sequenced for Month 5–6 delivery |
| `WP-PROC-CAB-MV` | 33kV XLPE Underground MV Cables & Cold-Shrink Kits | meters | 30,000 | MTO Alignment | 0 | 0 | 0 | 0 | 0 | Sequenced for Month 6–7 delivery |
