# CARLA ADAS Validation Testbench - Project Architecture

## 1. Project Objective

This project demonstrates a simulation-based ADAS validation workflow using CARLA and Python.

The objective is to create a modular validation testbench where different driving scenarios can be executed, measured and reviewed using logged vehicle telemetry.

The project is designed from an automotive validation perspective, focusing on:

- repeatable scenario execution
- measurable vehicle behavior
- controlled test conditions
- basic pass/fail evaluation
- evidence generation through CSV logs
- modular Python test structure

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
| Scenario setup                                 |
| Ego vehicle spawn                              |
| Obstacle / pedestrian spawn                    |
| Weather configuration                          |
| Control logic                                  |
| Runtime telemetry capture                      |
| Pass/fail decision                             |
+------------------------+-----------------------+
                         |
                         |
+------------------------v-----------------------+
|               Validation Evidence              |
|------------------------------------------------|
| CSV logs                                       |
| Console traces                                 |
| Screenshots                                    |
| Future: HTML/PDF reports                       |
+------------------------------------------------+