import cityflow
import gym
import cityflowenv 
import numpy as np


env = gym.make('gym_envs.cityflowenvs.envs:cityflow1intenv')
env.reset()
for i in range(75):
    env.next_step()
    while not is_done:
        action = np.random.randint(low=0, high=9)
        state, reward, is_done, _ = env.step(action)
