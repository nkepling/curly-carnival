from MCTS.mcts import MCTS
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

env = gym.make('MyGridWorld',render_mode="human")
init_state = env.reset()
observation, info = init_state
src = observation['agent'] #staring location
tgt = observation['target'] #ending location

print(f"Agent start: {src}")
print(f"Targt loc: {tgt}")

c = 1/np.sqrt(2)

simple_render = np.full((5,5),"-")
# gridworld = np.zeros((5,5))
# gridworld[src[0],src[1]] = 1
# gridworld[tgt[0],tgt[1]] = 2



simple_render[src[0],src[1]] = "A"
simple_render[tgt[0],tgt[1]] = "X"

# def simple_renderer(simple_render,src,action):
    
#     action_to_direction = {
#             0: np.array([1, 0]),
#             1: np.array([0, 1]),
#             2: np.array([-1, 0]),
#             3: np.array([0, -1]),
#         }
    

#     dir = action_to_direction[action]
#     simple_render[src[0],src[1]] = "-"
#     src  = src + dir
#     simple_render[src[0],src[1]] = "A"
    
#     print(simple_render)
    
#     return src

print(simple_render)




# # Create a figure and axis
# fig, ax = plt.subplots()

# # Customize the gridworld display
# cmap = plt.get_cmap('tab20')  # Define a colormap
# ax.imshow(gridworld, cmap=cmap, interpolation='nearest')

# # Customize the tick marks
# ax.set_xticks(np.arange(-0.5, 5, 1))
# ax.set_yticks(np.arange(-0.5, 5, 1))
# ax.set_xticklabels([])
# ax.set_yticklabels([])
# ax.grid(color='black', linestyle='-', linewidth=2)

# # # Show the gridworld
# plt.show()



done = False
iter_num = 0
while not done:
    mcts = MCTS(env,init_state,10,50000,c)
    action = mcts.search()
    observation,reward,done,truncated, info = env.step(action=action)

    simple_render[src[0],src[1]] ="-"
    # gridworld[src[0],src[1]] = 0

    src = observation["agent"]
    simple_render[src[0],src[1]] ="A"
    # gridworld[src[0],src[1]] = 1

    # ax.imshow(gridworld, cmap=cmap, interpolation='nearest')
    # plt.show()
    print(simple_render)

    if done:
        print("Found ya!")

    iter_num+=1
    print(f"Inter Numbher:{iter_num}") 
    print(observation,info)
