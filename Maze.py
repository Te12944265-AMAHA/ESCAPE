import pygame
import math
import random
import sys
import Constants as c
from Colors import *
from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

pygame.init()


class Maze(pygame.sprite.Sprite):
    
    def __init__(self, w,h,row, col, size, margin,apple):
        sys.setrecursionlimit(3000)
        self.width = w 
        self.height = h
        self.row = row
        self.col = col
        self.size = size
        self.margin = margin
        self.w = self.col*self.size + 2*self.margin
        self.h = self.row*self.size+2*self.margin
        self.mazeSurface = pygame.Surface((self.w, self.h))
        self.screen = pygame.Surface((self.width,self.height))
        #self.mazeSurface = pygame.Surface((self.row*size+self.margin*2,self.col*size+self.margin*2),0,32)
        self.walls = {}
        gridList = []
        for i in range(self.row):
            for j in range(self.col):
                self.walls[(i,j)] = {"left":True, "right": True, "up": True, "down": True}
                gridList.append((i,j))
        self.score = 0
        self.apple = set()
        gridList.pop()
        gridList.pop(0)
        for a in range(apple):
            this = random.choice(gridList)
            self.apple.add(this)
            gridList.remove(this)
        self.neighbors = {}
        for i in range(self.row):
            for j in range(self.col):
                self.neighbors[(i,j)] = self.getNeighbors((i,j))
        self.visited = set()
        self.route = []
        self.path = []
        self.currCell = (0,0)
        
        self.myGrid = (0,0)
        self.done = False
        self.passed = False
        
        self.generateRoute() # remove walls, generate a path
        
        self.palmOpen = False
        self.curRightWristX = self.curRightWristY = None
        self.curRightHandX = self.curRightHandY = None
        self.movingDirection = None

        self.bodies = None
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        self.timerCalled = 0
        self.auto  = False
        
    
    def keyPressed(self,event):
        if event.key == pygame.K_UP:
            self.auto = True
            self.timerCalled = 0
            self.myGrid = (0,0)
        
        
        
    def updateKinect(self):
        if self.kinect.has_new_body_frame(): 
                self.bodies = self.kinect.get_last_body_frame()

                if self.bodies is not None: 
                    for i in range(0, self.kinect.max_body_count):
                        body = self.bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 
                        if body.hand_right_state == 3:
                            self.palmOpen = False
                        else: self.palmOpen = True
                        joints = body.joints 
                        # save the hand positions
                        mappedJoints = self.kinect.body_joints_to_color_space(joints)
                        if joints[PyKinectV2.JointType_WristRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curRightWristX = mappedJoints[PyKinectV2.JointType_WristRight].x
                            self.curRightWristY = mappedJoints[PyKinectV2.JointType_WristRight].y
                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curRightHandX = mappedJoints[PyKinectV2.JointType_HandRight].x
                            self.curRightHandY = mappedJoints[PyKinectV2.JointType_HandRight].y
                        
                        
    def updateDirection(self):
        try:
            if self.palmOpen == True:
                if abs(int(self.curRightWristX - self.curRightHandX)/c.K_TO_DISPLAY) < 15:
                    if self.curRightWristY > self.curRightHandY:
                        self.movingDirection = "up"
                    else:
                        self.movingDirection = "down"
                elif abs(int(self.curRightWristY - self.curRightHandY)/c.K_TO_DISPLAY) < 15:
                    if self.curRightWristX > self.curRightHandX:
                        self.movingDirection = "left"
                    else:
                        self.movingDirection = "right"
            else:
                self.movingDirection = None  
        except: 
            self.movingDirection = None              
    
    
    def updateMove(self):
        if self.movingDirection == "up":
            if self.walls[self.myGrid]["up"] == False:
                self.myGrid = (self.myGrid[0]-1,self.myGrid[1])
        elif self.movingDirection == "down":
            if self.walls[self.myGrid]["down"] == False:
                self.myGrid = (self.myGrid[0]+1,self.myGrid[1])
        elif self.movingDirection == "left":
            if self.walls[self.myGrid]["left"] == False:
                self.myGrid = (self.myGrid[0],self.myGrid[1]-1)
        elif self.movingDirection == "right":
            if self.walls[self.myGrid]["right"] == False:
                self.myGrid = (self.myGrid[0],self.myGrid[1]+1)
                
    def updateMoveAuto(self):
        try:
            self.myGrid = self.path[self.path.index(self.myGrid)+1]
        except: pass
        
                
    def getPos(self,cell):
        pos = (self.margin + self.size // 2 + cell[1]*self.size,
               self.margin + self.size // 2 + cell[0]*self.size)
        return pos
                
    def drawMe(self,surface):
        pygame.draw.circle(surface, Color.red, self.getPos(self.myGrid), int(self.size//2*0.7), 0)
    
    
    def drawApple(self,surface):
        for a in self.apple:
            pygame.draw.circle(surface, Color.black, self.getPos(a), int(self.size//2*0.7), 0)
            
            
    def updateApple(self):
        if self.myGrid in self.apple:
            self.apple.remove(self.myGrid)
            self.score += 1
            c.totalScore += 1
        
        
    def generateRoute(self):
        if len(self.visited) == self.row*self.col: return
        else:
            unvisitedNeighbor = []
            self.visited.add(self.currCell)
            if (self.row-1,self.col-1) == self.currCell:
                    self.path += self.route
                    self.path.append((self.row-1,self.col-1))
            for neighbor in self.neighbors[self.currCell]:
                if neighbor not in self.visited:
                    unvisitedNeighbor.append(neighbor)
            if len(unvisitedNeighbor) != 0:
                self.route.append(self.currCell)
                chosenCell = random.choice(unvisitedNeighbor)
                self.removeWall(self.currCell, chosenCell)
                self.currCell = chosenCell
                self.visited.add(chosenCell)
            else:
                prevCell = self.route.pop()
                self.currCell = prevCell
            self.generateRoute()
                
        
    def redrawAll(self):
        self.screen.fill(Color.black)   
        self.mazeSurface.fill(Color.white)
        self.drawGrids()
        self.drawApple(self.mazeSurface)
        self.drawMe(self.mazeSurface)
        self.screen.blit(self.mazeSurface,(self.width/2-self.w/2,self.height/2 - self.h/2))
        

    def removeWall(self,thisCell,neighbor):
        if neighbor[0] == thisCell[0]:
            if neighbor[1] > thisCell[1]:
                self.walls[thisCell]["right"] = False
                self.walls[neighbor]["left"] = False
            else:
                self.walls[thisCell]["left"] = False
                self.walls[neighbor]["right"] = False
        elif neighbor[1] == thisCell[1]:
            if neighbor[0] > thisCell[0]:
                self.walls[thisCell]["down"] = False
                self.walls[neighbor]["up"] = False
            else:
                self.walls[thisCell]["up"] = False
                self.walls[neighbor]["down"] = False
        
    def drawGrids(self):
        for i in range(self.row):
            for j in range(self.col):
                for side in self.walls[(i,j)]:
                    if self.walls[(i,j)][side] == True:
                        self.drawWall(self.mazeSurface, i, j, side)

    
    def drawWall(self,surface,i,j,side):
        topLeft = (self.margin+j*self.size,self.margin+i*self.size)
        topRight = (self.margin+(j+1)*self.size,self.margin+i*self.size)
        bottomLeft = (self.margin+j*self.size,self.margin+(i+1)*self.size)
        bottomRight = (self.margin+(j+1)*self.size,self.margin+(i+1)*self.size)
        if side == "left":
            pygame.draw.line(surface, Color.black,topLeft,bottomLeft, 3)
        elif side == "right":
            pygame.draw.line(surface, Color.black,topRight, bottomRight , 3)
        elif side == "up":
            pygame.draw.line(surface, Color.black,topLeft, topRight, 3)
        elif side == "down":
            pygame.draw.line(surface, Color.black,bottomLeft, bottomRight, 3)
        
        
                
    def getNeighbors(self, point):
        neighbors = []
        x,y = point
        for drow in [-1,0,1]:
            for dcol in [-1,0,1]:
                newx = x + drow
                newy = y + dcol
                if abs(drow) != abs(dcol) and 0 <= newx <= self.row-1 and 0 <= newy <= self.col-1:
                    neighbors.append((newx,newy))
        return neighbors
            
    def timerFired(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.done = True # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                self.keyPressed(event)
        self.timerCalled += 1
        if self.auto == False:
            self.updateKinect()
            self.updateDirection()
            if self.timerCalled % 15 == 0:
                self.updateMove()
                self.updateApple()
        else:
            if self.timerCalled % 1 == 0:
                self.updateMoveAuto()
                self.updateApple()
        self.redrawAll()
        if self.myGrid == (self.row-1,self.col-1):
            self.passed = True
            
    def run(self):
        while not self.done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                elif event.type == pygame.KEYDOWN:
                    self.keyPressed(event)
            self.timerCalled += 1
            if self.auto == False:
                self.updateKinect()
                self.updateDirection()
                if self.timerCalled % 15 == 0:
                    self.updateMove()
                    self.updateApple()
            else:
                if self.timerCalled % 1 == 0:
                    self.updateMoveAuto()
                    self.updateApple()
            self.redrawAll()
            if self.myGrid == (self.row-1,self.col-1):
                self.done = True
            pygame.display.update()

            # --- Limit to 60 frames per second
            self.clock.tick(25)
        self.kinect.close()
        # close the window and quit.
        pygame.quit()

#maze = Maze(1200,675,20,20,30,10,15)
#maze.run()
#maze.generateRoute()
#print(maze.path)   