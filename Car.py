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

    def points(self):
        m = math.tan(math.radians(self.angle)) + 0.00000000001
        b = (-m * self.pos[0]) + self.pos[1]
        
        #y1 = m(0) + b
        y1 = b
        y2 = (m * 800) + b

        #x1 = (0 - b)/m
        x1 = -b / m
        x2 = (500 - b) / m

        return [(0, y1),(800, y2),(x1, 0),(x2, 500)]
        
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
            if(self.angle >= 360):
                self.angle = 0
            elif(self.angle <= -1):
                self.angle = 359
        
        diffX, diffY = self.vec(self.angle, self.speed, 0.01) 
        self.pos = (self.pos[0] + diffX, self.pos[1] + diffY)

    def cast_ray(self, fov = 90, rays = 4, length = 4):
        #rays on each side
        fov = fov
        inc = (fov // 2) // rays 
        for side in range(2):

            for ray in range(rays):
                poi = self.points()
                
                #left side
                pygame.draw.line(self.screen, (255,0,0), self.pos, poi[0],width = 2)
                pygame.draw.circle(self.screen, (255,0,0), poi[0], 30)
                #right side
                pygame.draw.line(self.screen, (0,255,0), self.pos, poi[1],width = 2)
                pygame.draw.circle(self.screen, (0,255,0), poi[1], 30)
                #uppder side
                pygame.draw.line(self.screen, (0,0,255), self.pos, poi[2],width = 2)
                pygame.draw.circle(self.screen, (0,0,255), poi[2], 30)
                #lower side
                pygame.draw.line(self.screen, (200,200,200), self.pos, poi[3],width = 2)
                pygame.draw.circle(self.screen, (200,200,200), poi[3], 30)

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

    # for i in range(359):
    #     print(i, ": \t",math.tan(math.radians(i)))
        



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
        aCar.cast_ray(fov = 0, rays = 1)
        aCar.draw()
        #print(aCar.angle)
        pygame.display.update()
        clock.tick(120)
    pygame.quit()
