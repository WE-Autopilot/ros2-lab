#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class FahrenheitLogger(Node):
    def __init__(self):
        # Initalize node.
        super().__init__('fahrenheit_logger')
        # Subscribe to Fahrenheit topic.
        self.subscription = self.create_subscription(
            Float32,
            'temperature_f',
            self.callback,
            10
        )
        self.get_logger().info('FahrenheitLogger node started.')

    def callback(self, msg):
        # Log the recieved Fahrenheit value.
        self.get_logger().info(f'Received Fahrenheit: {msg.data:.2f} °F')

def main(args=None):
    rclpy.init(args=args)
    node = FahrenheitLogger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
