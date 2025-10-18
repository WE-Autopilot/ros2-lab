#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class SafetySubscriber(Node):
    def __init__(self):
        super().__init__('safety_subscriber')
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.cmd_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('SafetySubscriber started!')

    def pose_callback(self, msg):
        danger_zone = 1.0
        if msg.x < danger_zone or msg.x > 11 - danger_zone or msg.y < danger_zone or msg.y > 11 - danger_zone:
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.cmd_publisher.publish(stop_msg)
            self.get_logger().warn('Near wall — Stopping turtle!')
        else:
            self.get_logger().info(f'Safe: x={msg.x:.2f}, y={msg.y:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = SafetySubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()