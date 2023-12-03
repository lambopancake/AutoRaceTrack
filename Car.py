import math
import sys
import pygame

class Car():
    def __init__(self, screen):
        self.MAXSPEED = 200
        self.speed = 0
        self.angle = 0 # 0-359
        self.pos = (-100,-100) # (x,y)
        self.size = 10
        self.screen = screen

    def vec(self, direction, magnitude, scale = 1):
        return (magnitude * math.cos(math.radians(direction)) * scale, magnitude * math.sin(math.radians(direction)) * scale)

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
        length = 1000#self.size * length
        inc = (fov // 2) // rays 
        for side in range(2):
            ang = self.angle
            for ray in range(rays):
                slope = math.tan(math.radians(ang)) + 0.00000000001# * -1
                x1 = slope * (0 - self.pos[0]) + self.pos[1]
                x2 = slope * (800 - self.pos[0]) + self.pos[1]
                y1 = ((500 - self.pos[1]) / slope) + self.pos[0]
                y2 = ((0 - self.pos[1]) / slope) + self.pos[0]
                   
                pygame.draw.line(self.screen, (0,200,90), self.pos, (x1, 0),width = 2)
                pygame.draw.circle(self.screen, (0,200,90), (x1, 0), 30)

                pygame.draw.line(self.screen, (0,200,90), self.pos, (x2, 500),width = 2)
                pygame.draw.circle(self.screen, (0,200,90), (x2, 500), 30)

                pygame.draw.line(self.screen, (0,200,90), self.pos, (0, y1),width = 2)
                pygame.draw.circle(self.screen, (0,200,90), (0, y1), 30)

                pygame.draw.line(self.screen, (0,200,90), self.pos, (800, y2),width = 2)
                pygame.draw.circle(self.screen, (0,200,90), (800, y2), 30)

                #print("\t\t", (endX, endY))
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

    for i in range(359):
        print(i, ": \t",math.tan(math.radians(i)))
        



    # while running:
    #     screen.fill((0,0,0))
    #     forward = 0
    #     turn = 0
    #     for event in pygame.event.get():
    #          #############################
    #         if event.type == pygame.QUIT:
    #             running = False
    #          ################################
        
    #     key = pygame.key.get_pressed()
    #     if(key[pygame.K_UP]):
    #         forward = 1
    #     if(key[pygame.K_LEFT]):
    #         turn += 1
    #     if(key[pygame.K_RIGHT]):
    #         turn -= 1

    #     aCar.move(forward, turn)
    #     aCar.cast_ray(fov = 0, rays = 1)
    #     aCar.draw()
    #     #print(aCar.angle)
    #     pygame.display.update()
    #     clock.tick(120)
    # pygame.quit()
