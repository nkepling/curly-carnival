from MCTS.mcts import MCTS
from find_nearest import GoToNearestToken
import gymnasium as gym
import numpy as np
# from render import SimpleRender
from render import HumanRenderer
from gymnasium import register
from saftey_monitor import Monitor
import yaml


#TODO: Figure out how to have a seed for random components 
# TODO: https://stackoverflow.com/questions/73201176/python-stable-baselines3-assertionerror-the-observation-returned-by-reset
register(
    id="WalledGridWorld-v0",
    entry_point="envs.walled_gridworld:WalledGridworld",
    max_episode_steps=300
)

with open('./MAPS.yaml','r') as f:
     MAPS  = yaml.load(f,Loader=yaml.FullLoader)

map_name= "9x9"
size = 9
max_steps = 16
number_of_tokens = 10
seed = 2

env = gym.make("WalledGridWorld-v0",size = size,target_objects = [i for i in range(number_of_tokens)],max_steps = max_steps,seed=seed,map_name=map_name)
state = env.reset()
observation, info = state
src = observation['agent'] #staring location
tgt = observation['targets'] #ending location

done = False
iter_num = 0
print(iter_num)
c = 1.44
gamma = 1
m = 10
d = 1000

R = HumanRenderer(size = size,desc = MAPS[map_name])
R.render_frame(src,tgt)

mcts = MCTS(env,state,d=d,m=m,c=c,gamma=gamma)
token_finder = GoToNearestToken(MAPS[map_name],size=size)
done = False

monitor = Monitor(desc=MAPS[map_name],size=size,max_steps = max_steps)


while not done:
    action = mcts.search()
    # action = token_finder.search(observation=observation)
    monitor.do_all_checks(state=state,action=action)
    observation,reward,done,truncated, info = env.step(action=action)
    print(f"Reward: {reward}")
    state =  observation,reward,done,truncated, info

    # simple_render[src[0],src[1]] ="-"
    src = observation["agent"]
    # simple_render[src[0],src[1]] ="A"
    
    R.render_frame(src,tgt)
    # print(simple_render,end="\n")
    iter_num+=1
    
    # print(iter_num)
    if done: 
        print("Found")
        print(f"Info: {info['objects_collected']}")


  


