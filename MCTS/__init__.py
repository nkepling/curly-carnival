from gymnasium.envs.registration import register


register(
    id="MyGridWorld",
    entry_point="envs.my_grid_world:MyGridWorld",
    max_episode_steps=300,
)
