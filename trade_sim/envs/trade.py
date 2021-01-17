import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding

from trade_sim.trade_env.env import env as sim_trade

import logging
logger = logging.getLogger(__name__)

class TradeEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.env = sim_trade()
        self.observation_space = spaces.Box(low=-10., high=10.,
                                            shape=(self.env.getStateSize(),))

        #self.action_space = spaces.Discrete(3)
        self.action_space = spaces.Box(low=0,high=1,shape=(10,))

    def reset(self,testing=False):
        return self.env.reset(testing=testing)

    def step(self, action):
        ob, reward, done = self.env.step(action)
        return ob, reward, done, {}

    def render(self, mode='human', close=False):
        return

    def close(self):
        return

    def seed(self, seed=None):
        self.env.seed(seed)
