#! /usr/bin/env python3

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CirclePublisher(Node):
    def __init__(self):
        super().__init__('circle_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.linear_speed = 2.0  
        self.angular_speed = 2.0
        self.timer = self.create_timer(0.5, self.publish_circle)

        self.get_logger().info('CirclePublisher started.')

    def publish_circle(self):
        msg = Twist()
        msg.linear.x = self.linear_speed
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = self.angular_speed
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: linear.x={msg.linear.x}, angular.z={msg.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    node = CirclePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()