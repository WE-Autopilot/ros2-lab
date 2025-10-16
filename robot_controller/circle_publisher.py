#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePublisher(Node):
    def __init__(self):
        super().__init__('circle_publisher')  # ✅ correct call

        # Create publisher to the turtle velocity topic
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.timer = self.create_timer(0.5, self.timer_callback)
        self.linear_speed = 2.0
        self.angular_speed = 1.0
        self.get_logger().info('CirclePublisher node started!')

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = self.linear_speed
        msg.angular.z = self.angular_speed
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing velocity command')

def main(args=None):
    rclpy.init(args=args)
    node = CirclePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
