import pygame
import numpy as np
from io import StringIO
from gymnasium import utils
from contextlib import closing
import pygame
import sys
import random


class Render:
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
        
        



# Constants
WIDTH = 800
HEIGHT = 800
GRID_SIZE = 9
AGENT_SIZE = 20
TOKEN_SIZE = 15
WALL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169,169,169)

# # Initialize Pygame
# pygame.init()

# Create the game window
# window = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Grid World")

# Define the Agent class
class Agent:
    def __init__(self):
        self.x = random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE
        self.y = random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE

    def draw(self):
        pygame.draw.rect(window, RED, (self.x, self.y, AGENT_SIZE, AGENT_SIZE))

# Define the Token class
class Token:
    def __init__(self):
        self.x = random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE
        self.y = random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE

    def draw(self):
        pygame.draw.circle(
            window, BLUE, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), TOKEN_SIZE
        )

# Define the Wall class
class Wall:
    def __init__(self):
        self.x = random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE
        self.y = random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE

    def draw(self):
        pygame.draw.rect(window, BLACK, (self.x, self.y, WALL_SIZE, WALL_SIZE))




# Create instances of Agent, Token, and Wall
# agent = Agent()
# tokens = [Token() for _ in range(5)]
# walls = [Wall() for _ in range(10)]


# class dr



# # Game loop
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     # Update logic here

#     # Drawing code
#     window.fill(WHITE)

#     agent.draw()

#     for token in tokens:
#         token.draw()

#     for wall in walls:
#         wall.draw()

#     pygame.display.flip()
#     pygame.time.Clock().tick(30)


class HumanRenderer:
    def __init__(self,size,desc) -> None:
        self.window = None
        self.clock = None
        # self.window_size = 512
        self.window_size = 800
        self.size = size
        # self.objects_collected = 0
        self.desc = [list(i) for i in desc]
        self.walls = []
        for i in range(self.size):
            for j in range(self.size):
                if self.desc[j][i] == "W":
                    self.walls.append((j,i))

        

    def render_frame(self,agent_location,target_location):
        if self.window is None:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        pix_square_size = (
            self.window_size // self.size
        )  # The size of a single grid square in pixels

        #Draw the target

        # Draw the walls

        for wall in self.walls:
            pygame.draw.rect(canvas, GRAY, (wall[0]*pix_square_size , wall[1]*pix_square_size, pix_square_size, pix_square_size))

        TARGET_SIZE = pix_square_size/3
        for t in target_location:
            pygame.draw.rect(canvas,RED,(t[0]*pix_square_size,t[1]*pix_square_size,pix_square_size,pix_square_size))

            # x = (cell_width - rectangle_width) // 2

        # # Dray the agent
        pygame.draw.circle(
            canvas,
            BLUE,
            (agent_location+0.5) * pix_square_size,
            pix_square_size / 5,
        )

        # gridlines
        for x in range(self.size + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * x),
                (self.window_size, pix_square_size * x),
                width=3,
            )
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * x, 0),
                (pix_square_size * x, self.window_size),
                width=3,
            )

        #Add font

        font = pygame.font.Font(None, 36)
        objects_collected = len(target_location)
        text = f"{objects_collected}"

        text_surface = font.render(text, True, (255, 0, 0))

        # if self.render_mode == "human":
        # The following line copies our drawings from `canvas` to the visible window
        self.window.blit(canvas, canvas.get_rect())
        self.window.blit(text_surface,(10,10))
        pygame.event.pump()
        pygame.display.update()

        # We need to ensure that human-rendering occurs at the predefined framerate.
        # The following line will automatically add a delay to keep the framerate stable.
        # self.clock.tick(100)
        # pygame.time.delay(500) 
        # else:  # rgb_array
        #     return np.transpose(
        #         np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
        #     )
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


    

            


if __name__ == "__main__":
    import yaml
    with open('/Users/nathankeplinger/Documents/Vanderbilt/Research/MCTS_LLMs/curly-carnival/MultiObjectSearch/MAPS.yaml','r') as f:
        MAPS  = yaml.load(f,Loader=yaml.FullLoader)

    map_name="9x9"
    size = 9
    R = HumanRenderer(size=size,desc=MAPS[map_name])
    while True:
        R.render_frame(np.array([1,1]),[(3,3)]) 




