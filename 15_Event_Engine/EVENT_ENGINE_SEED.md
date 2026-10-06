# HELIOS EPC — EVENT ENGINE SEED FILE
# These are pre-planted events injected by Danesh (PD) during simulation.
# Each event hits specific agents and triggers realistic responses.
# Danesh injects by opening a new GitHub Issue referencing the Event ID.

---

## PHASE 1 — LNTP to Month 4 (Engineering & Early Procurement)

| Event ID | Month | Event | Agents Hit | Expected Chain Reaction |
|---|---|---|---|---|
| EVT-001 | M1 | Geotechnical report shows rock layer at 0.8m in Block 6 (design assumed 1.5m) | TERRA, MERIDIAN, BASTION, KRONOS, COUNSEL | TERRA issues FDC, COUNSEL files Sub-Clause 4.12 claim, KRONOS logs delay event |
| EVT-002 | M2 | UzbekEnergo requests protection philosophy resubmission — new grid code issued | VOLTA, CIPHER, ARCHON, KRONOS, COUNSEL | Design delay, KRONOS logs EOT event, COUNSEL issues Sub-Clause 20.1 notice |
| EVT-003 | M3 | Module vendor (LUMINOS) requests 8-week delivery extension due to cell shortage | FORGE, CONVOY, KRONOS, WATT, CLAIMS | WATT flags near-critical path, CONVOY negotiates, KRONOS runs TIA |

---

## PHASE 2 — Month 4 to Month 9 (Peak Construction)

| Event ID | Month | Event | Agents Hit | Expected Chain Reaction |
|---|---|---|---|---|
| EVT-004 | M4 | Dust storm shuts down module installation for 3 days | AEGIS, GUARDIAN, STRATUM, EREKTOR, KRONOS | AEGIS issues stop-work, EREKTOR claims standby costs, KRONOS logs weather delay |
| EVT-005 | M5 | GROUNDWORK pile driving crew reduced from 4 rigs to 2 (equipment breakdown) | BASTION, VECTOR, RAMPART, KRONOS, LEDGER | SPI drops, RAMPART issues default notice, LEDGER quantifies back-charge |
| EVT-006 | M6 | NCR raised: 47 piles in Block 3 out of tolerance (E-W deviation >20mm) | STRATUM, TORQUE, SENTINEL, EREKTOR, TERRA | SENTINEL issues NCR, EREKTOR disputes, PRISM does joint survey, re-drive ordered |
| EVT-007 | M7 | 33kV MV cable joint fails VLF test on Circuit INV3 to Main SS | ARCLINE, OHMMETER, ELECTRA, VOLTA, KRONOS | Work stopped, joint cut out, ELECTRA re-joints, extended VLF test, 5-day delay |
| EVT-008 | M8 | Client (PATRON) rejects MPR — claims progress is overstated by 8% | SIGMA, KRONOS, ATLAS, COUNSEL, INVOICE | SIGMA reconciles data, COUNSEL prepares formal response, billing dispute |

---

## PHASE 3 — Month 9 to Month 15 (Procurement Critical Path)

| Event ID | Month | Event | Agents Hit | Expected Chain Reaction |
|---|---|---|---|---|
| EVT-009 | M9 | 220kV transformer held at Khorgos border — missing GOST-UZ certificate | ROUTE, TRACER, CONVOY, KRONOS, COUNSEL | ROUTE mobilises broker, COUNSEL issues EOT notice, KRONOS opens D-series delay event |
| EVT-010 | M10 | Transformer arrives with 3-axis impact recorder showing 5.2g (threshold 4g) | TRACER, VAULT, SWITCHMAN, RELAY, CONVOY | Equipment quarantined, vendor field engineers called, SFRA test ordered, insurance claim |
| EVT-011 | M11 | Subcontractor ELECTRA threatens to demobilise — claims EPC owes 3 months back-payment | CHECKER, INVOICE, COUNSEL, RAMPART, ATLAS | CHECKER audits billing, COUNSEL reviews pay-when-paid clause, ATLAS escalates to Danesh |
| EVT-012 | M12 | Extreme winter — ground frozen solid, piling and concrete impossible for 18 days | AEGIS, VECTOR, BASTION, KRONOS, CLAIMS | KRONOS checks if exceptional vs baseline winter, CLAIMS prepares force majeure or EOT |

---

## PHASE 4 — Month 13 to Month 18 (Commissioning & Grid)

| Event ID | Month | Event | Agents Hit | Expected Chain Reaction |
|---|---|---|---|---|
| EVT-013 | M13 | PATRON issues scope change instruction — add 5MW BESS reserve area | ATLAS, COUNSEL, KRONOS, ARCHON, LEDGER | COUNSEL issues VO notice, KRONOS builds fragnet, LEDGER prices prolongation |
| EVT-014 | M14 | Protection relay settings rejected by UzbekEnergo — new reactive power spec | CIPHER, VOLTA, RELAY, GRIDLOCK, KRONOS | CIPHER recalculates settings, factory re-programming, KRONOS logs utility delay |
| EVT-015 | M15 | IV curve test shows 12% of strings in Block 4 below Fill Factor threshold | SPARK, OHMMETER, AMPERE, EREKTOR, SENTINEL | EREKTOR investigates, EL test ordered, microcracks found in 200 modules — vendor claim |
| EVT-016 | M16 | UzbekEnergo delays energisation consent by 4 weeks — internal approval backlog | GRIDLOCK, IGNITE, KRONOS, COUNSEL, ATLAS | COUNSEL documents utility delay, EOT notice, KRONOS shows COD impact, Danesh escalates |
| EVT-017 | M17 | Performance Ratio test result: 76% (target 80%) — below PAC threshold | IGNITE, GRIDLOCK, SPARK, SIGMA, PATRON | T&C investigates (soiling? shading? underperforming strings?), client withholds PAC |

---

## HOW TO INJECT AN EVENT (Instructions for Danesh/PD)

1. Open a new GitHub Issue in HELIOS-EPC-Simulation
2. Title: [EVENT] EVT-00X — [Event Name]
3. Tag the agents listed in "Agents Hit" in the body
4. Set Priority: HIGH or CRITICAL
5. The agents must respond within their defined escalation and workflow rules
6. Watch the Issue comments — that is the simulation playing out in real time

---

## NOTES
- Events can be injected earlier or later than the listed month
- Multiple events can run simultaneously (tests concurrent delay handling)
- Danesh can add new unlisted events at any time
- Agents must not know events are coming — they respond to them as if real
