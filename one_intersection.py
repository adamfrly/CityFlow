import cityflow
import gymnasium as gym
from gymnasium import spaces
import cityflowenv 
import numpy as np
import stable_baselines3 as sb
import os

env = gym.make('OneIntersection-v0', config_file="config/rl_config.json")

model_path = "ppo_traffic_policy_300k"

if not os.path.exists(model_path + ".zip"):
    model = sb.PPO(
        "MlpPolicy",
        env,
        verbose=1,
        n_steps=1500,
        batch_size=30
    )
    model.learn(total_timesteps=300000)
    model.save(model_path)
else:
    model = sb.PPO.load(model_path)

obs, _ = env.reset()
is_done = False
while not is_done:
    action, _states = model.predict(obs)
    obs, reward, is_done, truncated, info = env.step(action)
