# The Busbar — Published Topics Tracking

Used for duplicate detection. **Every section of every edition gets recorded here**, so future editions can avoid repeating themes, products, recalls, deep-dives, forum threads, or videos.

Before writing a new edition, the agent reads this file end-to-end and skips any topic already covered. After writing, the agent appends new entries into the matching section.

## Stories Published

<!-- Format: - YYYY-MM-DD | Tag | One-line summary -->
- 2026-04-21 | Inverter | Victron Microgrid: frequency-droop load sharing, no central controller, scales to 400kW (VE.Bus firmware S97/S98)
- 2026-04-21 | Firmware | Lynx Smart BMS NG firmware v1.17 — DVCC charge instability fix; regression: cell serial IDs missing from diagnostics
- 2026-04-21 | Battery | SuperPack NG firmware v1.05 — 2C continuous discharge, wider temperature range, self-heating to -30°C
- 2026-04-21 | Firmware | Venus OS v3.72 — ESS safeguard, Pylontech CAN detection, Node-RED fixes (released 2026-03-30)
- 2026-04-21 | Industry | Victron 2026 product pipeline: MultiPlus 48V 20kVA, split-phase inverter, TR Smart 48/12 60A, Orion XS 12/12 70A
- 2026-04-21 | Battery | EVE MB31 314Ah cells at ~$83–$85/cell (4-pack retail); DIYSolarForum raw-cell economics discussion
- 2026-04-27 | Battery | Battle Born 100Ah technical note (31 Mar) — company claims melting positive terminal is intentional thermal-fuse mechanism (PA-765 polymer at 85°C, ~700 field activations, 0.4%); Will Prowse and Mike Sokol set up independent verification
- 2026-04-27 | Firmware | Multi RS firmware v1.29 (26 Mar) — Denmark grid code, phase-rotation detection, VE.Bus BMS NG safe-mode fix
- 2026-04-27 | Firmware | VictronConnect v6.32 (31 Mar) — trends-fetching fix, VE.Bus updater error 29 fix, Android Auto stability
- 2026-04-27 | Battery | Bluetti FridgePower Kickstarter launch (16 Apr) — 2,016Wh LiFePO4, 1,800W, 75mm slim, 10ms switchover, $759 backer
- 2026-04-27 | Firmware | JK Inverter-BMS V19.31B special firmware — Off-Grid Garage caution about parallel-BMS feature and RS485 inverter compatibility
- 2026-04-27 | Safety | Casely Power Pods recall reannounced (CPSC, 16 Apr) — 429,000 units, 1 fatality, model E33A 5,000 mAh MagSafe (lithium-ion power banks, not LFP)
- 2026-05-04 | Battery | Panbo / Ben Stein lithium-cycle test part 2 (28 Apr) — WattCycle 100Ah Mini past 1,100 cycles, projected 3,000–4,000 cycles vs 5,000-cycle marketing claim; Blue Heron 100Ah Extreme at 500 cycles with capacity-bump anomaly; 93.7% round-trip efficiency; vs Duracell flooded "16x cost per kWh"
- 2026-05-04 | Battery | Dragonfly Energy first Japanese patent allowance (23 Apr) — "Powderized Solid-State Electrolyte and Electroactive Materials"; foundation of dry-electrode all-solid-state cell roadmap; no near-term Battle Born product implication
- 2026-05-04 | Industry | OffGrid Benchmark public launch (late April) — independent review platform by Jordan Stambaugh (WA); 92 products at launch across 6 categories; no manufacturer payments; programmatic comparison engine
- 2026-05-04 | Marine | Victron M/V Cowboy case study (24 Apr) — 74-foot motor vessel rebuild; 2 of 4 Quattros not connected; double AC bonding; hand-loose DC terminations found via thermal imaging; rebuild used Ekrano GX + ARCO Zeus + GX Tank 140 modules
- 2026-05-04 | Industry | Trek Systems Victron 2-day hands-on training Denver (announced ~30 Apr) — 28–29 May; 16 RVTI Level-3 credit hours; 20-attendee cap

## Product Radar — Already Featured

<!-- Format: - YYYY-MM-DD | Manufacturer | Product name -->
- 2026-04-21 | Victron Energy | Lithium SuperPack NG 12.8V 100Ah
- 2026-04-21 | EG4 Electronics | Chargeverter GC (48V 100A, $549.99)
- 2026-04-21 | Victron Energy | TR Smart 48/12 60A (announced, not yet shipping)
- 2026-04-27 | Epoch Batteries | 12V 460Ah V2-T Elite Series (Group 8D, IP67, integrated 400A Class T fuse, ABYC/NMEA/NMMA, $2,199)
- 2026-04-27 | Bluetti | FridgePower (Kickstarter, 2,016Wh LiFePO4, 1,800W, $759 backer / $1,299 retail)
- 2026-04-27 | Bluetti | EnergyPro 13K (EP13K hybrid inverter + AT1 panel + EnergyPack 500 modular battery, from $7,919)
- 2026-05-04 | WattCycle | 12V 100Ah Mini Bluetooth LiFePO4 (Group 22NF, 1,280Wh, 100A BMS, IP65, no heater/CAN, $199 Amazon) — Lead test reference
- 2026-05-04 | Blue Heron | 100Ah 12.8V Group 27 LiFePO4 EXTREME Series (heater, Bluetooth, Victron-comm, NMEA 2000, 500A 3-sec pulse, UL 1973, $789) — Lead test reference
- 2026-05-04 | ARCO Marine | Zeus High-Energy Alternator Regulator (Bluetooth + CAN-bus + NMEA 2000, 12–48V, dual shunt input, ~$1,099 US) — featured in News 3 Cowboy case study

## Recalls — Already Covered

<!-- Format: - YYYY-MM-DD | Manufacturer | Recall ID / short description -->
- 2026-04-27 | Casely | Power Pods 5,000 mAh MagSafe (model E33A) — CPSC reannounced 16 April after fatality

## Background Deep-Dives — Already Done

<!-- Don't repeat the same angle on the same topic within ~6 months. Variation on the same subject is fine if the angle is genuinely different. -->
<!-- Format: - YYYY-MM-DD | Type | One-line summary of the angle/thesis -->
- 2026-04-21 | market_analysis | The 314Ah cell crossover: raw-cell economics vs pre-built packs in 2026, plus BMS compatibility friction (Redodo/Victron DVCC)
- 2026-04-27 | market_analysis | China's PV/battery export VAT rebate elimination (1 April 2026) — module pricing impact 10–14%, battery pricing impact lagging into late Q3/Q4 2026 and Q1 2027

## Community Pulse — Threads & Discussions Already Featured

<!-- Same forum thread/Reddit post should not appear twice. New replies in the same thread are not a reason to re-feature. -->
<!-- Format: - YYYY-MM-DD | Forum | Thread title / topic — short note -->
- 2026-04-21 | r/diysolar | WireSizer Pro Android beta testers wanted
- 2026-04-21 | r/vandwellers | It's nearly official, I can run AC 24/7 offgrid
- 2026-04-21 | DIYSolarForum | EVE 314Ah cells: charge to 3.65V per cell? (tech sheet discussion)
- 2026-04-27 | Airstream Forums | Battle Born 12V 100Ah Battery Failures: Field Reports, Testing, and Alternatives
- 2026-04-27 | iRV2 | Battleborn Battery Safety Issue
- 2026-04-27 | DIYSolarForum | BMS in LG Chem ESS modules (9 April thread)
- 2026-05-04 | r/diySolar | 12v LiFepO4 server rack batteries other than EG4 LL? (30 April) — unverified OP claim that EG4 has emailed customers about discontinuation; treated in edition as forum signal only
- 2026-05-04 | r/diySolar | AC Frequency Stability in Off Grid Systems (2 May) — 49–51 Hz drift question, hybrid-inverter AC-input frequency tolerance discussion
- 2026-05-04 | r/diySolar | Bluecarbon system connectivity (30 April) — concrete comms-quirk reports for the Chinese all-in-one inverter

## On the Bench — YouTube Videos Already Featured

<!-- Each VIDEO_ID appears at most once. New videos from the same channel are fine. -->
<!-- Format: - YYYY-MM-DD | VIDEO_ID | Channel — Title -->
- 2026-04-21 | GNKAUiY6izc | Trek Systems — Victron Energy Updates in 2026: New Products, All-In-One, Microgrid
- 2026-04-21 | HarRKsrqOss | DIY Solar Power with Will Prowse — 2026 Will Prowse Approved Solar Products: Which Ones Survived?!
- 2026-04-27 | BVbCD9NNxj4 | DIY Solar Power with Will Prowse — 12V 460Ah Epoch "V2-T" Marine Rated Battery! Holy Cow..
- 2026-04-27 | rVXyM-uU_0M | Off-Grid Garage — SOC Accuracy Test Result: New Gobelpower BMS vs JK-BMS vs Victron Smart Shunt
- 2026-04-27 | uT0mSH3991o | DIY Solar Power with Will Prowse — Battleborn Batteries Responds: Our Batteries Work Great! "Technical Note" Explained
