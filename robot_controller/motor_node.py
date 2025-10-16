import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Motor(Node):
    def __init__(self):
        super().__init__('motor')
        self.vel_subscription = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.current_speed = 1.0

    def cmd_vel_callback(self, msg):
        self.get_logger().info(f'Received new speed command...')
        if msg.linear.x == 0.0:
            self.current_speed = 1.0
        else:
            self.current_speed = self.current_speed * msg.linear.x

        self.get_logger().info(f'Current Speed -> {self.current_speed:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = Motor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
