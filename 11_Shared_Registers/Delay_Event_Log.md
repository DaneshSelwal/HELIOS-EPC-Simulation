# HELIOS EPC — Delay Event Log (DEL)

**Project:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**Contract:** FIDIC Yellow Book 1999  
**Custodians:** KRONOS (Planning Manager) & COUNSEL (Contracts Manager)  
**Last Updated:** 2026-10-06 (Day 2, Month 1)

---

## 1. Summary of Logged Events

| Delay ID | Event Ref | Date Occurred | Event Description | Responsible Party | Affected Path / WBS | Critical Path? | Unmitigated Delay | Net Project Delay | Notice 20.1 Deadline | Notice 20.1 Status | Log Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEL-001** | EVT-001 | 2026-10-06 | Geotechnical Anomaly — Competent Rock Layer encountered at 0.80m in PV Block 6 vs 1.50m design embedment depth causing pile refusal. | Employer (FIDIC Sub-Clause 4.12 Unforeseeable Physical Condition) | `HEL.60` PV Field Piling (Block 6) / `HEL-CIV-PV-PLG-0600` | No (Float: +45d) | +24 calendar days (Block 6 local path) | **0 days** (Absorbed by re-sequencing Blocks 1–5 first & float) | 2026-11-03 (28 days) | Issued: HELIOS-NTC-001 (2026-10-06) | **ACTIVE / MITIGATION IMPLEMENTED** |

---

## 2. Event Detail Records

### DEL-001 / EVT-001: Block 6 Shallow Rock Horizon Refusal
- **Event Identifier:** DEL-001 (Cross-reference: GitHub Issue #7 / EVT-001)
- **Date of Occurrence:** 2026-10-06 (Project Day 2, Month 1)
- **Location / WBS:** Block 6 Array, WBS `HEL.60` (Construction – PV Field), Activity `HEL-CIV-PV-PLG-0600`
- **Root Cause & Description:** Competent bedrock stratum encountered at depth of 0.80 m below EGL across Block 6, resulting in immediate hydraulic ramming refusal. Tender geotechnical documentation provided by Employer represented uniform alluvial loose/medium sand to $>2.5\text{ m}$ depth with design pile embedment at 1.50 m (`HEL-ST-CAL-0010`). Terminating piles at 0.80 m provides $<35\%$ passive lateral resistance, causing structural failure under wind gust overturning moments per KMK 2.01.07-96.
- **Contractual Classification:** Unforeseeable Physical Condition under FIDIC Yellow Book 1999 Sub-Clause 4.12. Entitlement asserted under Sub-Clause 8.4(b) (Extension of Time) and Sub-Clause 4.12 (Cost incurred).
- **Statutory Notice Clock (Sub-Clause 20.1):** 
  - Date Aware: 2026-10-06 (Day 2)
  - 28-Day Statutory Notice Cut-off: **2026-11-03 (Day 30)**
  - Notice Directive: Formal Notice HELIOS-NTC-001 issued by COUNSEL on 2026-10-06 (Day 2, 26 days ahead of time-bar). Claim Ref CLM-001.
- **CPM Schedule & Float Impact:**
  - Master Critical Path: Runs through 220kV GSS and MPT manufacturing chain (0 days total float). Block 6 is off the master critical path.
  - PV Field Total Float: **+45 calendar days** to Mechanical Completion (Month 15).
  - Unmitigated Block 6 Piling Impact: +24 calendar days due to DTH rig cycle time reduction (35–40 piles/day vs 120 piles/day) and rig procurement lead time.
  - Net Project Impact: **0 days** delay to COD (Month 18) or Milestone `HEL.10` First Pile (Month 4).
- **Mitigation & Fragnet Plan:**
  1. **Workfront Re-sequencing:** RAMPART/GROUNDWORK directed to re-sequence hydraulic ramming sequence to commence in alluvial sandy sectors (Blocks 1 through 5) at Month 4. Block 6 shifted to Workfront 6 (Month 6–7), creating 10–12 weeks of lead time buffer.
  2. **Technical Remediation:** Adoption of Option 1 (DTH rock pilot pre-drilling $\varnothing 180-220\text{ mm}$ + 500mm rock socket + non-shrink cementitious grout annulus) per Technical Memorandum `HEL-CV-MEM-0001`.
  3. **Fragnet Insertion:** Inserted Fragnet `FRAG-EVT-001` (36 calendar days total qualification/mobilization duration executed concurrently during Months 1–3 before piling start).
- **Cost & Commercial Implications:**
  - Additional Cost items: Crawler DTH drilling rigs mobilization, 21 bar air compressors, consumable tungsten carbide drill bits, cementitious grout (M15/C12/15) batching, confirmatory core boreholes (MERIDIAN), and calibration pile testing.
  - LEDGER and CLAIMS notified to track all associated cost codes separately under `CC-VAR-EVT-001`.
