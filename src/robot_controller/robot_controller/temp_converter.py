#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TempConverter(Node):
    def __init__(self):
        super().__init__('temp_converter')
        # Subscriber listens to /temperature_raw
        self.subscription = self.create_subscription(
            Float32,
            '/temperature_raw',
            self.listener_callback,
            10
        )
        # Publisher sends to /temperature_converted
        self.publisher_ = self.create_publisher(Float32, '/temperature_converted', 10)
        self.get_logger().info('Temperature Converter Node Started')

    def listener_callback(self, msg):
        temp_c = msg.data
        temp_f = (temp_c * 9/5) + 32
        out_msg = Float32()
        out_msg.data = temp_f
        self.publisher_.publish(out_msg)
        self.get_logger().info(f'Received: {temp_c:.2f}°C → Converted: {temp_f:.2f}°F')

def main(args=None):
    rclpy.init(args=args)
    node = TempConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
