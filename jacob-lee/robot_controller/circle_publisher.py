#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePublisher(Node):
    def __init__(self):
        super().__init__("circle_publisher")
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.create_timer(0.5, self.timer_callback)
        self.linear_speed = 2.0
        self.angular_speed = 1.5

        self.get_logger().info(f'CirclePublisher has started')  # prints message

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = self.linear_speed
        msg.angular.z = self.angular_speed

        self.publisher_.publish(msg)

        self.get_logger().info(f"linear.x: {msg.linear.x} and angular.z: {msg.angular.z}")


def main(args=None):
    rclpy.init(args=args)    # start ROS 2
    node = CirclePublisher() # create node
    rclpy.spin(node)         # keep node running
    rclpy.shutdown()         # safely exit

if __name__ == "__main__":
    main()