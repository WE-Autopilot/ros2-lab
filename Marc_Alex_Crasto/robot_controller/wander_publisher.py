#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import random

class WanderPublisher(Node):
    def __init__(self):
        super().__init__('wander_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.publish_random_movement)
        self.get_logger().info('WanderPublisher started!')

    def publish_random_movement(self):
        msg = Twist()
        msg.linear.x = random.uniform(0.5, 2.0)
        msg.angular.z = random.uniform(-2.0, 2.0)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Random Move: linear.x={msg.linear.x:.2f}, angular.z={msg.angular.z:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = WanderPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()