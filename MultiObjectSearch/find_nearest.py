import networkx as nx
from get_graph import get_graph
import numpy as np

class GoToNearestToken:
    """
    Find the next closest token from agent and go to it
    """
    def __init__(self,desc,size) -> None:

        desc = np.array([list(i) for i in desc])
        self.G = get_graph(desc,size)
        self.actions = []

    def search(self,observation):
        """

        Seach for path to nearest token. If path is known return action to take to get there. 
        """
        if self.actions:
            return self.actions.pop()
        else:
            agent = observation["agent"]
            targets = observation["targets"]
            min_d = np.inf
            for t in targets:
                # d = self._heuristic_function(agent,t)
                d = nx.astar_path_length(self.G,(agent[0],agent[1]), (t[0],t[1]), heuristic=self._heuristic_function)
                if d < min_d:
                    min_d = d
                    nearest_target = t

            p = nx.astar_path(self.G, (agent[0],agent[1]), (nearest_target[0],nearest_target[1]), heuristic=self._heuristic_function)
            self.actions = self._path_to_actions(p)
            return self.actions.pop()

    def _heuristic_function(self,src,tgt):
        """
        l1 norm 
        """
        d = np.linalg.norm(np.array(tgt)-np.array(src),1)
        return d
        
    def _path_to_actions(self,p):
        """
        List of tuples to list of actions 
        """

        dir_2_action = dict(zip([(1,0),
                                        (0,1),
                                        (-1,0),
                                        (0,-1)], [0,1,2,3]))
        actions = []
        for i  in range(1, len(p)):
     
            dx = p[i][0] - p[i-1][0]
            dy = p[i][1] - p[i-1][1]
            dir  = (dx,dy)
            actions.append(dir_2_action[dir])
        actions = actions[::-1]
        return actions
        






if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import gymnasium as gym
    from gymnasium import register
    import yaml
    
    with open("MultiObjectSearch/MAPS.yaml","r") as f:
        MAPS = yaml.load(f, Loader=yaml.FullLoader)

    map_name = "9x9"
    size = 9
    
    # desc = np.array([list(i) for i in MAPS[map_name]])

    token_finder = GoToNearestToken(desc = MAPS[map_name],size=size)

    register(
    id="WalledGridWorld-v0",
    entry_point="envs.walled_gridworld:WalledGridworld",
    max_episode_steps=300
    )
    env = gym.make("WalledGridWorld-v0",size = size,target_objects = [i for i in range(6)],max_steps = 20,seed = 123,map_name=map_name)
    state = env.reset()
    observation, info = state

    p = token_finder.search(observation)
    print(p)

    




            
            
