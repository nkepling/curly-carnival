from MCTS.mcts import MCTS
from find_nearest import GoToNearestToken
import gymnasium as gym
import numpy as np
# from render import SimpleRender
from render import HumanRenderer
from gymnasium import register
import yaml
import time

#TODO: Figure out how to have a seed for random components 
# TODO: https://stackoverflow.com/questions/73201176/python-stable-baselines3-assertionerror-the-observation-returned-by-reset
register(
    id="WalledGridWorld-v0",
    entry_point="envs.walled_gridworld:WalledGridworld",
    max_episode_steps=300
)

with open('/Users/nathankeplinger/Documents/Vanderbilt/Research/MCTS_LLMs/curly-carnival/MultiObjectSearch/MAPS.yaml','r') as f:
     MAPS  = yaml.load(f,Loader=yaml.FullLoader)

map_name="9x9"
size =9

# seeds where MCTS out performs greedy: seed = 2 , steps = 15, 10 objects

env = gym.make("WalledGridWorld-v0",size = size,target_objects = [i for i in range(10)],max_steps = 17,seed=2,map_name=map_name)
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
print(iter_num)
c = 1.44
gamma = 1
m = 30000
d = 100



print(simple_render)
# R = SimpleRender(MAPS[map_name])
R = HumanRenderer(size = size,desc = MAPS[map_name])
R.render_frame(src,tgt)
mcts = MCTS(env,state,d=d,m=m,c=c,gamma=gamma)
token_finder = GoToNearestToken(MAPS[map_name],size=size)
# time.sleep(20)
while not done:
    action = mcts.search()
    # action = token_finder.search(observation=observation)
    observation,reward,done,truncated, info = env.step(action=action)
    print(f"Reward: {reward}")
    state =  observation,reward,done,truncated, info

    simple_render[src[0],src[1]] ="-"
    src = observation["agent"]
    simple_render[src[0],src[1]] ="A"
    
    R.render_frame(src,tgt)
    # print(simple_render,end="\n")
    iter_num+=1
    
    print(iter_num)
    if done: 
        print("Found")
        print(f"Info: {info['objects_collected']}")

  


