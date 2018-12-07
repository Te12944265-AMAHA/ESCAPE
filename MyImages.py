'''
Created on 2018 M11 23

@author: Tina
'''

import pygame

class MyImage(object):
    def __init__(self,imagePath,cx,cy):
        self.pic = pygame.image.load(imagePath)
        self.x = cx 
        self.y = cy 
        
    def getSize(self):
        return self.pic.get_rect().size
    
    def updatePos(self,x,y):
        self.x = x 
        self.y = y
    
    def draw(self,surface):
        w,h = self.getSize()
        surface.blit(self.pic,(self.x-w/2,self.y-h/2))
        
    def resize(self,w,h):
        targetSurf = pygame.transform.scale(self.pic, (w,h))
        self.pic = targetSurf
        
class Hand(MyImage):
    def __init__(self,hand):
        open = pygame.image.load("icon/hand/hand_right_release.gif")
        tempOpen = pygame.transform.scale(open, (int(open.get_rect().size[0]*0.3),int(open.get_rect().size[1]*0.3)))
        close = pygame.image.load("icon/hand/hand_right_grip.gif")
        tempClose = pygame.transform.scale(close, (int(close.get_rect().size[0]*0.3),int(close.get_rect().size[1]*0.3)))
        if hand == "right": pass
        elif hand == "left" :
            tempOpen1 = pygame.transform.flip(tempOpen, True, False)
            tempClose1 = pygame.transform.flip(tempClose, True, False)
            tempOpen = tempOpen1
            tempClose = tempClose1
        self.pic = {"open": tempOpen, "close": tempClose}
        self.handState = "open"
        self.prevHandState = "open"
        self.pos = None

        
    def getSize(self):
        return self.pic[self.handState].get_rect().size
        
    def draw(self,surface):
        w, h = self.getSize()
        try:
            x,y = self.pos
            surface.blit(self.pic[self.handState],(x-w/2,y-h/2))
        except: pass
        

class Button(MyImage):
    def __init__(self,imagePath,cx,cy):
        defaultImg = pygame.image.load(imagePath)
        self.pic = {"default": defaultImg, "pass": defaultImg, "press": None, "release": defaultImg}
        x,y = self.getSize()
        #targetSurf = pygame.Surface((int(x*0.9),int(y*0.9)))
        targetSurf = pygame.transform.scale(defaultImg, (int(x*0.9),int(y*0.9)))
        #print(targetSurf == None)
        self.pic["press"] = targetSurf
        self.buttonState = "default"
        self.x = self.originalx =  cx 
        self.y = self.originaly = cy
        
        
    def getSize(self,state = "default"):
        return self.pic[state].get_rect().size
    
    def contains(self,pos):
        #print(self.getRect())
        return self.getRect().collidepoint(pos)
    
    def getRect(self):
        w, h = self.getSize()
        x = self.x - w/2
        y = self.y - h/2
        return pygame.Rect(x,y,w,h)
        
        
    def draw(self,surface):
        w, h = self.getSize(self.buttonState)
        surface.blit(self.pic[self.buttonState],(self.x-w/2,self.y-h/2))
        
class Door(Button):
    def __init__(self,imagePath1,imagePath2,cx,cy):
        defaultImg = pygame.image.load(imagePath1)
        passImg = pygame.image.load(imagePath2)
        self.pic = {"default": defaultImg, "pass": passImg, "press": None, "release": passImg}
        x,y = self.getSize("pass")
        #targetSurf = pygame.Surface((int(x*0.9),int(y*0.9)))
        targetSurf = pygame.transform.scale(passImg, (int(x*0.9),int(y*0.9)))
        #print(targetSurf == None)
        self.pic["press"] = targetSurf
        self.buttonState = "default"
        self.x = self.originalx =  cx 
        self.y = self.originaly = cy
        