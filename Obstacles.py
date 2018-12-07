'''
Created on 2018 M11 24

@author: Tina
'''
import pygame
import random
from Colors import *
from MyImages import *



class Obstacle(object):
    @staticmethod
    def contains(rect,pos):
        return rect.collidepoint(pos)
    
    def __init__(self,x,y,w,h, color = Color.black):
        self.originalx = x 
        self.displayx = self.originalx
        self.y = self.originaly = self.displayy = y
        self.width = w
        self.height = h
        self.color = color
        self.rect = pygame.Rect(self.displayx,self.displayy,self.width,self.height)
    
        
    def getOriginalRect(self):
        return pygame.Rect(self.originalx,self.originaly,self.width,self.height)
        

    def updateRect(self,deltax):
        self.displayx = self.originalx-deltax
        self.rect = pygame.Rect(self.displayx,self.y,self.width,self.height)
        
    def updateRect_FullUpdate(self,deltax,deltay):
        self.displayx = self.originalx-deltax
        self.displayy = self.originaly-deltay
        self.rect = pygame.Rect(self.displayx,self.displayy,self.width,self.height)
    
    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        
        
        
class RandomObstacle(Obstacle):
    def __init__(self, x, y, screenHeight,color = Color.black):
        # x, y coordinate of upper left corner
        self.originalx = x 
        self.displayx = self.originalx
        self.y = self.originaly = self.displayy = y
        self.width = random.randint(50,300)
        self.height = screenHeight - y
        self.color = color
        self.rect = pygame.Rect(self.displayx,self.displayy,self.width,self.height)
        
        
        
class Road(Obstacle):
    def __init__(self,x,y,imagePath):
        self.originalx = x
        self.displayx = self.originalx
        self.y = self.originaly = self.displayy = y
        self.image = pygame.image.load(imagePath)
        self.width, self.height = self.image.get_rect().size
    
    def updateRect(self,deltax):
        self.displayx = self.originalx-deltax
        
    def draw(self,surface):
        surface.blit(self.image,(self.displayx-self.width/2,self.y-self.height/2))
        