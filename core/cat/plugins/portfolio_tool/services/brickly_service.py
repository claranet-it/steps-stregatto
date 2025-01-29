from abc import ABC, abstractmethod

from requests import get


class BricklyService(ABC):
    @abstractmethod
    def get_result(self, parameter: str):
        pass

    def get_json_response(self):
        bearer = f"Bearer {self.token}"

        return get(self.url, headers={"Authorization": bearer}).json()

    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
