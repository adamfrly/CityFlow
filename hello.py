import cityflow
import gym
from gym import spaces
import cityflowenv 
import numpy as np


env = gym.make('OneIntersection-v0', config_file="config/rl_config.json")
env.reset()
is_done = False
for i in range(5):
    while not is_done:
        action = env.action_space.sample()
        state, reward, is_done, _ = env.step(action)
