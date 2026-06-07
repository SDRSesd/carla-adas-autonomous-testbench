"""
CARLA ADAS Autonomous Driving Validation Testbench

Scenario:
- Spawn an ego vehicle.
- Enable CARLA Traffic Manager autopilot.
- Attach a collision sensor.
- Log speed, throttle, brake, steering and position.
- Run a short autonomous validation cycle.

Author focus:
This script is written like a validation engineer's first baseline test:
simple, measurable, repeatable and easy to extend.
"""

import time
import carla

from utils_logger import (
    VehicleDataLogger,
    get_vehicle_speed_kmph,
    print_test_header,
    print_test_result
)


SCENARIO_NAME = "baseline_autonomous_drive"
TEST_DURATION_SEC = 60
CARLA_HOST = "127.0.0.1"
CARLA_PORT = 2000


def get_safe_spawn_point(world):
    spawn_points = world.get_map().get_spawn_points()

    if not spawn_points:
        raise RuntimeError("No spawn points available in the selected CARLA map")

    return spawn_points[0]


def main():
    print_test_header("CARLA Baseline Autonomous Driving Validation")

    client = carla.Client(CARLA_HOST, CARLA_PORT)
    client.set_timeout(20.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    traffic_manager = client.get_trafficmanager(8000)
    traffic_manager.set_global_distance_to_leading_vehicle(2.5)

    ego_vehicle = None
    collision_sensor = None
    collision_detected = False

    logger = VehicleDataLogger(SCENARIO_NAME)

    def on_collision(event):
        nonlocal collision_detected
        collision_detected = True
        print("[FAULT] Collision detected during baseline drive")

    try:
        vehicle_bp = blueprint_library.filter("vehicle.tesla.model3")[0]
        spawn_point = get_safe_spawn_point(world)

        ego_vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        ego_vehicle.set_autopilot(True, traffic_manager.get_port())

        collision_bp = blueprint_library.find("sensor.other.collision")
        collision_sensor = world.spawn_actor(
            collision_bp,
            carla.Transform(),
            attach_to=ego_vehicle
        )
        collision_sensor.listen(on_collision)

        print("[INFO] Ego vehicle spawned successfully")
        print("[INFO] Autopilot enabled")
        print(f"[INFO] Log file: {logger.log_file}")

        start_time = time.time()
        test_status = "RUNNING"

        while time.time() - start_time < TEST_DURATION_SEC:
            elapsed_time = time.time() - start_time

            control = ego_vehicle.get_control()
            location = ego_vehicle.get_location()
            speed_kmph = get_vehicle_speed_kmph(ego_vehicle)

            if collision_detected:
                test_status = "FAILED"
            else:
                test_status = "RUNNING"

            logger.write_row(
                time_s=elapsed_time,
                speed_kmph=speed_kmph,
                throttle=control.throttle,
                brake=control.brake,
                steer=control.steer,
                location_x=location.x,
                location_y=location.y,
                collision_detected=collision_detected,
                test_status=test_status
            )

            print(
                f"t={elapsed_time:05.2f}s | "
                f"speed={speed_kmph:06.2f} km/h | "
                f"throttle={control.throttle:.2f} | "
                f"brake={control.brake:.2f} | "
                f"steer={control.steer:.2f} | "
                f"collision={collision_detected}"
            )

            time.sleep(0.2)

        if collision_detected:
            print_test_result(
                SCENARIO_NAME,
                "FAILED",
                "Collision event detected during autonomous driving cycle"
            )
        else:
            print_test_result(
                SCENARIO_NAME,
                "PASSED",
                "Vehicle completed baseline autonomous drive without collision"
            )

    finally:
        print("[INFO] Cleaning up CARLA actors")

        if collision_sensor is not None:
            collision_sensor.stop()
            collision_sensor.destroy()

        if ego_vehicle is not None:
            ego_vehicle.destroy()

        print("[INFO] Baseline test completed")


if __name__ == "__main__":
    main()