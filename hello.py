import cityflow
import gym


eng = cityflow.Engine("./config/rl_config.json")

eng.reset()
for i in range(75):
    eng.next_step()

