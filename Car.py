import math
import sys
import pygame

class Car():
    def __init__(self, screen , screenSize = (800,500)):
        self.MAXSPEED = 200
        self.speed = 0
        self.angle = 0 # 0-359
        self.pos = (-100,-100) # (x,y)
        self.size = 10
        self.screen = screen
        self.screenSize = screenSize 

    def vec(self, direction, magnitude, scale = 1):
        return (magnitude * math.cos(math.radians(direction)) * scale, magnitude * math.sin(math.radians(direction)) * scale)

    def endPoint(self, angle):
        angle = self.normAngle(angle + 0.0001)
        m = math.tan(math.radians(angle)) + 0.00000001
        b = (-m * self.pos[0]) + self.pos[1]
        
        #y1 = m(0) + b
        y1 = b
        y2 = (m * 800) + b

        #x1 = (0 - b)/m
        x1 = -b / m
        x2 = (500 - b) / m

        if(angle >= 270): #quad 4
            return (x1,0) if not((x1,0) > (self.screenSize[0],y2)) else (self.screenSize[0],y2)
        elif(angle >= 180): #quad 3
            return (x1,0) if (x1,0) > (0,y1) else (0,y1)
        elif(angle >= 90): #quad 2
            return (x2,self.screenSize[1]) if (x2,self.screenSize[1]) > (0,y1) else (0,y1)
        else: #quad 1
            return (x2,self.screenSize[1]) if not((x2,self.screenSize[1]) > (self.screenSize[0], y2)) else (self.screenSize[0], y2)
        

    def normAngle(self, ang):
        if(ang >= 360): #angle range (1 - 360)
            return ang - 360
        elif(ang <= 0):
            return ang + 360
        else:
            return ang
        
    def draw(self, color = (255,0,0)):
        length = 100#self.size * 2
        diffX, diffY = self.vec(self.angle, length)
        pygame.draw.circle(self.screen, color, self.pos, self.size)
        pygame.draw.line(self.screen, color, self.pos, (self.pos[0] + diffX, self.pos[1] + diffY),width = 2)
    
    def move(self, forward, turn):
        #forward 0 or 1
        #turn is -1, 0, or 1
        accel = 10
        deccel = 2
        if(forward == 1):
            if(self.speed  < self.MAXSPEED):
                self.speed += accel
            else:
                self.speed = self.MAXSPEED
        elif(forward == 0):
            if(self.speed > 0):
                self.speed -= deccel
            else:
                self.speed = 0
        if(turn != 0):
            self.angle -= turn
            self.angle = self.normAngle(self.angle)
        
        diffX, diffY = self.vec(self.angle, self.speed, 0.01) 
        self.pos = (self.pos[0] + diffX, self.pos[1] + diffY)

    def cast_ray(self, fov = 90, rays = 4):
        #rays on each side
        fov = fov
        inc = (fov // 2) // rays 
        poi = self.endPoint(self.angle)
        pygame.draw.line(self.screen, (0,200,90), self.pos, poi,width = 2)
        pygame.draw.circle(self.screen, (0,200,90), poi, 10)
        ang = self.angle
        for side in range(2):
            for ray in range(rays):
                ang += inc
                poi = self.endPoint(ang)
                pygame.draw.line(self.screen, (0,200,90), self.pos, poi,width = 2)
                pygame.draw.circle(self.screen, (0,200,90), poi, 10)
            ang = self.angle
            inc *= -1
    
    def carPosition(self):
        return (int(self.pos[0]), int(self.pos[1]))
if __name__ == "__main__":
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800,500))
    pygame.display.flip()

    running = True
    aCar = Car(screen)
    aCar.pos = (100,100)
    forward = 0
    turn = 0

    while running:
        screen.fill((0,0,0))
        forward = 0
        turn = 0
        for event in pygame.event.get():
             #############################
            if event.type == pygame.QUIT:
                running = False
             ################################
        
        key = pygame.key.get_pressed()
        if(key[pygame.K_UP]):
            forward = 1
        if(key[pygame.K_LEFT]):
            turn += 1
        if(key[pygame.K_RIGHT]):
            turn -= 1

        aCar.move(forward, turn)
        aCar.cast_ray(360,10)
        aCar.draw()
        pygame.display.update()
        clock.tick(120)
    pygame.quit()
