#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

#Publisher to draw letters
class Drawer (Node):
    def __init__(self):
        super().__init__('Drawer') 
        self.publisher = self.create_publisher(Twist, '/WEAP/cmd_vel', 10)
        self.draw(0.0, -1.0, 0.0, 0.0)  
    

    def draw(self, x, y, z, angular):
        msg = Twist()
        msg.linear.x = x
        msg.linear.y = y
        msg.linear.z = z
        msg.angular.z = angular

    def stop():
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0


def main(args=None):
    rclpy.init(args=args)   
    node = Drawer()      
    rclpy.spin(node)        
    rclpy.shutdown()        

if __name__ == '__main__':
    main()