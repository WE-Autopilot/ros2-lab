#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import turtlesim.msg as tmsg

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')  # registers node name in ROS graph
        self.subscription = self.create_subscription(
            tmsg.Pose,
            '/turtle1/pose',
            self.pose_callback,
            10)
        self.subscription  # prevent unused variable warning

    def pose_callback(self, msg):
        self.get_logger().info(f'Received Pose - x: {msg.x}, y: {msg.y}, theta: {msg.theta}')

def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = PoseSubscriber()    # create node
    rclpy.spin(node)        # keep node running

    node.destroy_node()
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()

