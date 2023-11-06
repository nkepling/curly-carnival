import gymnasium as gym
from gymnasium.envs.registration import register
from envs.grid_world import GridWorldEnv
from a_star_search import a_star_search
import numpy as np
import networkx as nx
"""
Make a basic taxi environment
"""


register(
     id="GridWorld-v0",
     entry_point="envs.grid_world:GridWorldEnv",
     max_episode_steps=300,
)

register(
    id="MyGridWorld",
    entry_point="envs.my_grid_world:MyGridWorld",
    max_episode_steps=300,
)

env = gym.make('MyGridWorld',render_mode="human")
observation, info = env.reset()

src = observation['agent'] #staring location
tgt = observation['target'] #ending location

print(f"Agent start: {src}")
print(f"Targt loc: {src}")

# actions = env.action_space

dist = lambda s,t : np.abs(t[0]-s[0]) + np.abs(t[1]-s[1]) 
# dirs = nx.astar_path(env.G, tgt,src, heuristic=dist, weight="cost")
# print(env.G)
# actions = a_star_search(src,tgt,env.G) #return path from taget to src to that we can pop from the end. 
for _ in range(1000):
    action = env.action_space.sample() ## Search plocicy goes here 
    # if not actions:
    #     actions = a_star_search(src,tgt,env.G)
    # else:
    #     action = actions.pop(0)

    observation, reward, terminated, truncated, info  = env.step(action)
    print(terminated)

    if terminated or truncated:
        observation, info = env.reset()
        src = observation['agent'] #staring location
        tgt = observation['target'] #ending location
        # actions =  a_star_search(src,tgt,env.G)
env.close()