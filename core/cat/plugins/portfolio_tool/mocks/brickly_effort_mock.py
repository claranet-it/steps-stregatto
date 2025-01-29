from cat.plugins.portfolio_tool.mocks.fixtures import effort_data
from cat.plugins.portfolio_tool.services.brickly_effort import BricklyEffort


class BricklyEffortMock(BricklyEffort):
    def get_json_response(self):
        return effort_data
