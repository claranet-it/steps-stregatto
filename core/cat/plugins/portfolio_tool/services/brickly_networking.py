import os
import re

from cat.plugins.portfolio_tool.services.brickly_service import BricklyService

NETWORKING_URL = (
    f"{os.getenv('PORTFOLIO_URL')}/prod/api/networking/effort/next?months=3&company=it"
)


class BricklyNetworking(BricklyService):
    def get_result(self, parameter: str):
        response_data = self.get_json_response()

        filtered_data = self.__filter_data(response_data, parameter)

        result_string = f"{filtered_data}"

        return result_string

    def __filter_data(self, companies_data, parameter):
        filtered_data = []
        pattern = re.compile(re.escape(parameter), re.IGNORECASE)
        for element in companies_data:
            for company_name, company in element.items():
                for skill in company:
                    if pattern.search(skill["skill"]):
                        skill_copy = skill.copy()
                        skill_copy["name"] = company_name
                        available_effort = []
                        for month in skill["effort"]:
                            month_copy = {
                                "month_year": month["month_year"],
                                "people": month["people"],
                                "availableEffort": 100 - month["totalEffort"],
                            }
                            available_effort.append(month_copy)
                        skill_copy["effort"] = available_effort
                        filtered_data.append(skill_copy)
        return filtered_data

    def __init__(self, token: str):
        super().__init__(NETWORKING_URL, token)
