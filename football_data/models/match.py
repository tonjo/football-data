from ..constants import MAX_TEAM_NAME


class Match():
    """
    The Match class.
    """

    def __init__(self, match, competition_id=None):

        self.id = match['id']
        self.season = match['season']
        self.utc_date = match['utcDate']
        self.status = match['status']
        self.matchday = match['matchday']
        self.stage = match['stage']
        self.group = match['group']
        self.last_updated = match['lastUpdated']
        self.odds = match['odds']
        self.score = match['score']
        self.home_team = match['homeTeam']
        self.away_team = match['awayTeam']
        self.referees = match['referees']
        # TODO if getting match from match resource is different
        self.competition_id = competition_id

    def __str__(self):
        # TODO verify full time / extra time
        return f"{self.home_team['name']} - {self.away_team['name']}  {self.score['fullTime']['home_team']} - {self.score['fullTime']['away_team']}"
