# TECHNICAL MEMORANDUM

**DOCUMENT ID:** HEL-CV-MEM-0001  
**PROJECT:** HELIOS 100MW Solar PV + 33/220kV GSS, Uzbekistan  
**DISCIPLINE:** Civil & Structural Engineering (EN-02)  
**AUTHOR:** TERRA (Civil / Structural Lead Engineer)  
**REVIEWER:** ARCHON (Design Manager)  
**DATE:** 2026-10-06  
**STATUS:** Issued for Review / Event Action (REV 0)  
**SUBJECT:** Technical Assessment & Engineering Directives — Geotechnical Anomaly in Block 6: Shallow Bedrock at 0.8m Depth vs 1.5m Design Embedment (EVT-001)

---

## 1. Executive Summary & Event Context
During initial site geotechnical verification and pile driving advance in **Block 6**, competent bedrock was encountered at a depth of **0.80 m** below existing ground level (EGL). The approved Issued For Construction (IFC) foundation design basis (Document Ref: `HEL-ST-CAL-0010`) specifies standard direct hydraulic-rammed galvanized steel piles (C-channel / W-beam profiles) with a minimum design embedment depth of **1.50 m**.

Direct impact driving into the 0.8m rock stratum is physically unachievable with standard hydraulic ramming rigs. Forcing installation against refusal creates severe structural pile distortion, shaft buckling, and immediate hammer rejection. 

This memorandum establishes:
1. Technical and structural assessment under applicable Uzbek Building Codes (KMK / ShNK).
2. Frost depth versus bedrock heave dynamics.
3. Comparative evaluation of structural engineering remediation options.
4. Mandatory engineering directives for immediate site execution, geotechnical investigation, scheduling, and commercial notification under FIDIC Yellow Book Sub-Clause 4.12.

---

## 2. Technical & Regulatory Assessment

### 2.1 Design Embedment vs. Refusal Depth
The tender geotechnical baseline assumed homogenous, loose-to-medium dense alluvial sand/silt deposits ($N_{SPT} = 12-25$) across the entire solar field array. Under this assumption, 1.50 m embedment provides:
- Ultimate compressive capacity: $R_c \ge 45\text{ kN}$
- Ultimate aerodynamic uplift pull-out capacity: $R_t \ge 32\text{ kN}$ (governed by wind suction load combinations per KMK 2.01.07-96)
- Allowable lateral deflection under tracker wind drag: $\delta_h \le 15\text{ mm}$ at ground line.

At 0.80 m refusal:
- Overburden soil provides less than 35% of required lateral passive resistance ($E_{p}$).
- Without positive anchoring or socketing into the bedrock, tracker overturning moment under wind gust loading will yield the upper soil column, causing excessive lateral displacement, binding of tracker torque tubes, and structural failure of single-axis slew drives.
- Attempting to overdrive piles into competent rock results in flange buckling, web crippling, and top-of-pile elevation deviations exceeding project QC tolerance ($\pm 30\text{ mm}$ elevation, $\pm 1^\circ$ verticality).

### 2.2 Uzbek Building Code Compliance (KMK & ShNK)
- **KMK 2.02.01-98 / ShNK 2.02.01-19 ("Foundations of Buildings and Structures"):**
  - Section 2.25 to 2.29 stipulates foundation embedment depths relative to standard seasonal freezing depth ($d_{fn}$). For the Bukhara / Navoi semi-arid climate zone, $d_{fn} \approx 0.90\text{ m} - 1.10\text{ m}$.
  - Under normal cohesive or silty soils, embedment depth must satisfy $d \ge d_f$ to prevent frost heave (adfreezing shear stress along the pile shaft lifting foundations during freeze-thaw cycles).
  - **Clause 2.27 Exemption:** For solid, monolithic, non-weathered bedrock strata (Group I rock), foundation depth is **independent of seasonal frost penetration**, as solid rock is non-frost-susceptible (free moisture content is negligible and ice lensing cannot develop).
  - Consequently, encountering competent rock at 0.80 m eliminates the geotechnical frost heave hazard at the rock interface.
  - **However**, code compliance mandates that structural stability (overturning, uplift, sliding, and seismic shear per KMK 2.01.03-19 for MSK-64 Intensity 8-9) must be fully verified. Piles terminating loosely at 0.80 m without structural connection into the rock stratum violate KMK 2.02.01-98 ultimate limit state (ULS) requirements.

---

## 3. Engineering Solution Options Evaluation

| Option | Engineering Methodology | Structural & Geotechnical Feasibility | Equipment & Material Requirements | Schedule & Cost Impact | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option 1: DTH Pre-drilling + Rock Socket & Grout Backfill** | Drill pilot hole ($\varnothing 180 - 220\text{ mm}$) through 0.8m overburden and socket $400 - 600\text{ mm}$ into rock (total depth $1.20 - 1.40\text{ m}$). Insert pile profile and pressure-grout annulus with lean concrete / non-shrink cementitious grout (M15 / C12/15). | **High.** Rock socket provides massive shaft shear ($f_s \ge 350\text{ kPa}$) and tip resistance. 500mm socket exceeds 1.5m soil pullout and lateral resistance. | Crawler-mounted Down-The-Hole (DTH) pneumatic drill rig, high-pressure air compressor ($21\text{ bar}$), mobile grouting pump. | Rig mobilization 5-7 days. Drilling cycle: 8-12 min/hole vs 2 min/driven pile. Medium cost delta. | **PREFERRED (Primary Baseline)** |
| **Option 2: Micro-piling & Rock Anchors with Transition Flange** | Drill small-diameter hole ($\varnothing 75 - 100\text{ mm}$) $1.20 - 1.50\text{ m}$ into bedrock. Install high-tensile threaded steel bar (e.g. $\varnothing 32\text{ mm}$ SAS 670 / GEWI), structural epoxy/grout, and bolt to custom tracker stub column. | **High.** Superior axial tension capacity; excellent shear resistance in hard rock. | Rotary micro-piling rig, specialized threaded anchor tendons, structural epoxy, custom torque tube transition brackets. | High material cost for proprietary anchors. Custom bracket design and fabrication adds 3-4 weeks lead time. | **CONTINGENCY (For hard rock pinnacles)** |
| **Option 3: Surface Concrete Ballast / Spread Footings with Dowels** | Excavate 0.8m overburden to bedrock surface. Clean rock, drill and chemical-dowel $4\times \varnothing 16\text{ mm}$ rebars ($300\text{ mm}$ embedment with Hilti HIT-RE 500 V4 per KMK 2.02.01-98). Cast-in-place reinforced concrete plinth ($1.0\times 1.0\times 0.5\text{ m}$). | **Medium.** Structural stability achieved via gravity deadweight and rock dowels. Negates drilling deep holes in ultra-hard rock. | Backhoes, formwork, rebar bending yard, batching plant transit mixers, wet curing equipment. | Severe concrete consumption ($> 400\text{ m}^3$). Extreme thermal curing challenges in arid climate. Major cost escalation. | **REJECTED (Except for Inverter Stations)** |

### Selected Engineering Strategy:
Adopt **Option 1 (Pre-drilling with DTH Rock Tooling + Annular Grouting)** as the project standard for Block 6. This maintains the approved single-axis tracker geometry, pile top coordinate tolerances, and mechanical bracket interfaces without altering tracker supply packages from SOLARIS.

---

## 4. Multi-Disciplinary Action Directives

### 4.1 Directive to MERIDIAN (Survey & Geotechnical Engineer)
1. **Confirmatory Delineation Grid:** Mobilize immediate diamond core drilling rig to Block 6. Execute 6 to 8 confirmatory boreholes on a $50\text{ m}\times 50\text{ m}$ staggered grid to delineate the rock roof topography and establish whether the anomaly is an isolated pinnacle, a fault ridge, or a continuous sub-horizontal formation.
2. **Rock Core Testing:**
   - Unconfined Compressive Strength (UCS) per GOST 21153.2-84 / ASTM D7012.
   - Rock Quality Designation (RQD %) and Core Recovery (TCR/SCR).
   - Point Load Strength Index ($I_{s(50)}$).
   - Weathering classification (W1 fresh to W5 completely weathered per ISRM).
3. **Chemical & Thermal Aggressiveness:** Test groundwater and rock pore moisture for water-soluble sulfates ($SO_4^{2-}$) and chlorides ($Cl^-$) per KMK 2.02.01-98 to specify sulfate-resistant cement (SRC) for annular grout.
4. **Soil/Rock Resistivity:** Conduct Wenner 4-pin testing in Block 6 to evaluate rock resistivity impact on VOLTA's buried earthing grid calculations.

### 4.2 Directive to BASTION (Civil Supervision) & GROUNDWORK (Civil Subcontractor)
1. **Immediate SWA (Stop Work Authority):** Cease all standard direct hydraulic ramming of tracker piles in Block 6 with immediate effect. No pile shall be subjected to destructive driving against rock refusal.
2. **Refusal Threshold Definition:** Standard refusal is strictly defined as penetration rate $< 20\text{ mm}$ per 10 blows of hydraulic hammer, or 3 minutes of continuous hammering with zero penetration. Upon reaching this threshold, driving MUST stop immediately.
3. **Field Survey of Refused Piles:** For any piles previously driven and refused at $< 1.20\text{ m}$, survey and log coordinates $(X, Y, Z)$, plumbness, and refusal depth in the Pile Installation Record. Cutting off pile heads without TERRA written approval is strictly prohibited.
4. **Calibration Test Pile Campaign:** Following mobilization of trial pre-drilling equipment, install 3 calibrated test piles in Block 6:
   - 1 No. Axial Static Compression Test (ASTM D1143 / KMK 2.02.01-98).
   - 1 No. Static Tension (Pull-Out) Test (ASTM D3689).
   - 1 No. Lateral Load Test (ASTM D3966).
   - Hold point verification co-signed by BASTION and PLUMBLINE (QC).

### 4.3 Directive to ARCHON (Design Manager), KRONOS (Planning), & COUNSEL (Contracts)
1. **Commercial & Contractual Escalation (FIDIC Yellow Book 1999 Sub-Clause 4.12):**
   - The presence of competent bedrock at 0.80 m directly contradicts the Tender Geotechnical Baseline and Employer's Requirements (which indicated deep, drivable alluvial soils).
   - This constitutes an **Unforeseeable Physical Condition** under Sub-Clause 4.12.
   - **COUNSEL:** Issue formal Notice of Claim under Sub-Clause 20.1 to the Employer and Engineer immediately within the mandatory 28-day notice period, asserting entitlement to:
     - Extension of Time (EOT) under Sub-Clause 8.4(b).
     - Additional Cost incurred (DTH drilling equipment, air compressor mobilization, drill bits/tooling wear, grouting materials, and subcontractor standby costs).
2. **Schedule Impact & Mitigation (KRONOS):**
   - Open a formal entry in `11_Shared_Registers/Delay_Event_Log.md` for Event Ref `EVT-001`.
   - Re-sequence GROUNDWORK piling rigs from Block 6 to adjacent sandy blocks (Block 1 / Block 2) immediately to maintain daily pile production rates and eliminate contractor idle equipment standing charges.
   - Insert a Schedule Fragnet in the L3 P6 Master Schedule capturing: DTH rig procurement/mobilization (7 days), confirmatory geotech testing (5 days), test pile installation and 7-day grout curing, and reduced piling cycle rate (30-40 piles/day/rig).
3. **Design Revision (ARCHON):**
   - Authorize issuance of Field Design Change `FDC-CIV-001` (Rock Pre-drill & Grout Detail) and initiate Revision 1 update of `HEL-ST-CAL-0010` upon receipt of MERIDIAN's certified rock mechanical test data.

---

**APPROVED BY:**  
TERRA  
Civil / Structural Lead Engineer (EN-02)  
HELIOS 100MW Solar PV Project, Uzbekistan
