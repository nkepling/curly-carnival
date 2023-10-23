import gymnasium as gym
from gymnasium.envs.registration import register
from envs.grid_world import GridWorldEnv
"""
Make a basic taxi environment

"""


register(
     id="GridWorld-v0",
     entry_point="envs.grid_world:GridWorldEnv",
     max_episode_steps=300,
)


env = gym.make('GridWorld-v0',render_mode="human")
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info  = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()