import pygame
import sys
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

while running:  

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
    if(key[pygame.K_d]):#deletes track
        pygame.draw.circle(race_track, GRASS_COLOR,pos,rad)
    if(key[pygame.K_s]):#start line squre
        pygame.draw.rect(race_track,START_COLOR,[pos[0]-25,pos[1]-25,50,50], 30)
        origin = pos
    if(key[pygame.K_e]):#end Line
        pygame.draw.rect(race_track,FINISHLINE_COLOR,[pos[0]-25,pos[1]-25,50,50], 30)
    if(key[pygame.K_q]):#adds car
        car_cords = origin
    #Moves car
    if(key[pygame.K_LEFT]):
        car_cords = (car_cords[0] - inc,car_cords[1])
    if(key[pygame.K_RIGHT]):
        car_cords = (car_cords[0] + inc,car_cords[1])
    if(key[pygame.K_UP]):
        car_cords = (car_cords[0] ,car_cords[1] - inc)
    if(key[pygame.K_DOWN]):
        car_cords = (car_cords[0] ,car_cords[1] + inc)
    
    #Saves an image of the track
    if(key[pygame.K_b]):
        race_track.set_at((0,0),(origin[0],origin[1],0))
        screen.blit(race_track,(0,0))  # Blit portion of the display to the image
        pygame.image.save(screen,"raceTrack.png")

    reset = False
    if(car_cords > (0,0) and car_cords < SCREEN_SIZE):
        if(race_track.get_at(car_cords) == GRASS_COLOR):
            print("crash")
            reset = True
        elif(race_track.get_at(car_cords) == FINISHLINE_COLOR):
            print("You've won")
            reset = True
        if(reset == True):
            car_cords = origin

   
    screen.blit(race_track, (0,0))
    pygame.draw.circle(screen, CAR_COLOR,car_cords,rad - 20)
    pygame.display.flip()

    clock.tick(60)