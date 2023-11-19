import gymnasium as gym
import numpy as np 
from gymnasium import spaces
import networkx as nx
from dataclasses import dataclass

# TODO: Function to randomly spawn agent/Maybe the agent always starts in a corner of a room.... 
# TODO: Function to spawn target obejects in rooms that make sense given the object type. 
# TODO: Walls not only to deliniate rooms and hallways but also an outer wall. 
# TODO: Should this be modeled as a POMDP?????
# TODO: Fix the dictionary uses... it fucks with deepcopy for MCTS
# NOTE: There maybe some FIXME spread about

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
    ],
    "14x14" : [
        "WWWWWWWWWWWWWW",
        "W----W--W----W",
        "W------------W",
        "W------------W",
        "W----W--W----W",
        "WW--WW--WW--WW",
        "W------------W",
        "W------------W",
        "WW--WW--WW--WW",
        "W----W--W----W",
        "W------------W",
        "W------------W",
        "W----W--W----W",
        "WWWWWWWWWWWWWW",
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
    loc : tuple
    item: str
    roomtype: str
    neighbors: list 

def make_graph(map_name):
    #floorplan = np.asarray(MAPS[map_name],dtype='c')
    floorplan = np.array([list(i) for i in MAPS[map_name]])

    row,col = floorplan.shape
    
    for i in range(row):
        for j in range(col):
            cell = Cell
            cell.loc = (i,j)
            if floorplan[i,j] == b"W": 
                cell.roomtype = "wall"
            else: 
                cell.roomtype = "empty" #TODO  Figure out how to assign other roomtypes here

                # TODO: Add a function that adds items to each cell.


class WalledGridworld(gym.Env):
    """
    This is a custom environment for a mulitobject detection 

    The environment creates a gridworld environment according with walls according to an input map configuration.

    The gridworld meant to represent someapartment layout where each cell in the grid world is a Cell object. (See Cell class for details)
    Each cell will have location i.e (x,y) coordinates, item, roomtype, and a neighor attribute. 

    The goal of the agent in this environement is to find all multiple objects within the apartment. 
    We can assume that the agent can precieve the items of the cell that it is in and what is directly adjacent to it.

    Should this be modeled as a POMDP?????

    
    ## Action space

    - 0: Move left
    - 1: Move down
    - 2: Move right
    - 3: Move up

    ## Rewards

    ## Episode end
    The episode ends if the followiing happens:

    - Termination:
        1. The agent moves into a wall.
        2. The agent collects all the objects. 
    
    """
    
    def __init__(self,size: int,target_objects: list,map_name="12x12") -> None:

        """
        int size: side length of square grid
        list target_objects: list of obejects that the agent needs to retrieve. 
        """
        super().__init__()

        self.size = size #The size of the square gridworld
        self.G = None # Maybe I'll add a netorkx graph here to make my life easier. 

        ## I am going to hard code in walls ... 

        self.floorplan =floorplan = np.array([list(i) for i in MAPS[map_name]])
        # print(floorplan)


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

        #NOTE: Change to a numpy array. Dictionaries are slow for deepcopy ...
        # self._action_to_direction = {
        #     0: np.array([1, 0]),
        #     1: np.array([0, 1]),
        #     2: np.array([-1, 0]),
        #     3: np.array([0, -1]),
        # }

        self._action_to_direction = np.array([[1,0],
                                              [0,1],
                                              [-1,0],
                                              [0,-1]])

        # 
        
        self.target_objects = target_objects
        self.objects_collected = 0  #Have all objects been collected?


    def reset(self,seed=None,options=None):

        """
        Set the initial agent location
        Set the target locations s.t they are not ontop of each other.
            TODO: Have it so that the 
        
        list target_objects : a list of target objects [1,2,3,4], they could corresnd to actual household items [dishwahser...]
        """
        self._agent_location = np.array((1,1)) #(0,0) would be a wall

        # FIXME: Can you use np.where or something here????
        valid_locs = []
        for i in range(self.size):
            for j in range(self.size):

                if self.desc[i][j] == "-" and [i,j]!=[1,1]:
                    valid_locs.append([i,j])
        
        valid_locs = np.array(valid_locs)
        inds = np.random.choice(range(len(valid_locs)),len(self.target_objects),replace = False)
        self._target_locations = list(valid_locs[inds,:])

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

        #Set target locations.... 


    def step(self,action):
        """
        Step in a direction, terminal if we find the object. 
        I am going to define a collion wiht negtive rewarard and as a termnial state/
        The other terminating condition is that all rewards are found. 

        INPUTS:

        action 

        OUTPUTS:

        reward
        terminated
        observation
        truncated 
        info

        """
        direction = self._action_to_direction[action,:] #FIXME 

        self._agent_location = self._agent_location + direction #We don't have to worry about leaving the gird becasue the outside walls are terminal states.
        
        if self.desc == "W":
            reward = -1
            terminated = True

        else: #TODO: Fix this because its a a dumb way to do this .. 
            for ind , loc in self._agent_location:
                if all(self._agent_location == loc):
                    reward = 1 
                    self._agent_location.pop(ind)
                    self.objects_collected+=1
                    break 

            
        if self.objects_collected == len(self.target_objects):
            reward+=1 # You get an additional rewards for finding all the objects
            terminated = True

        observation = self._get_obs()
        info = self._get_info(0)
        truncated = False
        return observation,reward,terminated,truncated,info

    
    def _get_info(self):
        """
        Return: A dictionary with distances between agent and location


        TODO: add a k,v term for precieved items in gridworld... 
        """
        return {

            "distances" : [np.linalg.norm(self._agent_location - t,ord=1) for t in self._target_locations ]
        }

    def _get_obs(self):
        """
        We want to return a dictionalry of observation space

        How do you decide what the observation space should be?
        """
        return {"agent":self._agent_location,"targets": self._target_location}
    

        






 


if __name__ == "__main__":
    e = WalledGridworld(14,"14x14")
    e.reset([1,2,3,4])
    print(e.target_locations)




