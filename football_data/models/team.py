import json
from types import SimpleNamespace
from ..constants import LEAGUE_CODE


class Team():
    """
    The Team class.
    """

    def __init__(self, team_data):
        team = json.loads(
            team_data, object_hook=lambda d: SimpleNamespace(**d))
        self = team

    def __str__(self):
        return self.name
