import numpy as np
from copy import deepcopy
import gymnasium as gym
from mctsNode import Node
from collections import defaultdict,namedtuple





class MCTS:

    """
    This is my own implementation of MCTS. 

    The algoirhtm procedes as follows

    1. Given some root node we need to find the best action.
    2. We do this by statring at the root node, 
    3. From the root node we select some candidate state (by taking an action)
    4. Fromt the candidate state we simulate.
        4.1 moves are made during simluation according to some default policy (in the simplist case a unifrom distribution of moves. )
    5. The search tree is then reccursivly updated using backprop. 
    6. The selected node is then added to the search tree.

    There are four steps applied per serach iteration

    1. Selection: starting from the root node a child selection policiy is recursively applied to descend through the tree until the most "urgent" expandable node is reached. 
        1.1: A node is expandable if it is non-terminal and un-expanded children. 
    2. Expansion: One or more child nodes are added to expand the tree (according to available actions)
    3. Simulation: A simulation is run form the new nodes according to default polict to produce an outcome
    4. Backpropagation: The simlulation result it backpropagets through the selectd nodse to update their statistics


    Selection and expansion are combined into the "treepolicy method"
    The rollout/simluation is the "default" policy. 
    """
    def __init__(self,env:gym.Env,Q,d,m,c,U) -> None:
        self.env = env # This is the current state of the mdp

        # state = {"observation":None,
        #          "reward":None,
        #          "terminated":None,
        #          "info":None }#observation, reward, terminated, False, info
        # self.N = 0 # visit counts TODO: does this need do be a dict of (s,a):counts pairs???
        # self.Q = Q # State-Action value estimates TODO: Does this need to be a dict of (s,a): U pairs?
        self.d = d # depth
        self.m = m # number of simulations
        self.c = c # exploration constant
        #self.U = U # value funciton estimate
        self.v0 = Node(parent=None,env=env,action=None)  #root node of search tree. 


    def search(self,s):
        """
        Do the MCTS by doing m simulations from the current state s. 
        After doing m simulations we simply choose the action that maximizes the estimate of Q(s,a)
        """
        for k in range(self.m):
            vl = self._tree_policy(self.v0) #vl is the last node visitied by the tree search
            R = self._default_policy(vl)
            self._backpropagation(R,vl )

        a = np.argmax(self.Q)
        return a



    def _tree_policy(self,v:Node):
        while not v.is_terminal(): #TODO: Figure out how the root node would behave here. 
            if not v._is_fully_expanded():
                return self._expand(v)
            else:
                v = self._selection(v)
        return v 


    def _default_policy(self,v):
        """
        While state is non-terminal choose  an action uniformly at random, transition to new state.

        Return then reward for final  state. 
        """
        sim_env = deepcopy(v.env)
        action = sim_env.action_space.sample()
        observation,reward,terminated,info = sim_env.step(action)
        while not terminated:
            action = sim_env.action_space.sample()
            observation,reward,terminated,info = sim_env.step(action)
        return reward

    def _selection(self,v:Node):
        """
        Pick the next node to go down in the search tree based on UTC
        """
        child_nodes = v.children
        best_child_ind = np.argmax([child.Q/child.N + self.c * np.sqrt(2*np.log(v.N)/(child.N)) for child in child_nodes])
        return child_nodes[best_child_ind]    
    
    def _expand(self,v):
        pass 


        

    def _simulate(self,s):
        """
        Run a simulation from the current state s to some depth d. 
        During simulation update teh action value function Q(s,a) 
        and record the number of times a particular state-action pair has been selected        
        """

        sim_env = deepcopy(self.env)
        N,Q,c = self.N,self.Q,self.c 
        A = sim_env.action_space
        Q = sim_env.TR

    def _backpropagation(self,R,v:Node):
        pass

