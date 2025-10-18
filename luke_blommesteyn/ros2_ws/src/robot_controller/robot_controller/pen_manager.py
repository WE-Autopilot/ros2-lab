#!/usr/bin/env python3
from typing import Optional, Tuple

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from turtlesim.msg import Pose
from turtlesim.srv import SetPen


class PenManager(Node):
    """Change the turtle pen colour per quadrant and lift the pen after reaching the goal."""

    def __init__(self) -> None:
        super().__init__("pen_manager")
        self.declare_parameter("turtle_name", "weap_turtle")
        self.declare_parameter("pen_width", 4)

        turtle_name = self.get_parameter("turtle_name").get_parameter_value().string_value
        self._pen_client = self.create_client(SetPen, f"/{turtle_name}/set_pen")
        self._last_colour: Optional[Tuple[int, int, int]] = None
        self._pen_disabled = False

        self.create_subscription(
            Pose,
            f"/{turtle_name}/pose",
            self._on_pose,
            10,
        )
        self.create_subscription(
            Bool,
            f"/{turtle_name}/goal_reached",
            self._on_goal_status,
            10,
        )

    def _on_pose(self, pose: Pose) -> None:
        if self._pen_disabled:
            return

        colour = self._colour_for_pose(pose.x, pose.y)
        if colour == self._last_colour:
            return

        if not self._pen_client.service_is_ready():
            self.get_logger().warn(
                "Waiting for /set_pen service before updating colour...",
                throttle_duration_sec=5.0,
            )
            return

        request = SetPen.Request()
        request.r, request.g, request.b = colour
        request.width = self.get_parameter("pen_width").get_parameter_value().integer_value
        request.off = False

        future = self._pen_client.call_async(request)
        future.add_done_callback(self._set_pen_callback)
        self._last_colour = colour

        self.get_logger().info(
            f"Updated pen colour to RGB={colour} at x={pose.x:.2f}, y={pose.y:.2f}"
        )

    def _on_goal_status(self, msg: Bool) -> None:
        if not msg.data or self._pen_disabled:
            return
        self._pen_disabled = True

        if not self._pen_client.service_is_ready():
            self.get_logger().warn("Goal reached but /set_pen unavailable to lift pen.")
            return

        request = SetPen.Request()
        request.r = 0
        request.g = 0
        request.b = 0
        request.width = self.get_parameter("pen_width").get_parameter_value().integer_value
        request.off = True
        future = self._pen_client.call_async(request)
        future.add_done_callback(self._set_pen_callback)
        self.get_logger().info("Goal reached: pen lifted to preserve final pose.")

    def _set_pen_callback(self, future) -> None:
        try:
            future.result()
        except Exception as error:  # noqa: BLE001
            self.get_logger().error(f"SetPen service call failed: {error}")

    @staticmethod
    def _colour_for_pose(x: float, y: float) -> Tuple[int, int, int]:
        if x < 5.5 and y < 5.5:
            return (255, 99, 71)  # tomato
        if x < 5.5 and y >= 5.5:
            return (50, 205, 50)  # lime green
        if x >= 5.5 and y < 5.5:
            return (123, 104, 238)  # medium slate blue
        return (32, 178, 170)  # light sea green


def main(args=None) -> None:
    rclpy.init(args=args)
    node = PenManager()
    try:
        rclpy.spin(node)
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
