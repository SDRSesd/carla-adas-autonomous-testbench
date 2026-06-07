# ADAS Validation Plan

## 1. Purpose

This document defines the basic validation plan for the CARLA ADAS Autonomous Driving Validation Testbench.

The plan focuses on simulation-based functional validation of selected ADAS/autonomous driving scenarios.

---

## 2. Scope

The current validation scope includes:

- baseline autonomous driving
- obstacle-based emergency braking
- pedestrian warning-zone braking
- wet road braking behavior
- vehicle telemetry logging
- pass/fail status generation

---

## 3. Out of Scope

The current project does not include:

- production-grade AEB algorithm
- camera perception model
- LiDAR object detection
- radar fusion
- ISO 26262 safety case
- AUTOSAR integration
- real ECU deployment

---

## 4. Test Cases

| Test ID | Test Scenario | Objective | Expected Result |
|---|---|---|---|
| TC_ADAS_001 | Baseline Autonomous Drive | Validate ego vehicle autopilot and telemetry logging | Vehicle completes drive cycle without collision |
| TC_ADAS_002 | Emergency Braking | Validate braking when obstacle enters safety threshold | Vehicle stops before minimum safety distance violation |
| TC_ADAS_003 | Pedestrian Crossing | Validate braking when pedestrian enters warning zone | Vehicle applies braking and reaches stop condition |
| TC_ADAS_004 | Wet Road Braking | Validate stopping behavior under rainy/wet road condition | Vehicle reaches stop threshold within configured test time |

---

## 5. Entry Criteria

- CARLA simulator installed and running.
- Python CARLA module installed.
- Simulator map fully loaded.
- Port `localhost:2000` accessible.
- Scenario script launched from project root folder.

---

## 6. Exit Criteria

- Scenario execution completed.
- Runtime telemetry captured.
- CSV log generated.
- Console result shows pass/fail outcome.
- Actors are cleaned up after test completion.

---

## 7. Validation Signals

The following runtime signals are logged during each scenario execution. These signals are selected to support basic ADAS validation review, stop-condition analysis and post-test debugging.

| Signal | Engineering Usage |
|---|---|
| Speed | Used to evaluate vehicle motion, stop condition and braking response |
| Brake | Used to confirm brake command activation during risk scenarios |
| Throttle | Used to verify acceleration command during baseline and approach phase |
| Steering | Used to observe lateral control behavior during autonomous movement |
| Location X/Y | Used for position tracking and distance-based scenario evaluation |
| Collision flag | Used to identify unsafe contact events during scenario execution |
| Test status | Used to track runtime pass/fail state for validation evidence |

---

## 8. Evidence

The following evidence should be captured for portfolio presentation:

- CARLA simulator screenshot
- PowerShell execution screenshot
- generated CSV log screenshot
- GitHub repository link
- README explanation
- architecture diagram
- Scenario video recording from ego-vehicle camera
- MP4 evidence for baseline drive, emergency braking, pedestrian crossing and wet braking

---

## 9. Video Evidence

| Scenario                  | Video Output                           |
|---------------------------|----------------------------------------|
| Baseline Autonomous Drive | `videos/baseline_autonomous_drive.mp4` |
| Emergency Braking         | `videos/emergency_brake_test.mp4`      |
| Pedestrian Crossing       | `videos/pedestrian_crossing_test.mp4`  |
| Wet Road Braking          | `videos/wet_braking_test.mp4`          |

