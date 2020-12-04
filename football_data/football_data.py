"""
Contains the FootballData class used to interact with the API.
"""
import os
import re
import requests
import urllib.parse

from .constants import LEAGUE_CODE, TEAM_ID
from .utils import json2obj

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
            if 'FOOTBALL_API_KEY' in os.environ:
                api_key = os.environ['FOOTBALL_API_KEY']
            else:
                raise ValueError(
                    'FOOTBALL_API_KEY environment variable not set or no API key given.')

        self.api_key = api_key
        self.headers = {'X-Auth-Token': api_key}

    def competitions(self):
        """
        Returns a list of all the available competitions.
        """

        url = self._generate_url('competitions')
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

        url = self._generate_url(f'competitions/{competition}')
        res = self._api_request(url)

        if res:
            json_tmp = json2obj(res)
            competition = json_tmp
        else:
            competition = None
        return competition

    def competition_teams(self, competition=None):
        """
        Returns a list of Team objects of teams that are playing in the given
        competition.
        """
        # competition could be an id or a code like 'WC'

        if competition:
            url = self._generate_url(f'competitions/{competition}/teams')
            res = self._api_request(url)
            if res:
                json_tmp = json2obj(res)
                return json_tmp.teams
            else:
                logger.error(f'teams: no data found')
                return None
        else:
            logger.error(f'teams: specify competition')
            return None

    def competition_matches(self, competition, time_frame=None):
        """
        Returns a list of Match objects made from the matches of the given
        competition.
        """
        # Allow users to use both id or name
        if isinstance(competition, str):
            try:
                competition = LEAGUE_CODE[competition]
            except KeyError as error:
                return error

        query_params = {}

        # Error checking for query parameter time_frame
        if time_frame:
            time_frame = str(time_frame)
            pattern = re.compile(r"p | n[1 - 9]{1, 2}")
            if not pattern.match(time_frame):
                raise ValueError('time_frame is invalid.')
            query_params['timeFrame'] = time_frame

        url = self._generate_url(
            f'competitions/{competition}/matches', query_params)

        # res = requests.get(url, headers=self.headers)  # .json()
        res = self._api_request(url, False)
        json_tmp = json2obj(res)
        return json_tmp.matches

    def matches(self, time_frame=None, league_code=None):
        """
        Returns a list of Match objects made from the matches across either
        all competitions or a specific league.
        """
        query_params = {}
        # Error checking for query parameter time_frame
        if time_frame:
            time_frame = str(time_frame)
            pattern = re.compile(r"p | n[1 - 9]{1, 2}")
            if not pattern.match(time_frame):
                raise ValueError('time_frame is invalid.')
            query_params['timeFrame'] = time_frame

        # Error checking for query parameter league_code
        if league_code:
            if league_code not in LEAGUE_CODE.keys():
                raise ValueError('league_code is invalid.')
            query_params['league'] = league_code

        url = self._generate_url('matches', query_params)
        matches = requests.get(url, headers=self.headers).json()

        return [Match(match) for match in res['matches']]

    def match(self, match_id):
        """
        Returns a Match object of the match with the given ID.
        """
        url = self._generate_url(f'matches/{match_id}')
        match = requests.get(url, headers=self.headers).json()
        return Match(match['match'])

    def team_matches(self, team, season=None, time_frame=None, venue=None):
        """
        Returns a list of Match objects made from the matches of the team
        with the given ID, in a certain season, time frame or venue.
        """
        # If string try to convert to ID
        if isinstance(team, str):
            if team.lower() in TEAM_ID.keys():
                team = TEAM_ID[team.lower()]
            else:
                raise ValueError(f'{team} is not a valid team or ID!')

        query_params = {}
        # Error checking for query parameter season
        if season:
            season = str(season)
            pattern = re.compile(r"\d\d\d\d")
            if not pattern.match(season):
                raise ValueError('season is invalid.')
            query_params['season'] = season

        # Error checking for query parameter time_frame
        if time_frame:
            time_frame = str(time_frame)
            pattern = re.compile(r"p | n[1 - 9]{1, 2}")
            if not pattern.match(time_frame):
                raise ValueError('time_frame is invalid.')
            query_params['timeFrame'] = time_frame

        # Error checking for query parameter venue
        if venue:
            if venue not in ('home', 'away'):
                raise ValueError('venue is invalid.')
            query_params['venue'] = venue

        url = self._generate_url(f'teams / {team} / matches', query_params)
        matches = requests.get(url, headers=self.headers).json()

        return [Match(match) for match in matches['matches']]

    def team(self, team):
        """
        Returns a Team object made from the given team.
        """
        # If string try to convert to ID
        if isinstance(team, str):
            if team.lower() in TEAM_ID.keys():
                team = TEAM_ID[team.lower()]
            else:
                raise ValueError(f'{team} is not a valid team or ID!')

        url = self._generate_url(f'teams / {team}')
        team = requests.get(url, headers=self.headers).json()
        return Team(team)

    def players(self, team):
        """
        Returns a list of Player objects made from players playing for the team
        with the given ID.
        """
        # If string try to convert to ID
        if isinstance(team, str):
            if team.lower() in TEAM_ID.keys():
                team = TEAM_ID[team.lower()]
            else:
                raise ValueError(f'{team} is not a valid team or ID!')

        url = self._generate_url(f'teams / {team} / players')
        players = requests.get(url, headers=self.headers).json()

        return [Player(player, team) for player in players['players']]

    def _generate_url(self, action, query_params=None):
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
