import numpy as np
import pandas as pd

class env():
    def __init__(self):
        '''
        SETUP PARAMETERS
        '''

        self.TICKER         = "AAPL"    #Stock Ticker
        self.INTERVAL       = 5         #value difference of strike prices

        self.STEP_LEN       = 2         #Two timesteps occur per day
        self.SIM_LEN        = 150       #How many timesteps
        self.HISTORY_LEN    = 50        #Number of timesteps given

        self.INIT_CAPITAL   = 10000     #Starting Capital
        self.RFR            = .0106     #Risk free rate
        self.NUM_OPTIONS    = 2         #Number of options on either side of spot price

        self.PRICE_DATA     = np.array(pd.read_csv("trade_sim/data/history/full/"+str(ticker)+".csv")).flatten()
        self.CHANGE_DATA    = np.array(pd.read_csv("trade_sim/data/history/"+str(ticker)+".csv")).flatten()

        self.SIGMA          = np.sqrt(252) * np.std(self.CHANGE_DATA[::2])


    def reset(self, testing=False):
        '''
        RETURNS INITIAL STATE
        reset variables
        '''
        if not testing:
            maxlen = len(self.PRICE_DATA) - self.HISTORY_LEN - self.SIM_LEN
            index  = random.randint(0, maxlen)

            self.prices   = self.PRICE_DATA[index:index+self.HISTORY_LEN+self.SIM_LEN]
            self.changes  = self.CHANGE_DATA[index:index+self.HISTORY_LEN+self.SIM_LEN]

            self.testing  = False
        else:
            self.prices     = np.array(pd.read_csv("trade_sim/data/testing/full/"+str(ticker)+".csv")).flatten()
            self.changes    = np.array(pd.read_csv("trade_sim/data/testing/"+str(ticker)+".csv")).flatten()

            self.SIGMA      = np.sqrt(252) * np.std(self.changes[::2])

            self.testing  = True


        self.position   = np.zeros(self.NUM_OPTIONS * 2 + 2)
        self.old_opt    = np.zeros(self.NUM_OPTIONS * 2 + 2)
        self.pos_change = np.zeros(self.NUM_OPTIONS * 2 + 2)
        self.opt_change = np.zeros(self.NUM_OPTIONS * 2 + 2)




        self.capital    = self.INIT_CAPITAL #Reset capital

        self.step       = 1                 #Reset Step
        self.day        = 0                 #0-4 mon-friday
        self.open       = True              #Open or Close

        self.options    = []                #Options chains

        self.history = np.array([
            self.changes[0:self.HISTORY_LEN],
            self.prices[0:self.HISTORY_LEN]])

        price   = int(self.history[1][len(self.history-1)])

        self.get_options(price)
        self.old_opt = self.options

        stdev   = np.std(self.history[0])
        state = [
            self.history[0],
            self.pos_change,
            self.options,
            self.opt_change,
            self.capital,
            stdev*np.sqrt(4-self.day),
            (np.log(price) - (0.5 * (stdev**2) * (4 - self.day))),
            4-self.day
            ]

        return state

    def step(self, action):

        #buy
        pos = np.asarray(self.options)[np.in1d(np.where(action==1)[0],np.where(self.position == 0)[0])]
        if sum(pos * 100) < self.capital:
            self.position = pos

        #else give negative reward
        #sell
        pos = np.in1d(np.where(action==0)[0],np.where(self.position != 0)[0])
        self.capital += sum((self.options[pos] - self.position[pos]) * 100)
        self.position[pos] = 0

        self.history = np.array([
            self.changes[self.cur_step:self.HISTORY_LEN+self.cur_step],
            self.prices[self.cur_step:self.HISTORY_LEN+self.cur_step]])

        price   = int(self.history[1][len(self.history-1)])
        stdev   = np.std(self.history[0])
        self.get_options(price)

        pos = np.where(self.position != 0)[0]
        self.pos_change = (self.options[pos] - self.position[pos])/abs(self.position)
        self.opt_change = (self.options - self.old_opt)/abs(self.old_opt)
        self.old_opt = self.options

        state = [
            self.history[0],
            self.pos_change,
            self.options,
            self.opt_change,
            self.capital,
            stdev*np.sqrt(4-self.day),
            (np.log(price) - (0.5 * (stdev**2) * (4 - self.day))),
            4-self.day
            ]

        if self.capital < 0:
            done = True

        if (self.step < self.SIM_LEN):
            self.step  += 1
            self.day   = (self.day + 1) % 5


        else:
            if(self.testing):
                print("Done")
            done = True


        return state, reward, done

    def get_options(self, spot):
        t = (4 - self.day)/252
        S = self.round(spot)

        self.calls,self.puts = [],[]
        ii = -int(self.NUM_OPTIONS/2)
        for i in range(int(self.NUM_OPTIONS)+1):
            K = i * self.INTERVAL + ii + S
            d1 = np.log(S/(K/(1 + self.RFR)**t)/(self.SIGMA*sqrt(t))) + (self.SIGMA*sqrt(t))/2
            d2 = d1 - self.SIGMA * np.sqrt(t)
            c = S * norm.cdf(d1) - (K/(1 + self.RFR)**t) * norm.cdf(d2)
            self.options.append(c)#[spot - K,c])
            self.options.append(K*(np.e**(-self.RFR*t)) - S + c)#[spot-K, K*(np.e**(-self.RFR*t)) - S + c])

    def round(self, spot):
        return self.INTERVAL * round(spot/self.INTERVAL)


    def getStateSize(self):
        """
        Return the size the state
        """
        return
            self.HISTORY_LEN    +
            len(self.pos_change)+
            len(self.options)   +
            len(self.opt_change)+
            len(self.capital)   +
            3

    def get_total_actions(self):
        """
        Return the size action vector
        """
        return self.NUM_OPTIONS*2+2

    def get_env_info(self):
        """
        Return basic infos about the environment
        """
        env_info = {"state_shape": self.getStateSize(),
                    "n_actions": self.get_total_actions(),
                    "n_agents": 1,
                    "episode_limit": self.SIM_LEN}
        return env_info

    def close(self):
        """
        Close the environment
        """
        return

    def seed(self, seed_num):
        np.random.seed(seed_num)
