import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class Controller(Node):
    def __init__(self):
        super().__init__('controller')

        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.temp_subscription = self.create_subscription(Float32, '/temperature', self.temp_callback, 10)

        self.target_temp = 100.0
        self.command_speed = 1.0

    def temp_callback(self, msg):
        current_temp = msg.data
        self.get_logger().info('Recieved Temperature...')

        msg_out = Twist()
        if current_temp < self.target_temp:
            msg_out.linear.x = 1.1
            self.get_logger().info(f'Temperature below max, preparing speed increase command...')
        else:
            msg_out.linear.x = 0.0
            self.get_logger().info(f'Temperature at max, preparing stop command...')

        self.cmd_vel_publisher.publish(msg_out)
        self.get_logger().info(f'Publishing Speed command...')

def main(args=None):
    rclpy.init(args=args)
    node = Controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
