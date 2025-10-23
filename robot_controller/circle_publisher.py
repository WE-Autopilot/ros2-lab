#! /usr/bin/env python3
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePublisher(Node):
    def __init__(self):
        # 1. Register node
        super().__init__('circle_publisher')

        # 2. Create publisher (publishes Twist messages to "cmd_vel")
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        # 3. Store linear and angular speeds
        self.linear_speed = 0.2
        self.angular_speed = 0.2

        # 4. Create timer (callback every 0.5 sec)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.publish_velocity)

    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = self.linear_speed
        msg.angular.z = self.angular_speed
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: linear={msg.linear.x}, angular={msg.angular.z}')


def main(args=None):
    rclpy.init(args=args)
    node = CirclePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()