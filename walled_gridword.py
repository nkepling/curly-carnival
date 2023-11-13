import gymnasium as gym
import numpy as np 
from gymnasium import spaces
import networkx as nx
from dataclasses import dataclass



MAPS = {
    "12x12" : [
        "----W--W----",
        "------------",
        "------------",
        "----W--W----",
        "W--WW--WW--W",
        "------------",
        "------------",
        "W--WW--WW--W",
        "----W--W----",
        "------------",
        "------------",
        "----W--W----"
    ]

}

@dataclass
class Cell:
    """
    A cell in the grid word. TBH idk if this is necessary yet.
    Has one atribute. The item it holds 

    item: a household item (fork, washing machine etc)
    rootype: (kitchen,bathroom,wall)

    """
    item: str
    roomtype: str





class WalledGridworld(gym.Env):
    
    def __init__(self,size,map_name="12x12") -> None:
        super().__init__()

        self.size = size #The size of the square gridworld
        self.G = None

        ## I am going to hard code in walls ... 

        desc = MAPS[map_name]


        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
            }
        )

        self.action_space = spaces.Discrete(4)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }


    def step(self,action):
        """
        Step in a direction, terminal if we find the object. 

        For right now I am just going to let the agent 
        """
        pass

    def reset(self,seed=None,options=None):
        pass

    
    def _get_info(self):
        pass

 







