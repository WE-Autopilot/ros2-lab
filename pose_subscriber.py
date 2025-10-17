#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')
        
        # Create subscriber for pose information
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        
        self.get_logger().info('Pose subscriber node started!')
    
    def pose_callback(self, msg):
        # This function is called every time a new pose message is received
        self.get_logger().info(
            f'Position: x={msg.x:.2f}, y={msg.y:.2f}, theta={msg.theta:.2f} '
            f'Velocity: linear={msg.linear_velocity:.2f}, angular={msg.angular_velocity:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

