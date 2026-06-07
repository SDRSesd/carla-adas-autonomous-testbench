"""
CARLA camera recording utility.

This module attaches an RGB camera behind the ego vehicle, saves raw frames
during scenario execution and converts them into an MP4 video after the test.

The intent is to provide visual validation evidence for GitHub portfolio
presentation and post-test review.
"""

import os
import cv2
import carla


class CarlaVideoRecorder:
    def __init__(
        self,
        world,
        blueprint_library,
        ego_vehicle,
        scenario_name,
        image_width=1280,
        image_height=720,
        fps=20
    ):
        self.world = world
        self.blueprint_library = blueprint_library
        self.ego_vehicle = ego_vehicle
        self.scenario_name = scenario_name
        self.image_width = image_width
        self.image_height = image_height
        self.fps = fps

        self.camera = None
        self.frame_count = 0

        self.frame_dir = f"videos/frames/{scenario_name}"
        self.video_path = f"videos/{scenario_name}.mp4"

        os.makedirs(self.frame_dir, exist_ok=True)
        os.makedirs("videos", exist_ok=True)

    def start(self):
        camera_bp = self.blueprint_library.find("sensor.camera.rgb")
        camera_bp.set_attribute("image_size_x", str(self.image_width))
        camera_bp.set_attribute("image_size_y", str(self.image_height))
        camera_bp.set_attribute("fov", "90")

        camera_transform = carla.Transform(
            carla.Location(x=-8.0, y=0.0, z=4.0),
            carla.Rotation(pitch=-15.0, yaw=0.0, roll=0.0)
        )

        self.camera = self.world.spawn_actor(
            camera_bp,
            camera_transform,
            attach_to=self.ego_vehicle
        )

        self.camera.listen(self._save_frame)
        print(f"[INFO] Video recording started: {self.video_path}")

    def _save_frame(self, image):
        file_path = f"{self.frame_dir}/frame_{self.frame_count:06d}.png"
        image.save_to_disk(file_path)
        self.frame_count += 1

    def stop(self):
        if self.camera is not None:
            self.camera.stop()
            self.camera.destroy()
            self.camera = None

        self._create_video()
        print(f"[INFO] Video saved: {self.video_path}")

    def _create_video(self):
        if self.frame_count == 0:
            print("[WARN] No video frames captured")
            return

        first_frame_path = f"{self.frame_dir}/frame_000000.png"
        first_frame = cv2.imread(first_frame_path)

        if first_frame is None:
            print("[WARN] Unable to read captured frames")
            return

        height, width, _ = first_frame.shape

        video_writer = cv2.VideoWriter(
            self.video_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            self.fps,
            (width, height)
        )

        for frame_index in range(self.frame_count):
            frame_path = f"{self.frame_dir}/frame_{frame_index:06d}.png"
            frame = cv2.imread(frame_path)

            if frame is not None:
                video_writer.write(frame)

        video_writer.release()