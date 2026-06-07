# CARLA ADAS Autonomous Driving Validation Testbench

## Overview

This project is a simulation-based ADAS and autonomous driving validation testbench built using the CARLA simulator and Python API.

The project demonstrates how virtual driving scenarios can be created, executed and evaluated before moving toward vehicle-level testing.

The focus is not only on running CARLA, but on building a structured validation workflow with:

- scenario setup
- vehicle actor control
- runtime telemetry logging
- collision monitoring
- threshold-based decision logic
- CSV-based validation evidence
- modular Python test cases

---

## Project Motivation

Automotive software development increasingly depends on simulation-driven validation, especially for ADAS, autonomous driving and vehicle dynamics use cases.

This project was created to demonstrate hands-on experience in:

- ADAS scenario validation
- autonomous driving simulation
- Python-based test automation
- vehicle telemetry analysis
- simulation-based engineering workflow
- validation evidence generation

---

## Key Features

- CARLA simulator integration
- Ego vehicle spawning and control
- CARLA Traffic Manager autopilot usage
- Emergency braking validation
- Pedestrian crossing risk scenario
- Wet road braking scenario
- Collision sensor integration
- Runtime vehicle telemetry logging
- CSV evidence generation
- Modular senior-engineering style project structure

---

## Tools and Technologies

| Area            | Tools / Technologies |
|-----------------|----------------------|
| Simulator       | CARLA 0.9.16         |
| Programming     | Python               |
| API             | CARLA Python API     |
| Platform        | Windows              |
| Execution       | PowerShell           |
| Data Logging    | CSV                  |
| Version Control | Git and GitHub       |

---

## Project Structure

```text
carla-adas-autonomous-testbench
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src
│   ├── main_autonomous_drive.py
│   ├── utils_logger.py
│   ├── video_recorder.py
│   ├── emergency_brake_test.py
│   ├── pedestrian_crossing_test.py
│   └── wet_braking_test.py
│
├── logs
│   └── .gitkeep
│
├── reports
│   ├── .gitkeep
│   ├── validation_plan.md
│   └── sample_test_summary.md
│
├── screenshots
│   ├── .gitkeep
│   ├── baseline_autonomous_drive_console.png
│   ├── pedestrian_crossing_validation_console.png
│   ├── wet_braking_validation_console.png
│   └── emergency_brake_test_passed.png
│
├── videos
│   ├── .gitkeep
│   ├── emergency_brake_test.mp4
│   └── frames
│       └── .gitkeep
│
└── docs
    ├── project_architecture.md
    ├── development_timeline.md
    └── interview_notes.md
```

---

## Scenario Video Evidence

The emergency braking scenario includes ego-vehicle camera recording for visual validation evidence.

| Scenario          | Evidence                          |
| ----------------- | --------------------------------- |
| Emergency Braking | `videos/emergency_brake_test.mp4` |

The video is captured using a CARLA RGB camera sensor attached behind the ego vehicle. This provides a real-time view of the scenario execution and supports post-test validation review.

The raw frame cache is stored under `videos/frames/` during execution and is excluded from Git tracking to avoid committing large temporary image files.


