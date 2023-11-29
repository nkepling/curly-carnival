# from envs.walled_gridworld import WalledGridworld
from gymnasium.envs.registration import register
from MCTS.mcts import MCTS

# register(
#     id="MyGridWorld",
#     entry_point="envs.my_grid_world:MyGridWorld",
#     max_episode_steps=300,
# )

# register(
#     id="WalledGridWorld-v0",
#     entry_point="envs.walled_gridworld:WalledGridworld",
#     max_episode_steps=300
# )