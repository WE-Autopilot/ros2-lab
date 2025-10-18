from setuptools import setup

package_name = "robot_controller"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    author="Luke Blommesteyn",
    author_email="luke.blommesteyn@example.com",
    maintainer="Luke Blommesteyn",
    maintainer_email="luke.blommesteyn@example.com",
    description="Spawn, waypoint control, and pen management nodes for the turtlesim lab",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "initial_setup = robot_controller.initial_setup:main",
            "waypoint_controller = robot_controller.waypoint_controller:main",
            "pen_manager = robot_controller.pen_manager:main",
        ],
    },
)
