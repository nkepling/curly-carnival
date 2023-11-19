import gymnasium as gym

desc=["SFFF", "FHFH", "FFFH", "HFFG"]
env = gym.make('FrozenLake-v1', desc=desc, map_name="8x8", is_slippery=False,render_mode="human")


observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info  = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()




