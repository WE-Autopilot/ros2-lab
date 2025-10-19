#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class TemperatureConverter(Node):
    """
    A node that subscribes to temperature in Celsius, converts to Fahrenheit,
    and logs the result.
    """
    
    def __init__(self):
        super().__init__('temperature_converter')
        
        # Create subscriber for temperature in Celsius
        self.subscription = self.create_subscription(
            Float32,
            'temperature_celsius',
            self.temperature_callback,
            10
        )
        
        # Create publisher for temperature in Fahrenheit (optional - for other nodes to use)
        self.publisher_ = self.create_publisher(Float32, 'temperature_fahrenheit', 10)
        
        self.get_logger().info('Temperature Converter Node has started.')
        self.get_logger().info('Subscribed to topic: temperature_celsius')
        self.get_logger().info('Publishing to topic: temperature_fahrenheit')
    
    def celsius_to_fahrenheit(self, celsius):
        """
        Convert temperature from Celsius to Fahrenheit.
        Formula: F = (C × 9/5) + 32
        """
        return (celsius * 9.0 / 5.0) + 32.0
    
    def temperature_callback(self, msg):
        """
        Callback function that processes incoming Celsius temperatures.
        """
        celsius = msg.data
        fahrenheit = self.celsius_to_fahrenheit(celsius)
        
        # Log the conversion
        self.get_logger().info(f'Received: {celsius:.2f}°C → Converted: {fahrenheit:.2f}°F')
        
        # Publish the Fahrenheit temperature for other nodes to use
        fahrenheit_msg = Float32()
        fahrenheit_msg.data = fahrenheit
        self.publisher_.publish(fahrenheit_msg)


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureConverter()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
