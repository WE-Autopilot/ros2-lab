#!/usr/bin/env python3
from typing import Optional

import rclpy
from rclpy.node import Node
from turtlesim.srv import Kill, Spawn


class InitialSetup(Node):
    """Replace the default turtlesim turtle with a named turtle at a chosen pose."""

    def __init__(self) -> None:
        super().__init__("initial_setup")
        self.declare_parameter("turtle_name", "weap_turtle")
        self.declare_parameter("kill_default", True)
        self.declare_parameter("spawn_x", 5.5)
        self.declare_parameter("spawn_y", 5.5)
        self.declare_parameter("spawn_theta", 0.0)

        self._kill_client = self.create_client(Kill, "/kill")
        self._spawn_client = self.create_client(Spawn, "/spawn")
        self._has_finished = False

        # Timer retries the setup until services are available.
        self.create_timer(0.2, self._attempt_setup)

    def _attempt_setup(self) -> None:
        if self._has_finished:
            return

        if not self._spawn_client.service_is_ready():
            self.get_logger().info("Waiting for /spawn service...", throttle_duration_sec=5.0)
            return

        if (
            self.get_parameter("kill_default").get_parameter_value().bool_value
            and not self._kill_client.service_is_ready()
        ):
            self.get_logger().info("Waiting for /kill service...", throttle_duration_sec=5.0)
            return

        turtle_name = self.get_parameter("turtle_name").get_parameter_value().string_value
        spawn_x = self.get_parameter("spawn_x").get_parameter_value().double_value
        spawn_y = self.get_parameter("spawn_y").get_parameter_value().double_value
        spawn_theta = self.get_parameter("spawn_theta").get_parameter_value().double_value

        if self.get_parameter("kill_default").get_parameter_value().bool_value:
            kill_request = Kill.Request()
            kill_request.name = "turtle1"
            if not self._call_service(self._kill_client, kill_request):
                self.get_logger().error("Failed to kill turtle1.")
                return
            self.get_logger().info("Successfully removed default turtle1.")

        spawn_request = Spawn.Request()
        spawn_request.x = float(spawn_x)
        spawn_request.y = float(spawn_y)
        spawn_request.theta = float(spawn_theta)
        spawn_request.name = turtle_name

        if not self._call_service(self._spawn_client, spawn_request):
            self.get_logger().error(f"Failed to spawn turtle '{turtle_name}'.")
            return

        self.get_logger().info(
            f"Spawned turtle '{turtle_name}' at ({spawn_x:.2f}, {spawn_y:.2f}, {spawn_theta:.2f} rad)."
        )
        self._has_finished = True
        self.destroy_node()

    def _call_service(self, client, request) -> bool:
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=3.0)
        if not future.done():
            self.get_logger().error("Service call timed out.")
            return False

        try:
            future.result()
        except Exception as error:  # noqa: BLE001
            self.get_logger().error(f"Service call failed: {error}")
            return False
        return True


def main(args=None) -> None:
    rclpy.init(args=args)
    node = InitialSetup()
    try:
        rclpy.spin(node)
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
