import pygame
import math
import numpy as np
from pathlib import Path

# assumptions
# 1. the robot does not turn and only moves in x and y direction. Rotation only
# makes the physics more complex and does not have any addition to the disturbance observer

class Robot:
    def __init__(self,startpos):
        self.m2p = 3779.52          # Converting from meter to pixels for simulation
        
        # Initiate torques
        self.motor_torque_right = 0
        self.motor_torque_left = 0

        # initiate wheel angles, both have same angle for simplicity
        # Note that this is the angle on which the torque is applied
        # clockwise, 0 is in x direction
        self.motor_torque_angle = 0

        # Initiate robot states based on torques
        self.heading = 0 # robot heading angle in map, not used for now
        self.vrx = 0 # individual motor speeds in different directions
        self.vry = 0 #  - Note that each motor can virtually go in every direction
        self.vlx = 0 #  - Direction much be same on the end.
        self.vly = 0 
        self.vx = 0 # speeds of the robot in absolute map
        self.vy = 0
        self.x = startpos[0] # absolute locations
        self.y = startpos[1]

        # robot properties
        self.w = 10 # weight of robot in kg, assume center of mass between wheels
        self.dw = 1 # distance between wheels in meter
        self.rw = 0.1 # diameter of wheel in meter


    def kinematics(self, dt, ext_f, ext_f_angle,torque_r,torque_l,angle,friction_f):
        # Update states of the robot
        self.motor_torque_right = torque_r
        self.motor_torque_left = torque_l
        self.motor_torque_angle = angle

        # Torque to force
        frx = self.motor_torque_right*self.rw*math.cos(self.motor_torque_angle)
        fry = self.motor_torque_right*self.rw*math.sin(self.motor_torque_angle)
        flx = self.motor_torque_left*self.rw*math.cos(self.motor_torque_angle)
        fly = self.motor_torque_left*self.rw*math.sin(self.motor_torque_angle)
        
        # Calculate global force angle to local 

        # Update motor speeds based on
        # - old velocity
        # - Induced torque
        # - (Half of) external forces which act on the motor
        # - Friction in each direction, can be made a noise in the future
        self.vrx += frx*dt + ext_f*math.cos(ext_f_angle) - math.copysign(pow(self.vrx,2),self.vrx)*friction_f*dt
        self.vry += fry*dt + ext_f*math.sin(ext_f_angle) - math.copysign(pow(self.vry,2),self.vry)*friction_f*dt
        self.vlx += flx*dt + ext_f*math.cos(ext_f_angle) - math.copysign(pow(self.vlx,2),self.vlx)*friction_f*dt
        self.vly += fly*dt + ext_f*math.sin(ext_f_angle) - math.copysign(pow(self.vly,2),self.vly)*friction_f*dt
        # Update general robot speed in absolute map,
        # In theory, vrx = vlx and vry = vly due to the assumption
        # that the robot does not change in angle
        self.vx = (self.vrx+self.vlx)/2
        self.vy = (self.vry+self.vly)/2

        # Update robot position
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt

class Graphics: # (not changed)
    def __init__(self, dimensions, robot_img_path, map_img_path) -> None:
        pygame.init()

        # Defining colours
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)

        # MAP
        # Loading images 

        self.robot = pygame.image.load(robot_img_path)
        self.map_img = pygame.image.load(map_img_path)


        # Dimensions
        self.height, self.width = dimensions

        # Window settings
        pygame.display.set_caption("Obstacle Avoidance")
        self.map = pygame.display.set_mode((self.width,self.height))
        self.map.blit(self.map_img, (0,0))

    def draw_robot(self, x, y, heading):
        rotated = pygame.transform.rotozoom(self.robot, math.degrees(heading), 1)
        rect = rotated.get_rect(center = (x, y))
        self.map.blit(rotated, rect)

class Simulator:
    def __init__(self,robot_startpos,graph_dimensions,robot_img_path,map_img_path):
        self.python_env_folder_name = 'Python_based_env'
        self.robot_img_path = self.__find_png(robot_img_path)
        self.map_img_path = self.__find_png(map_img_path)
        self.graphics = Graphics(graph_dimensions,self.robot_img_path,self.map_img_path)
        self.robot = Robot(robot_startpos)

        self.last_time = pygame.time.get_ticks()
        self.running = True

        # Pressed keys
        self.key1 = False
        self.key2 = False

    def __find_png(self,png_name):
        start_path = Path.cwd()
        target_path_index = start_path.parts.index(self.python_env_folder_name) if self.python_env_folder_name in start_path.parts else None
        if target_path_index is not None:
            start_path = Path(*start_path.parts[:target_path_index + 1])
        for p in start_path.rglob(png_name):
            if p.is_file():
                return p
        return None

    def run(self):
        self.running = True
        external_force = 0
        external_force_angle = 0
        friction_force = 0.05
        torque = 0
        angle = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                general_torque = 10*self.robot.m2p

                if event.type == pygame.KEYDOWN:
                    # Monitor key actions for robot
                    if event.key == pygame.K_UP:
                        # robot upwards
                        angle = 1.5*math.pi
                        torque = general_torque
                    elif event.key == pygame.K_DOWN:
                        # robots downwards
                        angle = 0.5*math.pi
                        torque = general_torque
                    elif event.key == pygame.K_RIGHT:
                        angle = 0
                        torque = general_torque
                    elif event.key == pygame.K_LEFT:
                        angle = math.pi
                        torque = general_torque
                    else:
                        torque = 0

                    # Monitor key actions for external force
                    general_external_force = 1
                    external_force = 0
                    if event.key == pygame.K_w:
                        external_force_angle = 1.5*math.pi
                        external_force = general_external_force
                    elif event.key == pygame.K_s:
                        external_force_angle = 0.5*math.pi
                        external_force = general_external_force
                    elif event.key == pygame.K_d:
                        external_force_angle = 0
                        external_force = general_external_force
                    elif event.key == pygame.K_a:
                        external_force_angle = math.pi
                        external_force = general_external_force
                    else:
                        external_force = 0    
                
                elif event.type == pygame.KEYUP:
                    torque = 0
                    external_force = 0

            
            dt = (pygame.time.get_ticks() - self.last_time)/1000
            self.last_time = pygame.time.get_ticks()

            self.graphics.map.blit(self.graphics.map_img, (0,0))

            self.robot.kinematics(dt,external_force,external_force_angle,torque,torque,angle,friction_force)
            self.graphics.draw_robot(self.robot.x, self.robot.y, self.robot.heading)
            pygame.display.update()


if __name__ =='__main__':
    
    # Define map dimensions
    MAP_DIMENSIONS = (600, 1200)

    # Environment graphics
    robot_img_path = 'DifferentialDriveRobot.png'
    obstacle_img_path = 'ObstacleMap.png'
    # The Robot
    start = (200, 200)
    width = 0.001*3779.52

    simulator = Simulator(start,MAP_DIMENSIONS,robot_img_path,obstacle_img_path)

    simulator.run()