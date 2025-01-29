from cat.plugins.portfolio_tool.mocks.fixtures import skills_data
from cat.plugins.portfolio_tool.services.brickly_skills import BricklySkills


class BricklySkillsMock(BricklySkills):
    def get_json_response(self):
        return skills_data
