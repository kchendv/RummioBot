import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register
from gymnasium.utils.env_checker import check_env
import numpy as np

class RummioEnv(gym.Env):
    metadata = {"render_modes":["human"], "render_fps":1}

    def __init__(self, render_mode = None):
        self.render_mode = render_mode
        self.action_space = spaces.Discrete(25) # Size of grid
        self.observation_space = spaces.Box(
            low = 0,
            high = np.array([11] for i in range(26)),
            shape=(26,),
            dtype= np.int32
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        obs = [] # TODO ADD
        info = {}
        if(self.render_mode=='human'):
            self.render()

        return obs, info
    
    def step(self, action):
        # TODO TAKE ACTION
        is_game_end = 1 # TODO ADD
        info = {}
        obs = {} # TODO ADD
        return obs, (0 if is_game_end else 1), is_game_end, False, info


    def render():
        pass


if __name__ == "__main__":
    env = gym.make('rummio', render_mode="human")
    print("Check environment")
    check_env(env.unwrapped)
    obs = env.reset()[0]
    for i in range(10):
        rand_action = env.action_space.sample()
        obs, reward, terminated, _, _ = env.step(rand_action)