import pygame
import sys
import os
from rewards import rewardPoints, rewardLocation, rewardCalc, calcTrackLength
from time import sleep
from Car import Car

SCREEN_SIZE = (800,500)
GRASS_COLOR = (20,183,43)
ROAD_COLOR = (75,75,75)
FINISHLINE_COLOR = (20,0,200)
START_COLOR = (0,0,0)
CAR_COLOR = (255,0,0)

screen = pygame.display.set_mode(SCREEN_SIZE)

race_track = pygame.Surface(SCREEN_SIZE)
race_track.fill(GRASS_COLOR)
running = True
car_cords = (-100,-100)
origin = (-100,-100)
clock = pygame.time.Clock()

inc = 1

aCar = Car(screen)

n = 0
roadCenter = []
current_point = 0
while running:  
    forward = 0
    turn = 0
    for event in pygame.event.get():
    #############################
        if event.type == pygame.QUIT:
            running = False
    #############################

    key = pygame.key.get_pressed()
    rad = 30
    length, width = 10,5
    pos = pygame.mouse.get_pos()
    
    if(key[pygame.K_w]):#draws track
        pygame.draw.circle(race_track, ROAD_COLOR,pos,rad)
        n += 1
        roadCenter.append(pos)
    if(key[pygame.K_d]):#deletes track
        pygame.draw.circle(race_track, GRASS_COLOR,pos,rad)
    if(key[pygame.K_s]):#start line squre
        pygame.draw.rect(race_track,START_COLOR,[pos[0]-25,pos[1]-25,50,50], 30)
        origin = pos
    if(key[pygame.K_e]):#end Line
        pygame.draw.rect(race_track,FINISHLINE_COLOR,[pos[0]-25,pos[1]-25,50,50], 30)
    if(key[pygame.K_q]):#adds/ resets car
        aCar.pos = origin
    #Moves car
    if(key[pygame.K_UP]):
        forward = 1
    if(key[pygame.K_DOWN]):
            forward -= 1
    if(key[pygame.K_LEFT]):
        turn += 1
    if(key[pygame.K_RIGHT]):
        turn -= 1

    
    #Saves an image of the track
    if(key[pygame.K_b]):
        race_track.set_at((0,0),(origin[0],origin[1],0,255))
        screen.blit(race_track,(0,0))  # Blit portion of the display to the image
        pygame.image.save(screen,"raceTrack.png")
   
    reset = False
    if(aCar.pos > (0,0) and aCar.pos < SCREEN_SIZE):
        rewards = rewardPoints(roadCenter, rad = 50)
        for i in range(len(rewards)): #used to track the current reward point
            if(current_point == i):
                pygame.draw.circle(race_track, (155,115,255),rewards[i],3)
            else:
                pygame.draw.circle(race_track, (255,215,0),rewards[i],5)

        current_point = rewardLocation(roadCenter, aCar.carPosition(), current_point)
        # print(current_point, end = "  ")
        # print(rewardCalc(roadCenter, aCar.carPosition(), current_point))
        # print("track length: ", calcTrackLength(roadCenter, len(roadCenter)), end = "   ")
        # print(f"Completed Track point: {current_point + 1}   driven: {calcTrackLength(roadCenter, current_point)}", )
        if(race_track.get_at(aCar.carPosition()) == GRASS_COLOR):
            print("crash")
            reset = True
            
        elif(race_track.get_at(aCar.carPosition()) == FINISHLINE_COLOR):
            print("You've won")
            reset = True
            
        if(reset == True):
            aCar.pos = origin
            current_point = 0
            aCar.speed = 0
            aCar.angle = 0
            sleep(0.2)

    screen.blit(race_track, (0,0))
    aCar.move(forward, turn)
    if((aCar.pos[0] <= 800 and aCar.pos[0] >= 0) and (aCar.pos[1] <= 500, aCar.pos[1] >= 0)):
        
        list_ = aCar.cast_ray_color(GRASS_COLOR, FINISHLINE_COLOR)
        aCar.draw()
        
    pygame.display.flip()

    clock.tick(50)
