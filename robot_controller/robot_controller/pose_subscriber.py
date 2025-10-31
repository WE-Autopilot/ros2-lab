#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.listener_callback,
            10)
        self.get_logger().info('Pose subscriber started and listening to /turtle1/pose')

    def listener_callback(self, msg):
        self.get_logger().info(
            f"x: {msg.x:.2f}, y: {msg.y:.2f}, theta: {msg.theta:.2f}, "
            f"linear_vel: {msg.linear_velocity:.2f}, angular_vel: {msg.angular_velocity:.2f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
