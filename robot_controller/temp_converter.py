#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TempConverter(Node):
    def __init__(self):
        super().__init__('temp_converter')
        self.sub = self.create_subscription(Float32, '/temp_c', self.on_celsius, 10)
        self.pub = self.create_publisher(Float32, '/temp_f', 10)
        self.get_logger().info('Converting /temp_c to /temp_f')

    def on_celsius(self, msg: Float32):
        f = msg.data * 9.0 / 5.0 + 32.0
        out = Float32()
        out.data = f
        self.pub.publish(out)
        self.get_logger().info(f'C={msg.data:.2f}  F={f:.2f}')

def main():
    rclpy.init()
    node = TempConverter()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
