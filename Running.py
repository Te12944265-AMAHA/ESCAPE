from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import ctypes
import _ctypes
import pygame
import sys
import math
import random

from MyImages import *
from Colors import *
from MatchMan import *
from Obstacles import *
from Colors import *

    


class ShootingGame(object):
    def __init__(self,w,h,numObstacle):
        self.width = w 
        self.height = h 
        self.numObstacle = numObstacle
        self.done = False
        self.clock = pygame.time.Clock()
        #self.shootingGameSurface = pygame.display.set_mode((self.width,self.height))
        #self.road = Road(0,self.height - 140,"icon/road/road_black.gif")
        #self.scroll = 0
        self.road = Obstacle(0,self.height-140,6000,140)
        self.matchMan = MatchMan(300,self.height-140-103)
        self.obstacles = [self.road]
        #self.obstaclesRectList = [self.road.getOriginalRect()]
        self.obstaclesRectList = [self.road.getOriginalRect()]
        for obstacle in range(numObstacle):
            x = random.randint(500,1000)
            y = random.randint(self.height-140-105,self.height-140-50)
            thisObstacle = RandomObstacle(x,y,self.height,Color.black)
            self.obstacles.append(thisObstacle)
            self.obstaclesRectList.append(thisObstacle.getOriginalRect()) # 
        print(self.obstaclesRectList)
        self.timerCalled = 0
        
    def keyPressed1(self,event):
        if event.key == pygame.K_UP:
            self.matchMan.state = "jump"
            self.matchMan.jump()
        elif event.key == pygame.K_DOWN:
            self.matchMan.state = "stand"
        elif event.key == pygame.K_LEFT:
            if self.matchMan.state != "jump":
                self.matchMan.state = "run"
            self.matchMan.direction = "left"
            self.matchMan.moveX()
        elif event.key == pygame.K_RIGHT:
            self.matchMan.direction = "right"
            if self.matchMan.state != "jump":
                self.matchMan.state = "run"
            self.matchMan.moveX()
        
    def keyPressed(self,keys):
        if keys[pygame.K_LEFT]:
            if self.matchMan.state != "jump":
                self.matchMan.state = "run"
            self.matchMan.direction = "left"
            self.matchMan.moveX()
        
        if keys[pygame.K_RIGHT]:
            self.matchMan.direction = "right"
            if self.matchMan.state != "jump":
                self.matchMan.state = "run"
            self.matchMan.moveX()
        
        if keys[pygame.K_UP]:
            self.matchMan.state = "jump"
            self.matchMan.jump(self.height-140)
        
        if keys[pygame.K_DOWN]:
            pass
    
    def keyReleased(self,event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            if self.matchMan.state == "run":
                self.matchMan.state = "stand"
  
        
    def redrawAll(self):
        self.shootingGameSurface.fill(Color.white)
        for obstacle in self.obstacles:
            obstacle.draw(self.shootingGameSurface)
        self.matchMan.draw(self.shootingGameSurface, self.timerCalled%self.matchMan.gifSize)
        
    
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    self.keyPressed(event)
                elif event.type == pygame.KEYUP:
                    self.keyReleased(event)
            keys = pygame.key.get_pressed()
            self.keyPressed(keys)
            self.matchMan.updatePos(self.obstaclesRectList,keys)
            deltax = self.matchMan.getDeltaX()
            for obstacle in self.obstacles:
                obstacle.updateRect(deltax)
                
            self.redrawAll()
            
            self.timerCalled += 1
            pygame.display.update()
            self.clock.tick(25)
        pygame.quit()
        
#game = ShootingGame(1200,700,1)
#game.run()
                    
                    