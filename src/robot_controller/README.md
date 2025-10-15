# ROS2 OA  

OA for basic understanding of ros2.  
  
ros project for Part D is allowing the user to input the start and end coordinates and the turtle moves randomly until it reaches the end point  

3 terminals are required (windows command line):  

Terminal 1: runs "ros2 run turtlesim turtlesim_node"  
  
Terminal 2: runs
"colcon build"  
"call install\setup.bat"  
"ros2 run robot_controller initial_spawn"  
"ros2 run robot_controller random_movement"  
initial_spawn lets the user choose where the turtle spawns, random_movement starts turtle movement.  
  
Terminal 3: runs
"colcon build"  
"call install\setup.bat"  
"ros2 run robot_controller stopper"  
stopper works with random_movement to stop the turtle and exit the program. 


