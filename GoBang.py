import pygame 
import math
from Colors import *
from MyImages import *
import Constants as c
from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

class GobangGame(object):
    def __init__(self,w,h):
        #pygame.init()
        self.c = 0
        self.x0 = []
        self.flag = False
        
        self.done = False
        self.over = False
        self.gameover = False
        self.gameover1 = False
        self.passed = False
        self.width = w
        self.height = h 
        #get the game surface
        #self.gobangGameSurface = pygame.display.set_mode((self.width,self.height))
        self.gobangGameSurface = pygame.Surface((self.width,self.height))
        #get the chess board surface
        self.boardWidth = 450
        self.boardHeight = 450
        # the center of the board
        self.centerx = self.width/2
        self.centery = self.height/2
        self.gobang = pygame.Surface((self.boardWidth,self.boardHeight))
        self.rows = 15
        self.cols = 15
        self.me = True # the player goes first
        self.chessBoard = [([0] * self.cols) for row in range(self.rows)] #storing current grid info
        self.chessBoardColor = [([0] * self.cols) for row in range(self.rows)]
        self.count=0
        self.win = []
        #self.win = [(([False]*3) for col in range(self.cols)) for row in range(self.rows)]
        
        #temp2d = []
        #for col in range(self.cols): temp2d += [[False]*572]
        #for row in range(self.rows): self.win += [temp2d] 
        self.win = testList = [[[False for k in range(572)] for j in range(self.cols)] for i in range(self.rows)]
        print(len(self.win),len(self.win[0]),len(self.win[0][0]))
        self.initializeWinCount()
        # initialize the number of chess dropped for each winning ways
        print(self.count)
        for i in range(15):
            for j in range(15):
                if self.win[i][j][0] == True:
                    print((i,j))
        self.myDrop = [0]*self.count
        self.pcDrop = [0]*self.count
        self.clock = pygame.time.Clock()
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        self.cursorRight = Hand("right")
        self.bodies = None
        self.curRightHandY = self.curRightHandX = self.curLeftHandX = self.curLeftHandY = None
        
        
        self.gameOverPage = MyImage("icon/instructions/gameOver.gif",self.width/2,self.height/2)
        self.replayButton = Button("icon/buttons/replay.gif",self.width/2,self.height*3/4)
        self.gameOverPageButtons = [self.replayButton]
        
    def gameOverRedrawAll(self,surface):
        surface.fill(Color.white)
        self.gameOverPage.draw(surface)
        self.replayButton.draw(surface)
        self.drawCursor()
        
        
    def updateCursorPos(self):
        try:
            rightx = int(self.curRightHandX/c.K_TO_DISPLAY)
            righty = int(self.curRightHandY/c.K_TO_DISPLAY)
            self.cursorRight.pos = (rightx,righty)
            #self.cursorRight.draw(self.startSurface)
        except:  self.cursorRight.pos = None
            
    def drawCursor(self):      
        self.cursorRight.draw(self.gobangGameSurface)
        
        
    def redrawAll(self):
        self.gobangGameSurface.fill(Color.black)
        self.gobang.fill(Color.white)
        self.drawChessBoard()
        self.drawChess(self.gobang)
        self.gobangGameSurface.blit(self.gobang,(self.centerx-self.boardWidth/2,self.centery-self.boardHeight/2))
        if self.cursorRight.handState == "close":
            pygame.draw.circle(self.gobangGameSurface,Color.black,self.cursorRight.pos,15,0)
            # boarder
            pygame.draw.circle(self.gobangGameSurface,Color.black,self.cursorRight.pos,15,1)
        self.drawCursor()
        
    def updateKinect(self):
        if self.kinect.has_new_body_frame(): 
                self.bodies = self.kinect.get_last_body_frame()

                if self.bodies is not None: 
                    for i in range(0, self.kinect.max_body_count):
                        body = self.bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 
                        if body.hand_right_state == 3:
                            self.cursorRight.prevHandState = self.cursorRight.handState
                            self.cursorRight.handState = "close"
                        else:
                            self.cursorRight.prevHandState = self.cursorRight.handState
                            self.cursorRight.handState = "open"
#                         if body.hand_left_state == 3:
#                             self.cursorLeft.handState = "close"
#                         else:
#                             self.cursorLeft.handState = "open"
                        #print(body.hand_right_state)
                        joints = body.joints 
                        # save the hand positions
                        mappedJoints = self.kinect.body_joints_to_color_space(joints)
                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curRightHandX = mappedJoints[PyKinectV2.JointType_HandRight].x
                            self.curRightHandY = mappedJoints[PyKinectV2.JointType_HandRight].y
                            
                            #print(self.curRightHandX, self.curRightHandY)
#                         if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
#                             self.curLeftHandX = mappedJoints[PyKinectV2.JointType_HandLeft].x
#                             self.curLeftHandY = mappedJoints[PyKinectV2.JointType_HandLeft].y
    def updateSmallButton(self,buttons):
        for button in buttons:
            try:
                if button.contains(self.cursorRight.pos):
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
                elif not(button.contains(self.cursorRight.pos)):
                    button.buttonState = "default"
            except: pass
        
        
    def timerFired(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.done = True # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.mousePressed(pos)
        self.updateKinect()
        self.updateCursorPos()
        if self.over and self.gameover1 == False:
            c.totalScore += 25
            self.passed = True
        elif self.gameover1:
            self.updateSmallButton(self.gameOverPageButtons)
            self.gameOverRedrawAll(self.gobangGameSurface)
            if self.replayButton.buttonState == "release":
                self.replayButton.buttonState = "default"
                self.gameover = True
                self.passed = True
        else:
            if self.cursorRight.prevHandState == "close" and self.cursorRight.handState == "open":
                self.mousePressed(self.cursorRight.pos)
            self.redrawAll() 
            
    
        
    
    def run(self):
        while not self.done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousePressed()
            self.redrawAll() 
            pygame.display.update()
            # --- Limit to 10 frames per second
            self.clock.tick(10)
            
        # Close our Kinect sensor, close the window and quit.
        pygame.quit() 

        
    def initializeWinCount(self):
        #horizontal
        for i in range(15):
            for j in range(0,11):
                for k in range(0,5):
                    self.win[i][j+k][self.count] = True
                self.count += 1
        #vertical
        for i in range(0,15):
            for j in range(0,11):
                for k in range(0,5):
                    self.win[j+k][i][self.count] = True
                self.count += 1
        #cross downward
        for i in range(0,11):
            for j in range(0,11):
                for k in range(0,5):
                    self.win[i+k][j+k][self.count] = True
                self.count += 1
        #cross upward
        for i in range(0,11):
            for j in range(14,3,-1):
                for k in range(0,5):
                    self.win[i+k][j-k][self.count] = True
                self.count += 1

   
    # drawing method for the board grid
    def drawChessBoard(self):
        margin = 15
        size = 30
        gridNum = 14
        color = Color.gray
        thickness = 4
        for i in range(gridNum):
            starty = margin + i*size
            for j in range(gridNum):
                startx = margin + j*size
                thisRect = pygame.Rect(startx,starty,size,size)
                pygame.draw.rect(self.gobang,color,thisRect,thickness)
                
                
    def drawChess(self,surface):
        margin = 15
        size = 30
        for i in range(len(self.chessBoard)):
            for j in range(len(self.chessBoard[0])):
                if self.chessBoard[i][j] != 0:
                    #print(self.chessBoardColor[i][j],(margin + j*size,margin + i*size),size//2,0)
                    pygame.draw.circle(surface,self.chessBoardColor[i][j],(margin + j*size,margin + i*size),size//2,0)
                    # boarder
                    pygame.draw.circle(surface,Color.black,(margin + j*size,margin + i*size),size//2,3)
        
    
    # draw chess on a grid point
    def onStep(self,i,j,me):
        if me: self.chessBoardColor[i][j] = Color.black
        else: self.chessBoardColor[i][j] = Color.white
        
        
        

    def mousePressed(self,pos):
        if self.over: 
            print("over")
            return
        if not self.me: 
            print("not me")
            return
        print(pos)
        x = pos[0] - (self.centerx-self.boardWidth/2)
        y = pos[1] - (self.centery-self.boardHeight/2)
        print(x,y)
        i = math.floor(y/30)
        j = math.floor(x/30)
        print(i,j)
        if not(0<=i<15 and 0<=j<15):
            return
        if self.chessBoard[i][j] == 0:
            self.onStep(i,j,self.me)
            self.chessBoard[i][j] = 1
            # violent debug: abbreviated
            for k in range(self.count):
                if self.win[i][j][k] == True:
                    self.myDrop[k]+=1
                    self.pcDrop[k]=6
                    if self.myDrop[k]==5:
                        # the player wins
                        #self.doSomething()
                        self.over = True
                        print("i win")
            print(self.myDrop)
            if not self.over:
                self.me = not self.me
                self.pcAI()


    # computer dropping chess based on importance of each grid
    def pcAI(self):
        myScore = [([0] * self.cols) for row in range(self.rows)]
        pcScore = [([0] * self.cols) for row in range(self.rows)]
        max = 0
        u = 0
        v = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.chessBoard[i][j] == 0:
                    for k in range(self.count):
                        if self.win[i][j][k] == True:
                            # last version:
                            # 100,400,2000,10000,200,350,2500,20000
                            # 100,400,2500,10000,200,400,2000,20000
                            #print("mydrop at %d: "%k,self.myDrop[k])
                            #print("pcdrop at %d: "%k,self.myDrop[k])
                            if self.myDrop[k] == 1:
                                myScore[i][j]+= 100
                            elif self.myDrop[k] == 2:
                                myScore[i][j] += 400
                            elif self.myDrop[k] == 3:
                                myScore[i][j] += 2500
                            elif self.myDrop[k] == 4:
                                myScore[i][j] += 10000
                            
                            if self.pcDrop[k] == 1:
                                pcScore[i][j]+=200;
                            elif self.pcDrop[k] == 2:
                                pcScore[i][j]+=400;
                            elif self.pcDrop[k] == 3:
                                pcScore[i][j]+=2000;
                            elif self.pcDrop[k] == 4:
                                pcScore[i][j]+=20000;
                            #print("pcscore i j: ",pcScore[i][j])
                    if myScore[i][j]>max:
                        max=myScore[i][j]
                        u=i
                        v=j
                    elif myScore[i][j]==max:
                        if pcScore[i][j]>pcScore[u][v]:
                            max=pcScore[i][j]
                            u=i
                            v=j        
                    if pcScore[i][j]>max:
                        max=pcScore[i][j]
                        u=i
                        v=j
                    elif pcScore[i][j]==max:
                        if myScore[i][j]>myScore[u][v]:
                            max=myScore[i][j]
                            u=i
                            v=j
        print(u,v,"pc")
        #print(pcScore[u][v])
        #print(pcScore[5][5])
        self.onStep(u,v,False)
        self.chessBoard[u][v]=2
        for k in range(self.count):
            if self.win[u][v][k] == True:
                self.pcDrop[k]+=1
                self.myDrop[k]=6
                if self.pcDrop[k]==5:
                    # the pc wins
                    #self.doSomething()
                    self.over = True
                    self.gameover1 = True
                    print("pc wins")
        #print(self.pcDrop)
        if not self.over:
            self.me = not self.me
            
#game = GobangGame(1200,700)
#game.run()              