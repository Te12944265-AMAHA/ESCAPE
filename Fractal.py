
import pygame
import random
import math
from Colors import *


    
class FractalTree(object):
    def __init__(self,w,h):
        self.level = 10
        self.width = w 
        self.height = h
        self.done = False
        self.color = random.choice(Color.getAllColors())
        self.treeSurface = pygame.Surface((self.width,self.height))
        self.treeSurface.set_colorkey(Color.white)
        self.clock = pygame.time.Clock()
    
    
    def fractalTree(self, xs, ys, r, theta, level,color,depth):
        # using depth, so that each layer corresponds to a color
        # regardless which level the recursion is at
        if level == 1:
            # only a circle at the center, no beams
            #canvas.create_line(xs,ys,xs,ys+r)
            pass     
        else:
            if depth%2 == 0:
                theta1 = theta
                theta2 = theta +math.radians(20)
                newr1 = r
                newr2 = r / 2
                thick1 = 0.8
                thick2 = 0.5
            elif depth%2 == 1:
                theta1 = theta -math.radians(20)
                theta2 = theta +math.radians(20)
                newr1 = r / 2
                newr2 = r / 2
                thick1=thick2 = 0.6
            xe1 = xs+newr1*math.cos(theta1)
            ye1 = ys-newr1*math.sin(theta1)
            xe2 = xs+newr2*math.cos(theta2)
            ye2 = ys-newr2*math.sin(theta2)
            # first draw the beams, then draw the circles
            pygame.draw.line(self.treeSurface, color, (xs,ys), (xe1,ye1), int((8 - depth)*1.5*thick1))
            #canvas.create_line(xs, ys, xe1, ye1,fill = color, width = int((8 - depth)*1.5*thick1))
            pygame.draw.line(self.treeSurface, color, (xs,ys), (xe2,ye2), int((8 - depth)*1.5*thick2))
            #canvas.create_line(xs, ys, xe2, ye2,fill = color, width = int((8 - depth)*1.5*thick2))
            self.fractalTree(xe1, ye1, newr1, theta1, level-1,color,depth= depth+1)
            self.fractalTree(xe2, ye2, newr2, theta2, level-1,color,depth = depth+1)
            #fractalTree(canvas, xe1, ye1, newr1, theta1, level-1,color,depth= depth +1)
            #fractalTree(canvas, xe2, ye2, newr2, theta2, level-1,color,depth = depth +1)
            
    def drawTree(self):
        self.treeSurface.fill(Color.white)
        pygame.draw.line(self.treeSurface, self.color, (self.width/2,0), (self.width/2,100), 9)
        #canvas.create_line(data.width/2,0,data.width/2,200,fill = color, width=9)
        self.fractalTree(self.width/2, 100, 100, -math.pi/2, self.level,self.color,0)
        #fractalTree(canvas, data.width/2, 200, 200, -math.pi/2,data.level,color, 0)
        
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            self.drawTree()
            pygame.display.update()
            self.clock.tick(25)
        pygame.quit()
        
        
class Tree_Two(FractalTree):
    def __init__(self,x,y,w,h):
        super().__init__(w, h)
        self.x =self.originalx= x 
        self.y = y
        self.drawTree()
        #self.displaySurface = pygame.display.set_mode((self.width,self.height))
        
    def fractalTree(self, xs, ys, r, theta, level, color, depth):
        if level == 1:
            pass     
        else:
            if depth%2 == 0:
                theta1 = theta - math.radians(random.randint(0,50))
                theta2 = theta + math.radians(random.randint(15,30))
                newr1 = r * random.choice([0.3,0.4,0.5,0.6,0.7,0.8,0.9])
                newr2 = r *random.choice([0.5,0.6,0.7,0.8,0.9])
                thick1 = 0.8
                thick2 = 0.5
            elif depth%2 == 1:
                theta1 = theta -math.radians(random.randint(20,45))
                theta2 = theta +math.radians(random.randint(20,30))
                newr1 = r *random.choice([0.3,0.4,0.5,0.6])
                newr2 = r *random.choice([0.5,0.6,0.7,0.8])
                thick1=thick2 = 0.6
            xe1 = xs+newr1*math.cos(theta1)
            ye1 = ys-newr1*math.sin(theta1)
            xe2 = xs+newr2*math.cos(theta2)
            ye2 = ys-newr2*math.sin(theta2)
            # first draw the beams, then draw the circles
            pygame.draw.line(self.treeSurface, color, (xs,ys), (xe1,ye1), int((8 - depth)*1.5*thick1))
            #canvas.create_line(xs, ys, xe1, ye1,fill = color, width = int((8 - depth)*1.5*thick1))
            pygame.draw.line(self.treeSurface, color, (xs,ys), (xe2,ye2), int((8 - depth)*1.5*thick2))
            #canvas.create_line(xs, ys, xe2, ye2,fill = color, width = int((8 - depth)*1.5*thick2))
            self.fractalTree(xe1, ye1, newr1, theta1, level-1,color,depth= depth+1)
            self.fractalTree(xe2, ye2, newr2, theta2, level-1,color,depth = depth+1)
            
    def drawTree(self):
        self.treeSurface.fill(Color.white)
        # r? 100 - 200.. level = 10, theta1, theta 2, thick = 9
        pygame.draw.line(self.treeSurface, self.color, (self.width/2,self.height), (self.width/2,self.height-200), 9)
        self.fractalTree(self.width/2, self.height-200, 200, math.pi/2, self.level,self.color,0)
        
    def draw(self,surface):
        surface.blit(self.treeSurface,(self.x-self.width/2,self.y-self.height/2+1))
        
    def updatePos(self,x,y):
        self.x = x 
        self.y = y
        
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            #self.displaySurface.fill(Color.black)
            #self.displaySurface.blit(self.treeSurface,(0,0))
            pygame.display.update()
            self.clock.tick(25)
        pygame.quit()
    
 
#pygame.init()       
#tree = FractalTree(1200,700)
#tree2 = Tree_Two(700,700)
#tree2.run()
        


