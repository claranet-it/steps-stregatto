import os
import re

from cat.plugins.portfolio_tool.services.brickly_service import BricklyService

SKILLS_URL = f"{os.getenv('PORTFOLIO_URL')}/prod/api/skill-matrix?company=it"


class BricklySkills(BricklyService):
    def get_result(self, parameter: str) -> str:
        response_data = self.get_json_response()

        filtered_data = self.__filter_data(response_data)

        if parameter and len(parameter) > 0:
            filtered_data = self.__filter_data_for_specific_skill(
                filtered_data, parameter
            )

        result_string = f"[{filtered_data}]"

        return result_string

    def __filter_data(self, skills_data, devs_only=True):
        transformed_data = []
        for person_data in skills_data:
            for name, info in person_data.items():
                skills = info["skills"]
                filtered_skills = {
                    tech: level for tech, level in skills.items() if level > 1
                }
                entry = {name: filtered_skills}
                if devs_only:
                    if info["crew"] not in ["Hydra", "Cloud"]:
                        transformed_data.append(entry)
                else:
                    transformed_data.append(entry)
        return transformed_data

    def __filter_data_for_specific_skill(self, skills_data, skill):
        transformed_data = {}
        pattern = re.compile(re.escape(skill), re.IGNORECASE)
        for person_data in skills_data:
            for name, info in person_data.items():
                for tech in info:
                    if pattern.search(tech):
                        transformed_data[name] = f"{skill} skill level: {info[tech]}"
        if not transformed_data:
            return skills_data

        return transformed_data

    def __init__(self, token: str):
        super().__init__(SKILLS_URL, token)
