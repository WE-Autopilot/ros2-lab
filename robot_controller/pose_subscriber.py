#! /usr/bin/env python3

# this node listens to the turtle pose and prints x y theta
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')
        self.sub = self.create_subscription(
            Pose,                 # message type
            '/turtle1/pose',      # topic name
            self.on_pose,         # callback
            10                    # queue size
        )
        self.get_logger().info('pose_subscriber started and listening on /turtle1/pose')

    def on_pose(self, msg: Pose):
        # print rounded values for readability
        self.get_logger().info(
            f'x={msg.x:.2f}  y={msg.y:.2f}  theta={msg.theta:.2f}  '
            f'v_lin={msg.linear_velocity:.2f}  v_ang={msg.angular_velocity:.2f}'
        )

def main():
    rclpy.init()
    node = PoseSubscriber()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
