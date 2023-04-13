from gym.envs.registration import register

register(
    id='cityflowenvs:CityFlowOneInt',
    entry_point='gym_envs.cityflowenvs.envs:cityflow1intenv',
)

register(
    id='CityFlowEnvs:CityFlow',
    entry_point='gym_envs.cityflowenvs.envs:cityflowenv',
)