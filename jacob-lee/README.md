# Part D
For part D, I repurposed/implemted the circle and pose nodes to now support up to 3 turtles in which they can collide with some helper functions. The publisher and subscriber nodes are pretty much identical to our `circle_publisher` and our `pose_subscriber`, only difference is that running the following two commands can add up to 3 turtles in which they can collide with each other.

### Adding more turtles
1. `ros2 service call /spawn turtlesim/srv/Spawn "{x: 5.0, y: 5.0, theta: 0.0, name: 'turtle2'}"`
2. `ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 7.0, theta: 0.0, name: 'turtle3'}"`
