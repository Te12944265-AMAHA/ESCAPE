import pygame
import random
import os
import math
from MyImages import *


class MatchMan(object):
    def __init__(self, x, y):
        self.rightCollided = 0
        self.x = x
        self.y = y
        self.prevx = x
        self.prevy = y
        self.displayx = x
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
    
    def getCoordinate(self):
        w,h = self.getSize()
        return (self.x - w/2,self.y - h/2)
    
    def getDisplayCoordinate(self):
        w,h = self.getSize()
        return (self.displayx - w/2,self.y-h/2)
    
    # the first version. I have written three versions, none of them are fully functioning.
    # other versions are commented below.
    def updatePos(self,groundHeight):
        self.updateSp(groundHeight)
        self.prevx = self.x
        self.prevy = self.y
        self.prevvy = self.vy
        self.updateState(groundHeight)
#         for rect in rectList:
#             if self.isCollided(rect):
#                 print(rect)
#                 self.updateCollision(rect)
        self.x +=self.vx
        self.y += self.vy
        x,y = self.getCoordinate()
        w,h = self.getSize()
        if y+h + self.vy >= groundHeight:
            self.y = groundHeight-h/2
            self.vy = 0
            self.vx = 0
        self.updateState(groundHeight)
        
    def updateSp(self,groundHeight):
        self.updateAcceleration(groundHeight)
        x,y = self.getCoordinate()
        w,h = self.getSize()
        self.vy += self.ay
        self.vx += self.ax
        
    def updateAcceleration(self,groundHeight):
        x,y = self.getCoordinate()
        w,h = self.getSize()
        if y + h >= groundHeight:
            self.ay = 0
        else: self.ay = 100/25
        
    def updateState(self,groundHeight):
        x,y = self.getCoordinate()
        w,h = self.getSize()
        if self.prevy < self.y and y+h >= groundHeight:
            self.state = "stand"
            
    def updateCollision(self,rect):
        if self.isBottomCollided(rect):
            self.state = "stand"
            self.ay = 0
            self.vy = 0
        else:
            self.ay = 100/25
        if self.isTopCollided(rect):
            self.vy = -self.vy
        if self.isLeftCollided(rect) or self.isRightCollided(rect):
            self.vx = 0
            if self.state == "run":
                self.state = "stand"
                
                
    def getBottom(self):
        w,h = self.getSize()
        return self.y+h/2
    
    def isBottomCollided(self,rect):
        print("checking bottom collision")
        print(abs(self.getBottom() - rect.y))
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
        print(abs(self.getRight() - rect.x))
        if abs(self.getRight() - rect.x) <= 6:
            print("RightCollided!")
            return True
        return False
            
#     def isCollided(self,rect):
#         return self.getRect().colliderect(rect)
#     
#     def updatePos(self,rectList,keys):
#         self.updateState(rectList, keys)
#         self.updateSp()
#         self.x += self.vx
#         self.y += self.vy
#         
#         
#     def updateSp(self):
#         self.updateAcceleration()
#         if self.state == "run":
#             self.moveX()
#         elif self.state == "stand":
#             self.vx = 0
#         self.vy += self.ay
#         self.vx += self.ax
#         
#     def updateAcceleration(self):
#         
#         if self.state == "run":
#             self.ay = 0
#         elif self.state == "jump":
#             self.ay = 100/25
#         
#     def jump(self):
#         self.vy = -40
#         
#     def updateState(self,rectList,keys):
#         bottomCollided = False
#         leftCollided = False
#         rightCollided = False
#         #print(keys[pygame.K_UP])
#         for rect in rectList[0:2]:
#             if self.isCollided(rect):
#                 print("yes,collided with this rect:")
#                 if self.isBottomCollided(rect):
#                     bottomCollided = True
#                 if self.isRightCollided(rect):
#                     self.rightCollided += 1
#                     rightCollided = True
#                 if self.isLeftCollided(rect):
#                     leftCollided = True
#                  
#             else: 
#                 print("not collided with this rect:")
#                 if self.rightCollided == 1:
#                     print(rect,"   ", self.getRect())
#         print(self.rightCollided)
#         if bottomCollided == True:
#             if self.vy == 0:
#                 self.state = "stand"
#                 self.ay = 0
#                 if keys[pygame.K_RIGHT]:
#                     if not rightCollided:
#                         self.state = "run"
#                         self.direction = "right"
#                     elif rightCollided:
#                         self.state = "stand"
#                         self.vx = 0
#                 elif keys[pygame.K_LEFT]:
#                     if not leftCollided:
#                         self.state = "run"
#                         self.direction = "left"
#                     elif leftCollided:
#                         self.state = "stand"
#                         self.vx = 0
#                 if keys[pygame.K_UP]:
#                     self.state = "jump"
#                     self.jump()
#             # moving up yet bottom collided
#             elif self.vy < 0 :
#                 self.state = "jump"
#             
#             # falling down
#             elif self.vy > 0:
#                 self.state = "stand"
#                 self.vy = 0
#                 self.ay = 0
#                 self.vx = 0
#         elif bottomCollided == False:
#             if self.state == "jump":
#                 if rightCollided or leftCollided:
#                     self.vx = 0
#             elif self.state == "run" or self.state == "stand":
#                 self.state = "jump"
                
        
        
#     def updateState(self,rectList,keys):
#         bottomCollided = False
#         leftCollided = False
#         rightCollided = False
#         #print(keys[pygame.K_UP])
#         for rect in rectList[0:2]:
#             if self.isCollided(rect):
#                 print("yes,collided with this rect:")
#                 if self.isBottomCollided(rect):
#                     bottomCollided = True
#                 if self.isRightCollided(rect):
#                     self.rightCollided += 1
#                     rightCollided = True
#                 if self.isLeftCollided(rect):
#                     leftCollided = True
#                  
#             else: 
#                 print("not collided with this rect:")
#                 if self.rightCollided == 1:
#                     print(rect,"   ", self.getRect())
#         print(self.rightCollided)
#         if keys[pygame.K_LEFT]: self.direction = "left"
#         elif keys[pygame.K_RIGHT]: self.direction = "right"
#         if bottomCollided and (leftCollided or rightCollided) and self.state!= "jump":
#             print("pic should fix!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
#             self.state = "stand"
#             self.vx = 0
#             self.vy = 0
#             self.ay = 0
#             if ((keys[pygame.K_LEFT] and not leftCollided) or 
#             (keys[pygame.K_RIGHT] and not rightCollided)):
#                 print("only this ............................")
#                 self.state = "run"
#             if keys[pygame.K_UP]:
#                 self.state = "jump"
#                 self.jump()
#         elif (bottomCollided and
#             ((keys[pygame.K_LEFT] and not leftCollided) or 
#             (keys[pygame.K_RIGHT] and not rightCollided))):
#             print("only this ............................")
#             self.state = "run"
#         
#         elif (bottomCollided and keys[pygame.K_UP]):
#             print("called")
#             self.state = "jump"
#             self.jump() # trigger jump
#         elif bottomCollided:
#             self.state = "stand"
#             # probably need changes
#             self.vy = 0
#             self.ay = 0
#             if ((leftCollided and not keys[pygame.K_LEFT]) or
#                 (rightCollided and not keys[pygame.K_RIGHT])):
#                 self.ay = 100/25 # no support force, falling down
#         elif not bottomCollided:
#             if leftCollided or rightCollided:
#                 self.state = "stand"
#                 self.ay = 100/25   
#             elif self.state == "jump" and not leftCollided and not rightCollided:
#                 self.state = "jump"
        #print(self.state) 
            
    
#     def jump(self,groundHeight):
#         x,y = self.getCoordinate()
#         w,h = self.getSize()
#         if self.prevvy == 0 and y + h >= groundHeight:
#             self.vy = -40
        
    def moveX(self):
        if self.direction == "right":
            self.vx = 150/25
        elif self.direction == "left":
            self.vx = -150/25
            
    def jump(self,groundHeight):
        x,y = self.getCoordinate()
        w,h = self.getSize()
        if self.prevvy == 0 and y + h >= groundHeight:
            self.vy = -40
            
    def getDeltaX(self):
        return self.x - self.displayx
        

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
        