#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random


class TemperaturePublisher(Node):
    """
    A node that publishes random temperature values in Celsius.
    """
    
    def __init__(self):
        super().__init__('temperature_publisher')
        
        # Create publisher for temperature in Celsius
        self.publisher_ = self.create_publisher(Float32, 'temperature_celsius', 10)
        
        # Set timer to publish every 2 seconds
        self.timer_period = 2.0  # seconds
        self.timer = self.create_timer(self.timer_period, self.publish_temperature)
        
        self.get_logger().info('Temperature Publisher Node has started.')
        self.get_logger().info('Publishing temperatures in Celsius on topic: temperature_celsius')
    
    def publish_temperature(self):
        """
        Publish a random temperature value in Celsius (range: -10 to 40 degrees).
        """
        msg = Float32()
        # Generate random temperature between -10 and 40 degrees Celsius
        msg.data = random.uniform(-10.0, 40.0)
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data:.2f}°C')


def main(args=None):
    rclpy.init(args=args)
    node = TemperaturePublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
