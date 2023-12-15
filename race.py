import cv2
import pygame
import numpy as np
from time import sleep
from Car import Car

fileName = "tracks//raceTrack1.png"
img = cv2.imread(fileName)

fileOut = []

with open("tracks//raceTrack1.txt",'r') as file:
    fileOut = list(file)

#Completed in two to make it easier
fileOut = list(map(lambda x: tuple(x[:-1].split()), fileOut))
fileOut = list(map(lambda x: tuple(map(lambda y: int(y), x)), fileOut))

origin = fileOut[0]
rewards = fileOut[1:]


print(type(img))
print(img.shape)


running = True

GRASS_COLOR = (20,183,43)
ROAD_COLOR = (75,75,75)
FINISHLINE_COLOR = (20,0,200)
START_COLOR = (0,0,0)


x, y = 0, 0

screen = pygame.display.set_mode((800,500))
raceTrack = pygame.image.load(fileName)
screen.blit(raceTrack, (0,0))
pygame.display.flip()

clock = pygame.time.Clock()

aCar = Car(img)
aCar.pos = origin


while(running):

   
    screen.blit(raceTrack, (0,0))
    ##################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ##################
    
    forward = 0
    turn = 0
    ######CONTROLS######
    key = pygame.key.get_pressed()
    if(key[pygame.K_UP]):
        forward = 1
    if(key[pygame.K_LEFT]):
        turn += 1
    if(key[pygame.K_RIGHT]):
        turn -= 1
    if(key[pygame.K_DOWN]):
        forward -= 1
    ###################

    
    #########ACTIONS##########
    aCar.move(forward,turn)


    rgb = tuple(img.transpose(1,0,2)[aCar.carPosition()[0], aCar.carPosition()[1]])

    ######RESET######
    if(rgb[::-1] == GRASS_COLOR):
        aCar.pos = origin
        aCar.speed = 0
        aCar.angle = 0
        sleep(0.2)
    elif(rgb[::-1] == FINISHLINE_COLOR):
        aCar.pos = origin
        aCar.speed = 0
        aCar.angle = 0
        sleep(0.2)

    
    ######sensor########
    #print(aCar.ray_dist(GRASS_COLOR, FINISHLINE_COLOR))
    
    ########rewards#######
    

    ####
    #####RENDER############
    pygame.draw.circle(screen, (255,0,0),aCar.pos, 5)
    pygame.draw.line(screen, (255,0,0), aCar.pos, aCar.forwardArrow(),width = 2)

    raysPoints = aCar.cast_ray_points(GRASS_COLOR, FINISHLINE_COLOR)
    
    for rays in raysPoints:
        pygame.draw.circle(screen, (255,0,0),rays, 2)
        pygame.draw.line(screen, (255,0,0), aCar.pos, rays,width = 1)
    
    pygame.display.update()
    clock.tick(50)
pygame.quit()
