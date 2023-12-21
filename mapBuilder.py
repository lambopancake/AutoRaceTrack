import pygame
import sys
import os
from Rewards import rewardPoints, rewardLocation, rewardCalc, calcTrackLength
from time import sleep
from Car import Car

SCREEN_SIZE = (800,500)
GRASS_COLOR = (20,183,43)
ROAD_COLOR = (75,75,75)
FINISHLINE_COLOR = (20,0,200)
START_COLOR = (0,0,0)
CAR_COLOR = (255,0,0)

screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill(GRASS_COLOR)

running = True
origin = None
clock = pygame.time.Clock()
end = None

roadCenter = []
trackDist = 50

space = 0
while running:  
    
    for event in pygame.event.get():
    #############################
        if event.type == pygame.QUIT:
            running = False
    #############################

    key = pygame.key.get_pressed()
    rad = 30
    #length, width = 10,5
    pos = pygame.mouse.get_pos()
    
    if(key[pygame.K_q]):#draws track
        pygame.draw.circle(screen, ROAD_COLOR,pos,rad)
            # n += 1
        roadCenter.append(pos)
    if(key[pygame.K_w]):#start line squre
        pygame.draw.rect(screen,START_COLOR,[pos[0]-25,pos[1]-25,50,50], 30)
        origin = pos
    if(key[pygame.K_e]):#end Line
        pygame.draw.rect(screen,FINISHLINE_COLOR,[pos[0]-25,pos[1]-25,50,50], 30) 
        end = pos
    if(key[pygame.K_SPACE]): #update this so that the reward dots appear when you press space
        space = 2
    
    if(space == 1 ):
        points = rewardPoints(roadCenter, rad = trackDist)
        for point in points:
            pygame.draw.circle(screen, ROAD_COLOR,point,int(rad * 0.25))
        if (not(origin == None)):
            pygame.draw.circle(screen, START_COLOR, origin,int(rad * 0.25))
        if (not(end == None)):
            pygame.draw.circle(screen, FINISHLINE_COLOR, end,int(rad * 0.25))
        space -= 1
        
    if(len(roadCenter) >= 1 and space == 2):
        points = rewardPoints(roadCenter, rad = trackDist)
        for point in points:
            pygame.draw.circle(screen, (255,215,0),point,int(rad * 0.25))
        if (not(origin == None)):
            pygame.draw.circle(screen, (255,100,100), origin,int(rad * 0.25))
        if (not(end == None)):
            pygame.draw.circle(screen, (255,100,100), end,int(rad * 0.25))
        space -= 1
    
    #Saves an image of the track
    if(key[pygame.K_b]):
        num = 1
        while(os.path.exists(f"tracks//raceTrack{num}.png")):
            num += 1
            
        pygame.image.save(screen,f"tracks//raceTrack{num}.png")
        points = rewardPoints(roadCenter, rad = trackDist)
        with open(f"tracks//raceTrack{num}.txt", 'w') as file:
            pList = []
            pList.append(origin)
            pList.extend(points)
            pList.append(end)

            for tups in pList:
                file.write(str(tups[0]) + " " + str(tups[1]) + "\n")


        sleep(1)
   
    pygame.display.update()
