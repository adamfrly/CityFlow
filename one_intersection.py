import cityflow
import gym
from gym import spaces
import cityflowenv 
import numpy as np
import stable_baselines3 as sb

env = gym.make('OneIntersection-v0', config_file="config/rl_config.json")

model = sb.PPO(
    "MlpPolicy",
    env,
    verbose=1,
    n_steps=1500,
    batch_size=30
)
model.learn(total_timesteps=30000)
model.save("ppo_traffic_policy")

obs = env.reset()
is_done = False
while not is_done:
    action = env.action_space.sample() # model.predict(obs)
    obs, reward, is_done, truncated, info = env.step(action)
