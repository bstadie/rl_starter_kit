import gym
import d4rl
import random
import numpy as np


def main():
    env = gym.make('maze2d-umaze-v1')
    env.reset()
    env.step(env.action_space.sample())
    for i in range(10000):
        action = env.action_space.sample()
        next_obs, reward, terminated, info = env.step(action)
        env.render()
    env.close()

class GoalMaze:
    def __init__(self, maze_env, corruption = True):
        self.env = maze_env
        self.goal = None
        self.corruption = corruption

    def set_goal(self, goal):
        self.goal = goal

    # def step(self, action, goal):
    #     obs = self.env.step(action)
    #     if np.linalg.norm(obs - goal) < eps:
    #         rew = 1
    #     else:
    #         rew = 0
    #     if self.corruption is True:
    #         return s[4:6+noise]

    def step(self, action):
        obs, reward, terminated, info = self.env.step(action)
        diff = obs[0:2] - self.goal
        if np.linalg.norm(diff) < self.eps:
            reward = 1
            terminated = True
        else:
            reward = 0
        if self.corruption is True:
            if np.linalg.norm(obs[0:2]) < 1:
                obs = [obs[0]+random.uniform(-0.2,0.2),obs[1]+random.uniform(-0.2,0.2),obs[2]+random.uniform(-0.1,0.1),obs[3]+random.uniform(-0.1,0.1)]
        return obs, reward, terminated




if __name__ == "__main__":
    main()