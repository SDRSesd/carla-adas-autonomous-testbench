# Development Timeline

## Phase 1 - Environment Setup

- Downloaded and configured CARLA 0.9.16.
- Installed CARLA Python API from the packaged wheel file.
- Verified simulator-client communication through `localhost:2000`.
- Confirmed basic CARLA example script execution.

---

## Phase 2 - Project Structure

- Created modular Python project structure.
- Added source, documentation, reports, logs and screenshots folders.
- Added `.gitignore` to avoid committing runtime files and CARLA binaries.
- Added basic dependency file.

---

## Phase 3 - Baseline Autonomous Drive

- Implemented ego vehicle spawn.
- Enabled CARLA Traffic Manager autopilot.
- Added collision sensor.
- Logged vehicle speed, throttle, brake, steer and position.
- Added baseline pass/fail logic.

---

## Phase 4 - Scenario-Based ADAS Tests

- Added emergency braking scenario.
- Added pedestrian crossing scenario.
- Added wet road braking scenario.
- Added scenario-specific thresholds and stop conditions.

---

## Phase 5 - Validation Evidence

- Added reusable CSV logger.
- Added validation plan.
- Added sample test summary.
- Added architecture documentation.
- Prepared project for GitHub portfolio presentation.

---

## Phase 6 - Visual Validation Evidence

- Added CARLA RGB camera sensor recording.
- Attached scenario camera behind ego vehicle.
- Generated MP4 video evidence for each validation scenario.
- Excluded raw frame cache from Git tracking.
- Updated README, validation plan and project architecture with video evidence workflow.

---

## Phase 7 - Planned Enhancements

- Add LiDAR capture.
- Add JSON scenario configuration.
- Add automated HTML/PDF reports.
- Add visual dashboard.
- Add ROS2 bridge integration.