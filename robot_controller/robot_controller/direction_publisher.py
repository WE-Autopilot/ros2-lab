#!/usr/bin/env python3
import rclpy
import random
from rclpy.node import Node
from geometry_msgs.msg import Twist


class DirectionPublisher(Node):
    def __init__(self):
        super().__init__('direction_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.linear_speed = 0.5
        self.angular_speed = 0.5
        self.linear_timer = self.create_timer(0.5, self.publish_linear) #timer continuously updates the turtles velocity and angle of movement
        self.angular_timer = self.create_timer(2.0, self.direction_change) #timer goes off every 2 seconds, calls direction_change to switch the turtles angle of movement

        self.get_logger().info('DirectionPublisher started.')

    def publish_linear(self): #publishes the updated velocity and angle of movement for the turtle
        msg = Twist()
        msg.linear.x = self.linear_speed
        msg.angular.z = self.angular_speed
        self.publisher_.publish(msg)

    def direction_change(self): #generates a random angular velocity between -2.0 and 2.0, logs the adjustment
        random_float = random.uniform(-2.0,2.0)
        self.angular_speed = random_float

        self.get_logger().info(f"Adjusted angular speed to {self.angular_speed:.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = DirectionPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
