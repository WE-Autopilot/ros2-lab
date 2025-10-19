#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String

class CounterSubscriber(Node):
    def __init__(self):
        super().__init__('counter_subscriber')
        
        # Create subscription to /counter topic
        self.subscription = self.create_subscription(
            Int32,
            '/counter',
            self.counter_callback,
            10
        )
        
        # Create publisher for /counter_status topic (NEW!)
        self.status_publisher = self.create_publisher(String, '/counter_status', 10)
        
        self.get_logger().info('Counter Subscriber started! Waiting for numbers...')
    
    def counter_callback(self, msg):
        # Receive the number and print a message
        number = msg.data
        self.get_logger().info(f'Received number: {number} - Count is now {number}!')
        
        # Publish status message (NEW!)
        status_msg = String()
        if number % 2 == 0:
            status_msg.data = f"EVEN number received: {number}"
        else:
            status_msg.data = f"ODD number received: {number}"
        
        self.status_publisher.publish(status_msg)
        self.get_logger().info(f'Status: {status_msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = CounterSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
