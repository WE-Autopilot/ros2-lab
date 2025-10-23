#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePublisher (Node):
    def __init__(self):
        super().__init__('circle_publisher')  # registers node name in ROS graph
        self.get_logger().info('Circle Publisher Node has been started.')  # prints message
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)  # create publisher
        self.create_timer(0.5, self.callback)  # create timer

        
    def callback(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.8
        self.publisher_.publish(msg)  # publish message
        self.get_logger().info('Publishing: "%s"' % msg)  # print message
    

def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = CirclePublisher()      # create node
    rclpy.spin(node)        # keep node running
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()

