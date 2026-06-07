"""
Emergency Braking Scenario - CARLA ADAS Validation

Objective:
Validate whether the ego vehicle can detect a stationary obstacle condition
using distance-based logic and apply braking before reaching the obstacle.

This is not a production AEB algorithm. It is a portfolio-level validation
scenario that demonstrates scenario design, vehicle telemetry logging and
safety threshold handling.
"""

import time
import math
import carla

from utils_logger import (
    VehicleDataLogger,
    get_vehicle_speed_kmph,
    print_test_header,
    print_test_result
)


SCENARIO_NAME = "emergency_brake_test"
CARLA_HOST = "127.0.0.1"
CARLA_PORT = 2000
TEST_DURATION_SEC = 45
BRAKE_TRIGGER_DISTANCE_M = 18.0
MIN_SAFE_DISTANCE_M = 5.0


def get_distance(actor_a, actor_b):
    loc_a = actor_a.get_location()
    loc_b = actor_b.get_location()

    dx = loc_a.x - loc_b.x
    dy = loc_a.y - loc_b.y
    dz = loc_a.z - loc_b.z

    return math.sqrt(dx * dx + dy * dy + dz * dz)


def main():
    print_test_header("CARLA Emergency Braking Validation")

    client = carla.Client(CARLA_HOST, CARLA_PORT)
    client.set_timeout(20.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    spawn_points = world.get_map().get_spawn_points()

    ego_vehicle = None
    obstacle_vehicle = None
    logger = VehicleDataLogger(SCENARIO_NAME)

    try:
        ego_bp = blueprint_library.filter("vehicle.tesla.model3")[0]
        obstacle_bp = blueprint_library.filter("vehicle.audi.tt")[0]

        ego_spawn = spawn_points[0]
        obstacle_spawn = spawn_points[1]

        ego_vehicle = world.spawn_actor(ego_bp, ego_spawn)
        obstacle_vehicle = world.spawn_actor(obstacle_bp, obstacle_spawn)

        print("[INFO] Ego vehicle and obstacle vehicle spawned")
        print(f"[INFO] Log file: {logger.log_file}")

        start_time = time.time()
        test_status = "RUNNING"
        brake_applied = False

        while time.time() - start_time < TEST_DURATION_SEC:
            elapsed_time = time.time() - start_time
            distance_m = get_distance(ego_vehicle, obstacle_vehicle)
            speed_kmph = get_vehicle_speed_kmph(ego_vehicle)
            location = ego_vehicle.get_location()

            if distance_m > BRAKE_TRIGGER_DISTANCE_M:
                control = carla.VehicleControl(throttle=0.45, brake=0.0, steer=0.0)
            else:
                control = carla.VehicleControl(throttle=0.0, brake=1.0, steer=0.0)
                brake_applied = True

            ego_vehicle.apply_control(control)

            if distance_m < MIN_SAFE_DISTANCE_M and speed_kmph > 2.0:
                test_status = "FAILED"
            elif brake_applied and speed_kmph < 2.0:
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
                break
            else:
                test_status = "RUNNING"

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
                f"distance={distance_m:06.2f} m | "
                f"brake={control.brake:.2f} | "
                f"status={test_status}"
            )

            if test_status == "FAILED":
                break

            time.sleep(0.1)

        if test_status == "PASSED":
            print_test_result(
                SCENARIO_NAME,
                "PASSED",
                "Vehicle stopped after brake trigger without violating minimum safe distance"
            )
        else:
            print_test_result(
                SCENARIO_NAME,
                "FAILED",
                "Vehicle did not stop within the defined safety threshold"
            )

    finally:
        print("[INFO] Cleaning up CARLA actors")

        if ego_vehicle is not None:
            ego_vehicle.destroy()

        if obstacle_vehicle is not None:
            obstacle_vehicle.destroy()


if __name__ == "__main__":
    main()