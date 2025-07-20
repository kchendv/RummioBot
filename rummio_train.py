import os
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
import rummio_env

def train_sb3():
    model_dir = "models"
    log_dir = "logs"
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    env = make_vec_env("rummio", n_envs=4, vec_env_cls=SubprocVecEnv)
    model = PPO('MlpPolicy', env, verbose = 1, device='cpu', tensorboard_log=log_dir, n_steps= 256)

    TIMESTEPS = 1000
    iters = 0
    while True:
        iters += 1
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
        model.save(f"{model_dir}/ppo_{iters}")
    
def test_sb3(model_n = 2, render=True):
    env = gym.make('rummio', render_mode='human' if render else None)

    model = A2C.load(f'models/ppo_{model_n}', env=env)

    obs = env.reset()[0]
    terminated = False
    while True:
        action, _ = model.predict(observation=obs, deterministic=True)
        obs, _, terminated, _, _ = env.step(action)

        if terminated:
            break

if __name__ == '__main__':
    # Train/test using StableBaseline3
    train_sb3()
    # test_sb3()