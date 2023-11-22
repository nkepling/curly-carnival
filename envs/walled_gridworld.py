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
class Item:
    """
    Item class 

    """
    name: str
    found: bool = False 



class Cell:
    """
    A cell in the grid word. TBH idk if this is necessary yet.
    Has one atribute. The item it holds 

    item: a household item (fork, washing machine etc)
    rootype: (kitchen,bathroom,wall)

    """
    item: Item = Item("empty")
    roomtype: str = "None"
    




def make_graph(map_name):
    #floorplan = np.asarray(MAPS[map_name],dtype='c')
    floorplan = np.array([list(i) for i in MAPS[map_name]])

    row,col = floorplan.shape
    
    for i in range(row):
        for j in range(col):
            cell = Cell
            cell.loc = (i,j)
            if floorplan[i,j] == "W": 
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

    -1 if agent goes into a wall
    +1 if agent collects an object
    +1 if agent collects all the objects
    0 otherwise

    ## Episode end
    The episode ends if the followiing happens:

    - Termination:
        1. The agent moves into a wall.
        2. The agent collects all the objects. 
    
    """
    
    def __init__(self,size: int,target_objects: list,map_name,render_mode=False) -> None:

        """
        int size: side length of square grid
        list target_objects: list of obejects that the agent needs to retrieve. 
        """
        super().__init__()

        self.size = size #The size of the square gridworld
        self.G = None # Maybe I'll add a netorkx graph here to make my life easier. 

        self.floorplan =floorplan = np.array([list(i) for i in MAPS[map_name]])
        r = np.zeros((size,size))
        self.r = r
        
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "targets": spaces.Box(0, size - 1, shape=(2,len(target_objects)), dtype=int),
            }
        )

        self.action_space = spaces.Discrete(4)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        # up, right , down, left
        self._action_to_direction = np.array([[1,0],
                                              [0,1],
                                              [-1,0],
                                              [0,-1]])

        self.target_objects = target_objects # list of item names as strings
        self.item_lookup = {k+1:v for k,v in enumerate(target_objects)} # NOTE: It may be better to use a list here b/c we need to deep copy in MCTS... 
        self.objects_collected = {k:False for k,v in zip(self.item_lookup.keys(),self.item_lookup.keys())}
        self.item_lookup[len(target_objects) + 1] = "W"
        self.item_lookup[0] = "empty"
        self.item_map = np.zeros((size,size))
        # self.item_lookup = [target_objects + "W"]
        # self.objects_collected = 0  #Have all objects been collected?
        self.render_mode = render_mode


    def reset(self,seed=None,options=None):

        """
        Set the initial agent location
        Set the target locations s.t they are not ontop of each other.
            TODO: Have it so that the 
        
        list target_objects : a list of target objects [1,2,3,4], they could corresnd to actual household items [dishwahser...]
        """
        self._agent_location = np.array((1,1)) #(0,0) would be a wall

        #### RANDOMLY DISTRIBUTE OBJECTS IN MAP #########
        # FIXME: Can you use np.where or something here????
        valid_locs = []
        for i in range(self.size):
            for j in range(self.size):
                if self.floorplan[i,j] == "-" and [i,j]!=[1,1]:
                    valid_locs.append([i,j])
        
        valid_locs = np.array(valid_locs)
        inds = np.random.choice(range(len(valid_locs)),len(self.target_objects),replace = False)
        self._target_locations = valid_locs[inds,:]
 
        ##### SET REWARDS MATRIX and ITEM MAP ##########
        for ind,loc in enumerate(self._target_locations): 
            self.r[loc[0],loc[1]] = 1
            self.item_map[loc[0],loc[1]] = ind + 1 # We can then look up the item type now 

        for i in range(self.size):
            for j in range(self.size):
                if self.floorplan[i,j] == "W":
                    self.item_map[i,j] = len(self.target_objects) + 1
        ##### SET ITEM MAP ##############
        
        # # self.item_map = [[] for i in range(self.size)]
        # self.item_map = [[0 for _ in range(self.size)] for _ in range(self.size)]
        # items = self.target_objects

        # for i in range(self.size):
        #     for j in range(self.size):
        #         if self.r[i,j] == 1:
        #             item = items.pop()
        #             self.item_map[i][j] = Item(item)
        #         elif self.floorplan[i,j] == "W": 
        #             self.item_map[i][j]= Item("wall")
        #         else:
        #             self.item_map[i][j] = Item("empty")
        #print(self.r)
        # print(self.item_map)

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == True:
            self._simple_render()

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
        direction = self._action_to_direction[action,:] 

        x,y=self._agent_location = np.clip(
            self._agent_location + direction, 0, self.size - 1
        )
        # x,y = self._agent_location = self._agent_location + direction
        
        item_in_cell = self.item_lookup[self.item_map[x,y]]

        # if self.item_map[x,y] == len(self.target_objects) + 1:
        #     terminated = True 
        if item_in_cell == "W": 
            terminated = True
            reward = 0 
        else: 
            terminated = False
            reward = 0
    

        ########################################################################
        # Give a reward for reaching a cell with an object for the first time. #
        ########################################################################

        if 0 < self.item_map[x,y] <= len(self.target_objects):
            if not self.objects_collected[self.item_map[x,y]]:
                # reward = 10 ** (sum(self.objects_collected.values())+1) 
                reward = 100
                # terminated = True
                # reward = 100
                self.objects_collected[self.item_map[x,y]]  = True

        #################################################################################################
        # Give a really big reward for collecting all the objects. This is also the terminal state.... ##
        #################################################################################################

        if sum(self.objects_collected.values()) == len(self.target_objects):
            reward = 1000
            # reward = 10 ** (sum(self.objects_collected.values()) + 2) 
            terminated = True 

        # elif reward == 1 and self.item_map[x][y].found == False:
        #     self.objects_collected+=1 
        #     self.item_map[x][y].found = True
        #     terminated = True
        #     # if self.objects_collected == len(self.target_objects):
        #     #     terminated = True
        #     # else: terminated = False
        # else: terminated = False

        observation = self._get_obs()
        info = self._get_info()
        truncated = False

        if self.render_mode == True:
            self._simple_render()
        return observation,reward,terminated,truncated,info

    
    def _get_info(self):
        """
        Return: A dictionary with distances between agent and location


        TODO: add a k,v term for precieved items in gridworld... 
        """
        return {

            "distances" : [np.linalg.norm(self._agent_location - t,ord=1) for t in self._target_locations ],
            "objects_found" : self.objects_collected
        }

    def _get_obs(self):
        """
        We want to return a dictionalry of observation space

        How do you decide what the observation space should be?
        """
        return {"agent":self._agent_location,"targets": self._target_locations}
    
    def _simple_render(self):
        """
        Simply print the grid world, agent, and target locations of a single episode

        agent = "A"
        objects = 1,2,3,4 ... 
        walls = "W"  or maybe a # would look better 
        empty = 

        """

        # print(self.floorplan)

        f = self.floorplan
        x,y  = self._agent_location
        f[x,y] = "A"
        for ind,loc in enumerate(self._target_locations):
            f[loc[0],loc[1]] = f"{ind}"

        for i in f:
            i = "".join(i)
            if "W" in i:
                i = i.replace("W","#")
            if "-" in i:
                i = i.replace("-"," ")
            print(i)
        

        
    

        






 


if __name__ == "__main__":
    
    e = WalledGridworld(target_objects=[1,2,3,4],size = 14,map_name="14x14")
    e.reset()
    e._simple_render()
    print(e._target_locations)
    # print(e.floorplan)




