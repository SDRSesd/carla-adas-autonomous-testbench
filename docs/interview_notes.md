# Interview Notes

## Project Explanation

This project was developed to demonstrate simulation-based ADAS validation using CARLA and Python.

Instead of only running standard CARLA examples, I structured the project like an automotive validation testbench, with separate modules for baseline autonomous driving, emergency braking, pedestrian crossing and wet road braking.

---

## Why CARLA?

CARLA is useful for building virtual driving scenarios before physical vehicle testing. It allows engineers to simulate actors, vehicles, pedestrians, weather and road environments in a controlled way.

---

## What I Implemented

- Python-based CARLA client scripts
- Ego vehicle spawning
- Traffic Manager autopilot
- Collision sensor integration
- Emergency braking scenario
- Pedestrian warning-zone braking
- Wet road braking condition
- Runtime telemetry logging
- CSV evidence generation
- Modular project documentation

---

## Signals Logged

- Vehicle speed
- Throttle command
- Brake command
- Steering command
- Vehicle position
- Collision status
- Scenario status

---

## Engineering Thinking

The project follows a validation mindset:

1. Define the scenario.
2. Spawn required actors.
3. Execute controlled logic.
4. Log measurable signals.
5. Evaluate pass/fail status.
6. Save evidence for review.

---

## Limitations

The current project uses rule-based distance thresholds. It does not yet use camera-based perception, LiDAR processing or sensor fusion.

---

## Future Scope

The next planned step is to add sensor-based perception using CARLA camera and LiDAR data, followed by automated report generation.

---

## Visual Evidence Recording

To make the validation workflow more reviewable, I added a CARLA RGB camera recorder. The camera is attached behind the ego vehicle and records each scenario as an MP4 file.

This gives visual proof of the vehicle behavior along with CSV telemetry. In an engineering review, the CSV log supports signal-level analysis, while the video helps confirm scenario behavior visually.