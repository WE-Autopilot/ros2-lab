#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class SubscriptionNode(Node):
    def __init__(self):
        super().__init__('subscription_node')  # registers node name in ROS graph
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.sub_callback,
            10
        )
        self.get_logger().info('TurtlePoseListener has been started and is listening to /turtle1/pose')

    def sub_callback(self, msg: Pose):
         # Access and log the incoming message fields
        x = round(msg.x, 2)
        y = round(msg.y, 2)
        theta = round(msg.theta, 2)
        self.get_logger().info(f'Received pose -> x: {x}, y: {y}, theta: {theta}')

def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = SubscriptionNode()      # create node
    rclpy.spin(node)        # keep node running
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()
