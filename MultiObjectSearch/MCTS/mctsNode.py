from collections import defaultdict
import gymnasium as gym 

class Node:
    """
    This is a node of the MCTS search tree. 
    - Each node will capture a particular sate. The edges are actions. 
    """
    def __init__(self,parent,env,action) -> None:
        
        if len(env) == 2: # Is this the stating state of the environment env.reset() only returns obs and info ... 
            self.state = defaultdict(dict,{k:v for k,v in zip(["obs","info"],env)})
        else: self.state = defaultdict(dict,{k:v for k,v in zip(["obs","reward","terminated","info"],env)})
        self.action = action #what was the action taken to get here? The "incoming action"
        self.parent = parent #what is the parent node 
        self.children = {} #children coresponding to the action taken ... 
        self.N = 0 #N this the number of time this node has been visited
        self.Q = [] # What is the curretn value of this node ... 


    def is_leaf(self) -> bool:
        """
        Is the node terminal?
        """
        return self.children == []
    
    def is_fully_expanded(self) -> bool:
        """
        Is the node fuly expanded

        """
        return len(self.children) == len(self.state.action_space)
    
    def is_terminal(self):
        """
        Check if the current state of OpenAI gym is a terminal node ... 

        Returns: bool or empty dict is starting state ... 
        """
        return self.state["terminated"]





