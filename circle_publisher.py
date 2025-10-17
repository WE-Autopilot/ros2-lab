#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
class CirclePublisher(Node):
    def __init__(self):
        super().__init__('circle_publisher')  # Register node name
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)  # Every 0.5 seconds
        self.linear_speed = 2.0
        self.angular_speed = 1.0
    def timer_callback(self):
        # Create message
        msg = Twist()
        
        # Set movement values
        msg.linear.x = self.linear_speed
        msg.angular.z = self.angular_speed
        
        # Publish the message
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing velocity command')

def main(args=None):
    rclpy.init(args=args)
    node = CirclePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

