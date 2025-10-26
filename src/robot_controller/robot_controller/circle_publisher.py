#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePublisher(Node):
    def __init__(self):
        super().__init__('circle_publisher')  # registers node name in ROS graph
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        self.angular_velocity = 1.0  # radians per second
        self.linear_velocity = 0.5   # meters per second

        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        
        msg.linear.x = self.linear_velocity
        msg.angular.z = self.angular_velocity

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: linear.x={msg.linear.x}, angular.z={msg.angular.z}')

def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = CirclePublisher()    # create node
    rclpy.spin(node)        # keep node running

    node.destroy_node()
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()

