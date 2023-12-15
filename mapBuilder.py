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
# car_cords = (-100,-100)
# origin = (-100,-100)
clock = pygame.time.Clock()

# inc = 1

# aCar = Car(screen)

# n = 0
roadCenter = []
trackDist = 50
# current_point = 0
space = 0
while running:  
    # forward = 0
    # turn = 0
    # status = []
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
    if(key[pygame.K_SPACE]): #update this so that the reward dots appear when you press space
        space = 2
    
    if(space == 1 ):
        points = rewardPoints(roadCenter, rad = trackDist)
        for point in points:
            pygame.draw.circle(screen, ROAD_COLOR,point,int(rad * 0.25))
        if (not(origin == None)):
            pygame.draw.circle(screen, START_COLOR, origin,int(rad * 0.25))
        space -= 1
        
    if(len(roadCenter) >= 1 and space == 2):
        points = rewardPoints(roadCenter, rad = trackDist)
        for point in points:
            pygame.draw.circle(screen, (255,215,0),point,int(rad * 0.25))
        if (not(origin == None)):
            pygame.draw.circle(screen, (255,100,100), origin,int(rad * 0.25))
        space -= 1
    
    # if(key[pygame.K_q]):#adds/ resets car
    #     aCar.pos = origin
    #Moves car
    # if(key[pygame.K_UP]):
    #     forward = 1
    # if(key[pygame.K_DOWN]):
    #         forward -= 1
    # if(key[pygame.K_LEFT]):
    #     turn += 1
    # if(key[pygame.K_RIGHT]):
    #     turn -= 1

    
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

            for tups in pList:
                file.write(str(tups[0]) + " " + str(tups[1]) + "\n")


        sleep(1)
   #############
    # write the start and reward points on a text file
   #############
    # reset = False
    # if(aCar.pos > (0,0) and aCar.pos < SCREEN_SIZE):
    #     rewards = rewardPoints(roadCenter, rad = 50)
    #     for i in range(len(rewards)): #used to track the current reward point
    #         if(current_point == i):
    #             pygame.draw.circle(race_track, (155,115,255),rewards[i],3)
    #         else:
    #             pygame.draw.circle(race_track, (255,215,0),rewards[i],5)

    #     current_point = rewardLocation(roadCenter, aCar.carPosition(), current_point)
    #     per = rewardCalc(roadCenter, aCar.carPosition(), current_point, calcTrackLength(roadCenter, len(roadCenter)))
        
        
        # if(race_track.get_at(aCar.carPosition()) == GRASS_COLOR):
        #     print("crash")
        #     reset = True
            
        # elif(race_track.get_at(aCar.carPosition()) == FINISHLINE_COLOR):
        #     print("You've won")
        #     reset = True
            
        # if(reset == True):
        #     aCar.pos = origin
        #     current_point = 0
        #     aCar.speed = 0
        #     aCar.angle = 0
        #     sleep(0.2)
        

    #screen.blit(screen, (0,0))
    # aCar.move(forward, turn)
    # if((aCar.pos[0] <= 800 and aCar.pos[0] >= 0) and (aCar.pos[1] <= 500, aCar.pos[1] >= 0)):
        
    #     list_ = aCar.cast_ray_color(GRASS_COLOR, FINISHLINE_COLOR)
    #     aCar.draw()
    #     #[rewards, angle, speed, [distances]]
    #     status.append(per)
    #     status.append(aCar.angle / 360)
    #     status.append(aCar.speed / aCar.MAXSPEED)
    #     status.extend(list_)
    #     print(status)
    pygame.display.update()

    #pygame.display.flip()

    #clock.tick(50)



