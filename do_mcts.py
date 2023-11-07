from MCTS.mcts import MCTS
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

env = gym.make('MyGridWorld',render_mode="human")
state = env.reset()
observation, info = state
src = observation['agent'] #staring location
tgt = observation['target'] #ending location

print(f"Agent start: {src}")
print(f"Targt loc: {tgt}")

simple_render = np.full((10,10),"-")
simple_render[src[0],src[1]] = "A"
simple_render[tgt[0],tgt[1]] = "X"

print(simple_render)

done = False

iter_num = 0

c = 1.44
gamma = 0.9
while not done:
    mcts = MCTS(env,state,100,1000,c,gamma)
    action = mcts.search()
    observation,reward,done,truncated, info = env.step(action=action)
    state =  observation,reward,done,truncated, info
    simple_render[src[0],src[1]] ="-"
    src = observation["agent"]
    simple_render[src[0],src[1]] ="A"
 
    print(simple_render)
    print(observation)
    if done: 
        print("Found")

    iter_num+=1


