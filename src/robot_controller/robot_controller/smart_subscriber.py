#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class SmartSubscriber(Node):
    def __init__(self):
        super().__init__('smart_subscriber')
        self.sub_pose = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.sub_status = self.create_subscription(String, '/turtle1/status', self.status_callback, 10)
        self.pub_stop = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('Smart Subscriber started.')

    def pose_callback(self, msg):
        self.get_logger().info(f'Pose → x:{msg.x:.2f}, y:{msg.y:.2f}, θ:{msg.theta:.2f}')
        if msg.x > 8.0:
            self.get_logger().warn('Reached x > 8.0! Sending stop command.')
            stop_msg = Twist()
            self.pub_stop.publish(stop_msg)

    def status_callback(self, msg):
        self.get_logger().info(f'Status received: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = SmartSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
