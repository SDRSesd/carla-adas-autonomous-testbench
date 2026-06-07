"""
Pedestrian Crossing Scenario - CARLA ADAS Validation

Objective:
Create a basic pedestrian crossing risk scenario and apply controlled braking
when the pedestrian enters a defined safety zone.

This demonstrates scenario-based ADAS validation, not a production pedestrian
detection algorithm.
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

from video_recorder import CarlaVideoRecorder


SCENARIO_NAME = "pedestrian_crossing_test"
CARLA_HOST = "127.0.0.1"
CARLA_PORT = 2000
TEST_DURATION_SEC = 40
PEDESTRIAN_WARNING_DISTANCE_M = 15.0


def get_distance(actor_a, actor_b):
    loc_a = actor_a.get_location()
    loc_b = actor_b.get_location()

    dx = loc_a.x - loc_b.x
    dy = loc_a.y - loc_b.y
    dz = loc_a.z - loc_b.z

    return math.sqrt(dx * dx + dy * dy + dz * dz)


def main():
    print_test_header("CARLA Pedestrian Crossing Validation")

    client = carla.Client(CARLA_HOST, CARLA_PORT)
    client.set_timeout(20.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    spawn_points = world.get_map().get_spawn_points()

    ego_vehicle = None
    pedestrian = None
    video_recorder = None
    logger = VehicleDataLogger(SCENARIO_NAME)

    try:
        ego_bp = blueprint_library.filter("vehicle.tesla.model3")[0]
        walker_bp = blueprint_library.filter("walker.pedestrian.*")[0]

        ego_spawn = spawn_points[0]
        pedestrian_transform = carla.Transform(
            carla.Location(
                x=ego_spawn.location.x + 22.0,
                y=ego_spawn.location.y + 2.0,
                z=ego_spawn.location.z
            ),
            carla.Rotation()
        )

        ego_vehicle = world.spawn_actor(ego_bp, ego_spawn)
        pedestrian = world.spawn_actor(walker_bp, pedestrian_transform)

        video_recorder = CarlaVideoRecorder(
            world=world,
            blueprint_library=blueprint_library,
            ego_vehicle=ego_vehicle,
            scenario_name=SCENARIO_NAME
        )
        video_recorder.start()

        print("[INFO] Ego vehicle and pedestrian spawned")
        print(f"[INFO] Log file: {logger.log_file}")

        start_time = time.time()
        test_status = "RUNNING"
        brake_applied = False

        while time.time() - start_time < TEST_DURATION_SEC:
            elapsed_time = time.time() - start_time
            distance_m = get_distance(ego_vehicle, pedestrian)
            speed_kmph = get_vehicle_speed_kmph(ego_vehicle)
            location = ego_vehicle.get_location()

            if distance_m <= PEDESTRIAN_WARNING_DISTANCE_M:
                control = carla.VehicleControl(throttle=0.0, brake=1.0, steer=0.0)
                brake_applied = True
            else:
                control = carla.VehicleControl(throttle=0.35, brake=0.0, steer=0.0)

            ego_vehicle.apply_control(control)

            if brake_applied and speed_kmph < 2.0:
                test_status = "PASSED"
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
                f"pedestrian_distance={distance_m:06.2f} m | "
                f"brake={control.brake:.2f} | "
                f"status={test_status}"
            )

            if test_status == "PASSED":
                break

            time.sleep(0.1)

        if test_status == "PASSED":
            print_test_result(
                SCENARIO_NAME,
                "PASSED",
                "Vehicle stopped when pedestrian entered the warning zone"
            )
        else:
            print_test_result(
                SCENARIO_NAME,
                "FAILED",
                "Vehicle did not reach full stop within the scenario duration"
            )

    finally:
        print("[INFO] Cleaning up CARLA actors")

        if video_recorder is not None:
            video_recorder.stop()

        if ego_vehicle is not None:
            ego_vehicle.destroy()

        if pedestrian is not None:
            pedestrian.destroy()


if __name__ == "__main__":
    main()