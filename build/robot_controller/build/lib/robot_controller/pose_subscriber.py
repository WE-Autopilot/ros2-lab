#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


class PoseSubscriber (Node):
    def __init__(self):
        super().__init__('Pose_Subscriber') 
        self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.callback, 10)

    def callback(self, msg : Pose):
        self.get_logger().info(f'Pose(x = {round(msg.x, 2)}, y = {round(msg.y, 2)}, theta = {round(msg.theta, 2)})')


def main(args=None):
    rclpy.init(args=args)   
    node = PoseSubscriber()      
    rclpy.spin(node)        
    rclpy.shutdown()        

if __name__ == '__main__':
    main()