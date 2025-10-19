#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')
        
        # Create subscription to /turtle1/pose topic
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        
        self.get_logger().info('Pose Subscriber has started!')
    
    def pose_callback(self, msg):
        # Access and log the pose data
        self.get_logger().info(
            f'Turtle Position - x: {msg.x:.2f}, y: {msg.y:.2f}, theta: {msg.theta:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
