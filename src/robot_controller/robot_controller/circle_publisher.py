#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CirclePublisher (Node):
    def __init__(self):
        super().__init__('Circle_Publisher') 
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)  
        self.create_timer(0.5, self.callback)

    def callback(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 2.0
        
        self.publisher.publish(msg)
       
        self.get_logger().info(f'Publishing Twist(linear.x={msg.linear.x}, angular.z={msg.angular.z})')


def main(args=None):
    rclpy.init(args=args)   
    node = CirclePublisher()      
    rclpy.spin(node)        
    rclpy.shutdown()        

if __name__ == '__main__':
    main()