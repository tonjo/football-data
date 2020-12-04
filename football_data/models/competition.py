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
        self.last_updated = competition['lastUpdated']
        if 'numberOfAvailableSeasons' in competition:
            self.number_of_available_seasons = competition['numberOfAvailableSeasons']
        elif 'seasons' in competition:
            self.number_of_available_seasons = len(competition['seasons'])
        else:
            self.number_of_available_seasons = None
        if 'seasons' in competition:
            self.seasons = competition['seasons']
        else:
            self.seasons = None

    def __str__(self):
        return f'{self.id} - {self.name} ({self.number_of_available_seasons} seasons) updated: {self.last_updated}'
