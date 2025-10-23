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
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'hello_node = robot_controller.hello_node:main',
            'circle_publisher = robot_controller.circle_publisher:main',
            'pose_subscriber = robot_controller.pose_subscriber:main',
            'num_generator_publisher = robot_controller.num_generator_publisher:main',
            'summer = robot_controller.summer:main',
            'alert_subscriber = robot_controller.alert_subscriber:main',

        ],
    },
)
