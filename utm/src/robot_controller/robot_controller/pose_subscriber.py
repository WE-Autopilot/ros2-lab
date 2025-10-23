#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')  # registers node name in ROS graph
        self.get_logger().info('Starting Pose Subscriber!') 
        self.create_subscription(Pose, '/turtle1/pose', self.listener_callback, 10)  # create subscriber

    def listener_callback(self, msg):
        self.get_logger().info('Pose: x=%.2f, y=%.2f, theta=%.2f' % (msg.x, msg.y, msg.theta))  #log pose data
def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = PoseSubscriber()      # create node
    rclpy.spin(node)        # keep node running
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()


