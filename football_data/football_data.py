"""
Contains the FootballData class used to interact with the API.
"""
import os
import re
import requests
import urllib.parse

from .constants import LEAGUE_CODE, TEAM_ID
from .utils import json2obj, validate_date

import logging
logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class FootballData(object):
    """
    The FootballData class.
    """

    API_URL = 'https://api.football-data.org/v2/'

    def __init__(self, api_key=None):
        """
        Initialise a new instance of the FootballData class.
        """
        if not api_key:
            if 'FOOTBALL_DATA_API_KEY' in os.environ:
                api_key = os.environ['FOOTBALL_DATA_API_KEY']
            else:
                raise ValueError(
                    'FOOTBALL_DATA_API_KEY environment variable not set or no API key given.')

        self.api_key = api_key
        self.headers = {'X-Auth-Token': api_key}

    def competitions(self):
        """
        List all available competitions.
        """

        url = self._build_url('competitions')
        res = self._api_request(url)
        if res:
            json_tmp = json2obj(res)
            return json_tmp.competitions
        else:
            competitions = []
        return competitions

    def competition(self, competition):
        """
        List one particular competition.
        """

        url = self._build_url(f'competitions/{competition}')
        res = self._api_request(url)

        if res:
            json_tmp = json2obj(res)
            competition = json_tmp
        else:
            competition = None
        return competition

    def competition_teams(self, competition, season=None, stage=None):
        """
        List all teams for a particular competition.
        """

        # competition could be an id or a code like 'WC'
        query_params = {}

        if season:
            query_params['season'] = season
        if stage:
            query_params['stage'] = stage

        url = self._build_url(
            f'competitions/{competition}/teams', query_params)
        res = self._api_request(url)
        if res:
            json_tmp = json2obj(res)
            return json_tmp.teams
        else:
            logger.error(f'teams: no data found')
            return None

    def competition_matches(self, competition, dateFrom=None, dateTo=None, stage=None, status=None, matchday=None, group=None, season=None):
        """
        List all matches for a particular competition.
        """

        query_params = {}

        # Error checking for query parameter dateFrom
        if dateFrom and dateTo:
            if not validate_date(dateFrom) or not validate_date(dateTo):
                logger.error(f'competition_matches: invalid dateFrom/dateTo')
                return []
            query_params['dateFrom'] = dateFrom
            query_params['dateTo'] = dateTo
        elif dateFrom or dateTo:
            logger.error(
                'competition_matches: pecify both dateFrom and dateTo or none')
            return []
        if stage:
            query_params['stage'] = stage
        if status:
            query_params['status'] = status
        if matchday:
            query_params['matchday'] = matchday
        if group:
            query_params['group'] = group
        if season:
            query_params['season'] = season

        url = self._build_url(
            f'competitions/{competition}/matches', query_params)

        res = self._api_request(url)
        if res:
            json_tmp = json2obj(res)
            return json_tmp.matches
        else:
            return []

    def matches(self, competitions=None, dateFrom=None, dateTo=None, status=None):
        """
        List matches across (a set of) competitions.
        """
        query_params = {}
        # Error checking for query parameter dateFrom
        if dateFrom and dateTo:
            if not validate_date(dateFrom) or not validate_date(dateTo):
                logger.error(f'matches: invalid dateFrom/dateTo')
                return []
            query_params['dateFrom'] = dateFrom
            query_params['dateTo'] = dateTo
        elif dateFrom or dateTo:
            logger.error('matches specify both dateFrom and dateTo or none')
            return []

        # COMMA-separated list of competitions, e.g. 2000,2001 or WC,CL
        if competitions:
            query_params['competitions'] = competitions

        if status:
            query_params['status'] = status

        url = self._build_url('matches', query_params)
        res = self._api_request(url)
        if res:
            json_tmp = json2obj(res)
            return json_tmp.matches
        else:
            return []

    def match(self, match_id):
        """
        Show one particular match.
        """
        url = self._build_url(f'matches/{match_id}')
        res = self._api_request(url)
        if res:
            json_tmp = json2obj(res)
            return json_tmp.match
        else:
            return []

    def team_matches(self, team_id, dateFrom=None, dateTo=None, status=None, venue=None, limit=None):
        """
        Show all matches for a particular team.
        """

        query_params = {}

        # Error checking for query parameter dateFrom
        if dateFrom and dateTo:
            if not validate_date(dateFrom) or not validate_date(dateTo):
                logger.error(f'team_matches: invalid dateFrom/dateTo')
                return []
            query_params['dateFrom'] = dateFrom
            query_params['dateTo'] = dateTo
        elif dateFrom or dateTo:
            logger.error(
                'team_matches specify both dateFrom and dateTo or none')
            return []

        # Error checking for query parameter venue
        if venue:
            if venue not in ('HOME', 'AWAY'):
                logger.error('venue is invalid.')
                return []
            query_params['venue'] = venue
        if limit:
            if isinstance(limit, int):
                query_params['limit'] = limit
            else:
                logger.error('limit is invalid.')
                return []

        url = self._build_url(f'teams/{team_id}/matches', query_params)
        res = self._api_request(url)
        if res:
            json_tmp = json2obj(res)
            return json_tmp.matches
        else:
            return []

    def team(self, team_id):
        """
        Show one particular team.
        """

        url = self._build_url(f'teams/{team_id}')
        res = self._api_request(url)
        if res:
            json_tmp = json2obj(res)
            return json_tmp
        else:
            return None

    # def players(self, team):
    #     """
    #     Returns a list of Player objects made from players playing for the team
    #     with the given ID.
    #     """
    #     # If string try to convert to ID
    #     if isinstance(team, str):
    #         if team.lower() in TEAM_ID.keys():
    #             team = TEAM_ID[team.lower()]
    #         else:
    #             raise ValueError(f'{team} is not a valid team or ID!')

    #     url = self._build_url(f'teams / {team} / players')
    #     players = requests.get(url, headers=self.headers).json()

    #     return [Player(player, team) for player in players['players']]

    def _build_url(self, action, query_params=None):
        """
        Generates a URL for the given action, with optional query parameters
        that can be used to filter the response.
        """
        # if action == "competitions" or action == "matches":
        # action += "/"

        if query_params:
            query_params = urllib.parse.urlencode(query_params)
            action = f'{action}/?{query_params}'

        url = urllib.parse.urljoin(self.API_URL, action)

        return url

    def _api_request(self, url, json_format=False):
        try:
            res_raw = requests.get(url, headers=self.headers)
            res = res_raw.json()
            if 'errorCode' in res or 'error' in res:
                msg = res['message']
                logger.error(msg)
                return False
            else:
                return res if json_format else res_raw.content
        except:
            msg = 'requests.get error'
            logger.error(msg)
            return False
