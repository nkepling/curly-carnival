import pygame
import numpy as np
"""
Render for gridworld with PyGame or a simple render
"""


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
class Simple_Renderer:
    def __init__(self,target_locations, map_name="14x14") -> None:
         self.floorplan = np.array([list(i) for i in MAPS[map_name]])
         self.prev_agent_loc = np.array([1,1])
         self.target_location = []

    def simple_render(self,agent_location,target_locations):
        """
        Simply print the grid world, agent, and target locations of a single episode

        agent = "A"
        objects = 1,2,3,4 ... 
        walls = "W"  or maybe a # would look better 
        empty = 

        """

        # print(floorplan)
        
        f = self.floorplan

        prev_x , prev_y = self.prev_agent_loc
        f[prev_x,prev_y] = "-"

        for ind,loc in enumerate(target_locations):
            f[loc[0],loc[1]] = f"{ind}"

        
        x,y  = agent_location
        f[x,y] = "A"
        self.prev_agent_loc = agent_location


        for i in f:
            i = "".join(i)
            if "W" in i:
                i = i.replace("W","#")
            if "-" in i:
                i = i.replace("-"," ")
            print(i)
            


def human_render():
    pass



