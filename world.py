from agents import Car, Pedestrian, RectangleBuilding
from entities import Entity
from typing import Union
from visualizer import Visualizer
import csv
from csv import writer
import numpy as np
import time
from random import *
import sys

class World:
    def __init__(self, dt: float, width: float, height: float, ppm: float = 8):
        self.dynamic_agents = []
        self.static_agents = []
        self.t = 0.0 # simulation time
        self.dt = dt  # simulation time step
        self.visualizer = Visualizer(width, height, ppm=ppm)
        self.sensorStrength = 40  # change to 55 for  EMS case
        self.globalInformation = {}
        self.threshold = 21  #21 # Velocity is which if autonomous vehicle is below, automatically change lanes and attempt to get back to speed
        self.potentialCollisionLeft = []
        self.potentialCollisionRight = []
        self.autoV = []
        self.humanV = []
        self.noV2V = []
        self.accThreshold = 4   # 4 for human , 7 for AV !!!
        self.decrementAmt = 1
        self.numCollisions = 0
        self.lastCollision = None

    def add(self, entity: Entity):
        if entity.movable:
            self.dynamic_agents.append(entity)
            self.potentialCollisionLeft.append([False,1])
            self.potentialCollisionRight.append([False,1])
            if isinstance(entity, Car):
                self.globalInformation[entity.ID] = entity
                if entity.type == "H":
                    self.humanV.append(entity)
                elif entity.type == "A": 
                    self.autoV.append(entity)
                else:
                    self.noV2V.append(entity)
            if isinstance(entity, Pedestrian):
                self.humanV.append(entity)
                self.autoV.append(entity)
                self.noV2V.append(entity)
        else:
            self.static_agents.append(entity)
            self.potentialCollisionLeft.append([False,1])
            self.potentialCollisionRight.append([False,1])
    
    def delete(self):
        for car in self.dynamic_agents:
            if car.center.x < 0:
                self.dynamic_agents.remove(car)  
                del car


    def tick(self):
        for agent in self.dynamic_agents:
            agent.tick( self.dt, self.dynamic_agents, self.potentialCollisionLeft, self.potentialCollisionRight)
        self.t += self.dt

    def render(self):
        self.visualizer.create_window(bg_color='gray')
        self.visualizer.update_agents(self.agents)

    @property
    def agents(self):
        return self.static_agents + self.dynamic_agents

    def collision_exists(self, agent=None):
        if agent is None:
            for i in range(len(self.dynamic_agents)):
                for j in range(i + 1, len(self.dynamic_agents)):
                    if self.dynamic_agents[i].collidable and self.dynamic_agents[j].collidable:
                        if self.dynamic_agents[i].collidesWith(self.dynamic_agents[j]) :
                            currentCollision = [self.dynamic_agents[i], self.dynamic_agents[j]]
                            if currentCollision != self.lastCollision:
                                self.lastCollision = [self.dynamic_agents[i], self.dynamic_agents[j]]
                                #print("adding collision")
                                self.numCollisions +=1 

    def inRange(self, agent=None):
        if agent is None:
            for i in range(len(self.dynamic_agents)):
                for j in range(i + 1, len(self.dynamic_agents)):
                    if self.dynamic_agents[i].collidable and self.dynamic_agents[j].collidable and self.dynamic_agents[
                        i].sensor:
                        if self.dynamic_agents[i].inRangeWith(self.sensorStrength, self.dynamic_agents[j]):
                            # print( self.dynamic_agents[j].ID + " is within range of ", self.dynamic_agents[i].ID)
                            return True
                for j in range(len(self.static_agents)):
                    if self.dynamic_agents[i].collidable and self.static_agents[j].collidable and self.dynamic_agents[
                        i].sensor:
                        if self.dynamic_agents[i].inRangeWith(self.sensorStrength, self.static_agents[j]):
                            # print( self.dynamic_agents[j].ID + " is within range of ", self.dynamic_agents[i].ID)
                            return True
            return False

        if not agent.collidable: return False

        range_list = []
        for i in range(len(self.agents)):
            if self.agents[i] is not agent and self.agents[i].collidable and agent.inRangeWith(self.sensorStrength,
                                                                                               self.agents[i]):
                # print( self.agents[i].ID + " is within range of ", agent.ID)
                range_list.append(self.agents[i])
        return range_list

    def checkLeftLane(self, vehicle, curX, curY):
        if (abs(vehicle.center.x - curX) < self.calcStoppingDistance(vehicle)) and (vehicle.center.y > curY - 15):
            return False
        else:
            return True

    def checkRightLane(self, vehicle, curX, curY):
        if (abs(vehicle.center.x - curX ) < self.calcStoppingDistance(vehicle))  and (vehicle.center.y > curY + 15):
            return False
        else:
            return True
    
    def calcStoppingDistance(self, vehicle):
        if isinstance(vehicle, RectangleBuilding): return sys.maxsize

        mu = .9  # Mu constant in total stopping distance
        reactionTime = .5  # Perception-Reaction time
        worldAccelerationValue = 3.44  # Modelling a safe human driver, change up according to desired condition
        totalStop = vehicle.velocity.x * reactionTime + (np.square(vehicle.velocity.x) / (2 * mu * worldAccelerationValue))
        return totalStop

    def pedestrianAhead(self, vehicle, pedestrian):
        if vehicle.center.x > pedestrian.center.x and (vehicle.center.y - 5 < pedestrian.center.y and  vehicle.center.y + 5 > pedestrian.center.y): # vehicle.y - 5 < py < vehicle +5
            return True
        return False
    
    def obstacleAhead(self, vehicle, rangeList): # returns true is there is an obstacle ahead 
        for obstacle in rangeList:
            if obstacle.center.x > vehicle.center.x and (vehicle.center.y - 5 < obstacle.center.y and vehicle.center.y + 5 > obstacle.center.y):
                return True 
        return False
        
    def humanCollisionAvoidance(self):
        speed = False
        for i in self.humanV:
            if isinstance(i, Car):
                result = self.inRange(i)
                if len(result) != 0 and speed == False:
                    for j in result:  # this is range list 
                        if isinstance(j, Car):
                            if j.lane == i.lane:
                                # slow down car in back
                                if j.center.x > i.center.x:
                                    if j.acceleration > -1*self.accThreshold and j.velocity.x != 0 :
                                        j.inputAcceleration = j.acceleration - self.decrementAmt*2
                                else:
                                    if i.acceleration > -1*self.accThreshold and i.velocity.x != 0:
                                        i.inputAcceleration = i.acceleration - self.decrementAmt*2
                        if isinstance(j, Pedestrian) and self.pedestrianAhead(i,j):
                            if i.acceleration > -1*self.accThreshold and i.velocity.x != 0:
                                i.inputAcceleration = i.acceleration - self.decrementAmt*2
                elif not self.obstacleAhead(i, result) :  # if the range list is empty
                    if (abs(i.velocity.x) < 30) and (i.acceleration < self.accThreshold):
                        speed = True
                        i.inputAcceleration = i.acceleration + self.decrementAmt*2

    def autonomousCollisionAvoidance(self):
        for i in self.autoV:
            if isinstance(i, Car): 
                result = self.inRange(i)
                if len(result) != 0:
                    for j in result:  # this is range list 
                        if isinstance(j, Car):
                            if j.lane == i.lane:
                                if j.center.x > i.center.x:  # Want to slow down the vehicle behind first vehicle
                                    if abs(j.velocity.x) > 4 and (self.potentialCollisionRight[int(j.ID)][1] == 1 and self.potentialCollisionLeft[int(j.ID)][1] == 1):
                                        if j.acceleration > -1*self.accThreshold and j.velocity.x != 0 :
                                            j.inputAcceleration = j.acceleration - self.decrementAmt*2
                                    if abs(j.velocity.x) < self.threshold and (self.potentialCollisionRight[int(j.ID)][1] == 1 and self.potentialCollisionLeft[int(j.ID)][1] == 1):
                                        # left lane = 0
                                        # right lane = 1
                                        lane = randint(0, 1)
                                        curX = j.center.x
                                        curY = j.center.y
                                        if lane == 0:
                                            for vehicle in self.inRange(j):
                                                if self.checkLeftLane(vehicle, curX, curY) and j.lane != 1:
                                                    self.potentialCollisionLeft[int(j.ID)][0] = True 
                                                elif self.checkRightLane(vehicle, curX, curY) and j.lane != 4:
                                                    self.potentialCollisionRight[int(j.ID)][0] = True 
                                        else:
                                            for vehicle in self.inRange(j):
                                                if self.checkRightLane(vehicle, curX, curY) and j.lane != 4:
                                                    self.potentialCollisionRight[int(j.ID)][0] = True 
                                                elif self.checkLeftLane(vehicle, curX, curY) and j.lane != 1:
                                                    self.potentialCollisionLeft[int(j.ID)][0] = True 

                                else: # i is in back 
                                    if abs(i.velocity.x) > 4 and (self.potentialCollisionRight[int(i.ID)][1] == 1 and self.potentialCollisionLeft[int(i.ID)][1] == 1):
                                        if i.acceleration > -1*self.accThreshold and i.velocity.x != 0 :
                                            i.inputAcceleration = i.acceleration - self.decrementAmt*2
                                    if abs(i.velocity.x) < self.threshold and (self.potentialCollisionRight[int(i.ID)][1] == 1 and self.potentialCollisionLeft[int(i.ID)][1] == 1):
                                        lane = randint(0, 1)
                                        curX = i.center.x
                                        curY = i.center.y
                                        if lane == 0: # try merge left first 
                                            for vehicle in self.inRange(i):
                                                if self.checkLeftLane(vehicle, curX, curY) and i.lane != 1:
                                                    self.potentialCollisionLeft[int(i.ID)][0] = True
                                                elif self.checkRightLane(vehicle, curX, curY) and i.lane != 4:
                                                    self.potentialCollisionRight[int(i.ID)][0] = True 
                                                # if neither lane is free, do nothing 
                                        else: # try merge right first 
                                            for vehicle in self.inRange(i):
                                                if self.checkRightLane(vehicle, curX, curY) and i.lane != 4:
                                                    self.potentialCollisionRight[int(i.ID)][0] = True 
                                                elif self.checkLeftLane(vehicle, curX, curY) and i.lane != 1:
                                                    self.potentialCollisionLeft[int(i.ID)][0] = True 

                        if isinstance(j, Pedestrian) and self.pedestrianAhead(i, j):
                            if abs(i.velocity.x) > 4 and (self.potentialCollisionRight[int(i.ID)][1] == 1 and self.potentialCollisionLeft[int(i.ID)][1] == 1):
                                if i.acceleration > -1*self.accThreshold and i.velocity.x != 0 :
                                    i.inputAcceleration = i.acceleration - self.decrementAmt*4
                            if (abs(i.velocity.x) < self.threshold) and (self.potentialCollisionRight[int(i.ID)][1] == 1 and self.potentialCollisionLeft[int(i.ID)][1] == 1):
                                lane = randint(0, 1)
                                curX = i.center.x
                                curY = i.center.y
                                if lane == 0:
                                    for vehicle in self.inRange(i):
                                        if self.checkLeftLane(vehicle, curX, curY) and i.lane != 1:
                                            self.potentialCollisionLeft[int(i.ID)][0] = True
                                        elif self.checkRightLane(vehicle, curX, curY) and i.lane != 4:
                                            self.potentialCollisionRight[int(i.ID)][0] = True
                                        # if neither lane is free, do nothing 
                                else:
                                    for vehicle in self.inRange(i):
                                        if self.checkRightLane(vehicle, curX, curY) and i.lane != 4:
                                            self.potentialCollisionRight[int(i.ID)][0] = True 
                                        elif self.checkLeftLane(vehicle, curX, curY) and i.lane != 1:
                                            self.potentialCollisionLeft[int(i.ID)][0] = True 
                elif self.obstacleAhead(i, result) == False:  # if the range list is empty
                    if (abs(i.velocity.x) < 30) and (i.acceleration < self.accThreshold):
                        i.inputAcceleration = i.acceleration + self.decrementAmt*2
    

    def autonomousCollisionAvoidanceNoV2V(self):
        for i in self.noV2V:
            if isinstance(i, Car): 
                result = self.inRange(i)
                if len(result) != 0:
                    for j in result:  # this is range list 
                        if isinstance(j, Car):
                            if abs(j.velocity.x) > 4 and (self.potentialCollisionRight[int(j.ID)][1] == 1 and self.potentialCollisionLeft[int(j.ID)][1] == 1):
                                if j.acceleration > -1*self.accThreshold and j.velocity.x != 0 :
                                    j.inputAcceleration = j.acceleration - self.decrementAmt*2
                            if abs(j.velocity.x) < self.threshold and (self.potentialCollisionRight[int(j.ID)][1] == 1 and self.potentialCollisionLeft[int(j.ID)][1] == 1):
                                # left lane = 0
                                # right lane = 1
                                lane = randint(0, 1)
                                curX = j.center.x
                                curY = j.center.y
                                if lane == 0:
                                    for vehicle in self.inRange(j):
                                        if self.checkLeftLane(vehicle, curX, curY) and j.lane != 1:
                                            self.potentialCollisionLeft[int(j.ID)][0] = True 
                                        elif self.checkRightLane(vehicle, curX, curY) and j.lane != 4:
                                            self.potentialCollisionRight[int(j.ID)][0] = True 
                                else:
                                    for vehicle in self.inRange(j):
                                        if self.checkRightLane(vehicle, curX, curY) and j.lane != 4:
                                            self.potentialCollisionRight[int(j.ID)][0] = True 
                                        elif self.checkLeftLane(vehicle, curX, curY) and j.lane != 1:
                                            self.potentialCollisionLeft[int(j.ID)][0] = True 
                        if isinstance(j, Pedestrian) and self.pedestrianAhead(i, j):
                            if abs(i.velocity.x) > 4 and (self.potentialCollisionRight[int(i.ID)][1] == 1 and self.potentialCollisionLeft[int(i.ID)][1] == 1):
                                if i.acceleration > -1*self.accThreshold and i.velocity.x != 0 :
                                    i.inputAcceleration = i.acceleration - self.decrementAmt*4
                            if (abs(i.velocity.x) < self.threshold) and (self.potentialCollisionRight[int(i.ID)][1] == 1 and self.potentialCollisionLeft[int(i.ID)][1] == 1):
                                lane = randint(0, 1)
                                curX = i.center.x
                                curY = i.center.y
                                if lane == 0:
                                    for vehicle in self.inRange(i):
                                        if self.checkLeftLane(vehicle, curX, curY) and i.lane != 1:
                                            self.potentialCollisionLeft[int(i.ID)][0] = True
                                        elif self.checkRightLane(vehicle, curX, curY) and i.lane != 4:
                                            self.potentialCollisionRight[int(i.ID)][0] = True
                                        # if neither lane is free, do nothing 
                                else:
                                    for vehicle in self.inRange(i):
                                        if self.checkRightLane(vehicle, curX, curY) and i.lane != 4:
                                            self.potentialCollisionRight[int(i.ID)][0] = True 
                                        elif self.checkLeftLane(vehicle, curX, curY) and i.lane != 1:
                                            self.potentialCollisionLeft[int(i.ID)][0] = True 
                elif self.obstacleAhead(i, result) == False:  # if the range list is empty
                    if (abs(i.velocity.x) < 30) and (i.acceleration < self.accThreshold):
                        i.inputAcceleration = i.acceleration + self.decrementAmt*2

    def makeFile(self):
        with open('globalInformation.csv', 'w', newline='') as csvfile:
            fieldnames = ['time', 'ID', 'acceleration', 'velocity', 'position', 'collisions']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    def updateGlobalInformation(self):
        for key in self.globalInformation:
            acceleration = self.globalInformation[key].acceleration
            velocity = self.globalInformation[key].velocity
            position = self.globalInformation[key].center
            with open('globalInformation.csv', 'a+', newline='') as write_obj:
                csv_writer = writer(write_obj)
                csv_writer.writerow([self.t, key, acceleration, velocity, position, self.numCollisions])

    def close(self):
        self.reset()
        self.static_agents = []
        if self.visualizer.window_created:
            self.visualizer.close()

    def reset(self):
        self.dynamic_agents = []
        self.t = 0
