#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class FahrenheitConverter(Node):
    def __init__(self):
        # Initalize node.
        super().__init__('fahrenheit_converter')
        # Subscribe to Celsius topic.
        self.subscription = self.create_subscription(
            Float32,
            'temperature_c',
            self.callback,
            10
        )
        # Create publisher.
        self.publisher_ = self.create_publisher(Float32, 'temperature_f', 10)
        self.get_logger().info('FahrenheitConverter node started.')

    def callback(self, msg):
        # Get Celsius value and convert it.
        celsius = msg.data
        fahrenheit = celsius * 9.0 / 5.0 + 32
        # Create new Fahrenheit message.
        out_msg = Float32()
        out_msg.data = fahrenheit
        # Publish and log message.
        self.publisher_.publish(out_msg)
        self.get_logger().info(f'Converted: {celsius:.2f} °C → {fahrenheit:.2f} °F')

def main(args=None):
    rclpy.init(args=args)
    node = FahrenheitConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
