#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import random


# 3 turtles colliding
# Run these two commands in the terminal to spawn in our 2 other turtles

# ros2 service call /spawn turtlesim/srv/Spawn "{x: 5.0, y: 5.0, theta: 0.0, name: 'turtle2'}"
# ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 7.0, theta: 0.0, name: 'turtle3'}"
class MultiTurtleCollide(Node):
    def __init__(self):
        super().__init__("multi_turtle_collide")
        
        # Publisher Nodes
        self.publisher1 = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.publisher2 = self.create_publisher(Twist, "/turtle2/cmd_vel", 10)
        self.publisher3 = self.create_publisher(Twist, "/turtle3/cmd_vel", 10)
        
        # Subscription Nodes
        self.subscription1 = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback1, 10)
        self.subscription2 = self.create_subscription(Pose, "/turtle2/pose", self.pose_callback2, 10)
        self.subscription3 = self.create_subscription(Pose, "/turtle3/pose", self.pose_callback3, 10)
        
        # Positions
        self.pose1 = Pose()
        self.pose2 = Pose()
        self.pose3 = Pose()

        # Velocities
        self.vel1 = self.random_twist()
        self.vel2 = self.random_twist()
        self.vel3 = self.random_twist()

        # Timer to update velocities
        self.timer = self.create_timer(0.2, self.timer_callback)

        self.get_logger().info(f"Multi Turtle has started!")  # prints message

    def pose_callback1(self, msg): self.pose1 = msg
    def pose_callback2(self, msg): self.pose2 = msg
    def pose_callback3(self, msg): self.pose3 = msg

    # Changes turtles orientation when a collision happens
    def collision_twist(self):
        twist = Twist()
        twist.linear.x = random.uniform(1.0, 2.0)
        twist.angular.z = -1 * random.uniform(-2.0, 2.0)
        return twist

    def timer_callback(self):
        # Check for collisions
        if self.check_collision(self.pose1, self.pose2):
            self.vel1 = self.collision_twist()
            self.vel2 = self.collision_twist()
            self.get_logger().info(f"COLLIDED! Turtle 1 and Turlte 2 has COLLIDED!")

        if self.check_collision(self.pose1, self.pose3):
            self.vel1 = self.collision_twist()
            self.vel3 = self.collision_twist()
            self.get_logger().info(f"COLLIDED! Turtle 1 and Turlte 3 has COLLIDED!")
            
        if self.check_collision(self.pose2, self.pose3):
            self.vel2 = self.collision_twist()
            self.vel3 = self.collision_twist()
            self.get_logger().info(f"COLLIDED! Turtle 2 and Turlte 3 has COLLIDED!")

        # Publish velocities
        self.publisher1.publish(self.vel1)
        self.publisher2.publish(self.vel2)
        self.publisher3.publish(self.vel3)

    # Simple collision detection
    def check_collision(self, p1, p2):
        dist = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
        return dist < 1


def main(args=None):
    rclpy.init(args=args)
    node = MultiTurtleCollide()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()