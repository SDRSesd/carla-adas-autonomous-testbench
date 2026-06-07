# CARLA ADAS Validation Testbench - Project Architecture

## 1. Project Objective

This project demonstrates a simulation-based ADAS validation workflow using CARLA and Python.

The objective is to create a modular validation testbench where different driving scenarios can be executed, measured and reviewed using logged vehicle telemetry and visual evidence.

The project is designed from an automotive validation perspective, focusing on:

* repeatable scenario execution
* measurable vehicle behavior
* controlled test conditions
* basic pass/fail evaluation
* evidence generation through CSV logs
* visual validation evidence through scenario videos
* modular Python test structure
* post-test review support using logs, console traces, screenshots and MP4 recordings

---

## 2. High-Level Architecture

```text
+------------------------------------------------+
|              CARLA Simulator Server            |
|------------------------------------------------|
| Vehicle world, roads, weather, actors, traffic |
| TCP server: localhost:2000                     |
+------------------------+-----------------------+
                         |
                         | CARLA Python API
                         |
+------------------------v-----------------------+
|              Python Scenario Client            |
|------------------------------------------------|
| Scenario setup                                  |
| Ego vehicle spawn                               |
| Obstacle / pedestrian spawn                     |
| Weather configuration                           |
| Control logic                                   |
| Runtime telemetry capture                       |
| Pass/fail decision                              |
| RGB camera recording                            |
+------------------------+-----------------------+
                         |
                         |
+------------------------v-----------------------+
|               Validation Evidence              |
|------------------------------------------------|
| CSV logs                                        |
| Console traces                                  |
| Screenshots                                     |
| MP4 scenario videos                             |
| Future: HTML/PDF reports                        |
+------------------------------------------------+
```

---

## 3. Software Modules

| Module                        | Responsibility                                                     |
| ----------------------------- | ------------------------------------------------------------------ |
| `main_autonomous_drive.py`    | Baseline autonomous driving validation using CARLA Traffic Manager |
| `emergency_brake_test.py`     | Obstacle-based emergency braking validation scenario               |
| `pedestrian_crossing_test.py` | Pedestrian warning-zone braking scenario                           |
| `wet_braking_test.py`         | Wet road braking behavior under rainy road condition               |
| `utils_logger.py`             | Common logging, speed calculation and console reporting utilities  |
| `video_recorder.py`           | CARLA RGB camera recording utility for scenario video evidence     |

---

## 4. Runtime Data Flow

```text
CARLA World
   |
   | Actor state
   v
Ego Vehicle Object
   |
   | Velocity / location / control state
   v
Scenario Script
   |
   | speed, throttle, brake, steer, position, status
   v
VehicleDataLogger
   |
   v
CSV Validation Log
```

---

## 5. Visual Evidence Capture Flow

A CARLA RGB camera sensor is attached behind the ego vehicle during scenario execution. The camera records the scenario from a third-person validation perspective and stores the final output as an MP4 file.

```text
Ego Vehicle
   |
   | Attached RGB Camera Sensor
   v
Frame Capture
   |
   | Temporary frame cache
   v
MP4 Scenario Video
```

The raw frame cache is stored temporarily under:

```text
videos/frames/
```

The final video evidence is stored under:

```text
videos/
```

This supports post-test review and gives visual proof of vehicle behavior during ADAS scenario execution.

---

## 6. Logged Parameters

| Signal               | Engineering Usage                                                      |
| -------------------- | ---------------------------------------------------------------------- |
| `time_s`             | Used to track scenario elapsed time                                    |
| `scenario`           | Used to identify the active validation scenario                        |
| `speed_kmph`         | Used to evaluate vehicle motion, stop condition and braking response   |
| `throttle`           | Used to verify acceleration command during baseline and approach phase |
| `brake`              | Used to confirm brake command activation during risk scenarios         |
| `steer`              | Used to observe lateral control behavior during autonomous movement    |
| `location_x`         | Used for vehicle position tracking in the simulation world             |
| `location_y`         | Used for vehicle position tracking in the simulation world             |
| `collision_detected` | Used to identify unsafe contact events during scenario execution       |
| `test_status`        | Used to track runtime pass/fail state for validation evidence          |

---

## 7. Implemented Scenarios

### 7.1 Baseline Autonomous Drive

Purpose:

* validate CARLA Python API connection
* spawn ego vehicle
* enable Traffic Manager autopilot
* monitor speed, steering, throttle and brake
* detect collision events
* capture MP4 visual evidence

Validation idea:

```text
PASS: Ego vehicle completes the configured drive cycle without collision.
FAIL: Collision event is detected during the drive cycle.
```

---

### 7.2 Emergency Braking Test

Purpose:

* spawn ego vehicle and stationary obstacle
* place obstacle ahead on a valid driving lane
* calculate actor-to-actor distance
* apply braking command when obstacle enters threshold
* verify whether vehicle reaches stop condition
* capture MP4 visual evidence

Validation idea:

```text
PASS: Vehicle stops after brake trigger without violating minimum safety distance.
FAIL: Vehicle does not stop within configured safety threshold.
```

---

### 7.3 Pedestrian Crossing Test

Purpose:

* create basic pedestrian crossing risk zone
* apply full brake when pedestrian enters warning distance
* validate stop response
* capture MP4 visual evidence

Validation idea:

```text
PASS: Vehicle stops when pedestrian enters warning zone.
FAIL: Vehicle does not stop within scenario duration.
```

---

### 7.4 Wet Road Braking Test

Purpose:

* apply wet/rainy weather condition in CARLA
* accelerate ego vehicle
* apply full braking
* estimate stopping distance
* capture MP4 visual evidence

Validation idea:

```text
PASS: Vehicle reaches stop threshold within configured test time.
FAIL: Vehicle does not stop within configured test time.
```

---

## 8. Validation Evidence

The project generates multiple forms of validation evidence for review.

| Evidence Type   | Output Location   | Purpose                                         |
| --------------- | ----------------- | ----------------------------------------------- |
| CSV logs        | `logs/`           | Signal-level review and post-test analysis      |
| Console traces  | PowerShell output | Runtime execution visibility                    |
| Screenshots     | `screenshots/`    | Static evidence for GitHub portfolio            |
| Scenario videos | `videos/`         | Visual proof of vehicle behavior                |
| Frame cache     | `videos/frames/`  | Temporary camera frames used for MP4 generation |

---

## 9. Video Evidence Outputs

| Scenario                  | Video Output                           |
| ------------------------- | -------------------------------------- |
| Baseline Autonomous Drive | `videos/baseline_autonomous_drive.mp4` |
| Emergency Braking         | `videos/emergency_brake_test.mp4`      |
| Pedestrian Crossing       | `videos/pedestrian_crossing_test.mp4`  |
| Wet Road Braking          | `videos/wet_braking_test.mp4`          |

---

## 10. Engineering Assumptions

* This is a simulation validation project, not production ADAS software.
* Control logic is intentionally simple and traceable.
* The project focuses on scenario design, telemetry logging, visual evidence and validation thinking.
* CARLA autopilot is used for baseline autonomous driving.
* Manual control commands are used for braking-specific scenarios.
* Current implementation uses rule-based thresholds, not machine learning perception.
* Video recording is used as validation evidence, not as a perception input.

---

## 11. Current Limitations

* No camera-based object detection yet.
* No LiDAR point cloud processing yet.
* No ROS bridge integration yet.
* No ISO 26262 safety case included.
* No formal requirement traceability matrix yet.
* Braking scenario uses distance-based logic instead of a full perception pipeline.
* MP4 video files may need compression before committing to GitHub if file size is high.

---

## 12. Future Engineering Improvements

* Add camera sensor recording for dataset-style image capture.
* Add LiDAR sensor capture.
* Add radar-style distance tracking.
* Add JSON-based scenario configuration.
* Add automated HTML/PDF validation report generation.
* Add scenario pass/fail summary dashboard.
* Add OpenDRIVE route-based scenario testing.
* Add ROS2 bridge integration.
* Add requirement-to-test-case traceability.
* Add GitHub Actions smoke test for Python syntax validation.
* Add video compression workflow for GitHub-friendly evidence uploads.
