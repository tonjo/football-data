import requests


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

    def __str__(self):
        return self.name
