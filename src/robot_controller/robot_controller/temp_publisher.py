#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class TempPublisher(Node):
    def __init__(self):
        super().__init__('temp_publisher')
        # Create a publisher for topic /temperature_raw
        self.publisher_ = self.create_publisher(Float32, '/temperature_raw', 10)
        # Publish every 1 second
        self.timer = self.create_timer(1.0, self.publish_temperature)
        self.get_logger().info('Temperature Publisher Node Started')

    def publish_temperature(self):
        # Generate a random Celsius temperature
        temp_c = random.uniform(20.0, 35.0)
        msg = Float32()
        msg.data = temp_c

        # Publish to topic
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing Celsius: {temp_c:.2f}°C')

def main(args=None):
    rclpy.init(args=args)
    node = TempPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
