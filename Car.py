import math
import sys
import cv2
import pygame

class Car():
    def __init__(self, img, MAXSPEED = 700, barrier_COLOR = (20,183,43), finish_COLOR = (20,0,200)):
        self.MAXSPEED = MAXSPEED
        self.barrier_COLOR = barrier_COLOR
        self.finish_COLOR =  finish_COLOR
        self.speed = 0
        self.angle = 0 # 1-360
        self.position = None # (x,y)
        self.size = 10
        self.img = img
        self.imgSize = img.transpose(1,0,2).shape[:2]

    #returns (dx,dy) based on direction, magnitude, and scale
    def vec(direction, magnitude, scale = 1):
        radian = math.radians(direction)
        return (math.cos(radian) * magnitude * scale, math.sin(radian) * magnitude * scale)
    
    #returns distance between two points
    def distance(p1, p2): 
        return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))
    
    #returns an angle so its always between 1-360
    def setAngle(angle):
        if(angle >= 360): 
            return angle - 360
        elif(angle <= 0):
            return angle + 360
        else:
            return angle
    
    #returns a point in the front of the car
    def forwardPoint(self, length = 20): 
        dx, dy = Car.vec(self.angle, length)
        return (self.position[0] + dx, self.position[1] + dy)
    
    #returns a point on the edge of the screen
    #depending on the angle and car position
    def limit(self, angle): 
        angle = Car.setAngle(angle)
        m = math.tan(math.radians(angle)) #if error at + 0.0001
        b = (-m * self.position[0]) + self.position[1]
        
        y1 = b          #y1 = m(0) + b
        y2 = (m * 800) + b
        x1 = -b / (m + 0.000001)     #x1 = (0 - b)/m
        x2 = (500 - b) / (m + 0.000001)

        if(angle >= 270):   #quad 4
            return (x1,0) if not((x1,0) > (self.imgSize[0],y2)) else (self.imgSize[0],y2)
        elif(angle >= 180): #quad 3
            return (x1,0) if (x1,0) > (0,y1) else (0,y1)
        elif(angle >= 90):  #quad 2
            return (x2,self.imgSize[1]) if (x2,self.imgSize[1]) > (0,y1) else (0,y1)
        else:               #quad 1
            return (x2,self.imgSize[1]) if not((x2,self.imgSize[1]) > (self.imgSize[0], y2)) else (self.imgSize[0], y2)


    def move(self, forward, turn, accel = 3, deccel = 2, brake = 10): 
        #forward 0 or 1
        #turn is -1, 0, or 1

        # accel = accel
        # deccel = deccel
        # brake = brake
        
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
        elif(forward == -1):
            if(self.speed > 0):
                self.speed -= brake
            else:
                self.speed = 0
        if(turn != 0):
            self.angle -= turn
            self.angle = Car.setAngle(self.angle)
        
        diffX, diffY = Car.vec(self.angle, self.speed, 0.01) 
        self.position = (self.position[0] + diffX, self.position[1] + diffY)

    #returns the distances of the rays 
    #more details in cast_ray_points
    def ray_dist(self, fov = 90, rays = 3):
        distances = []
        #angle for each ray
        for angle in range(self.angle - (fov // 2), self.angle + (fov // 2) + 2, (fov // 2) // rays):

            limit = self.limit(angle)
            radian = math.radians(angle)
            dx = math.cos(radian)
            dy = math.sin(radian)
            cx, cy = self.position    

            for _ in range(int(Car.distance(self.position,limit))):

                color = tuple((self.img.transpose(1,0,2))[int(cx),int(cy)])[::-1]

                if(color == self.barrier_COLOR):
                    distances.append(int(Car.distance(self.position,(cx,cy))) / Car.distance((0,0), self.imgSize))
                    break
                elif(color == self.end_COLOR):
                    distances.append(1)
                    break

                cx += dx
                cy += dy

        return distances  

    def cast_ray_points(self, fov = 90, rays = 3): #Used for visuales
        #best rays parameter: 2,3,5,6
        #any ray number that (fov/2)/rays = whole #
        #barrier_color would be the grass
        #end_color would be the finish square color
        #   which returns 1 if the rays detects it
        distances = []
        for angle in range(self.angle - (fov // 2), self.angle + (fov // 2) + 2, (fov // 2) // rays):
        
            limit = self.limit(angle)
            dx = math.cos(math.radians(angle))
            dy = math.sin(math.radians(angle))
            cx, cy = self.position
            
            for _ in range(int(Car.distance(self.position, limit))):
                color = tuple((self.img.transpose(1,0,2))[int(cx),int(cy)])[::-1]
                if(color == self.barrier_COLOR):
                    distances.append((cx,cy))
                    break
                elif(color == self.finish_COLOR):
                    distances.append((cx,cy))
                    break

                cx += dx
                cy += dy

        return distances 


    def carPosition(self):
        return tuple(map(lambda x: int(x) , self.position))


###needs updating########
####Dont run######
####car object works#####
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
        if(key[pygame.K_DOWN]):
            forward -= 1

        aCar.move(forward, turn)
        aCar.cast_ray_boarder()
        aCar.draw()
        print(aCar.speed)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
