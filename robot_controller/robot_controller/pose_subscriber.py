#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class TurtlePoseSubscriber(Node):
    def __init__(self):
        super().__init__('turtle_pose_subscriber')

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.get_logger().info('TurtlePoseSubscriber node has started.')

    def pose_callback(self, msg):
        x = round(msg.x, 2)
        y = round(msg.y, 2)
        theta = round(msg.theta, 2)

        self.get_logger().info(f'Turtle Pose -> x: {x}, y: {y}, theta: {theta}')

def main(args=None):
    rclpy.init(args=args)
    node = TurtlePoseSubscriber()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()