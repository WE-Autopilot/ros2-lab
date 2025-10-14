#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

class poseColourSubscriber(Node):
    def __init__(self):
        super().__init__('pose_colour_subscriber')
        self.subscription_ = self.create_subscription(Pose, '/turtle1/pose', self.pose_colour_change, 10) #whenever position updates call pose_colour_change
        self.client = self.create_client(SetPen, '/turtle1/set_pen')
        self.last_colour = None
        self.get_logger().info('PoseColourSubscriber started.')

    def pose_colour_change(self, msg): # function checks the turtles current position in the 4 quadrants of the screen and changes the pen colour accordingly
        if msg.x < 6.0 and msg.y < 6.0: # turtle in bottom left -- change to red
            r = 252
            g = 3
            b = 3
        elif msg.x < 6.0 and msg.y >= 6.0: # turtle in top left -- change to green
            r = 78
            g = 252
            b = 3
        elif msg.x >= 6.0 and msg.y < 6.0: # turtle in bottom right -- change to pink
            r = 227
            g = 3
            b = 252
        else: # turtle in top right -- change to turtquoise
            r = 3
            g = 227
            b = 252
        
        new_colour = (r, g, b) #setting the new colour
        if new_colour == self.last_colour: #if the colour stayed the same, no need to set it again -- just return
            return
        self.last_colour = new_colour

        # requesting a pen colour change
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = 3
        request.off = False

        # Wait for service before sending
        if not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('/turtle1/set_pen service not available.')
            return
        
        self.client.call_async(request)
        # logging the colour change
        self.get_logger().info(f"Set pen color to RGB=({r},{g},{b}) at x={msg.x:.2f}, y={msg.y:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = poseColourSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()