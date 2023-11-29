from MCTS.mcts import MCTS
import gymnasium as gym
import numpy as np
from render import SimpleRender
from gymnasium import register
import yaml


#TODO: Figure out how to have a seed for random components 
# TODO: https://stackoverflow.com/questions/73201176/python-stable-baselines3-assertionerror-the-observation-returned-by-reset
register(
    id="WalledGridWorld-v0",
    entry_point="envs.walled_gridworld:WalledGridworld",
    max_episode_steps=300
)

with open('MAPS.yaml','r') as f:
     MAPS  = yaml.load(f,Loader=yaml.FullLoader)

map_name="9x9"
size = 9 

env = gym.make("WalledGridWorld-v0",size = size,target_objects = ['a','b'],map_name=map_name)
state = env.reset()
observation, info = state
src = observation['agent'] #staring location
tgt = observation['targets'] #ending location

print(f"Agent start: {src}")
print(f"Targt loc: {tgt}")

simple_render = np.array([list(i) for i in MAPS[map_name]])
simple_render[src[0],src[1]] = "A"

for ind,loc in enumerate(tgt):
        simple_render[loc[0],loc[1]] = f"{ind}"

done = False
iter_num = 0

c = 1.44
gamma = 0.99

print(simple_render)
R = SimpleRender(MAPS[map_name])
mcts = MCTS(env,state,d=1000,m=50000,c=c,gamma=gamma)
while not done:
    action = mcts.search()
    print(f"root: {mcts.v0}")
    observation,reward,done,truncated, info = env.step(action=action)
    # r.simple_render(observation["agent"],observation["targets"])
    state =  observation,reward,done,truncated, info
    simple_render[src[0],src[1]] ="-"
    src = observation["agent"]
    simple_render[src[0],src[1]] ="A"
    
    print(simple_render)
    print(iter_num)
    if done: 
        print("Found")

    iter_num+=1


