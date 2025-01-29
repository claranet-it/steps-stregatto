import os

from cat.plugins.portfolio_tool.mocks.brickly_effort_mock import BricklyEffortMock
from cat.plugins.portfolio_tool.mocks.brickly_networking_mock import (
    BricklyNetworkingMock,
)
from cat.plugins.portfolio_tool.mocks.brickly_skills_mock import BricklySkillsMock
from cat.plugins.portfolio_tool.services.brickly_effort import BricklyEffort
from cat.plugins.portfolio_tool.services.brickly_networking import BricklyNetworking
from cat.plugins.portfolio_tool.services.brickly_skills import BricklySkills


class BricklyServiceFactory:
    @staticmethod
    def get_brickly_skills_service(token: str):
        if BricklyServiceFactory.__is_prod_env():
            return BricklySkills(token)
        return BricklySkillsMock(token)

    @staticmethod
    def get_brickly_effort_service(token: str):
        if BricklyServiceFactory.__is_prod_env():
            return BricklyEffort(token)
        return BricklyEffortMock(token)

    @staticmethod
    def get_brickly_networking_service(token: str):
        if BricklyServiceFactory.__is_prod_env():
            return BricklyNetworking(token)
        return BricklyNetworkingMock(token)

    @staticmethod
    def __is_prod_env():
        if os.getenv("BRICKLY_TEST_ENV", False):
            return False
        return True
