import gym
from gym import spaces, logger
import cityflow
import numpy as np
import os

# TODO Write function to convert roadnet file specified in config to a state space and to determine legal action space
# State space will be one element for each lane in the intersection and its magnitude will be the number of cars in that lane.
# Action space will be binary vector whose length is the number of traffic lights (i.e. number of lanes)

class CityFlowEnv(gym.Env):

    metadata = {'render.modes':['human']}
    def __init__(self, config_file=None, render_mode=None):
        super().__init__()
        self.config_file = config_file

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.steps_per_episode = 1500
        self.current_step = 0
        self.is_done = False
        self.reward_range = (-float('inf'), float('inf'))

        self.cityflow = cityflow.Engine(self.config_file)

    def _get_obs(self):
        pass #TODO Add observation of the state (i.e. cars in each lane of the intersection and the traffic lights)

    def _get_info(self):
        pass #TODO Add statuses of each traffic light and how many cars each light has let through
             # Brainstorm more info that could be useful (typically stuff that's the agent isn't allowed to see related to rewards)

    def _get_reward(self):
        pass #TODO Implement this

    def _get_state(self):
        pass #TODO Implement this

    def reset(self, seed=None):
        super.reset(seed=seed)
        self.cityflow.reset()

        self.is_done = False
        self.current_step = 0
        
        observation = self._get_obs()
        info = self._get_info()

        return observation, info
    
    def render(self, mode='human'):
        print("Current time: " + self.cityflow.get_current_time())
    
    def step(self, action):
        assert self.action_space.contains(action), f"Invalid action {action}, {type(action)}"

        self.cityflow.set_tl_phase(self.intersection_id, action)
        self.cityflow.next_step()

        state = self._get_state()
        reward = self._get_reward()
        info = self._get_info()

        self.current_step = self.current_step + 1

        if self.is_done:
            logger.warn("You are calling 'step()' even though this environment has already returned done = True. "
                        "You should always call 'reset()' once you receive 'done = True' "
                        "-- any further steps are undefined behavior.")
            reward = 0.0

        if self.current_step + 1 == self.steps_per_episode:
            self.is_done = True

        return state, reward, self.is_done, info
    