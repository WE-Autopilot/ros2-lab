#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class AlertSubscriber(Node):
    def __init__(self):
        super().__init__('alert_subscriber')  # registers node name in ROS graph
        self.get_logger().info('Starting Alert Subscriber!')  
        self.create_subscription(Int32, 'sum', self.listener_callback, 10) #create subscriber
        

    def listener_callback(self, msg):
        if (msg.data > 600): #only alert if sum is greater than threshold
            self.get_logger().info('ALERT: Threshold has been reached. Summation value %d' % msg.data) 


def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = AlertSubscriber()      # create node
    rclpy.spin(node)        # keep node running
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()


