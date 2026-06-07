"""
Wet Braking Scenario - CARLA ADAS Validation

Objective:
Simulate rainy/wet road conditions and measure the vehicle stopping behavior
after a full brake command.

This is useful for demonstrating vehicle dynamics awareness and validation
thinking around road condition impact.
"""

import time
import carla

from utils_logger import (
    VehicleDataLogger,
    get_vehicle_speed_kmph,
    print_test_header,
    print_test_result
)


SCENARIO_NAME = "wet_braking_test"
CARLA_HOST = "127.0.0.1"
CARLA_PORT = 2000
ACCELERATION_TIME_SEC = 8
MAX_TEST_TIME_SEC = 35
STOP_SPEED_THRESHOLD_KMPH = 2.0


def set_wet_weather(world):
    weather = carla.WeatherParameters(
        cloudiness=90.0,
        precipitation=80.0,
        precipitation_deposits=85.0,
        wind_intensity=40.0,
        sun_altitude_angle=25.0
    )
    world.set_weather(weather)


def main():
    print_test_header("CARLA Wet Road Braking Validation")

    client = carla.Client(CARLA_HOST, CARLA_PORT)
    client.set_timeout(20.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    spawn_points = world.get_map().get_spawn_points()

    ego_vehicle = None
    logger = VehicleDataLogger(SCENARIO_NAME)

    try:
        set_wet_weather(world)

        ego_bp = blueprint_library.filter("vehicle.tesla.model3")[0]
        ego_vehicle = world.spawn_actor(ego_bp, spawn_points[0])

        print("[INFO] Wet weather applied")
        print("[INFO] Ego vehicle spawned")
        print(f"[INFO] Log file: {logger.log_file}")

        start_time = time.time()
        brake_start_location = None
        stop_location = None
        test_status = "RUNNING"

        while time.time() - start_time < MAX_TEST_TIME_SEC:
            elapsed_time = time.time() - start_time
            speed_kmph = get_vehicle_speed_kmph(ego_vehicle)
            location = ego_vehicle.get_location()

            if elapsed_time < ACCELERATION_TIME_SEC:
                control = carla.VehicleControl(throttle=0.55, brake=0.0, steer=0.0)
            else:
                control = carla.VehicleControl(throttle=0.0, brake=1.0, steer=0.0)

                if brake_start_location is None:
                    brake_start_location = location

            ego_vehicle.apply_control(control)

            if brake_start_location is not None and speed_kmph < STOP_SPEED_THRESHOLD_KMPH:
                stop_location = location
                test_status = "PASSED"

            logger.write_row(
                elapsed_time,
                speed_kmph,
                control.throttle,
                control.brake,
                control.steer,
                location.x,
                location.y,
                False,
                test_status
            )

            print(
                f"t={elapsed_time:05.2f}s | "
                f"speed={speed_kmph:06.2f} km/h | "
                f"throttle={control.throttle:.2f} | "
                f"brake={control.brake:.2f} | "
                f"status={test_status}"
            )

            if test_status == "PASSED":
                break

            time.sleep(0.1)

        if brake_start_location is not None and stop_location is not None:
            stopping_distance = brake_start_location.distance(stop_location)

            print_test_result(
                SCENARIO_NAME,
                "PASSED",
                f"Vehicle stopped under wet condition. Estimated stopping distance: {stopping_distance:.2f} m"
            )
        else:
            print_test_result(
                SCENARIO_NAME,
                "FAILED",
                "Vehicle did not stop within the configured test time"
            )

    finally:
        print("[INFO] Cleaning up CARLA actors")

        if ego_vehicle is not None:
            ego_vehicle.destroy()


if __name__ == "__main__":
    main()