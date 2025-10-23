#!/usr/bin/env python3
import rclpy
import random
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class NumGeneratorPublisher(Node):
    def __init__(self):
        super().__init__('num_generator')  # registers node name in ROS graph
        self.get_logger().info('Starting num generator publisher') 
        self.publisher_ = self.create_publisher(Int32MultiArray, 'randNumsArray', 10)  # create publisher
        self.create_timer(1.0, self.timer_callback)  # create timer

    def timer_callback(self):
        # generate 10 random integers between 0 and 100
        nums=[0]*10
        for i in range(len(nums)):
            nums[i] = random.randint(0, 100)

        msg = Int32MultiArray()
        msg.data = nums

        self.get_logger().info('Generated numbers: ' + str(nums)) 
        self.publisher_.publish(msg)  # publish message


def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = NumGeneratorPublisher()      # create node
    rclpy.spin(node)        # keep node running
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()


