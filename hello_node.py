import rclpy
from rclpy.node import Node
class HelloNode(Node):
    def __init__(self):
        super().__init__('hello_node')  # registers node name in ROS graph
        self.get_logger().info('Hello from ROS 2!')  # prints message

def main(args=None):
    rclpy.init(args=args)   # start ROS 2
    node = HelloNode()      # create node
    rclpy.spin(node)        # keep node running
    rclpy.shutdown()        # safely exit

if __name__ == '__main__':
    main()

