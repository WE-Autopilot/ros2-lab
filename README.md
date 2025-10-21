run as admin

pixi shell

colcon build --symlink-install
pixi run ros2 run robot_controller hello_node
OR
. install\local_setup.ps1
ros2 run robot_controller hello_node

