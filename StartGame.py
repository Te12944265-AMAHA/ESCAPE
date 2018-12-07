'''
Created on 2018 M11 23

@author: Tina
'''
'''This can run. Use kinect to trigger the buttons.'''


from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import ctypes
import _ctypes
import pygame
import sys
import math
import random

import Constants as c
from MyImages import *
from Colors import *


class StartGame(object):
    def __init__(self,w,h):
        self.width = w
        self.height = h 
        #self.startSurface = pygame.display.set_mode((self.width,self.height))
        self.startSurface = pygame.Surface((self.width,self.height))
        self.startButton = Button("icon/buttons/start_default_white.gif",self.width/2,self.height/3*2)
        self.instructionButton = Button("icon/buttons/instructions_default_white.gif",self.width/2,self.height/4*3.2)
        #self.settingsButton = Button("icon/buttons/settings_default_white.gif",self.width/2,self.height/6*5.3)
        self.buttons = [self.startButton,self.instructionButton]
        self.logo = MyImage("icon/escapeRoom.gif",self.width/2,self.height/3.5)
        self.done = False
        self.passed = False
        self.clock = pygame.time.Clock()
        self.cursorLeft = Hand("left")
        self.cursorRight = Hand("right")
        
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        #self.backBuffer = pygame.Surface((self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height), 0, 32)
        self.curRightHandY = self.curRightHandX = self.curLeftHandX = self.curLeftHandY = None
        
        #instruction, settings
        self.instructionPage1 = MyImage("icon/instructions/instruction_startGame_1.gif",self.width/2,self.height/2)
        self.instructionPage2 = MyImage("icon/instructions/instruction_startGame_2.gif",self.width/2,self.height/2)
        self.instructionPage3 = MyImage("icon/instructions/instruction_startGame_3.gif",self.width/2,self.height/2)
        self.instructionPage4 = MyImage("icon/instructions/instruction_startGame_4.gif",self.width/2,self.height/2)
        self.instructionPage5 = MyImage("icon/instructions/instruction_startGame_5.gif",self.width/2,self.height/2)
        self.instructionPages = [self.instructionPage1,self.instructionPage2,self.instructionPage3,self.instructionPage4,self.instructionPage5]
        self.currPage = 0
        self.closeButton = Button("icon/buttons/closeButton.png",1000,100)
        self.rightButton = Button("icon/buttons/right_4.gif",self.width-200,self.height/2)
        self.leftButton = Button("icon/buttons/left_4.gif",200,self.height/2)
        self.instructionPageButtons = [self.closeButton,self.rightButton,self.leftButton]
        
    def updateCursorPos(self):
        try:
            leftx = int(self.curLeftHandX/c.K_TO_DISPLAY)
            lefty = int(self.curLeftHandY/c.K_TO_DISPLAY)
            self.cursorLeft.pos = (leftx,lefty)
            #self.cursorLeft.draw(self.startSurface)
        except: self.cursorLeft.pos = None
        try:
            rightx = int(self.curRightHandX/c.K_TO_DISPLAY)
            righty = int(self.curRightHandY/c.K_TO_DISPLAY)
            self.cursorRight.pos = (rightx,righty)
            #self.cursorRight.draw(self.startSurface)
        except:  self.cursorRight.pos = None
            
    def drawCursor(self):
        self.cursorLeft.draw(self.startSurface)      
        self.cursorRight.draw(self.startSurface)
        
    def updateButton(self,buttons):
        for button in buttons:
            try:
                if (button.contains(self.cursorLeft.pos) and 
                    button.contains(self.cursorRight.pos)):
                    if (self.cursorLeft.handState == "close" and
                        self.cursorRight.handState == "close"):
                        button.buttonState = "press"
                    else:
                        if self.cursorLeft.handState == "open" and self.cursorRight.handState == "open":
                            if button.buttonState == "press":
                                button.buttonState = "release"
                else:
                    if button.buttonState == "press":
                        button.buttonState = "default"
            except: pass
            
    def updateSmallButton(self,buttons):
        for button in buttons:
            try:
                if button.contains(self.cursorLeft.pos):
                    if button.contains(self.cursorLeft.pos):
                        if self.cursorLeft.handState == "close":
                            button.buttonState = "press"
                        else:
                            if button.buttonState == "press":
                                button.buttonState = "release"
                            else:
                                button.buttonState = "pass"
                    else:
                        if button.buttonState == "press" or button.buttonState == "pass":
                            button.buttonState = "default"
                elif button.contains(self.cursorRight.pos):
                    if button.contains(self.cursorRight.pos):
                        if self.cursorRight.handState == "close":
                            button.buttonState = "press"
                        else:
                            if button.buttonState == "press":
                                button.buttonState = "release"
                            else:
                                button.buttonState = "pass"
                    else:
                        if button.buttonState == "press" or button.buttonState == "pass":
                            button.buttonState = "default"
                elif not(button.contains(self.cursorRight.pos) or button.contains(self.cursorLeft.pos)):
                    button.buttonState = "default"
            except: pass
                    
    
    def mousePressed(self,event):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.contains(pos):
                button.buttonState = "press"
                
        
    def mouseReleased(self,event):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.contains(pos):
                if button.buttonState == "press":
                    button.buttonState = "release"
            elif not button.contains(pos):
                button.buttonState = "default"
            
        
    def redrawAll(self):
        self.startSurface.fill(Color.black)
        self.startButton.draw(self.startSurface)
        self.instructionButton.draw(self.startSurface)
        #self.settingsButton.draw(self.startSurface)
        self.logo.draw(self.startSurface)
        self.drawCursor()
        
        # cursors
        
    
    def updateKinect(self):
        if self.kinect.has_new_body_frame(): 
                self.bodies = self.kinect.get_last_body_frame()

                if self.bodies is not None: 
                    for i in range(0, self.kinect.max_body_count):
                        body = self.bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 
                        if body.hand_right_state == 3:
                            self.cursorRight.handState = "close"
                        else:
                            self.cursorRight.handState = "open"
                        if body.hand_left_state == 3:
                            self.cursorLeft.handState = "close"
                        else:
                            self.cursorLeft.handState = "open"
                        print(body.hand_right_state)
                        joints = body.joints 
                        # save the hand positions
                        mappedJoints = self.kinect.body_joints_to_color_space(joints)
                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curRightHandX = mappedJoints[PyKinectV2.JointType_HandRight].x
                            self.curRightHandY = mappedJoints[PyKinectV2.JointType_HandRight].y
                            
                            #print(self.curRightHandX, self.curRightHandY)
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curLeftHandX = mappedJoints[PyKinectV2.JointType_HandLeft].x
                            self.curLeftHandY = mappedJoints[PyKinectV2.JointType_HandLeft].y
                            
                            
    def instructionPageRedrawAll(self):    
        self.startSurface.fill(Color.white)
        self.instructionPages[self.currPage].draw(self.startSurface) 
        for button in self.instructionPageButtons:
            button.draw(self.startSurface)
        #self.closeButton.draw(self.startSurface)
        self.drawCursor()
        
                        
                        
    def timerFired(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.done = True # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #print("called")
                self.mousePressed(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                #print("called2")
                self.mouseReleased(event)
        self.updateKinect()
        self.updateCursorPos()
        
        if self.startButton.buttonState == "release":
            self.passed = True
        elif self.instructionButton.buttonState == "release":
            self.updateSmallButton(self.instructionPageButtons)
            self.instructionPageRedrawAll()
            if self.closeButton.buttonState == "release":
                self.closeButton.buttonState = "default"
                self.instructionButton.buttonState = "default"
            else:
                if self.rightButton.buttonState == "release":
                    self.rightButton.buttonState = "default"
                    if self.currPage < len(self.instructionPages)-1:
                        self.currPage+=1
                if self.leftButton.buttonState == "release":
                    self.leftButton.buttonState = "default"
                    if 0 < self.currPage:
                        self.currPage-=1
                    
        #elif self.settingsButton.buttonState == "release":
            # to be developed
        else:
            self.updateButton(self.buttons)
            #print(self.startButton.buttonState)   
            self.redrawAll()             

                            
    
    def run(self):
        while not self.done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #print("called")
                    self.mousePressed(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    #print("called2")
                    self.mouseReleased(event)
            self.updateKinect()
            self.updateCursorPos()
            
            if self.startButton.buttonState == "release":
                self.done = True
            elif self.instructionButton.buttonState == "release":
                self.updateSmallButton(self.instructionPageButtons)
                self.instructionPageRedrawAll()
                if self.closeButton.buttonState == "release":
                    self.closeButton.buttonState = "default"
                    self.instructionButton.buttonState = "default"
            #elif self.settingsButton.buttonState == "release":
                # to be developed
                
            else:
                self.updateButton(self.buttons)
                #print(self.startButton.buttonState)   
                self.redrawAll()             
            pygame.display.update()
                
            # --- Limit to 60 frames per second
            self.clock.tick(60)
            
        # Close our Kinect sensor, close the window and quit.
        pygame.quit()

#game = StartGame(1200,675)
#game.run()    
        