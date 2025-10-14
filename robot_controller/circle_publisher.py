#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')  # registers node name in ROS graph
        self.linear_speed = 2.0  # linear speed in x-axis
        self.angular_speed = 1.0  # angular speed in z-axis
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)  # creates publisher node
        self.create_timer(0.5, self.timer_callback)  # creates timer to call callback every 0.1 seconds
        
    def timer_callback(self):
        # Create and populate a Twist message
        msg = Twist()
        msg.linear.x = self.linear_speed
        msg.angular.z = self.angular_speed
        # Publish the message
        self.publisher_.publish(msg)
        # Log the published values
        self.get_logger().info(
            f'Publishing Twist(linear.x={msg.linear.x}, angular.z={msg.angular.z})'
        )

def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = PublisherNode()      # create node
    rclpy.spin(node)        # keep node running
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()
