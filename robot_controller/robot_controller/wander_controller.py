import random
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class WanderController(Node):
    def __init__(self):
          super().__init__('wander_controller')
          self.pub_cmd = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
          self.sub_stop = self.create_subscription(Bool, '/safety/stop', self.on_stop, 10)

          self.stopped = False
          self.timer = self.create_timer(0.2, self.tick)
          self.get_logger().info('WanderController started (publishes random Twist).')

    def on_stop(self, msg: Bool):
          self.stopped = msg.data
          if self.stopped:
             self.get_logger().info('Received STOP signal.')
          else:
             self.get_logger().info('STOP cleared.')

    def tick(self):
          msg = Twist()
          if not self.stopped:
            msg.linear.x = random.uniform(0.5, 1.5)
            msg.angular.z = random.uniform(-1.0, 1.0)
          else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
          self.pub_cmd.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = WanderController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
