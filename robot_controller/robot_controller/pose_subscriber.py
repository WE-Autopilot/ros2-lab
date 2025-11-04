import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
           super().__init__('pose_subscriber')
           self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
           self.get_logger().info('pose_subscriber started')

    def pose_callback(self, msg: Pose):
          self.get_logger().info(f"x={msg.x:.2f}, y={msg.y:.2f}, theta={msg.theta:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    try:
         rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
