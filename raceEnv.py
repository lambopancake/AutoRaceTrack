import gym
from gym import spaces
import cv2
import pygame
import numpy as np
from time import sleep
from random import choice, randint
from Car import Car
from Rewards import rewardLocation, rewardCalc, calcTrackLength, angles

fileNum = 3
fileName = f"tracks//raceTrack{fileNum}.png"
img = cv2.imread(fileName)

with open(f"tracks//raceTrack{fileNum}.txt",'r') as file:
  fileOut = list(file)

#Completed in two to make it easier
#To convert string back to list of tuples of (x,y)
fileOut = list(map(lambda x: tuple(x[:-1].split()), fileOut))
fileOut = list(map(lambda x: tuple(map(lambda y: int(y), x)), fileOut)) #tuple of string to tuple of int


origin = fileOut[0]
rewards = fileOut
trackLength = calcTrackLength(rewards, 0, len(rewards))
angles = angles(rewards)


GRASS_COLOR = (20,183,43)
ROAD_COLOR = (75,75,75)
FINISHLINE_COLOR = (20,0,200)
START_COLOR = (0,0,0)

class raceEnv(gym.Env):

  def __init__(self):
    self.action_space = spaces.Discrete(3) # forward, brake, left, right
    self.aCar = Car(img, MAXSPEED = 200)
    self.aCar.pos = origin
    self.prev_state = 0
    self.current_point = 0
    self.reward = 0
    self.render_mode = None
    self.start = randint(0,len(angles) - 1 )
    self.fileName = fileName

    # self.screen = pygame.display.set_mode((800,500))
    # self.raceTrack = pygame.image.load(fileName)
    # self.clock = pygame.time.Clock()

    # [0,6] = distance of rays
    # [7] = angle
    # [8] = speed
    self.observation_space = spaces.Box(low=0, high=1, shape=(9,), dtype=np.float32)
    self.reward_range = (-10,10)

  def step(self, action):
    
    self.observation = []
    
    curr_state = 0
    forward = 0
    turn = 0
    
    #action == 0 
      #0-> forward and turn
    if(action == 0): #forward
        forward = 1
    
    if(action == 1): #right
      turn += 1
    if(action == 2): #left
        turn -= 1
    # if(action == 3): #stop
    #     forward -= 1
    
    self.aCar.move(forward,turn)
    #elf.observation = []
    #raysDist = self.aCar.ray_dist(GRASS_COLOR, FINISHLINE_COLOR)
    self.observation = self.aCar.ray_dist(GRASS_COLOR, FINISHLINE_COLOR)
    #self.observation.extend(raysDist)
    self.observation.append(self.aCar.angle)
    self.observation.append((self.aCar.speed / self.aCar.MAXSPEED))

    self.observation = np.array(self.observation)
    

    self.current_point = rewardLocation(rewards, self.aCar.carPosition(), self.current_point)
    curr_state = rewardCalc(rewards, self.aCar.carPosition(), self.current_point, calcTrackLength(rewards, self.start, len(rewards)), self.start)

    
    reward_a = 0
    
    if(max(self.observation) == self.observation[3]):
      print("here")
      reward_a = 2
    
    reward_b = 0
    if(curr_state > self.prev_state):
        reward_b = 5
    elif(curr_state == self.prev_state):
        reward_b += -2
    else:
        reward_b += -7

    self.reward = reward_a + reward_b 
    if(self.reward <= -10):
      self.done = True
    # print(raysDist, end = "   ")
    # max_ = max(raysDist)
    # print(max_, " ", raysDist.index(max_))

    #print(self.aCar.carPosition(),  " ", action, " ", self.reward)
    self.prev_state = curr_state

    rgb = tuple(img.transpose(1,0,2)[self.aCar.carPosition()[0], self.aCar.carPosition()[1]])
    if(rgb[::-1] == GRASS_COLOR):
      self.done = True
      self.reward = -10
    elif(rgb[::-1] == FINISHLINE_COLOR):
      self.done = True
      self.reward = 10

    self.info = {}

    if self.render_mode == 'human':
      self.render()
    print(self.reward)
    return self.observation, self.reward, self.done, self.info
  
  def reset(self):  
    print("reset")
    print(self.reward)
    self.start = randint(0,len(angles) - 1 )
    self.aCar.pos = rewards[self.start]
    self.aCar.speed = 0
    self.aCar.angle = angles[self.start]
    self.done = False
    self.reward = 0
    self.current_point = self.start
  
    #self.observation = []
    self.observation = self.aCar.ray_dist(GRASS_COLOR, FINISHLINE_COLOR)
    #raysDist = self.aCar.ray_dist(GRASS_COLOR, FINISHLINE_COLOR)
    #self.observation.extend(raysDist)
    self.observation.append(self.aCar.angle)
    self.observation.append((self.aCar.speed / self.aCar.MAXSPEED))

    if (self.render_mode == 'human'):
      pygame.init()
      self.screen = pygame.display.set_mode((800,500))
      self.raceTrack = pygame.image.load(self.fileName)
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
    self.clock.tick()

  def close (self):
    pygame.quit()

# if __name__ == "__main__":
#   env = raceEnv()
#   episodes = 10

#   for episode in range(1, episodes + 1):
#       state = env.reset()
#       done = False
#       while not done:
#         env.render()
#         n_state, reward, done, info = env.step(0)
        
#       print(f"episode {episode}, reward: {reward}")