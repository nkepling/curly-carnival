import heapq
import numpy as np 
import networkx as nx
from envs.my_grid_world import MyGridWorld

# TODO: turn this into a an action wrapper for the gridworld environmetn 


def heuristic_function(src,tgt):
    """
    l1 norm 
    """
    d = np.linalg.norm(np.array(tgt)-np.array(src),1)
    return d



def reconstruct_path():
    pass

def a_star_search(src: tuple , tgt: tuple, G,h:heuristic_function = heuristic_function) -> list:
    """

    Use networkx astar but we need the output in a format we can use
    Inputs:

    touple src: starting location of agent
    touple tgt: target location 
    GridWorldEnv grid: the grid world environment  

    Out:

    dict path: shortest path

    For now I am going to assume the we know the target location

    TODO: The target location can be frontiers rather than the final reward .... 

    """


    path = list(map(np.array,nx.astar_path(G, (src[0],src[1]), (tgt[0],tgt[1]), heuristic=h , weight="cost")))

    directions = []

    for i in range(1,len(path)): #
        n = path[i] - path[i-1]
        directions.append(n)
    
    return directions




        


    



    




