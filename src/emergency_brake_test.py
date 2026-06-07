"""
Emergency Braking Scenario - CARLA ADAS Validation

Objective:
Validate a basic emergency braking response when a stationary obstacle is placed
ahead of the ego vehicle in the same driving lane.

This version uses waypoint-based lane following so the vehicle does not drive
straight into buildings or junction structures.
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


SCENARIO_NAME = "emergency_brake_test"

CARLA_HOST = "127.0.0.1"
CARLA_PORT = 2000

TEST_DURATION_SEC = 45.0

OBSTACLE_DISTANCE_M = 65.0
BRAKE_TRIGGER_DISTANCE_M = 35.0
MIN_SAFE_DISTANCE_M = 8.0
STOP_SPEED_THRESHOLD_KMPH = 2.0
TARGET_SPEED_KMPH = 28.0


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def normalize_angle_deg(angle):
    while angle > 180.0:
        angle -= 360.0
    while angle < -180.0:
        angle += 360.0
    return angle


def get_distance(actor_a, actor_b):
    loc_a = actor_a.get_location()
    loc_b = actor_b.get_location()
    return loc_a.distance(loc_b)


def find_stable_test_waypoint(world):
    """
    Finds a driving-lane waypoint with enough forward road distance.
    This avoids random spawn points near buildings, stairs or tight junctions.
    """
    carla_map = world.get_map()
    spawn_points = carla_map.get_spawn_points()

    for spawn in spawn_points:
        waypoint = carla_map.get_waypoint(
            spawn.location,
            project_to_road=True,
            lane_type=carla.LaneType.Driving
        )

        if waypoint is None:
            continue

        if waypoint.is_junction:
            continue

        route = [waypoint]
        current_wp = waypoint
        route_ok = True

        for _ in range(16):
            next_wps = current_wp.next(5.0)

            if not next_wps:
                route_ok = False
                break

            current_wp = next_wps[0]

            if current_wp.is_junction:
                route_ok = False
                break

            route.append(current_wp)

        if route_ok and len(route) >= 12:
            return waypoint

    raise RuntimeError("Unable to find a stable straight driving-lane waypoint")


def get_waypoint_ahead(start_waypoint, distance_m):
    next_wps = start_waypoint.next(distance_m)

    if not next_wps:
        raise RuntimeError("Unable to find waypoint ahead for obstacle placement")

    return next_wps[0]


def set_spectator_view(world, vehicle):
    vehicle_transform = vehicle.get_transform()
    forward_vector = vehicle_transform.get_forward_vector()

    spectator_location = carla.Location(
        x=vehicle_transform.location.x - forward_vector.x * 14.0,
        y=vehicle_transform.location.y - forward_vector.y * 14.0,
        z=vehicle_transform.location.z + 7.0
    )

    spectator_rotation = carla.Rotation(
        pitch=-22.0,
        yaw=vehicle_transform.rotation.yaw,
        roll=0.0
    )

    world.get_spectator().set_transform(
        carla.Transform(spectator_location, spectator_rotation)
    )


def calculate_lane_follow_steer(world, vehicle):
    """
    Simple waypoint steering controller.
    This is not production lateral control. It is enough for a controlled
    validation scenario and keeps the ego vehicle on the road.
    """
    carla_map = world.get_map()
    vehicle_transform = vehicle.get_transform()
    vehicle_location = vehicle_transform.location

    current_wp = carla_map.get_waypoint(
        vehicle_location,
        project_to_road=True,
        lane_type=carla.LaneType.Driving
    )

    if current_wp is None:
        return 0.0

    lookahead_wps = current_wp.next(8.0)

    if not lookahead_wps:
        return 0.0

    target_location = lookahead_wps[0].transform.location

    dx = target_location.x - vehicle_location.x
    dy = target_location.y - vehicle_location.y

    target_yaw = math.degrees(math.atan2(dy, dx))
    current_yaw = vehicle_transform.rotation.yaw

    yaw_error = normalize_angle_deg(target_yaw - current_yaw)

    steer = clamp(yaw_error / 45.0, -0.45, 0.45)

    return steer


def main():
    print_test_header("CARLA Emergency Braking Validation")

    client = carla.Client(CARLA_HOST, CARLA_PORT)
    client.set_timeout(20.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    ego_vehicle = None
    obstacle_vehicle = None
    video_recorder = None
    logger = VehicleDataLogger(SCENARIO_NAME)
    

    try:
        ego_bp = blueprint_library.filter("vehicle.tesla.model3")[0]
        obstacle_bp = blueprint_library.filter("vehicle.audi.tt")[0]

        start_waypoint = find_stable_test_waypoint(world)
        obstacle_waypoint = get_waypoint_ahead(start_waypoint, OBSTACLE_DISTANCE_M)

        ego_transform = start_waypoint.transform
        obstacle_transform = obstacle_waypoint.transform

        ego_transform.location.z += 0.4
        obstacle_transform.location.z += 0.4

        ego_vehicle = world.try_spawn_actor(ego_bp, ego_transform)

        if ego_vehicle is None:
            raise RuntimeError("Unable to spawn ego vehicle. Restart CARLA and try again.")

        obstacle_vehicle = world.try_spawn_actor(obstacle_bp, obstacle_transform)

        if obstacle_vehicle is None:
            raise RuntimeError("Unable to spawn obstacle vehicle. Restart CARLA and try again.")

        obstacle_vehicle.set_simulate_physics(False)

        set_spectator_view(world, ego_vehicle)

        video_recorder = CarlaVideoRecorder(
            world=world,
            blueprint_library=blueprint_library,
            ego_vehicle=ego_vehicle,
            scenario_name=SCENARIO_NAME
        )
        video_recorder.start()

        print("[INFO] Ego vehicle spawned on stable driving lane")
        print("[INFO] Stationary obstacle placed ahead on same lane")
        print(f"[INFO] Obstacle distance       : {OBSTACLE_DISTANCE_M} m")
        print(f"[INFO] Brake trigger distance : {BRAKE_TRIGGER_DISTANCE_M} m")
        print(f"[INFO] Minimum safe distance  : {MIN_SAFE_DISTANCE_M} m")
        print(f"[INFO] Target speed           : {TARGET_SPEED_KMPH} km/h")
        print(f"[INFO] Log file               : {logger.log_file}")

        time.sleep(1.0)

        start_time = time.time()
        brake_applied = False
        test_status = "RUNNING"
        result_reason = "Scenario ended before pass/fail decision"

        while time.time() - start_time < TEST_DURATION_SEC:
            elapsed_time = time.time() - start_time

            distance_m = get_distance(ego_vehicle, obstacle_vehicle)
            speed_kmph = get_vehicle_speed_kmph(ego_vehicle)
            location = ego_vehicle.get_location()

            steer_cmd = calculate_lane_follow_steer(world, ego_vehicle)

            if distance_m > BRAKE_TRIGGER_DISTANCE_M:
                if speed_kmph < TARGET_SPEED_KMPH:
                    throttle_cmd = 0.38
                else:
                    throttle_cmd = 0.08

                brake_cmd = 0.0
            else:
                throttle_cmd = 0.0
                brake_cmd = 1.0
                brake_applied = True

            control = carla.VehicleControl(
                throttle=throttle_cmd,
                brake=brake_cmd,
                steer=steer_cmd
            )

            ego_vehicle.apply_control(control)

            if brake_applied and speed_kmph <= STOP_SPEED_THRESHOLD_KMPH and distance_m > MIN_SAFE_DISTANCE_M:
                test_status = "PASSED"
                result_reason = "Vehicle stopped after brake trigger while maintaining safe distance"

            elif distance_m <= MIN_SAFE_DISTANCE_M and speed_kmph > STOP_SPEED_THRESHOLD_KMPH:
                test_status = "FAILED"
                result_reason = "Vehicle entered minimum safe distance before stop condition"

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
                collision_detected=False,
                test_status=test_status
            )

            print(
                f"t={elapsed_time:05.2f}s | "
                f"speed={speed_kmph:06.2f} km/h | "
                f"distance={distance_m:06.2f} m | "
                f"steer={control.steer:+.2f} | "
                f"brake={control.brake:.2f} | "
                f"status={test_status}"
            )

            if test_status in ["PASSED", "FAILED"]:
                break

            time.sleep(0.1)

        print_test_result(SCENARIO_NAME, test_status, result_reason)

    finally:
        print("[INFO] Cleaning up CARLA actors")

        if video_recorder is not None:
            video_recorder.stop()

        if ego_vehicle is not None:
            ego_vehicle.destroy()

        if obstacle_vehicle is not None:
            obstacle_vehicle.destroy()


if __name__ == "__main__":
    main()