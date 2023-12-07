import numpy as np
import networkx as nx
from get_graph import get_graph
from collections import deque



class Monitor:

    """
    An online monitor component checks saftey and liveness properties of the system:

    Saftey properties:
    
    GA (Agent.location != Wall)

    Liveness properties:

    F(Objects collected)


    """

    def __init__(self,desc,max_steps,size) -> None:
        """
        grid : gridworld map
        """ 
        self.grid = np.array([list(i) for i in desc])
        self.steps_taken = 0
        self.max_steps = max_steps
        self.checked_reachability = False
        self.size = size

        self.G = get_graph(self.grid,size)


    def do_all_checks(self,state,action):
        
        colliision = self._collision_avoidance(state,action)
        reachable = self._are_objects_reachable(state,action)

        checks = {"collision":colliision,"reachable":reachable}

        print(checks)

        return checks




    def _collision_avoidance(self,state,action) -> bool:
        """
        Check if the action will take the agent into a wall. 
        """
        
        agent_location = state[0]['agent']

        action_to_direction = np.array([[1,0],
                                        [0,1],
                                        [-1,0],
                                        [0,-1]])
        
        new_agent_location = np.clip(
            agent_location + action_to_direction[action], 0, self.size - 1
        )

        if self.grid[new_agent_location[0],new_agent_location[1]] == "W":
            return False
        else: 
            return True
        
    def _are_objects_reachable(self,state,action) -> bool:

       
        if not self.checked_reachability:
            self.checked_reachability = True
            target_locations = state[0]["targets"] 
            agent_location =state[0]["agent"]

            bfs_tree = nx.bfs_tree(self.G,(agent_location[0],agent_location[1]))

            reachable_nodes = set(bfs_tree.nodes)

            reachable_objects = reachable_nodes.intersection(target_locations)

            if len(reachable_objects) == len(target_locations):
                self.reachable = True
                return True
            else:
                self.reachable = False  
                return False
            
        else:
            return self.reachable
            
            
        
    def _llm_response_guardrail(action):
        #TODO
        pass
