import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from turtlesim.msg import Pose

class SafetyMonitor(Node):
    def __init__(self):
          super().__init__('safety_monitor')
          self.pub_stop = self.create_publisher(Bool, '/safety/stop', 10)
          self.sub_pose = self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
          self.min_xy = 1.0
          self.max_xy = 10.0
          self.stopped = False
          self.get_logger().info('SafetyMonitor started (publishes Bool on /safety/stop).')

    def on_pose(self, pose: Pose):
          out_of_bounds = ( pose.x < self.min_xy or pose.x > self.max_xy or pose.y < self.min_xy or pose.y > self.max_xy)
          msg = Bool()
          msg.data = out_of_bounds
          if msg.data != self.stopped:
             self.stopped = msg.data
             state = 'STOP' if self.stopped else 'RESUME'
             self.get_logger().info(f'Boundary state changed -> {state}')
          self.pub_stop.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SafetyMonitor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
