from gym.envs.registration import register

register(
    id='trad_sim-v0',
    entry_point='trade_sim.envs:TradeEnv'
)
