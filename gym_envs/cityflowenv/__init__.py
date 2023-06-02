import logging
from gymnasium.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='OneIntersection-v0',
    entry_point='cityflowenv.envs:CityFlow1IntEnv',
)

register(
    id='GeneralCity-v0',
    entry_point='cityflowenv.envs:CityFlowEnv',
)