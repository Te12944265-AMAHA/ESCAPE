'''
Created on 2018 M11 15

@author: Tina
This program draws a red and a yellow ball on the player's hands and draws a blue oval above
the player's head.
Reference: https://github.com/fletcher-marsh/kinect_python/blob/master/FlapPyKinect.py
'''
from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import ctypes
import _ctypes
import pygame
import sys
import math
import random

class GameRuntime(object):
    def __init__(self):
        pygame.init()
        
        self.screenWidth = 1920
        self.screenHeight = 1080

        self.curRightHandY = self.curRightHandX = 0
        self.realRightHandX = self.realRightHandY = 0
        
        self.curLeftHandX = self.curLeftHandY=0
        self.realLeftHandX = 0
        self.realLeftHandY = 100
        self.realLeftHandZ = 200
        
        self.curHeadX =0 
        self.curHeadY = 100

        self.gameover = False

        self.ballRight = (self.curRightHandX,self.curRightHandY)
        self.ballLeft = (self.curLeftHandX,self.curRightHandY)
        self.oval = (0,0,0,0)
        
        self.touch = False
        #self.lightning = []
        
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        # Set the width and height of the window [width/2, height/2]
        self.screen = pygame.display.set_mode((960,540), pygame.HWSURFACE|pygame.DOUBLEBUF, 32)

        # Loop until the user clicks the close button.
        self.done = False

        # Kinect runtime object, we want color and body frames 
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self.frameSurface = pygame.Surface((self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self.bodies = None
        #print((self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height))
        
    def drawBall(self,hand):
        if hand == "l":
            thisBall = self.ballLeft
            rgb = (200,200,0)
        elif hand == "r":
            rgb = (255,0,0)
            thisBall = self.ballRight
        pygame.draw.circle(self.frameSurface, 
                          rgb, 
                           thisBall, 40)
    
        
    def drawColorFrame(self, frame, targetSurface):
        targetSurface.lock()
        address = self.kinect.surface_as_array(targetSurface.get_buffer())
        # replacing old frame with new one
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        targetSurface.unlock()
        
    
    def drawOval(self):
        pygame.draw.ellipse(self.frameSurface,(0,0,255),self.oval,20)

    def run(self):
        # -------- Main Program Loop -----------
        while not self.done:
            # --- Main event loop
            if self.gameover:
                font = pygame.font.Font(None, 36)
                text = font.render("Game over!", 1, (0, 0, 0))
                self.frameSurface.blit(text, (100,100))
                break
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop

            # We have a color frame. Fill out back buffer surface with frame's data 
            if self.kinect.has_new_color_frame():
                frame = self.kinect.get_last_color_frame()
                self.drawColorFrame(frame, self.frameSurface)
                frame = None

            # We have a body frame, so can get skeletons
            if self.kinect.has_new_body_frame(): 
                self.bodies = self.kinect.get_last_body_frame()

                if self.bodies is not None: 
                    for i in range(0, self.kinect.max_body_count):
                        body = self.bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 
                    
                        joints = body.joints 
                        # save the hand positions
                        mappedJoints = self.kinect.body_joints_to_color_space(joints)
                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curRightHandX = mappedJoints[PyKinectV2.JointType_HandRight].x
                            self.curRightHandY = mappedJoints[PyKinectV2.JointType_HandRight].y
                            self.realRightHandX = joints[PyKinectV2.JointType_HandRight].Position.x
                            self.realRightHandY = joints[PyKinectV2.JointType_HandRight].Position.y
                            self.realRightHandZ = joints[PyKinectV2.JointType_HandRight].Position.z
                            
                            #print(self.curRightHandX, self.curRightHandY)
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curLeftHandX = mappedJoints[PyKinectV2.JointType_HandLeft].x
                            self.curLeftHandY = mappedJoints[PyKinectV2.JointType_HandLeft].y
                            self.realLeftHandX = joints[PyKinectV2.JointType_HandLeft].Position.x
                            self.realLeftHandY = joints[PyKinectV2.JointType_HandLeft].Position.y
                            self.realLeftHandZ = joints[PyKinectV2.JointType_HandLeft].Position.z
                            #print(self.curLeftHandX, self.curLeftHandY)
                        if joints[PyKinectV2.JointType_Head].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curHeadX = mappedJoints[PyKinectV2.JointType_Head].x
                            self.curHeadY = mappedJoints[PyKinectV2.JointType_Head].y
                            print(self.curHeadX,self.curHeadY)
                            

                        #print(self.realRightHandZ,self.realLeftHandZ)
                        
                        try:
                            self.ballRight = (int(self.curRightHandX),int(self.curRightHandY))
                        except:
                            pass
                        try:
                            self.ballLeft = (int(self.curLeftHandX),int(self.curLeftHandY))
                        except: 
                            pass
                        try:
                            self.oval = (self.curHeadX-150,self.curHeadY-200,300,80)
                        except:
                            pass
                            
                        #self.ballRight = (int(self.curRightHandX),int(self.curRightHandY))
                        #self.ballLeft = (int(self.curLeftHandX),int(self.curLeftHandY))
                        

            # --- Game logic
            try:
                self.drawBall("r")
            except:
                pass
            try:
                self.drawBall("l")
            except:
                pass
            try:
                print((self.ballRight[0]+self.ballLeft[0])//2,(self.ballRight[1]+self.ballLeft[1])//2)
            except: pass
            
            if (abs(self.realLeftHandX-self.realRightHandX)<0.1 and 
                abs(self.realLeftHandY- self.realRightHandY)<0.1 and
                abs(self.realLeftHandZ- self.realRightHandZ)<0.1):
                self.touch = True
            else:
                self.touch = False
            if self.touch == True and (not(math.isnan(self.curHeadX) or math.isnan(self.curHeadY))):
                self.drawOval()
                
            #pygame.draw.rect(self.frameSurface, (0,0,255), (1000,500,50,100), 30)

            # Optional debugging text
            #font = pygame.font.Font(None, 36)
            #text = font.render(str(self.flap), 1, (0, 0, 0))
            #self.frameSurface.blit(text, (100,100))

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            hToW = float(self.frameSurface.get_height()) / self.frameSurface.get_width()
            targetHeight = int(hToW * self.screen.get_width())
            surfaceToDraw = pygame.transform.scale(self.frameSurface, (self.screen.get_width(), targetHeight));
            self.screen.blit(surfaceToDraw, (0,0))
            surfaceToDraw = None
            pygame.display.update()

            # --- Limit to 60 frames per second
            self.clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self.kinect.close()
        pygame.quit()

game = GameRuntime()
game.run()