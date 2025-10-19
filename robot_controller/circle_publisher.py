#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePublisher(Node):
    def __init__(self):
        super().__init__('circle_publisher')

        # Create publisher for /turtle1/cmd_vel topic with Twist message type
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Create timer that calls the callback every 0.5 seconds
        self.timer = self.create_timer(0.5, self.publish_velocity)

        # Store linear and angular speed values
        self.linear_speed = 1.0
        self.angular_speed = 1.0

        self.get_logger().info('Circle Publisher has started!')

    def publish_velocity(self):
        # Create Twist message
        msg = Twist()

        # Set linear and angular velocities to make turtle move in circle
        msg.linear.x = self.linear_speed
        msg.angular.z = self.angular_speed

        # Publish the message
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CirclePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
