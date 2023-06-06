import gymnasium as gym
from gymnasium import spaces, logger
import cityflow
import numpy as np


# TODO Write function to convert roadnet file specified in config to a state space and to determine legal action space
# State space will be one element for each lane in the intersection and its magnitude will be the number of cars in that lane.
# Action space will be binary vector whose length is the number of traffic lights (i.e. number of lanes)

class CityFlow1IntEnv(gym.Env):

    metadata = {'render_modes':['human']}
    def __init__(self, config_file=None, render_mode=None):
        super().__init__()
        self.config_file = config_file

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.steps_per_episode = 3000
        self.current_step = 0
        self.is_done = False
        self.reward_range = (0, np.inf)

        low = np.array([0] * 56, dtype=np.float32)
        high = np.array([np.finfo(np.float32).max] * 56, dtype=np.float32)

        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32) # 7 Lane, 4 Directions to come from, 1 Entry, 1 Exit from the intersection, each in [0, inf)
        
        self.intersection_id = "intersection_1_1"

        self.cityflow = cityflow.Engine(self.config_file)


    def _get_obs(self):
        lane_vehicles_dict = self.cityflow.get_lane_vehicle_count()
        waiting_vechiles_dict = self.cityflow.get_lane_waiting_vehicle_count()
        total_vehicles_dict = {k: lane_vehicles_dict.get(k, 0) + waiting_vechiles_dict.get(k, 0) for k in set(lane_vehicles_dict)|set(waiting_vechiles_dict)}

        obs = np.array(list(total_vehicles_dict.values()), dtype=np.float32)
        return obs
        

    def _get_info(self):
        return {"foo": "bar"} #TODO Add statuses of each traffic light and how many cars each light has let through
             # Brainstorm more info that could be useful (typically stuff that's the agent isn't allowed to see related to rewards)

    def _get_reward(self):
        # Multiple potential reward signals: 
        # 1. The total number of vehicles in the intersection 
        # 2. The average velocity of the vehichles in the interesection
        # 3. Average waiting time of all vehicles at the intersection
        return self.cityflow.get_average_travel_time()

    def reset(self, seed=None, **options):
        self.cityflow.reset()

        self.is_done = False
        self.current_step = 0
        
        obs = self._get_obs()
        info = self._get_info()

        return obs, info
    
    def render(self):
        if self.render_mode == "human":
            print("Current time: " + str(self.cityflow.get_current_time()))
    
    def step(self, action):
        assert self.action_space.contains(action), f"Invalid action {action}, {type(action)}"

        self.cityflow.set_tl_phase(self.intersection_id, action)
        self.cityflow.next_step()

        state = self._get_obs()
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
        
        if self.render_mode == "human":
            self.render()

        return state, reward, self.is_done, False, info # False is for truncation which is never possible in this env by design
    