#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')
        self.subscription = self.create_subscription(
            Pose,                # message type
            '/turtle1/pose',     # topic name
            self.pose_callback,  # callback function
            10                   # queue size
        )
        self.get_logger().info('Pose subscriber node has started.')

    def pose_callback(self, msg):
        self.get_logger().info(
            f'Pose -> x: {msg.x:.2f}, y: {msg.y:.2f}, θ: {msg.theta:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
