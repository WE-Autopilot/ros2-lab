#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__("pose_subscriber")
        self.subscription = self.create_subscription(Pose, "/turtle1/pose", self.callback, 10)
        self.get_logger().info('PoseSubscriber has been started')

    def callback(self, msg):
        x = msg.x
        y = msg.y
        theta = msg.theta

        self.get_logger().info(f"x: {x:.2f}. y: {y:.2f}, theta: {theta:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()