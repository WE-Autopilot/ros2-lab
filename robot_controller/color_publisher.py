#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import SetPen

class PenColorCycler(Node):
    def __init__(self):
        super().__init__('pen_color_cycler')
        # Create the client for the /turtle1/set_pen service
        self.client = self.create_client(SetPen, '/turtle1/set_pen')
        self.get_logger().info('Waiting for /turtle1/set_pen service...')
        # Wait until turtlesim has brought up the service
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('Service /turtle1/set_pen not available, exiting')
            rclpy.shutdown()
            return

        # Initialize RGB values
        self.r = 0
        self.g = 0
        self.b = 0
        # Every second, call set_pen to cycle color
        self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('PenColorCycler started; cycling pen color every 1 s')

    def timer_callback(self):
        # Increment color channels
        self.r = (self.r + 50) % 256
        self.g = (self.g + 80) % 256
        self.b = (self.b + 110) % 256

        # Build the request
        req = SetPen.Request()
        req.r = self.r
        req.g = self.g
        req.b = self.b
        req.width = 5    # pen thickness
        req.off = False  # pen on

        # Call the service
        future = self.client.call_async(req)
        future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        try:
            future.result()  # empty response on success
            self.get_logger().info(f'Set pen to r={self.r}, g={self.g}, b={self.b}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = PenColorCycler()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
