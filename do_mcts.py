from MCTS.mcts import MCTS
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from render import Simple_Renderer

# env = gym.make('MyGridWorld',render_mode="human")
env = gym.make("WalledGridWorld-v0",size = 14,target_objects = ['a','b'],map_name="14x14")
state = env.reset()
observation, info = state
src = observation['agent'] #staring location
tgt = observation['targets'] #ending location

print(f"Agent start: {src}")
print(f"Targt loc: {tgt}")

simple_render = np.array([list(i) for i in [
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
    ]])
# simple_render = np.full((10,10),"-")
simple_render[src[0],src[1]] = "A"

for ind,loc in enumerate(tgt):
        simple_render[loc[0],loc[1]] = f"{ind}"

# simple_render[tgt[0],tgt[1]] = "X"
# print(simple_render)
# # r = Simple_Renderer()
done = False

iter_num = 0

# c = 1.44
c = 1.44

#gamma = 0.9
gamma = 0.9
# r.simple_render(src,tgt)

print(simple_render)
# print(env.r)

while not done:
    mcts = MCTS(env,state,d=10000,m=10000,c=c,gamma=gamma)
    action = mcts.search()
    observation,reward,done,truncated, info = env.step(action=action)
    # r.simple_render(observation["agent"],observation["targets"])
    state =  observation,reward,done,truncated, info


    simple_render[src[0],src[1]] ="-"
    src = observation["agent"]
    simple_render[src[0],src[1]] ="A"
 
    print(simple_render)
    print(observation)
    print(info)
    # print(iter_num)
    if done: 
        print("Found")

    iter_num+=1


