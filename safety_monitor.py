#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class SafetyMonitor(Node):
    def __init__(self):
        super().__init__('safety_monitor')
        
        # Subscribe to turtle's position
        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        
        # Publisher for emergency stop commands
        self.emergency_publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel', 
            10
        )
        
        # Safety boundary (1.0 unit from walls)
        self.safety_margin = 1.0
        self.screen_width = 11.0  # Turtlesim screen size
        self.screen_height = 11.0
        
        self.get_logger().info('🚀 Safety Monitor activated! Monitoring turtle position...')
    
    def pose_callback(self, msg):
        # Check if turtle is too close to any wall
        too_close_to_left = msg.x < self.safety_margin
        too_close_to_right = msg.x > (self.screen_width - self.safety_margin)
        too_close_to_bottom = msg.y < self.safety_margin
        too_close_to_top = msg.y > (self.screen_height - self.safety_margin)
        
        if too_close_to_left or too_close_to_right or too_close_to_bottom or too_close_to_top:
            # EMERGENCY STOP!
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.emergency_publisher.publish(stop_msg)
            
            # Log the emergency
            wall = "left" if too_close_to_left else \
                   "right" if too_close_to_right else \
                   "bottom" if too_close_to_bottom else "top"
                   
            self.get_logger().warn(f'🚨 EMERGENCY STOP! Turtle too close to {wall} wall! '
                                 f'Position: x={msg.x:.2f}, y={msg.y:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = SafetyMonitor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
