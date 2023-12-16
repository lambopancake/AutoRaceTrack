import os
from stable_baselines3 import PPO
from raceEnv import raceEnv


Log_path = os.path.join("Training", "Logs")
PPO_path = os.path.join("Training", "Models")


raceEnv = raceEnv()

model = PPO("MlpPolicy",raceEnv, verbose = 1, tensorboard_log = Log_path)

raceEnv.render_mode = "human"
model.learn(total_timesteps = 2000000)
