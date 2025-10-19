# Robot Controller - ROS2 WEAP OA Project 

This package contains ROS 2 nodes for lab assignments.

## Nodes
- `hello_node` - Simple hello world node
- `circle_publisher` - Publishes velocity commands to make turtle move in circle
- `pose_subscriber` - Subscribes to turtle pose
- `counter_publisher` - Publishes incrementing counter
- `counter_subscriber` - Subscribes to counter and publishes status

## Topics
- `/counter` - Int32 messages with count
- `/counter_status` - String messages with even/odd status
