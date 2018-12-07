'''Currently this class is still being developed.'''
'''Control class for entire project. Contains the game loop, and contains
the event_loop which passes events to States as needed. Logic for flipping
states is also found here.'''

import pygame
from StartGame import *
from GoBang import *
from Shooting import *
from Walking import *
from Maze import *
import Constants as c
from Fractal import *
from Colors import *


class Control(object):
    def __init__(self,w,h):
        self.width = w 
        self.height = h 
        self.displaySurface = pygame.display.set_mode((self.width,self.height))
        self.initialize()
        self.clock = pygame.time.Clock()
        
        
    def initialize(self):
        c.totalScore = 0
        self.startGame = StartGame(self.width,self.height)
        self.run1 = WalkingGobang(self.width,self.height,15)
        self.run2 = WalkingMaze(self.width,self.height,15)
        self.run3 = WalkingShoot(self.width,self.height,20)
        self.gobang = GobangGame(self.width,self.height)
        self.maze = Maze(self.width,self.height,25,25,20,20,15)
        self.shoot = Shooting(self.width,self.height,20)
        self.endGame = EndGame(self.width,self.height,2,50)
        self.done = False
        self.gameover = False

        
    
    def run(self):
        while True:
            while self.gameover == False:
                while self.startGame.passed == False:
                    self.startGame.timerFired()
                    self.displaySurface.blit(self.startGame.startSurface,(0,0))
                    if self.startGame.done == True:
                        self.startGame.kinect.close()
                        pygame.quit()
                        break
                    pygame.display.update() 
                    self.clock.tick(60)
                while self.run1.passed == False:
                    self.run1.timerFired()
                    self.displaySurface.blit(self.run1.walkingSurface,(0,0))
                    if self.run1.done == True:
                        self.run1.kinect.close()
                        pygame.quit()
                        break
                    pygame.display.update() 
                    self.clock.tick(25)
                if self.run1.gameover:
                    self.initialize()
                    break
                while self.gobang.passed == False:
                    self.gobang.timerFired()
                    self.displaySurface.blit(self.gobang.gobangGameSurface,(0,0))
                    if self.gobang.done == True:
                        #self.gobang.kinect.close()
                        pygame.quit()
                        break
                    if self.gobang.passed == True:
                        self.run1.passed = False
                    pygame.display.update()
                    self.clock.tick(25)
                if self.gobang.gameover:
                    self.initialize()
                    break
                while self.run1.passed == False:
                    self.run1.timerFired()
                    self.displaySurface.blit(self.run1.walkingSurface,(0,0))
                    if self.run1.done == True:
                        self.run1.kinect.close()
                        pygame.quit()
                        break
                    pygame.display.update() 
                    self.clock.tick(25)
                if self.run1.gameover:
                    self.initialize()
                    break
                while self.run2.passed == False:
                    self.run2.timerFired()
                    self.displaySurface.blit(self.run2.walkingSurface,(0,0))
                    if self.run2.done == True:
                        self.run2.kinect.close()
                        pygame.quit()
                        break
                    pygame.display.update() 
                    self.clock.tick(25)
                if self.run2.gameover:
                    self.initialize()
                    break
                while self.maze.passed == False:
                    self.maze.timerFired()
                    self.displaySurface.blit(self.maze.screen,(0,0))
                    if self.maze.done == True:
                        pygame.quit()
                        break
                    if self.maze.passed == True:
                        self.run2.passed = False
                    pygame.display.update()
                    self.clock.tick(25)
                while self.run2.passed == False:
                    self.run2.timerFired()
                    self.displaySurface.blit(self.run2.walkingSurface,(0,0))
                    if self.run2.done == True:
                        self.run2.kinect.close()
                        pygame.quit()
                        break
                    pygame.display.update() 
                    self.clock.tick(25)
                if self.run2.gameover:
                    self.initialize()
                    break
                while self.run3.passed == False:
                    self.run3.timerFired()
                    self.displaySurface.blit(self.run3.walkingSurface,(0,0))
                    if self.run3.done == True:
                        self.run3.kinect.close()
                        pygame.quit()
                        break
                    pygame.display.update() 
                    self.clock.tick(25)
                if self.run3.gameover:
                    self.initialize()
                    break
                while self.shoot.passed == False:
                    self.shoot.timerFired()
                    self.displaySurface.blit(self.shoot.shootingSurface,(0,0))
                    if self.shoot.done == True:
                        pygame.quit()
                        break
                    if self.shoot.passed == True:
                        self.run3.passed = False
                    pygame.display.update()
                    self.clock.tick(20)
                while self.run3.passed == False:
                    self.run3.timerFired()
                    self.displaySurface.blit(self.run3.walkingSurface,(0,0))
                    if self.run3.done == True:
                        self.run3.kinect.close()
                        pygame.quit()
                        break
                    pygame.display.update() 
                    self.clock.tick(25)
                if self.run3.gameover:
                    self.initialize()
                    break
                delta = c.totalScore - 50
                if delta > 0:
                    for tree in range(delta):
                        x = random.randint(50,4000)
                        self.endGame.trees.append(Tree_Two(random.randint(50,4000),self.height-140-675/2,675,675))
                elif delta < 0:
                    for tree in range(abs(delta)):
                        self.endGame.trees.pop()
                while self.endGame.passed == False:
                    self.endGame.timerFired()
                    self.displaySurface.blit(self.endGame.walkingSurface,(0,0))
                    if self.endGame.done == True:
                        self.endGame.kinect.close()
                        pygame.quit()
                        break
                    pygame.display.update() 
                    self.clock.tick(25)
                if self.endGame.gameover:
                    self.initialize()
                    break
            
            

#pygame.init()         
#bigPicture = Control(1200,675)
#bigPicture.run()

