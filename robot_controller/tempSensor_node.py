import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TempSensor(Node):
    def __init__(self):
        super().__init__('temp_sensor')

        self.temp_publisher = self.create_publisher(Float32, '/temperature', 10)
        self.current_temp = 0.0
        self.heating = True

        # Publish every second
        self.timer = self.create_timer(1.0, self.publish_temperature)

    def publish_temperature(self):
        # Heat up while active
        if self.heating:
            self.current_temp += 5.0  # faster heating for visible change

            # Once target temp reached, stop heating
            if self.current_temp >= 100.0:
                self.heating = False

        # When heating is off, snap temp back to zero
        else:
            self.current_temp = 0.0
            self.heating = True   # immediately restart next cycle

        # Publish current temperature
        msg = Float32()
        msg.data = self.current_temp
        self.temp_publisher.publish(msg)
        self.get_logger().info(f'Publishing Temperature -> °C = {self.current_temp:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = TempSensor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
