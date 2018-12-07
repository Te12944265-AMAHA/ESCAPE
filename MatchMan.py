import pygame
import random
import os
import math
from MyImages import *
from Obstacles import *


class MatchMan(object):
    def __init__(self, x, y):
        self.rightCollided = 0
        self.x = x
        self.y = y
        self.prevx = x
        self.prevy = y
        self.displayx = x
        self.displayy = y
        self.state = "stand"
        self.direction = "right"
        self.vx = 0 # per 0.04 s
        self.vy = 0
        self.prevvx = 0 
        self.prevvy = 0
        self.ax = 0
        self.ay = 0
        self.manRunRight = []
        self.manRunLeft = []
        currDir = "icon/match/run_right_raw"
        for file in os.listdir(currDir):
            fileName = currDir + "/" + file
            #print(fileName)
            rawImg = pygame.image.load(fileName)
            #x,y = self.getSize()
            #newImg = pygame.transform.scale(rawImg, (int(x*0.9),int(y*0.9)))
            flippedImg = pygame.transform.flip(rawImg,True,False)
            self.manRunRight.append(rawImg)
            self.manRunLeft.append(flippedImg)
        self.gifSize = len(self.manRunRight)
        self.manStand = pygame.image.load("icon/match/stand_raw2.gif")
        self.manJumpRight = pygame.image.load("icon/match/jump_right_raw2.gif")
        self.manJumpLeft = pygame.transform.flip(self.manJumpRight, True, False)
        #self.rect = pygame.Rect(x - self.radius, y - self.radius,2 * self.radius, 2 * self.radius)
        
    def isFall(self,screenHeight):
        return self.y - self.getSize()[1]/2 > screenHeight 
        
        
    def getSize(self):
        if self.state == "run":
            return self.manRunRight[0].get_rect().size
        elif self.state == "jump":
            return self.manJumpRight.get_rect().size
        elif self.state == "stand":
            return self.manStand.get_rect().size
    
    def getRect(self):
        w, h = self.getSize()
        return pygame.Rect(self.x - w/2,self.y - h/2,w,h)
    
    def getDisplayRect(self):
        w, h = self.getSize()
        return pygame.Rect(self.displayx - w/2, self.y - h/2,w,h)
    
    def getDisplayRect_FullUpdate(self):
        w, h = self.getSize()
        return pygame.Rect(self.displayx - w/2, self.y - h/2,w,h)
    
    def getCoordinate(self):
        w,h = self.getSize()
        return (self.x - w/2,self.y - h/2)
    
    def getDisplayCoordinate(self):
        w,h = self.getSize()
        return (self.displayx - w/2,self.y-h/2)
    
    def getDisplayCoordinate_FullUpdate(self):
        w,h = self.getSize()
        return (self.displayx - w/2,self.displayy-h/2)
                
                
    def getBottom(self):
        w,h = self.getSize()
        return self.y+h/2
    
    def isBottomCollided(self,rect):
        print("checking bottom collision")
        #print(self.getBottom() - rect.y)
        if abs(self.getBottom() - rect.y) <= 6:
            print("bottom collided!")
            return True
        return False
    
    def getTop(self):
        w,h = self.getSize()
        return self.y - h/2
    
    def isTopCollided(self,rect):
        if abs(self.getTop() - (rect.y+rect.size[1])) <= 6:
            return True
        return False
    
    def getLeft(self):
        w,h = self.getSize()
        return self.x-w/2
    
    def isLeftCollided(self,rect):
        print("checking left collision")
        #print(rect.x)
        #print(abs(self.getLeft() - (rect.x + rect.size[0])))
        if abs(self.getLeft() - (rect.x + rect.size[0])) <= 6:
            print("left collided!")
            return True
        return False
    
    def getRight(self):
        w,h = self.getSize()
        return self.x + w/2
    
    def isRightCollided(self,rect):
        print("checking right collision")
        #print(self.getRight() - rect.x)
        if abs(self.getRight() - rect.x) <= 6:
            print("RightCollided!")
            return True
        return False
            
    def isCollided(self,rect):
        return self.getRect().colliderect(rect)
    
    def updatePos(self,rectList,keys,bodyState,vy):
        self.updateState(rectList, keys,bodyState,vy)
        self.updateSp()
        self.x += self.vx
        self.y += self.vy
        
        
    def updateSp(self):
        self.updateAcceleration()
        if self.state == "run":
            self.moveX()
        elif self.state == "stand":
            self.vx = 0
        self.vy += self.ay
        self.vx += self.ax
        
    def updateAcceleration(self):
        if self.state == "run":
            self.ay = 0
        elif self.state == "jump":
            self.ay = 100/25
        
        
    def jump(self,vy):
        if abs(vy) > 1200:
            vy = 1200
        self.vy = -20-int((abs(vy)-400)*1/40)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1",self.vy)
        
    def updateState(self,rectList,keys,bodyState,vy):
        bottomCollided = False
        leftCollided = False
        rightCollided = False
        #print(keys[pygame.K_UP])
        for rect in rectList:
            if self.isCollided(rect):
                print("yes,collided with this rect:")
                if self.isBottomCollided(rect):
                    bottomCollided = True
                if self.isRightCollided(rect):
                    self.rightCollided += 1
                    rightCollided = True
                if self.isLeftCollided(rect):
                    leftCollided = True
                 
            else: 
                print("not collided with this rect:")
                if self.rightCollided == 1:
                    print(rect,"   ", self.getRect())
        print(self.getBottom())
        #print(self.rightCollided)
        if bottomCollided == True:
            if self.vy == 0:
                self.state = "stand"
                self.ay = 0
                if keys[pygame.K_RIGHT] or bodyState["right"]:
                    if not rightCollided:
                        self.state = "run"
                        self.direction = "right"
                    elif rightCollided:
                        self.state = "stand"
                        self.vx = 0
                elif keys[pygame.K_LEFT] or bodyState["left"]:
                    if not leftCollided:
                        self.state = "run"
                        self.direction = "left"
                    elif leftCollided:
                        self.state = "stand"
                        self.vx = 0
                if keys[pygame.K_UP] or bodyState["up"]:
                    self.state = "jump"
                    self.jump(vy)
            # moving up yet bottom collided
            elif self.vy < 0 :
                print("jumping!")
                self.state = "jump"
            
            # falling down
            elif self.vy > 0:
                print("falling down and bottom collide")
                self.state = "stand"
                self.vy = 0
                self.ay = 0
                self.vx = 0
        elif bottomCollided == False:
            if self.state == "jump":
                if rightCollided or leftCollided:
                    self.vx = 0
                else:
                    if keys[pygame.K_RIGHT] or bodyState["right"]:
                        self.direction = "right"
                        self.moveX()
                    elif keys[pygame.K_LEFT] or bodyState["left"]:
                        self.direction = "left"
                        self.moveX()
                for rect in rectList:
                    bottomRightCorner = self.x + math.ceil(self.getSize()[0]/2),self.y + math.ceil(self.getSize()[1]/2)
                    bottomLeftCorner = self.x - math.ceil(self.getSize()[0]/2),math.ceil(self.y + self.getSize()[1]/2)
                    if (self.vx == 0 and self.vy > 0  and 
                    (Obstacle.contains(rect,bottomRightCorner) and Obstacle.contains(rect,bottomLeftCorner))):
                        print("changes to stand")
                        self.state = "stand"
                        self.y = rect.y+1-self.getSize()[1]//2
                        self.ay = 0
                        self.vy = 0  
                    elif (self.vx != 0 and self.vy > 0  and 
                    (Obstacle.contains(rect,bottomRightCorner) or Obstacle.contains(rect,bottomLeftCorner))):
                        print("changes to stand")
                        self.state = "stand"
                        self.y = rect.y+1-self.getSize()[1]//2
                        self.ay = 0
                        self.vy = 0  
            elif self.state == "run" or self.state == "stand":
                self.state = "jump"
                
        
    def moveX(self):
        if self.direction == "right":
            self.vx = 150/25
        elif self.direction == "left":
            self.vx = -150/25
            
    def getDeltaX(self):
        return self.x - self.displayx
    
    def getDeltaY(self):
        return self.y - self.displayy
        

    def draw(self,surface,frame):
        if self.state == "stand":
            surface.blit(self.manStand,self.getDisplayCoordinate())
        elif self.state == "jump":
            if self.direction == "right":
                surface.blit(self.manJumpRight,self.getDisplayCoordinate())
            elif self.direction == "left":
                surface.blit(self.manJumpLeft,self.getDisplayCoordinate())
        elif self.state == "run":
            if self.direction == "right":
                surface.blit(self.manRunRight[frame],self.getDisplayCoordinate())
            elif self.direction == "left":
                surface.blit(self.manRunLeft[frame],self.getDisplayCoordinate())
     
    def draw_FullUpdate(self,surface,frame):
        if self.state == "stand":
            surface.blit(self.manStand,self.getDisplayCoordinate_FullUpdate())
        elif self.state == "jump":
            if self.direction == "right":
                surface.blit(self.manJumpRight,self.getDisplayCoordinate_FullUpdate())
            elif self.direction == "left":
                surface.blit(self.manJumpLeft,self.getDisplayCoordinate_FullUpdate())
        elif self.state == "run":
            if self.direction == "right":
                surface.blit(self.manRunRight[frame],self.getDisplayCoordinate_FullUpdate())
            elif self.direction == "left":
                surface.blit(self.manRunLeft[frame],self.getDisplayCoordinate_FullUpdate())           
    
        