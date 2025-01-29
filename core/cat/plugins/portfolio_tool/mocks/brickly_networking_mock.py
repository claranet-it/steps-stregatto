from cat.plugins.portfolio_tool.mocks.fixtures import networking_data
from cat.plugins.portfolio_tool.services.brickly_networking import BricklyNetworking


class BricklyNetworkingMock(BricklyNetworking):
    def get_json_response(self):
        return networking_data
