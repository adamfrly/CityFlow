import cityflow
import gym
from gym import spaces
import cityflowenv 
import numpy as np
import stable_baselines3 as sb
from stable_baselines3.common.env_checker import check_env

env = gym.make('OneIntersection-v0', config_file="config/rl_config.json")
print(env.observation_space.sample())

check_env(env)

print(spaces.MultiDiscrete([1] * 56).sample().shape)
print(spaces.Tuple([spaces.Box(low=0, high=np.inf)] * 56).sample())