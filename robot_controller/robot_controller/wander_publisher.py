#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import random

class WanderPublisher(Node):
    def __init__(self):
        super().__init__('wander_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info('Wander publisher started')

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = random.uniform(0.5, 2.0)
        msg.angular.z = random.uniform(-2.0, 2.0)
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: linear={msg.linear.x:.2f}, angular={msg.angular.z:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = WanderPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
