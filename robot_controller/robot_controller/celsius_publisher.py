#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class CelsiusPublisher(Node):
    def __init__(self):
        # Initalize node.
        super().__init__('celsius_publisher')
        # Create publisher.
        self.publisher_ = self.create_publisher(Float32, 'temperature_c', 10)
        # Call timer_callback every 1 second.
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        # Generate random Celsius temperature
        temp_c = random.uniform(-20.0, 40.0)
        # Create message.
        msg = Float32()
        msg.data = temp_c
        # Publish and log the message.
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing Celsius: {temp_c:.2f} °C')

def main(args=None):
    rclpy.init(args=args)
    node = CelsiusPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
