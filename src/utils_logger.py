"""
Utility module for CARLA ADAS validation logging.

This file is intentionally kept small and readable. In real automotive
validation work, logging is usually separated from the scenario logic so that
test cases remain easy to review and maintain.
"""

import csv
import os
from datetime import datetime


class VehicleDataLogger:
    def __init__(self, scenario_name):
        self.scenario_name = scenario_name
        self.log_file = self._create_log_file()

    def _create_log_file(self):
        os.makedirs("logs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"logs/{self.scenario_name}_{timestamp}.csv"

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "time_s",
                "scenario",
                "speed_kmph",
                "throttle",
                "brake",
                "steer",
                "location_x",
                "location_y",
                "collision_detected",
                "test_status"
            ])

        return file_path

    def write_row(
        self,
        time_s,
        speed_kmph,
        throttle,
        brake,
        steer,
        location_x,
        location_y,
        collision_detected,
        test_status
    ):
        with open(self.log_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                round(time_s, 2),
                self.scenario_name,
                round(speed_kmph, 2),
                round(throttle, 2),
                round(brake, 2),
                round(steer, 2),
                round(location_x, 2),
                round(location_y, 2),
                collision_detected,
                test_status
            ])


def get_vehicle_speed_kmph(vehicle):
    velocity = vehicle.get_velocity()
    speed_mps = (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5
    return speed_mps * 3.6


def print_test_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_test_result(scenario_name, status, reason):
    print("\n" + "-" * 70)
    print(f"Scenario : {scenario_name}")
    print(f"Result   : {status}")
    print(f"Reason   : {reason}")
    print("-" * 70)