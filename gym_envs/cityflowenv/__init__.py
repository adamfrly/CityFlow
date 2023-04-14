import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='cityflowenvs:CityFlowOneInt',
    entry_point='cityflowenvs.envs:cityflow1intenv',
)

register(
    id='CityFlowEnvs:CityFlow',
    entry_point='cityflowenvs.envs:cityflowenv',
)