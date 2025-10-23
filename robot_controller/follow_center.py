#! /usr/bin/env python3

# this node reads turtle pose and publishes velocity to move toward center
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

TARGET_X = 5.544
TARGET_Y = 5.544

class FollowCenter(Node):
    def __init__(self):
        super().__init__('follow_center')
        # publisher for velocity
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # subscriber for pose
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        # gains
        self.k_lin = 0.8
        self.k_ang = 4.0
        self.get_logger().info('follow_center started')

    def on_pose(self, pose: Pose):
        dx = TARGET_X - pose.x
        dy = TARGET_Y - pose.y
        dist = math.hypot(dx, dy)

        # angle from turtle to target
        desired = math.atan2(dy, dx)
        # smallest angle difference
        err_ang = self.normalize(desired - pose.theta)

        cmd = Twist()
        # rotate to face the target
        cmd.angular.z = self.k_ang * err_ang
        # move forward when roughly facing target
        if abs(err_ang) < 0.4:
            cmd.linear.x = self.k_lin * dist

        # cap speeds a bit for smooth motion
        cmd.linear.x = max(min(cmd.linear.x, 2.0), -2.0)
        cmd.angular.z = max(min(cmd.angular.z, 4.0), -4.0)

        self.pub.publish(cmd)
        self.get_logger().info(f'x={pose.x:.2f} y={pose.y:.2f} theta={pose.theta:.2f} dist={dist:.2f} ang_err={err_ang:.2f}')

    @staticmethod
    def normalize(a):
        # wrap angle to [-pi, pi]
        while a > math.pi:
            a -= 2 * math.pi
        while a < -math.pi:
            a += 2 * math.pi
        return a

def main():
    rclpy.init()
    node = FollowCenter()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

