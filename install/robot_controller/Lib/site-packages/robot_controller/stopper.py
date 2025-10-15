#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
from std_msgs.msg import Bool

#Subscriber to stop node when it is close to given end point
class Stopper (Node):
    def __init__(self):
        super().__init__('Stopper')

        self.x = float(input("Enter ending X position (float between 0.0 and 11.0): "))
        self.y = float(input("Enter ending Y position (float between 0.0 and 11.0): "))

        self.subscriber = self.create_subscription(Pose, '/WEAP/pose', self.callback, 10)

        self.moveMentPublisher = self.create_publisher(Twist, '/WEAP/cmd_vel', 10)

        self.counter = 0

        self.stopPublisher = self.create_publisher(Bool, '/stop_signal', 10)

    def callback(self, msg : Pose):
        self.counter += 1
        if self.counter % 10 == 0:
            self.get_logger().info(f'Pose(x = {round(msg.x, 2)}, y = {round(msg.y, 2)}, theta = {round(msg.theta, 2)})')

        distance = math.sqrt((msg.x - self.x)**2 + (msg.y - self.y)**2)

        if distance < 1.0:
            self.stop()

    def stop(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.moveMentPublisher.publish(msg)
        self.get_logger().info("Turtle stopped at given position!")
        stopMsg = Bool()
        stopMsg.data = True
        self.stopPublisher.publish(stopMsg)
        self.destroy_node()

def main(args=None):
    rclpy.init(args=args)   
    node = Stopper()      
    rclpy.spin(node)        
    rclpy.shutdown()        

if __name__ == '__main__':
    main()