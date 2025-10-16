#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose   # message type for turtle position/orientation

class PoseSubscriber(Node):
    def __init__(self):
        # initialize the node with a name
        super().__init__('pose_subscriber')
        
        # create a subscriber to the /turtle1/pose topic
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.listener_callback, 10) # queue size of 10

        self.get_logger().info('Pose Subscriber Node started and listening to /turtle1/pose')

    def listener_callback(self, msg):
        # triggered every time a new Pose message is received
        self.get_logger().info(
            f'Position -> x: {msg.x:.2f}, y: {msg.y:.2f}, θ: {msg.theta:.2f}, '
            f'Linear Vel: {msg.linear_velocity:.2f}, Angular Vel: {msg.angular_velocity:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    rclpy.spin(node)      # keep node alive to receive messages
    node.destroy_node()   # clean up before exit
    rclpy.shutdown()

if __name__ == '__main__':
    main()
