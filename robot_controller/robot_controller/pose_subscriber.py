#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')  # registers node name in ROS graph
        self.subscription_ = self.create_subscription(Pose, '/turtle1/pose', self.callback, 10)
        self.get_logger().info('PoseSubscriber started.')

    def callback(self, msg):
        self.get_logger().info(f"x={msg.x:.2f}, y={msg.y:.2f}, theta={msg.theta:.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

