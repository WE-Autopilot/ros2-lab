#!/usr/bin/env python3
import math
import random

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import turtlesim.msg as tmsg
import turtlesim.srv as tsrv


class LoopNode(Node):
    """
    Drive the turtle along a figure-eight / infinity symbol using a parametric
    path and a simple heading controller. After each full period the node
    requests /turtle1/set_pen to change color.
    """
    def __init__(self):
        super().__init__('loop_node')

        # publisher and subscriber
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose = None
        self.create_subscription(tmsg.Pose, '/turtle1/pose', self._pose_cb, 10)

        # service client for changing pen
        self.set_pen_client = self.create_client(tsrv.SetPen, '/turtle1/set_pen')
        if not self.set_pen_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn('/turtle1/set_pen service not available (pen changes will be skipped)')

        # path parameters
        self.A = 2.0                # x amplitude (meters, turtlesim units)
        self.B = 1.5                # y amplitude
        self.omega = 0.8            # angular speed for param t
        self.period = (2.0 * math.pi) / self.omega

        # controller gains
        self.k_ang = 5.0
        self.k_lin = 1.5
        self.max_lin = 2.0

        # time integration
        self.dt = 0.05              # seconds per timer tick (20 Hz)
        self.t = 0.0
        self.last_period_count = 0

        # offset to place figure-eight in the middle of the turtlesim window
        self.x0 = 5.5
        self.y0 = 5.5

        # timer driving control loop
        self.create_timer(self.dt, self._timer_cb)

        self.get_logger().info('LoopNode started; driving figure-eight path')

    def _pose_cb(self, msg: tmsg.Pose):
        self.pose = msg

    def _desired_xy(self, t):
        # parametric figure-eight (Lissajous-ish): x = A sin(w t), y = B sin(2 w t)
        x = self.x0 + self.A * math.sin(self.omega * t)
        y = self.y0 + self.B * math.sin(2.0 * self.omega * t)
        return x, y

    def _timer_cb(self):
        # advance time
        prev_t = self.t
        self.t += self.dt

        # detect period completion
        period_count = int(self.t / self.period)
        if period_count != self.last_period_count:
            self.last_period_count = period_count
            # completed one period -> change color
            self._change_pen_color()

        # need current pose to control
        if self.pose is None:
            return

        # desired point at current time
        xd, yd = self._desired_xy(self.t)

        # compute error and simple heading controller
        dx = xd - self.pose.x
        dy = yd - self.pose.y
        distance = math.hypot(dx, dy)

        desired_yaw = math.atan2(dy, dx)
        yaw_error = self._angle_diff(desired_yaw, self.pose.theta)

        # PD-like (proportional) control
        lin = min(self.k_lin * distance, self.max_lin)
        ang = self.k_ang * yaw_error

        # if heading is far off, reduce forward speed
        if abs(yaw_error) > 0.8:
            lin *= 0.2

        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.cmd_pub.publish(msg)

    def _angle_diff(self, a, b):
        """shortest difference between angles a and b"""
        d = a - b
        while d > math.pi:
            d -= 2.0 * math.pi
        while d < -math.pi:
            d += 2.0 * math.pi
        return d

    def _change_pen_color(self):
        """Call /turtle1/set_pen to set a new random color (non-blocking)."""
        if not self.set_pen_client.service_is_ready():
            self.get_logger().debug('SetPen service not ready; skipping color change')
            return

        req = tsrv.SetPen.Request()
        req.r = random.randint(0, 255)
        req.g = random.randint(0, 255)
        req.b = random.randint(0, 255)
        req.width = 3
        req.off = 0  # 0 = pen on
        self.get_logger().info(f'Changing pen color to ({req.r},{req.g},{req.b})')
        self.set_pen_client.call_async(req)


def main(args=None):
    rclpy.init(args=args)
    node = LoopNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

