#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray, Int32


class Summer(Node):
    def __init__(self):
        super().__init__('summer')  # registers node name in ROS graph
        self.get_logger().info('Starting the summer!')  
        self.create_subscription(Int32MultiArray, 'randNumsArray', self.listener_callback, 10)  # create subscriber
        self.publisher_ = self.create_publisher(Int32, 'sum', 10)  # create publisher

    def listener_callback(self, msg):
        total = sum(msg.data)
        self.get_logger().info('Sum: %d' % total)  
        
        msg = Int32()
        msg.data = total

        self.publisher_.publish(msg)  # publish message


def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = Summer()      # create node
    rclpy.spin(node)        # keep node running
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()


