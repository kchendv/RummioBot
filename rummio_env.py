import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register
from gymnasium.utils.env_checker import check_env
import numpy as np

from rummio_game import RummioGame


register(
    id = "rummio",
    entry_point="rummio_env:RummioEnv",
    nondeterministic=True
)

class RummioEnv(gym.Env):
    metadata = {"render_modes":["human"], "render_fps":1}

    def __init__(self, render_mode = None):
        self.game = RummioGame()
        self.prev_state = None
        self.render_mode = render_mode
        self.action_space = spaces.Discrete(25) # Size of grid
        self.observation_space = spaces.Box(
            low = 0,
            high = np.array([11 for i in range(26)]),
            shape=(26,),
            dtype= np.int32
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game.reset()
        obs = self.game.get_state()
        info = {}
        if(self.render_mode=='human'):
            self.render()

        return obs, info
    
    def step(self, action):
        self.game.do_click(action)
        obs = self.game.get_state()
        is_game_end = self.game.is_game_end(obs)
        reward = 0
        if (is_game_end):
            reward = -1
        elif obs == self.prev_state:
            reward = -1
        else:
            reward = 1
        self.prev_state = obs
        info = {
            "Action": action,
            "Reward": reward,
            "Is end": is_game_end
        }

        return obs, reward, is_game_end, False, info

    def render(self):
        pass


if __name__ == "__main__":
    env = gym.make('rummio', render_mode="human")
    print("Check environment")
    check_env(env.unwrapped)
    obs = env.reset()[0]
    for i in range(10):
        rand_action = env.action_space.sample()
        obs, reward, terminated, _, info = env.step(rand_action)
        print(obs, info)