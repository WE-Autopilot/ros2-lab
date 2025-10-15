from setuptools import find_packages, setup

package_name = 'robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='willi',
    maintainer_email='wleun28@uwo.ca',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hello_node = robot_controller.hello_node:main',
            'circle_publisher = robot_controller.circle_publisher:main',
            'pose_subscriber = robot_controller.pose_subscriber:main',
            'initial_spawn = robot_controller.initializeSpawn:main',
            'random_movement = robot_controller.randomMovement:main',
            'stopper = robot_controller.stopper:main'
        ],
    },
)
