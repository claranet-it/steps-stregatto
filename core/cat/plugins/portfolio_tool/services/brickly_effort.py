import os

from cat.plugins.portfolio_tool.services.brickly_service import BricklyService

EFFORT_URL = f"{os.getenv('PORTFOLIO_URL')}/prod/api/effort/next?company=it&months=3"


class BricklyEffort(BricklyService):
    def get_result(self, parameter: str, devs_only: bool = True):
        response_data = self.get_json_response()

        if devs_only:
            response_data = self.__filter_devs(response_data)

        # Mapping of month numbers to month names
        month_names = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December",
        }

        result = [
            {
                person_data["name"]: [
                    {
                        month_names[effort["month_year"][:2]]: 100
                        - (effort["confirmedEffort"] + effort["tentativeEffort"])
                    }
                    for effort in person_data["effort"]
                ]
            }
            for item in response_data
            for _, person_data in item.items()
        ]

        if (
            parameter is not None
            and parameter != "None"
            and parameter.capitalize() in month_names.values()
        ):
            date = parameter.capitalize()
            result = [
                {person: [effort for effort in person_effort if date in effort]}
                for person_effort in result
                for person, person_effort in person_effort.items()
            ]

        result_string = f"{result}"

        return result_string

    def __filter_devs(self, data):
        filtered_data = []
        for person_data in data:
            for name, info in person_data.items():
                if info["crew"] not in ["Hydra", "Cloud"]:
                    filtered_data.append({name: info})
        return filtered_data

    def __init__(self, token: str):
        super().__init__(EFFORT_URL, token)
