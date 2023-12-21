from stable_baselines3 import DQN
from raceEnv import raceEnv
from random import randint
import time
import cv2
from Car import Car
from Rewards import rewardLocation, rewardCalc, calcTrackLength, angles


fileNum = 4
fileName = f"tracks//raceTrack{fileNum}.png"
img2 = cv2.imread(fileName)

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



env = raceEnv()
env.aCar = Car(img2, MAXSPEED = 200)
env.fileName = fileName
model = DQN.load("DQNr1")
env.render_mode = "human"


while True:
    state = env.reset()
    done = False
    while not done:
        time.sleep(0.0001)
        action, _ = model.predict(state)
        state, reward, done, info = env.step(action)