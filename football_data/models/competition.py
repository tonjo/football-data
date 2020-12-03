import requests

from .fixture import Fixture
from .table import Table
from .team import Team
from ..utils import headers


class Competition():
    """
    The Competition class.
    """

    def __init__(self, competition):
        self.id = competition['id']
        self.area = competition['area']
        self.name = competition['name']
        self.code = competition['code']
        self.emblemUrl = competition['emblemUrl']
        self.plan = competition['plan']
        self.current_season = competition['currentSeason']
        self.numberOfAvailableSeasons = competition['numberOfAvailableSeasons']
        self.lastUpdated = competition['lastUpdated']

    def fixtures(self):
        """
        Returns all current fixtures of the competition.
        """
        response = requests.get(self._fixtures_url, headers=headers()).json()
        return [Fixture(fixture) for fixture in response['fixtures']]

    def teams(self):
        """
        Returns all teams currently participating in the competition.
        """
        response = requests.get(self._teams_url, headers=headers()).json()
        return [Team(team) for team in response['teams']]

    def table(self):
        """
        Returns the current league table of the competition.
        """
        response = requests.get(
            self._league_table_url, headers=headers()).json()
        return Table(response)

    def __str__(self):
        return self.name
