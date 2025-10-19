#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class CounterPublisher(Node):
    def __init__(self):
        super().__init__('counter_publisher')
        
        # Create publisher for /counter topic
        self.publisher_ = self.create_publisher(Int32, '/counter', 10)
        
        # Create timer that runs every 1 second
        self.timer = self.create_timer(1.0, self.publish_count)
        
        # Start counter at 0
        self.count = 0
        
        self.get_logger().info('Counter Publisher started! Counting...')
    
    def publish_count(self):
        # Increment counter
        self.count += 1
        
        # Create message
        msg = Int32()
        msg.data = self.count
        
        # Publish it
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {self.count}')

def main(args=None):
    rclpy.init(args=args)
    node = CounterPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
