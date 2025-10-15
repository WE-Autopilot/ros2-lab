#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import random
from std_msgs.msg import Bool

#Publisher for random movement
class RandomMovement (Node):
    def __init__(self):
        super().__init__('Random_Movement') 
        self.get_logger().info('Starting movement')
        self.publisher = self.create_publisher(Twist, '/WEAP/cmd_vel', 10)
        self.create_timer(0.5, self.callback)

        self.stop = False
        self.subscriber = self.create_subscription(Bool, '/stop_signal', self.stopMovement, 10)

    def callback(self):
        msg = Twist()
        if self.stop:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('End reached')
            self.destroy_node()
        else:
            msg.linear.x = random.uniform(-5.0, 5.0)
            msg.angular.z = random.uniform(-5.0, 5.0)
        
        self.publisher.publish(msg)

    def stopMovement(self, msg):
        self.stop = msg.data

def main(args=None):
    rclpy.init(args=args)   
    node = RandomMovement()      
    rclpy.spin(node)        
    rclpy.shutdown()        

if __name__ == '__main__':
    main()