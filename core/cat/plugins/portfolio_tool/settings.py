from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel


class BricklySettings(BaseModel):
    include_networking: bool = True


@plugin
def settings_model():
    return BricklySettings
