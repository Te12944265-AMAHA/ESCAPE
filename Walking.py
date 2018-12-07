from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import ctypes
import _ctypes
import pygame
import sys
import math
import random

from Fractal import *
from MyImages import *
from Colors import *
from MatchMan import *
from Obstacles import *
from Colors import *
import Constants as c


    


class Walking(object):
    def __init__(self,w,h,numObstacle):
        pygame.init()
        self.width = w 
        self.height = h 
        self.numObstacle = numObstacle
        self.gameover = False
        self.done = False
        self.passed = False
        self.clock = pygame.time.Clock()
        self.walkingSurface = pygame.Surface((self.width,self.height))
        #self.road = Road(0,self.height - 140,"icon/road/road_black.gif")
        #self.scroll = 0
        self.road = Obstacle(0,self.height-140,6000,140)
        self.matchMan = MatchMan(300,self.height-140-103)
        self.obstacles = [self.road]
        self.obstaclesRectList = [self.road.getOriginalRect()]
        for obstacle in range(numObstacle):
            x = random.randint(500,5000)
            y = random.randint(self.height-140-90,self.height-140-30)
            thisObstacle = RandomObstacle(x,y,self.height,Color.black)
            self.obstacles.append(thisObstacle)
            self.obstaclesRectList.append(thisObstacle.getOriginalRect()) # 
        print(self.obstaclesRectList)
        self.timerCalled = 0
        
        self.preprevy = 0
        self.prevy = 0
        self.vy = 0
        self.prevRightElbowX = self.curRightElbowX = None
        self.prevRightElbowY = self.curRightElbowY = None
        self.prevLeftElbowX = self.curLeftElbowX = None
        self.prevLeftElbowY = self.curLeftElbowY = None
        self.prevHeadX = self.curHeadX = None
        self.prevHeadY = self.curHeadY = None
        self.prevRightShoulderX = self.curRightShoulderX = None
        self.prevRightShoulderY = self.curRightShoulderY = None
        self.prevLeftShoulderX = self.curLeftShoulderX = None
        self.prevLeftShoulderY = self.curLeftShoulderY = None
        
        
        
        
        self.cursorLeft = Hand("left")
        self.cursorRight = Hand("right")
        self.curRightHandY = self.curRightHandX = self.curLeftHandX = self.curLeftHandY = None
        
        self.missionPage = MyImage("icon/instructions/instruction_model.gif",self.width/2,self.height/2)
        self.missionButton = Button("icon/buttons/pause.png",2000,self.height-140-256)
        self.cluePage = MyImage("icon/instructions/instruction_model.gif",self.width/2,self.height/2)
        self.clueButton = Button("icon/buttons/pause.png", 5000,self.height-140-256)
        self.closeButton = Button("icon/buttons/closeButton.png",1000,100)
        self.missionPageButtons = [self.closeButton]
        self.cluePageButtons = [self.closeButton]
        self.mainButtons = [self.missionButton,self.clueButton]
        
        self.gameOverPage = MyImage("icon/instructions/gameOver.gif",self.width/2,self.height/2)
        self.replayButton = Button("icon/buttons/replay.gif",self.width/2,self.height*3/4)
        self.gameOverPageButtons = [self.replayButton]
        
        
        self.bodyState = {"up":False, "right": False, "left":False}
        self.bodies = None
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        
        
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
                        joints = body.joints 
                        # save the hand positions
                        mappedJoints = self.kinect.body_joints_to_color_space(joints)
                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.prevRightElbowX = self.curRightElbowX
                            self.prevRightElbowY = self.curRightElbowY
                            self.curRightElbowX = mappedJoints[PyKinectV2.JointType_ElbowRight].x
                            self.curRightElbowY = mappedJoints[PyKinectV2.JointType_ElbowRight].y
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.prevLeftElbowX = self.curLeftElbowX
                            self.prevLeftElbowY = self.curLeftElbowY
                            self.curLeftElbowX = mappedJoints[PyKinectV2.JointType_ElbowLeft].x
                            self.curLeftElbowY = mappedJoints[PyKinectV2.JointType_ElbowLeft].y
                        if joints[PyKinectV2.JointType_ShoulderRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.prevRightShoulderX = self.curRightShoulderX
                            self.prevRightShoulderY = self.curRightShoulderY
                            self.curRightShoulderX = mappedJoints[PyKinectV2.JointType_ShoulderRight].x
                            self.curRightShoulderY = mappedJoints[PyKinectV2.JointType_ShoulderRight].y
                        if joints[PyKinectV2.JointType_ShoulderLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.prevLeftShoulderX = self.curLeftShoulderX
                            self.prevLeftShoulderY = self.curLeftShoulderY
                            self.curLeftShoulderX = mappedJoints[PyKinectV2.JointType_ShoulderLeft].x
                            self.curLeftShoulderY = mappedJoints[PyKinectV2.JointType_ShoulderLeft].y   
                        if joints[PyKinectV2.JointType_Head].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.prevHeadX = self.curHeadX
                            self.prevHeadY = self.curHeadY
                            self.curHeadX = mappedJoints[PyKinectV2.JointType_Head].x
                            self.curHeadY = mappedJoints[PyKinectV2.JointType_Head].y
                        # update hand position for cursor 
                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curRightHandX = mappedJoints[PyKinectV2.JointType_HandRight].x
                            self.curRightHandY = mappedJoints[PyKinectV2.JointType_HandRight].y
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curLeftHandX = mappedJoints[PyKinectV2.JointType_HandLeft].x
                            self.curLeftHandY = mappedJoints[PyKinectV2.JointType_HandLeft].y
                
                            
    def updateBodyState(self):
        # up
        try:
            self.preprevy = self.prevy
            self.prevy = self.vy
            self.vy = int((self.curHeadY - self.prevHeadY)/c.K_TO_DISPLAY/0.04) # per 1 s
            print("vy:  ", self.prevy)
            if self.preprevy <= 0 and self.prevy < -400 and self.vy < 0 and self.prevy < self.preprevy and self.prevy < self.vy:
                self.bodyState["up"] = True
            else: 
                self.bodyState["up"] = False
        except: 
            self.bodyState["up"] = False
        # right
        try:
            if abs((self.curRightElbowY - self.curRightShoulderY)/c.K_TO_DISPLAY) <= 40:
                self.bodyState["right"] = True
            else:
                self.bodyState["right"] = False
        except:
            self.bodyState["right"] = False
        # left
        try:
            if abs((self.curLeftElbowY - self.curLeftShoulderY)/c.K_TO_DISPLAY) <= 40:
                self.bodyState["left"] = True
            else:
                self.bodyState["left"] = False
        except:
            self.bodyState["left"] = False
        
        
                            
                        
                            
        
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
            
    def drawCursor(self,surface):
        self.cursorLeft.draw(surface)      
        self.cursorRight.draw(surface)
        
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
            
    def missionRedrawAll(self,surface):    
        surface.fill(Color.white)
        self.missionPage.draw(surface) 
        self.closeButton.draw(surface)
        self.drawCursor(surface)
        
    def clueRedrawAll(self,surface):    
        surface.fill(Color.white)
        self.cluePage.draw(surface) 
        self.closeButton.draw(surface)
        c.drawScore(surface)
        self.drawCursor(surface)
        
    def gameOverRedrawAll(self,surface):
        surface.fill(Color.white)
        self.gameOverPage.draw(surface)
        self.replayButton.draw(surface)
        c.drawScore(surface)
        self.drawCursor(surface)
  
        
    def redrawAll(self):
        self.walkingSurface.fill(Color.white)
        for obstacle in self.obstacles:
            obstacle.draw(self.walkingSurface)
        for button in self.mainButtons:
            button.draw(self.walkingSurface)
        self.matchMan.draw(self.walkingSurface, self.timerCalled%self.matchMan.gifSize)
        self.drawCursor(self.walkingSurface)
        
    def timerFired(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
#                 elif event.type == pygame.KEYDOWN:
#                     self.keyPressed(event)
            elif event.type == pygame.KEYUP:
                self.keyReleased(event)
        self.updateKinect()
        self.updateCursorPos()
        if self.missionButton.buttonState == "release":
            self.updateSmallButton(self.missionPageButtons)
            self.missionRedrawAll(self.walkingSurface)
            if self.closeButton.buttonState == "release":
                self.closeButton.buttonState = "default"
                self.missionButton.buttonState = "default"
                self.passed = True
                self.mainButtons.remove(self.missionButton)
        elif self.clueButton.buttonState == "release":
            self.updateSmallButton(self.cluePageButtons)
            self.clueRedrawAll(self.walkingSurface)
            if self.closeButton.buttonState == "release":
                self.closeButton.buttonState = "default"
                self.clueButton.buttonState = "default"
                self.passed = True
                self.mainButtons.remove(self.clueButton)
                
        else:
            if not self.matchMan.isFall(self.height):
                self.updateBodyState()
                keys = pygame.key.get_pressed()
                self.keyPressed(keys)
                
                self.matchMan.updatePos(self.obstaclesRectList,keys,self.bodyState,self.prevy)
                deltax = self.matchMan.getDeltaX()
                for obstacle in self.obstacles:
                    obstacle.updateRect(deltax)
                for button in self.mainButtons:
                    button.updatePos(button.originalx - deltax,button.y)
                self.updateSmallButton(self.mainButtons)
                self.redrawAll()
                self.timerCalled += 1
            else:
                self.updateSmallButton(self.gameOverPageButtons)
                self.gameOverRedrawAll(self.walkingSurface)
                if self.replayButton.buttonState == "release":
                    self.replayButton.buttonState = "default"
                    self.gameover = True
                    self.passed = True
                
        
    
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                #elif event.type == pygame.KEYDOWN:
                    #self.keyPressed(event)
                #elif event.type == pygame.KEYUP:
                    #self.keyReleased(event)
            self.updateKinect()
            self.updateBodyState()
            keys = pygame.key.get_pressed()
            #self.keyPressed(keys)
            self.matchMan.updatePos(self.obstaclesRectList,keys,self.bodyState,self.prevy)
            deltax = self.matchMan.getDeltaX()
            for obstacle in self.obstacles:
                obstacle.updateRect(deltax)
                
            self.redrawAll()
            
            self.timerCalled += 1
            pygame.display.update()
            self.clock.tick(25)
        pygame.quit()
        
#game = ShootingGame(1200,675,15)
#game.run()

class WalkingGobang(Walking):
    def __init__(self,w,h,numObstacle):
        super().__init__(w,h,numObstacle)
        self.missionPage = MyImage("icon/instructions/mission_gobang_1.gif",self.width/2,self.height/2)
        self.missionButton = Door("icon/buttons/door_close.gif","icon/buttons/door_open.gif",2000,self.height-140-256)
        self.cluePage = MyImage("icon/instructions/instruction_model.gif",self.width/2,self.height/2)
        self.clueButton = Door("icon/buttons/door_close.gif","icon/buttons/door_open.gif", 5000,self.height-140-256)
        self.closeButton = Button("icon/buttons/closeButton.png",1000,100)
        self.missionPageButtons = [self.closeButton]
        self.cluePageButtons = [self.closeButton]
        self.mainButtons = [self.missionButton,self.clueButton]
        
class WalkingMaze(Walking):
    def __init__(self,w,h,numObstacle):
        super().__init__(w,h,numObstacle)
        self.matchMan = MatchMan(400,self.height-140-103)
        self.obstacles.clear()
        self.obstaclesRectList.clear()
        self.obstacles = [self.road]
        self.obstacleAdded = False
        self.tempObstacles = []
        self.tempObstaclesRectList = []
        self.obstaclesRectList = [self.road.getOriginalRect()]
        self.fileString = c.readFile("path/path1.txt")
        self.pathString = self.fileString.split("\n")
        #print(self.pathString)
        self.buttonParam = []
        for path in self.pathString:
            print(path)
            if len(path.split(",")) == 4:
                if not path.startswith("#"):
                    parameter = path.split(",")
                    print(parameter)
                    thisObstacle = Obstacle(int(parameter[0]),int(parameter[1]),int(parameter[2]),int(parameter[3]))
                    self.obstacles.append(thisObstacle)
                    self.obstaclesRectList.append(thisObstacle.getOriginalRect())
                else:
                    path = path[1:]
                    parameter = path.split(",")
                    thisObstacle = Obstacle(int(parameter[0]),int(parameter[1]),int(parameter[2]),int(parameter[3]))
                    self.tempObstacles.append(thisObstacle)
                    self.tempObstaclesRectList.append(thisObstacle.getOriginalRect())
            elif len(path.split(",")) == 2:
                parameter = path.split(",")
                self.buttonParam.append((int(parameter[0]),int(parameter[1])))
        print(self.buttonParam)
        self.missionPage = MyImage("icon/instructions/mission_maze.gif",self.width/2,self.height/2)
        self.missionButton = Button("icon/buttons/sphinx.gif",self.buttonParam[0][0],self.buttonParam[0][1])
        self.cluePage = MyImage("icon/instructions/instruction_model.gif",self.width/2,self.height/2)
        self.clueButton = Door("icon/buttons/door_close.gif","icon/buttons/door_open.gif", self.buttonParam[1][0],self.buttonParam[1][1])
        self.closeButton = Button("icon/buttons/closeButton.png",1000,100)
        self.missionPageButtons = [self.closeButton]
        self.cluePageButtons = [self.closeButton]
        self.mainButtons = [self.missionButton,self.clueButton]
        
    def redrawAll(self):
        self.walkingSurface.fill(Color.white)
        for obstacle in self.obstacles:
            obstacle.draw(self.walkingSurface)
        for button in self.mainButtons:
            button.draw(self.walkingSurface)
        self.matchMan.draw_FullUpdate(self.walkingSurface, self.timerCalled%self.matchMan.gifSize)
        self.drawCursor(self.walkingSurface)
        
    
    def timerFired(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
#                 elif event.type == pygame.KEYDOWN:
#                     self.keyPressed(event)
            elif event.type == pygame.KEYUP:
                self.keyReleased(event)
        self.updateKinect()
        self.updateCursorPos()
        if self.missionButton.buttonState == "release":
            self.updateSmallButton(self.missionPageButtons)
            self.missionRedrawAll(self.walkingSurface)
            if self.closeButton.buttonState == "release":
                self.closeButton.buttonState = "default"
                self.missionButton.buttonState = "default"
                self.passed = True
                self.mainButtons.remove(self.missionButton)
        elif self.clueButton.buttonState == "release":
            self.updateSmallButton(self.cluePageButtons)
            self.clueRedrawAll(self.walkingSurface)
            if self.closeButton.buttonState == "release":
                self.closeButton.buttonState = "default"
                self.clueButton.buttonState = "default"
                self.passed = True
                self.mainButtons.remove(self.clueButton)
                
        else:
            self.updateBodyState()
            keys = pygame.key.get_pressed()
            self.keyPressed(keys)
            
            self.matchMan.updatePos(self.obstaclesRectList,keys,self.bodyState,self.prevy)
            if self.obstacleAdded == False and self.matchMan.x > self.obstaclesRectList[-1].x + 150:
                self.obstacles += self.tempObstacles
                self.obstaclesRectList += self.tempObstaclesRectList
                self.obstacleAdded = True
            deltax = self.matchMan.getDeltaX()
            deltay = self.matchMan.getDeltaY()
            for obstacle in self.obstacles:
                obstacle.updateRect_FullUpdate(deltax, deltay)
            for button in self.mainButtons:
                button.updatePos(button.originalx - deltax,button.originaly - deltay)
            self.updateSmallButton(self.mainButtons)
            self.redrawAll()
            self.timerCalled += 1
        
        
class WalkingShoot(Walking):
    def __init__(self,w,h,numObstacle):
        super().__init__(w, h, numObstacle)
        self.obstacles.clear()
        self.obstaclesRectList.clear()
        self.road = Obstacle(0,self.height-250,500,250)
        self.matchMan = MatchMan(300,self.height-250-103)
        self.obstacles = [self.road]
        self.obstaclesRectList = [self.road.getOriginalRect()]
        for obstacle in range(numObstacle):
            prevright = self.obstaclesRectList[-1].x+self.obstaclesRectList[-1].size[0]
            x = prevright+random.randint(130,170)
            w = random.randint(100,300)
            thisObstacle = Obstacle(x,self.height-250,w,250)
            self.obstacles.append(thisObstacle)
            self.obstaclesRectList.append(thisObstacle.getOriginalRect())
        self.missionPage = MyImage("icon/instructions/mission_shoot.gif",self.width/2,self.height/2)
        self.missionButton = Button("icon/buttons/gun.gif",2000,300)
        self.cluePage = MyImage("icon/instructions/instruction_model.gif",self.width/2,self.height/2)
        self.clueButton = Button("icon/buttons/ladder.gif",4000,self.height-250-350)
        self.closeButton = Button("icon/buttons/closeButton.png",1000,100)
        self.missionPageButtons = [self.closeButton]
        self.cluePageButtons = [self.closeButton]
        self.mainButtons = [self.missionButton,self.clueButton]
        
class EndGame(Walking):
    def __init__(self,w,h,numObstacle,numTree):
        super().__init__(w,h,numObstacle)
        self.obstacles.clear()
        self.obstaclesRectList.clear()
        self.missionPageButtons.clear()
        self.mainButtons.clear()
        self.obstacles = [self.road]
        self.obstaclesRectList = [self.road.getOriginalRect()]
        self.missionPage = MyImage("icon/instructions/endGame.gif",self.width/2,self.height/2)
        self.missionButton = Button("icon/buttons/people.gif",2500,self.height-140-105)
        self.mainButtons = [self.missionButton]
        self.replayButton = Button("icon/buttons/replay.gif",self.width/2,self.height*3/4)
        self.missionPageButtons = [self.replayButton]
        self.gameOverPageButtons = [self.replayButton]
        self.trees = []
        for tree in range(numTree):
            x = random.randint(50,4000)
            self.trees.append(Tree_Two(random.randint(50,4000),self.height-140-675/2,675,675))
            print(x)
        
    
    def missionRedrawAll(self,surface):    
        surface.fill(Color.white)
        self.missionPage.draw(surface) 
        self.replayButton.draw(surface)
        c.drawScore(surface)
        self.drawCursor(surface)       
            
    def redrawAll(self):
        self.walkingSurface.fill(Color.white)
        for tree in self.trees:
            tree.draw(self.walkingSurface)
        for obstacle in self.obstacles:
            obstacle.draw(self.walkingSurface)
        for button in self.mainButtons:
            button.draw(self.walkingSurface)
        self.matchMan.draw(self.walkingSurface, self.timerCalled%self.matchMan.gifSize)
        self.drawCursor(self.walkingSurface)
        
    
    def gameOverRedrawAll(self,surface):
        surface.fill(Color.white)
        self.gameOverPage.draw(surface)
        self.replayButton.draw(surface)
        c.drawScore(surface)
        self.drawCursor(surface)
        
        
    def timerFired(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
#                 elif event.type == pygame.KEYDOWN:
#                     self.keyPressed(event)
            elif event.type == pygame.KEYUP:
                self.keyReleased(event)
        self.updateKinect()
        self.updateCursorPos()
        if self.missionButton.buttonState == "release":
            self.updateSmallButton(self.missionPageButtons)
            self.missionRedrawAll(self.walkingSurface)
            if self.replayButton.buttonState == "release":
                self.replayButton.buttonState = "default"
                self.missionButton.buttonState = "default"
                self.passed = True  
                self.gameover = True       # go to starting page        
        else:
            if not self.matchMan.isFall(self.height):
                self.updateBodyState()
                keys = pygame.key.get_pressed()
                self.keyPressed(keys)
                
                self.matchMan.updatePos(self.obstaclesRectList,keys,self.bodyState,self.prevy)
                deltax = self.matchMan.getDeltaX()
                for obstacle in self.obstacles:
                    obstacle.updateRect(deltax)
                for button in self.mainButtons:
                    button.updatePos(button.originalx - deltax,button.y)
                for tree in self.trees:
                    tree.updatePos(tree.originalx - deltax,tree.y)
                self.updateSmallButton(self.mainButtons)
                self.redrawAll()
                self.timerCalled += 1
            else:
                self.updateSmallButton(self.gameOverPageButtons)
                self.gameOverRedrawAll(self.walkingSurface)
                if self.replayButton.buttonState == "release":
                    self.replayButton.buttonState = "default"
                    self.gameover = True
                    self.passed = True
            
        
        
                
                
        
                    
                    