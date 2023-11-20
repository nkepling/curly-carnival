from envs.grid_world import GridWorldEnv
from gymnasium.envs.registration import register


register(
    id="WalledGridWorld-v0",
    entry_point="envs.walled_gridworld:WalledGridworld",
    max_episode_steps=300
)