import gym
from gym import spaces
import cv2
import pygame
import numpy as np
from time import sleep
from random import choice
from Car import Car
from Rewards import rewardLocation, rewardCalc, calcTrackLength


fileName = "tracks//raceTrack1.png"
img = cv2.imread(fileName)

with open("tracks//raceTrack1.txt",'r') as file:
  fileOut = list(file)

#Completed in two to make it easier
#To convert string back to list of tuples of (x,y)
fileOut = list(map(lambda x: tuple(x[:-1].split()), fileOut))
fileOut = list(map(lambda x: tuple(map(lambda y: int(y), x)), fileOut)) #tuple of string to tuple of int

origin = fileOut[0]
rewards = fileOut
trackLength = calcTrackLength(rewards, len(rewards))


GRASS_COLOR = (20,183,43)
ROAD_COLOR = (75,75,75)
FINISHLINE_COLOR = (20,0,200)
START_COLOR = (0,0,0)


# screen = pygame.display.set_mode((800,500))
# raceTrack = pygame.image.load(fileName)
# screen.blit(raceTrack, (0,0))
# pygame.display.flip()


class raceEnv(gym.Env):

  def __init__(self):
    self.action_space = spaces.Discrete(3) # forward, brake, left, right
    self.aCar = Car(img, MAXSPEED = 200)
    self.aCar.pos = origin
    self.prev_state = 0
    self.current_point = 0
    self.reward = 0
    self.render_mode = None
    # [0,6] = distance of rays
    # [7] = angle
    # [8] = speed
    self.observation_space = spaces.Box(low=0, high=1, shape=(9,), dtype=np.float32)

  def step(self, action):
    
    self.observation = []
    
    curr_state = 0
    forward = 0
    turn = 0
    
    #action == 0 
      #0-> forward and turn
    if(action == 0): #forward
        forward = 1
    # if(action == 1): #stop
    #     forward -= 1
    if(action == 1): #right
      turn += 1
    if(action == 2): #left
        turn -= 1
    
    self.aCar.move(forward,turn, accel = 2, deccel = 5)
    self.observation = []
    raysDist = self.aCar.ray_dist(GRASS_COLOR, FINISHLINE_COLOR)

    self.observation.extend(raysDist)
    self.observation.append(self.aCar.angle)
    self.observation.append((self.aCar.speed / self.aCar.MAXSPEED))

    self.observation = np.array(self.observation)
    

    self.current_point = rewardLocation(rewards, self.aCar.carPosition(), self.current_point)
    curr_state = rewardCalc(rewards, self.aCar.carPosition(), self.current_point, calcTrackLength(rewards, len(rewards)))

    if(curr_state > self.prev_state):
      self.reward += 3
    elif(curr_state == self.prev_state):
      self.reward += -1
    else:
      self.reward += -2

    if(self.reward <= -300):
      self.done = True

    print(self.aCar.carPosition(),  " ", action, " ", self.reward)
    self.prev_state = curr_state

    rgb = tuple(img.transpose(1,0,2)[self.aCar.carPosition()[0], self.aCar.carPosition()[1]])
    if(rgb[::-1] == GRASS_COLOR):
      self.done = True
      self.reward -= 10
    elif(rgb[::-1] == FINISHLINE_COLOR):
      self.done = True
      self.reward += 10

    self.info = {}

    if self.render_mode == 'human':
      self.render()

    return self.observation, self.reward, self.done, self.info
  
  def reset(self):  
    print("reset")
    self.aCar.pos = choice(rewards)
    self.aCar.speed = 0
    self.aCar.angle = 0
    self.done = False
    self.reward = 0
    self.current_point = 0
  
    self.observation = []

    raysDist = self.aCar.ray_dist(GRASS_COLOR, FINISHLINE_COLOR)
    self.observation.extend(raysDist)
    self.observation.append(self.aCar.angle)
    self.observation.append((self.aCar.speed / self.aCar.MAXSPEED))

    if (self.render_mode == 'human'):
      pygame.init()
      self.screen = pygame.display.set_mode((800,500))
      self.raceTrack = pygame.image.load(fileName)
      self.clock = pygame.time.Clock()
      pygame.display.flip()

      self.render(self.render_mode)

    return self.observation  # reward, done, info can't be included

  def render(self, mode='human'):

    self.screen.blit(self.raceTrack, (0,0))

    raysPoints = self.aCar.cast_ray_points(GRASS_COLOR, FINISHLINE_COLOR)
    for ray in raysPoints:
        pygame.draw.circle(self.screen, (200,200,0),ray, 2)
        pygame.draw.line(self.screen, (200,200,0), self.aCar.pos, ray,width = 1)
    
    pygame.draw.circle(self.screen, (255,0,0),self.aCar.pos, 5)
    pygame.draw.line(self.screen, (255,0,0), self.aCar.pos, self.aCar.forwardArrow(),width = 2)
    # for re in rewards:
    #     pygame.draw.circle(self.screen, (200,200,0),re, 2)

    pygame.display.update()
    #self.clock.tick(50)

  def close (self):
    pygame.quit()

if __name__ == "__main__":
  env = raceEnv()
  episodes = 1

  for episode in range(1, episodes + 1):
      state = env.reset()
      done = False
      while not done:
        env.render()
        #print(env.reward)
        n_state, reward, done, info = env.step(0)
        
      print(f"episode {episode}, reward: {reward}")