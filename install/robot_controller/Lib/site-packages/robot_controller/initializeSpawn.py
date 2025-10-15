#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Kill, Spawn

#Node to kill and spawn turtle at a given location
class InitializeSpawn (Node):
    def __init__(self):
        super().__init__('Initialize_Spawn') 
        self.kill_client = self.create_client(Kill, '/kill')
        self.spawn_client = self.create_client(Spawn, '/spawn')

        self.kill_client.wait_for_service()
        self.spawn_client.wait_for_service()

        x = float(input("Enter spawn X position (float between 0.0 and 11.0): "))
        y = float(input("Enter spawn Y position (float between 0.0 and 11.0): "))

        self.repositionTurtle('turtle1', 'WEAP', x, y)

    def repositionTurtle(self, oldName, newName, x, y):
        reqKill = Kill.Request()
        reqKill.name = oldName
        futurereqKill = self.kill_client.call_async(reqKill)
        rclpy.spin_until_future_complete(self, futurereqKill)

        reqSpawn = Spawn.Request()
        reqSpawn.x = x
        reqSpawn.y = y
        reqSpawn.theta = 0.0
        reqSpawn.name = newName
        futureSpawn = self.spawn_client.call_async(reqSpawn)
        rclpy.spin_until_future_complete(self, futureSpawn)

def main(args=None):
    rclpy.init(args=args)   
    node = InitializeSpawn()      
    rclpy.spin_once(node)       
    rclpy.shutdown()      

if __name__ == '__main__':
    main()