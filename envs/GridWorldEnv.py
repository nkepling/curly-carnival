import gymnasium as gym
from gymnasium import spaces
import numpy as np




class GridWorldWithWalls(gym.Env):
    """
    Custom gridworld environment
    An agent starst at some location then ends at the target destination
    """
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self,render_mode=None, size=5):
        """
        Init: 
        actions we can take
        observation space
        initialize the space
    
        """
        self.size = size
        self.winsdow_size = 512 


        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
            }
        )  

        self.action_space = spaces.Discrete(4) # up, down, left right

        # 0: right, 1: up , 2: left, 3: right 
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }


    def step(self,action):
        """
        Defines what we do whenever we take a step
        Defines how we treat actions. 
        """
        direction = self._action_to_direction[action]

        # self._agent_location = self.
    def render(self):
        """
        See pygame
        """
        pass

    def reset(self):
        """
        Where we reset the environment after each training run/episode
        """
        pass

    def close(self):
        pass








