import pygame 
import random
import math
from Colors import *
from MyImages import *
from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *
import Constants as c

class Shooting(object):
    def __init__(self,w,h,t):
        pygame.font.init()
        self.width = w 
        self.height = h 
        self.done = False 
        self.gameover = False
        self.passed = False
        
        self.myfont = pygame.font.Font('font/munro.ttf', 60)
        self.timer = t
        
        self.offsety = 100
        
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        self.shootingSurface = pygame.Surface((self.width,self.height))
        self.aim = MyImage("icon/aim/aim_1.gif",self.width/2,self.height/2+self.offsety)
        self.aim.resize(200, 200)
        self.targets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        self.bodies = None
        
        self.prevRightLasso = self.prevLeftLasso = False
        self.curRightLasso = self.curLeftLasso = False
        self.hypotenuseLeft = self.hypotenuseRight = 0
        self.rightAngle = math.pi/4
        self.leftAngle = math.pi*3/4
        
        self.leftShoot = self.rightShoot = False
        self.curRightHandY = self.curRightHandX = 0
        self.curLeftHandX = self.curLeftHandY = 0                                                                                               
        self.curRightElbowX = self.curRightElbowY = 0
        self.curLeftElbowX = self.curLeftElbowY = 0
        
        self.clock = pygame.time.Clock()
        self.timerCalled = 0
        self.score = 0
        
        
    def drawDirection(self,surface,r):
        try:
            rightx = self.width/2 + r*math.cos(self.rightAngle)
            righty = self.height/2 - r*math.sin(self.rightAngle)
            pygame.draw.line(surface, Color.black, (self.width/2,self.height/2+self.offsety), (rightx,righty+self.offsety), 5)
        except:
            rightx = self.width/2+r*math.cos(math.pi/4)
            righty = self.height/2 - r*math.sin(math.pi*3/4)
            pygame.draw.line(surface,Color.black,(self.width/2,self.height/2+self.offsety), (rightx,righty+self.offsety), 5)
        try:
            leftx = self.width/2 + r*math.cos(self.leftAngle)
            lefty = self.height/2 - r*math.sin(self.leftAngle)
            pygame.draw.line(surface, Color.black, (self.width/2,self.height/2+self.offsety), (leftx,lefty+self.offsety), 5)
        except:
            leftx = self.width/2+r*math.cos(math.pi/4)
            lefty = self.height/2 - r*math.sin(math.pi*3/4)
            pygame.draw.line(surface, Color.black, (self.width/2,self.height/2+self.offsety), (leftx,lefty+self.offsety), 5)
        
        
        
    def redrawAll(self):
        self.shootingSurface.fill(Color.white)
        self.targets.draw(self.shootingSurface)
        self.bullets.draw(self.shootingSurface)
        self.drawDirection(self.shootingSurface, 150)
        self.aim.draw(self.shootingSurface)
        if self.timer < 0:
            text = self.myfont.render("Time:%4d s" % 0, False, Color.black)
        else:
            text = self.myfont.render("Time:%4d s" % self.timer, False, Color.black)
        self.shootingSurface.blit(text, (50,self.height-80))
        
        
    def updateKinect(self):
        if self.kinect.has_new_body_frame(): 
                self.bodies = self.kinect.get_last_body_frame()

                if self.bodies is not None: 
                    for i in range(0, self.kinect.max_body_count):
                        body = self.bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 
                        self.prevLeftLasso = self.curLeftLasso
                        self.prevRightLasso = self.curRightLasso
                        if body.hand_left_state == 2:
                            self.curLeftLasso = True
                        else: self.curLeftLasso = False
                        if body.hand_right_state == 2:
                            self.curRightLasso = True
                        else: self.curRightLasso = False
                        print(body.hand_right_state)
                        print(body.hand_left_state)
                        joints = body.joints 
                        # save the hand positions
                        mappedJoints = self.kinect.body_joints_to_color_space(joints)
                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curRightHandX = mappedJoints[PyKinectV2.JointType_HandRight].x
                            self.curRightHandY = mappedJoints[PyKinectV2.JointType_HandRight].y
                        if joints[PyKinectV2.JointType_ElbowRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curRightElbowX = mappedJoints[PyKinectV2.JointType_ElbowRight].x
                            self.curRightElbowY = mappedJoints[PyKinectV2.JointType_ElbowRight].y
                            
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curLeftHandX = mappedJoints[PyKinectV2.JointType_HandLeft].x
                            self.curLeftHandY = mappedJoints[PyKinectV2.JointType_HandLeft].y
                        if joints[PyKinectV2.JointType_ElbowLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curLeftElbowX = mappedJoints[PyKinectV2.JointType_ElbowLeft].x
                            self.curLeftElbowY = mappedJoints[PyKinectV2.JointType_ElbowLeft].y
                        print(self.curRightHandX,self.curRightHandY,"    ", self.curRightElbowX,self.curRightElbowY)

                            
    def updateDirection(self):
        try:
            self.hypotenuseRight = math.sqrt((self.curRightHandY - self.curRightElbowY)**2 + (self.curRightHandX - self.curRightElbowX)**2)
            tempRightAngle = round(math.acos((self.curRightHandX - self.curRightElbowX)/self.hypotenuseRight),4)
            if self.curRightHandY < self.curRightElbowY:
                self.rightAngle = tempRightAngle
        except: 
            print("except??right")
        try:
            self.hypotenuseLeft = math.sqrt((self.curLeftHandY - self.curLeftElbowY)**2 + (self.curLeftHandX - self.curLeftElbowX)**2)
            tempLeftAngle = round(math.acos((self.curLeftHandX - self.curLeftElbowX)/self.hypotenuseLeft),4)
            if self.curLeftHandY < self.curLeftElbowY:
                self.leftAngle = tempLeftAngle
        except:
            print("except??left")
            
                            
    def updateShoot(self):
        if self.prevRightLasso == False and self.curRightLasso == True:
            self.rightShoot = True
        else: self.rightShoot = False
        if self.prevLeftLasso == False and self.curLeftLasso == True:
            self.leftShoot = True
        else: self.leftShoot = False
        if self.rightShoot == True:
            v = random.choice([27,39])
            self.bullets.add(Bullet(self.width/2,self.height/2+self.offsety,v,self.rightAngle))
        if self.leftShoot == True:
            v = random.choice([27,39])
            try:
                self.bullets.add(Bullet(self.width/2,self.height/2+self.offsety,v,self.leftAngle))
            except: pass
            

            
    def timerFired(self):
        if self.timerCalled % 20 == 0:
            self.timer -= 1
     
        if self.timerCalled % 20 == 0:
            x = random.randint(0,self.width)
            y = random.randint(0,self.height)
            d = Dot(x,y)
            self.targets.add(d)
        self.updateKinect()
        self.updateDirection()
        self.updateShoot()
        self.targets.update(self.width,self.height)
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.x < 0 or bullet.x > self.width or bullet.y < 0 or bullet.y > self.height:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
        if pygame.sprite.groupcollide(self.targets, self.bullets, True, True, pygame.sprite.collide_circle):
            self.score += 1
            c.totalScore += 1
        self.redrawAll() 
        self.timerCalled += 1   
        if self.timer < 0:
            self.passed = True
        
        
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            self.timerCalled += 1
            if self.timerCalled % 90 == 0:
                x = random.randint(0,self.width)
                y = random.randint(0,self.height)
                d = Dot(x,y)
                self.targets.add(d)
            self.updateKinect()
            self.updateDirection()
            self.updateShoot()
            self.targets.update(self.width,self.height)
            self.bullets.update()
            for bullet in self.bullets:
                if bullet.x < 0 or bullet.x > self.width or bullet.y < 0 or bullet.y > self.height:
                    self.bullets.remove(bullet)
            if pygame.sprite.groupcollide(self.targets, self.bullets, True, True, pygame.sprite.collide_circle):
                self.score += 1
            self.redrawAll()
            pygame.display.update()
            self.clock.tick(60)
        self.kinect.close()
        pygame.quit()
        
# This class is modified from pygame tutorial on 112 course website
class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Dot, self).__init__()
        self.radius = random.randint(10, 70)
        self.x, self.y = x, y
        self.xSpeed = random.randint(-15, 15)
        self.ySpeed = random.randint(-15, 15)
        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)  # make it transparent
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, Color.gray,
                           (self.radius, self.radius), self.radius)

    def getRect(self):  # GET REKT
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def update(self, screenWidth, screenHeight):
        self.x += self.xSpeed
        self.y += self.ySpeed
        if self.x < 0:
            self.x = screenWidth
        elif self.x > screenWidth:
            self. x = 0
        if self.y < 0:
            self.y = screenHeight
        elif self.y > screenHeight:
            self.y = 0
        self.getRect()
        
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, v, theta):
        super(Bullet, self).__init__()
        self.radius = 10
        self.x, self.y = x, y
        self.xSpeed = int(v * math.cos(theta))
        self.ySpeed = int(v * math.sin(theta))
        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)  # make it transparent
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, Color.black,
                           (self.radius, self.radius), self.radius)


    def getRect(self):  # GET REKT
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def update(self):
        self.x += self.xSpeed
        self.y -= self.ySpeed
        self.getRect()


#thisGame = Shooting(1200,700)
#thisGame.run()
