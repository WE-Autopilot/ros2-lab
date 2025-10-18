#!/usr/bin/env python3
import math
from typing import Optional, Tuple

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import Bool
from turtlesim.msg import Pose


def shortest_angular_distance(current: float, target: float) -> float:
    """Compute the wrapped angular distance in radians."""
    delta = (target - current + math.pi) % (2.0 * math.pi) - math.pi
    return delta


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


class WaypointController(Node):
    """Drive the turtlesim turtle to a goal pose with a simple P controller."""

    def __init__(self) -> None:
        super().__init__("waypoint_controller")
        self.declare_parameter("turtle_name", "weap_turtle")
        self.declare_parameter("target_x", 9.0)
        self.declare_parameter("target_y", 9.0)
        self.declare_parameter("linear_gain", 1.5)
        self.declare_parameter("angular_gain", 4.0)
        self.declare_parameter("max_linear_speed", 2.0)
        self.declare_parameter("max_angular_speed", 4.0)
        self.declare_parameter("goal_tolerance", 0.4)

        turtle_name = self.get_parameter("turtle_name").get_parameter_value().string_value
        self._cmd_publisher = self.create_publisher(Twist, f"/{turtle_name}/cmd_vel", 10)
        self._goal_publisher = self.create_publisher(Bool, f"/{turtle_name}/goal_reached", 10)
        self._pose_subscription = self.create_subscription(
            Pose,
            f"/{turtle_name}/pose",
            self._on_pose,
            10,
        )

        self._last_pose: Optional[Pose] = None
        self._goal_announced = False
        self.create_timer(2.0, self._log_progress)

    def _on_pose(self, pose: Pose) -> None:
        self._last_pose = pose
        target_x = self.get_parameter("target_x").get_parameter_value().double_value
        target_y = self.get_parameter("target_y").get_parameter_value().double_value

        distance, heading_error = self._compute_errors(pose, target_x, target_y)
        if distance <= self.get_parameter("goal_tolerance").get_parameter_value().double_value:
            self._publish_goal(True)
            self._publish_twist(0.0, 0.0)
            return

        linear_gain = self.get_parameter("linear_gain").get_parameter_value().double_value
        angular_gain = self.get_parameter("angular_gain").get_parameter_value().double_value
        max_linear = self.get_parameter("max_linear_speed").get_parameter_value().double_value
        max_angular = self.get_parameter("max_angular_speed").get_parameter_value().double_value

        angular_speed = clamp(angular_gain * heading_error, -max_angular, max_angular)
        linear_speed = clamp(linear_gain * distance, 0.0, max_linear)
        if abs(heading_error) > math.radians(60):
            linear_speed *= 0.25

        self._publish_twist(linear_speed, angular_speed)
        self._publish_goal(False)

    def _compute_errors(self, pose: Pose, target_x: float, target_y: float) -> Tuple[float, float]:
        dx = target_x - pose.x
        dy = target_y - pose.y
        distance = math.hypot(dx, dy)
        target_heading = math.atan2(dy, dx)
        heading_error = shortest_angular_distance(pose.theta, target_heading)
        return distance, heading_error

    def _publish_twist(self, linear: float, angular: float) -> None:
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self._cmd_publisher.publish(msg)

    def _publish_goal(self, reached: bool) -> None:
        if reached and self._goal_announced:
            return

        msg = Bool()
        msg.data = reached
        self._goal_publisher.publish(msg)
        if reached:
            self._goal_announced = True

    def _log_progress(self) -> None:
        if self._last_pose is None:
            self.get_logger().info("Waiting for first pose...", throttle_duration_sec=5.0)
            return

        target_x = self.get_parameter("target_x").get_parameter_value().double_value
        target_y = self.get_parameter("target_y").get_parameter_value().double_value
        distance, heading_error = self._compute_errors(self._last_pose, target_x, target_y)
        heading_deg = math.degrees(heading_error)
        self.get_logger().info(
            f"Pose x={self._last_pose.x:.2f}, y={self._last_pose.y:.2f}, "
            f"distance to goal={distance:.2f}, heading error={heading_deg:.1f} deg"
        )


def main(args=None) -> None:
    rclpy.init(args=args)
    node = WaypointController()
    try:
        rclpy.spin(node)
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
