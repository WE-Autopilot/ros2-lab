#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random
import time

class TempPublisher(Node):
    def __init__(self):
        super().__init__('temp_publisher')
        self.pub = self.create_publisher(Float32, '/temp_c', 10)
        # timer: publish once per second
        self.timer = self.create_timer(1.0, self.publish_temp)
        self.get_logger().info('Publishing random Celsius temps to /temp_c')

    def publish_temp(self):
        # random temp between 15 and 30
        celsius = random.uniform(15.0, 30.0)
        msg = Float32()
        msg.data = celsius
        self.pub.publish(msg)
        self.get_logger().info(f'Published Celsius: {celsius:.2f}')

def main():
    rclpy.init()
    node = TempPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
