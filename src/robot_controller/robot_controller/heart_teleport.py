#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
import math
import time


class HeartTeleporter(Node):
    def __init__(self):
        super().__init__('heart_teleporter')
        self.teleport = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen = self.create_client(SetPen, '/turtle1/set_pen')

        self.get_logger().info('💗 Heart Teleporter node started.')
        while not self.teleport.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for teleport service...')

        self.req_tp = TeleportAbsolute.Request()
        self.req_pen = SetPen.Request()

        self.draw_heart()

    def set_pen(self, r, g, b, width, off):
        """Enable/disable pen and set its color."""
        self.req_pen.r = r
        self.req_pen.g = g
        self.req_pen.b = b
        self.req_pen.width = width
        self.req_pen.off = off
        self.pen.call_async(self.req_pen)

    def teleport_to(self, x, y, theta=0.0):
        """Teleport turtle instantly."""
        self.req_tp.x = float(x)
        self.req_tp.y = float(y)
        self.req_tp.theta = float(theta)
        self.teleport.call_async(self.req_tp)

    def draw_heart(self):
        self.get_logger().info('❤️ Drawing clean centered heart...')
        time.sleep(0.5)

        # Move without drawing to starting point
        self.set_pen(255, 0, 0, 3, 1)  # pen off (off=1)
        self.teleport_to(5.5, 5.5)
        time.sleep(0.5)

        # Pen down
        self.set_pen(255, 0, 0, 3, 0)

        # Heart equation
        scale = 0.09  # increase for larger heart
        offset_x = 5.5
        offset_y = 5.5

        for deg in range(0, 361):
            rad = math.radians(deg)
            x = 16 * math.sin(rad) ** 3
            y = 13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad)

            self.teleport_to(offset_x + x * scale, offset_y + y * scale)
            time.sleep(0.01)

        self.set_pen(255, 0, 0, 3, 1)
        self.get_logger().info('✅ Heart complete!')


def main(args=None):
    rclpy.init(args=args)
    node = HeartTeleporter()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
