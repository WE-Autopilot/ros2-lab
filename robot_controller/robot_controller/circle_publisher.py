#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePublisher(Node):
  def __init__(self):
    super().__init__('circle_publisher')
    self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
    
    self.linear_speed = 0.5
    self.angular_speed = 1.0

    self.create_timer(0.5, self.timer_callback)
  
  def timer_callback(self):
    msg = Twist()
    msg.linear.x = self.linear_speed
    msg.angular.z = self.angular_speed

    self.publisher.publish(msg)

    self.get_logger().info(
      f'Publishing: linear={msg.linear.x} m/s, angular={msg.angular.z} rad/s'
    )

def main(args=None):
  rclpy.init(args=args)
  node = CirclePublisher()
  rclpy.spin(node)

  node.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
  main()