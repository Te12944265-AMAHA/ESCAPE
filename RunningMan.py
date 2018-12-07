import pygame 


from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

from MyImages import *
from Colors import *
from MatchMan_no_collision import *
from Obstacles import *
from Colors import *
import Constants as c

class RunningMan(object):
    def __init__(self,w,h,numObstacle):
        self.width = w 
        self.height = h 
        self.numObstacle = numObstacle
        self.done = False
        self.passed = False
        self.clock = pygame.time.Clock()
        self.runningManSurface = pygame.Surface((self.width,self.height))
        #self.runningManSurface = pygame.display.set_mode((self.width,self.height))
        #self.road = Road(0,self.height - 140,"icon/road/road_black.gif")
        #self.scroll = 0
        self.road = Obstacle(0,self.height-140,6000,140)
        self.matchMan = MatchMan(300,self.height-140-105)
        self.obstacles = []
        #self.obstaclesRectList = [self.road.getOriginalRect()]
        self.obstaclesRectList = [self.road.getOriginalRect()]
        for obstacle in range(numObstacle):
            x = random.randint(500,5000)
            y = random.randint(self.height-140-105,self.height-140-50)
            thisObstacle = RandomObstacle(x,y,self.height,Color.black)
            self.obstacles.append(thisObstacle)
            self.obstaclesRectList.append(thisObstacle.getOriginalRect()) # 
        print(self.obstaclesRectList)
        self.timerCalled = 0
        
        self.cursorLeft = Hand("left")
        self.cursorRight = Hand("right")
        
        self.bodies = None
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        self.curRightHandY = self.curRightHandX = self.curLeftHandX = self.curLeftHandY = None
        
        self.missionPage = MyImage("icon/instructions/instruction_model.gif",self.width/2,self.height/2)
        self.missionButton = Button("icon/buttons/pause.png",2000,self.height-140-256)
        self.cluePage = MyImage("icon/instructions/instruction_model.gif",self.width/2,self.height/2)
        self.clueButton = Button("icon/buttons/pause.png", 5000,self.height-140-256)
        self.closeButton = Button("icon/buttons/closeButton.png",1000,100)
        self.missionPageButtons = [self.closeButton]
        self.cluePageButtons = [self.closeButton]
        self.mainButtons = [self.missionButton,self.clueButton]
        
        
        
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
                        if button.buttonState == "press":
                            button.buttonState = "default"
                elif button.contains(self.cursorRight.pos):
                    if button.contains(self.cursorRight.pos):
                        if self.cursorRight.handState == "close":
                            button.buttonState = "press"
                        else:
                            if button.buttonState == "press":
                                button.buttonState = "release"
                    else:
                        if button.buttonState == "press":
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
        self.drawCursor(surface)
        
#     def keyPressed1(self,event):
#         if event.key == pygame.K_UP:
#             self.matchMan.state = "jump"
#             self.matchMan.jump()
#         elif event.key == pygame.K_DOWN:
#             self.matchMan.state = "stand"
#         elif event.key == pygame.K_LEFT:
#             if self.matchMan.state != "jump":
#                 self.matchMan.state = "run"
#             self.matchMan.direction = "left"
#             self.matchMan.moveX()
#         elif event.key == pygame.K_RIGHT:
#             self.matchMan.direction = "right"
#             if self.matchMan.state != "jump":
#                 self.matchMan.state = "run"
#             self.matchMan.moveX()
        
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
        self.runningManSurface.fill(Color.white)
        self.road.draw(self.runningManSurface)
        for obstacle in self.obstacles:
            obstacle.draw(self.runningManSurface)
        for button in self.mainButtons:
            button.draw(self.runningManSurface)
        self.matchMan.draw(self.runningManSurface, self.timerCalled%self.matchMan.gifSize)
        self.drawCursor(self.runningManSurface)
        
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
            self.missionRedrawAll(self.runningManSurface)
            if self.closeButton.buttonState == "release":
                self.closeButton.buttonState = "default"
                self.missionButton.buttonState = "default"
                self.passed = True
                self.mainButtons.remove(self.missionButton)
        elif self.clueButton.buttonState == "release":
            self.updateSmallButton(self.cluePageButtons)
            self.clueRedrawAll(self.runningManSurface)
            if self.closeButton.buttonState == "release":
                self.closeButton.buttonState = "default"
                self.clueButton.buttonState = "default"
                self.mainButtons.remove(self.clueButton)
                
        else:
            keys = pygame.key.get_pressed()
            self.keyPressed(keys)
            self.matchMan.updatePos(self.height-140)
            deltax = self.matchMan.getDeltaX()
            for obstacle in self.obstacles:
                obstacle.updateRect(deltax) 
            for button in self.mainButtons:
                button.updatePos(button.originalx - deltax,button.y)
            self.updateSmallButton(self.mainButtons)
            self.redrawAll()
            self.timerCalled += 1
        
    
    def run(self):
        while not self.done:
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
                self.missionRedrawAll(self.runningManSurface)
                if self.closeButton.buttonState == "release":
                    self.closeButton.buttonState = "default"
                    self.missionButton.buttonState = "default"
            elif self.clueButton.buttonState == "release":
                self.updateSmallButton(self.cluePageButtons)
                self.clueRedrawAll(self.runningManSurface)
                if self.closeButton.buttonState == "release":
                    self.closeButton.buttonState = "default"
                    self.clueButton.buttonState = "default"
            else:
                keys = pygame.key.get_pressed()
                self.keyPressed(keys)
                self.matchMan.updatePos(self.height-140)
                deltax = self.matchMan.getDeltaX()
                for obstacle in self.obstacles:
                    obstacle.updateRect(deltax) 
                for button in self.mainButtons:
                    button.updatePos(button.originalx - deltax,button.y)
                self.updateSmallButton(self.mainButtons)
                self.redrawAll()
                self.timerCalled += 1
            pygame.display.update()
            self.clock.tick(25)
        pygame.quit()
    
    
class RunningGobang(RunningMan):
    def __init__(self,w,h,numObstacle):
        super().__init__(w,h,numObstacle)
        
#thisGame = RunningGobang(1200,675,15)
#thisGame.run()
        
    