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
        Returns a list of all the available competitions.
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
        Returns a specific competition by its competition.
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
        Returns a list of Team objects of teams that are playing in the given
        competition.
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
        Returns a list of Match objects made from the matches of the given
        competition.
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
        Returns a list of Match objects made from the matches across a set of competitions.
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
        Returns a Match object of the match with the given ID.
        """
        url = self._build_url(f'matches/{match_id}')
        res = self._api_request(url)
        if res:
            json_tmp = json2obj(res)
            return json_tmp.match
        else:
            return []

    # def team_matches(self, team, season=None, dateFrom=None, venue=None):
    #     """
    #     Returns a list of Match objects made from the matches of the team
    #     with the given ID, in a certain season, time frame or venue.
    #     """
    #     # If string try to convert to ID
    #     if isinstance(team, str):
    #         if team.lower() in TEAM_ID.keys():
    #             team = TEAM_ID[team.lower()]
    #         else:
    #             raise ValueError(f'{team} is not a valid team or ID!')

    #     query_params = {}
    #     # Error checking for query parameter season
    #     if season:
    #         season = str(season)
    #         pattern = re.compile(r"\d\d\d\d")
    #         if not pattern.match(season):
    #             raise ValueError('season is invalid.')
    #         query_params['season'] = season

    #     # Error checking for query parameter dateFrom
    #     if dateFrom:
    #         dateFrom = str(dateFrom)
    #         pattern = re.compile(r"p | n[1 - 9]{1, 2}")
    #         if not pattern.match(dateFrom):
    #             raise ValueError('dateFrom is invalid.')
    #         query_params['timeFrame'] = dateFrom

    #     # Error checking for query parameter venue
    #     if venue:
    #         if venue not in ('home', 'away'):
    #             raise ValueError('venue is invalid.')
    #         query_params['venue'] = venue

    #     url = self._build_url(f'teams / {team} / matches', query_params)
    #     matches = requests.get(url, headers=self.headers).json()

    #     return [Match(match) for match in matches['matches']]

    # def team(self, team):
    #     """
    #     Returns a Team object made from the given team.
    #     """
    #     # If string try to convert to ID
    #     if isinstance(team, str):
    #         if team.lower() in TEAM_ID.keys():
    #             team = TEAM_ID[team.lower()]
    #         else:
    #             raise ValueError(f'{team} is not a valid team or ID!')

    #     url = self._build_url(f'teams / {team}')
    #     team = requests.get(url, headers=self.headers).json()
    #     return Team(team)

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
