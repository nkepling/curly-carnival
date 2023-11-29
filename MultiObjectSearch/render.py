import pygame
import numpy as np
from io import StringIO
from gymnasium import utils
from contextlib import closing


class SimpleRender:
    def __init__(self,desc) -> None:
        
        self.desc = [[c for c in line]for line in desc]
        self.prev_agent_locations = None
        self.prev_target_locations = None

        for i in range(len(desc)):
            for j in range(len(desc)):
                if self.desc[i][j] == "W":
                    self.desc[i][j] = utils.colorize(self.desc[i][j],"white",highlight=True)
                if self.desc[i][j] == "-":
                    self.desc[i][j] =" "

    def render_text(self,agent_location,target_location):
        """
        prints agent location and target locations

        INPUTS:
        numpy array agent_location: coords of agent
        set(tuple) target_locationl: coords of target
        list[String] desc: map description

        OUTPUTS:
        StringIO object of map
        """
        # desc = self.desc.tolist()

        ###### Fix old locations
        if self.prev_agent_locations:
            self.desc[self.prev_agent_locations[0]][self.prev_agent_locations[1]] = " "
        
        if self.prev_target_locations:
            for t in self.prev_target_locations:
                self.desc[t[0]][t[1]] = " "
        ######

        outfile = StringIO()
        row, col = agent_location
        self.desc[row][col] = utils.colorize(self.desc[row][col], "cyan", highlight=True)
        for ind,t in enumerate(target_location):
            x,y = t
            self.desc[x][y] = f"{ind}"
            self.desc[x][y] = utils.colorize(self.desc[x][y],"red",highlight=True)
        # if self.lastaction is not None:
        #     outfile.write(f"  ({['Left', 'Down', 'Right', 'Up'][self.lastaction]})\n")
        # else:

        self.prev_agent_loc = agent_location
        self.prev_target_locations = target_location
        outfile.write("\n")
        outfile.write("\n".join("".join(line) for line in self.desc) + "\n")

        with closing(outfile):
            return outfile.getvalue()



    

            


if __name__ == "__main__":
    pass




