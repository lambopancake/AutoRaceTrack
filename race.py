import cv2
import pygame
import numpy as np
from time import sleep
from Car import Car
from Rewards import RewardSys
#from Rewards import rewardLocation, rewardCalc, calcTrackLength,angles

num = 3
fileName = f"tracks//raceTrack{num}.png"
img = cv2.imread(fileName)

fileOut = []

with open(f"tracks//raceTrack{num}.txt",'r') as file:
    fileOut = list(file)

#Completed in two to make it easier
#To convert string back to list of tuples of (x,y)
fileOut = list(map(lambda x: tuple(x[:-1].split()), fileOut))
fileOut = list(map(lambda x: tuple(map(lambda y: int(y), x)), fileOut)) #tuple of string to tuple of int

origin = fileOut[0]
rewards = fileOut
rewardSys = RewardSys(rewards)
rewardSys.trackLength = rewardSys.calcTrackLength()
angles = RewardSys.angles(rewards)


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

current_point = 0
i = 0
aCar = Car(img, MAXSPEED = 300)
aCar.position = fileOut[current_point] #which is origin

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
    rgb = tuple(img.transpose(1,0,2)[aCar.carPosition()[0], aCar.carPosition()[1]])
    if(rgb[::-1] == GRASS_COLOR):
        i += 1
        aCar.position = rewards[i]
        aCar.speed = 0
        aCar.angle = angles[i]
        sleep(0.2)
        current_point = i
        rewardSys.trackLength = rewardSys.calcTrackLength(i)
    elif(rgb[::-1] == FINISHLINE_COLOR):
        i += 1
        aCar.position = rewards[i]
        aCar.speed = 0
        aCar.angle = angles[i]
        sleep(0.2)
        current_point = i
        rewardSys.trackLength = rewardSys.calcTrackLength(i)

    ########rewards#######
    current_point = rewardSys.rewardLocation(aCar.carPosition(), current_point)
    per = rewardSys.rewardCalc(aCar.carPosition(), i, current_point)
    print(per)
    
    #####RENDER############
    pygame.draw.circle(screen, (255,0,0),aCar.position, 5)
    pygame.draw.line(screen, (255,0,0), aCar.position, aCar.forwardPoint(),width = 2)

    raysPoints = aCar.cast_ray_points()
    
    for rays in raysPoints:
        pygame.draw.circle(screen, (200,200,0),rays, 2)
        pygame.draw.line(screen, (200,200,0), aCar.position, rays,width = 1)
    
    for points in rewards:
        pygame.draw.circle(screen, (200,200,0),points, 2)
    
    pygame.display.update()
    clock.tick(60)
pygame.quit()
