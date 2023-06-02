import cityflow
import gymnasium as gym
from gymnasium import spaces
import cityflowenv 
import numpy as np


env = gym.make('OneIntersection-v0', config_file="config/rl_config.json")
env.reset()
is_done = False
while not is_done:
    action = env.action_space.sample()
    state, reward, is_done, truncated, info = env.step(action)
