"""
Contains unit tests for all functions in football.py.
"""
import os
import unittest
from football_data import FootballData


class FootballDataTest(unittest.TestCase):
    """
    Class for unit testing football.py.
    """
    football = FootballData(os.environ.get('FOOTBALL_DATA_API_KEY'))

    def test_competitions(self):
        """
        Tests for the football.competitions function.
        """
        # General tests
        competitions = self.football.competitions()
        self.assertIsInstance(competitions, list)
        if not isinstance(competitions, list):
            return False
        competition = competitions[0]
        self.assertEqual(competition.id, 2006)
        self.assertEqual(competition.name, 'WC Qualification')
        self.assertEqual(competition.numberOfAvailableSeasons, 2)
        self.assertEqual(competition.area.id, 2001)
        self.assertEqual(competition.area.name, 'Africa')

    def test_competition(self):
        """
        Tests for the football.competition function.
        """
        # General tests
        competition = self.football.competition(2001)
        self.assertEqual(competition.id, 2001)
        self.assertEqual(competition.name, 'UEFA Champions League')
        self.assertEqual(competition.code, 'CL')
        self.assertEqual(len(competition.seasons), 20)
        self.assertEqual(competition.area.id, 2077)
        self.assertEqual(competition.area.name, 'Europe')

        competition = self.football.competition('WC')
        self.assertEqual(competition.name, 'FIFA World Cup')

    def test_competition_teams(self):
        """
        Tests for the football.competition_teams function.
        """

        competition_teams = self.football.competition_teams(2022)
        self.assertTrue(self.football.error['code'] == 403)

        competition_teams = self.football.competition_teams(2019)
        self.assertTrue(self.football.error['code'] == None)
        teams_short_names = [team.shortName for team in competition_teams]
        self.assertTrue('Verona' in teams_short_names)
        competition_teams = self.football.competition_teams('WC')
        teams_short_names = [team.shortName for team in competition_teams]
        self.assertTrue('France' in teams_short_names)
        # TODO Test with query parameters
        competition_teams = self.football.competition_teams('CL', season=2020)
        teams_short_names = [team.shortName for team in competition_teams]
        self.assertTrue('Celje' in teams_short_names)
        competition_teams = self.football.competition_teams('CL', season=2018)
        teams_short_names = [team.shortName for team in competition_teams]
        self.assertFalse('Celje' in teams_short_names)
        competition_teams = self.football.competition_teams(
            'CL', season=2018, stage='FINAL')
        teams_short_names = [team.shortName for team in competition_teams]
        self.assertTrue(['Liverpool', 'Tottenham'] == teams_short_names)

    def test_competition_matches(self):
        """
        Tests for the football.competition_matches function.
        """
        matches = self.football.competition_matches(2019)
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) == 380)
        matches = self.football.competition_matches('WC')
        self.assertTrue(len(matches) == 64)

        matches = self.football.competition_matches(
            'WC', dateFrom='2018-07-08', dateTo='2018-07-15')
        self.assertTrue(len(matches) == 4)

        # Only one dateFrom/dateTo, not both
        matches = self.football.competition_matches(
            'WC', dateFrom='2018-07-08')
        self.assertTrue(matches == [])

        matches = self.football.competition_matches(
            'WC', dateTo='2018-07-08')
        self.assertTrue(matches == [])

        # Invalid dateFrom format
        matches = self.football.competition_matches(
            'WC', dateFrom='201-0-0', dateTo='2020-01-01')
        self.assertTrue(matches == [])

        # Season, stage, group
        matches = self.football.competition_matches(
            'CL', season=2019, stage='PRELIMINARY_SEMI_FINALS', group='Preliminary Semi-finals')
        self.assertIsInstance(matches, list)
        self.assertTrue(matches[0].id == 266391)

    def test_matches(self):
        """
        Tests for the football.matches function.
        """
        # General tests
        matches = self.football.matches('SA')
        self.assertIsInstance(matches, list)
        if len(matches) > 0:
            self.assertEqual(matches[0].homeTeam.name, 'Spezia Calcio')

    def test_match(self):
        """
        Tests for the football.matches function.
        """
        # General tests
        match = self.football.match(266391)
        self.assertEqual(match.venue, 'Stadiumi Fadil Vokrri')
        self.assertEqual(match.score.winner, 'AWAY_TEAM')

    def test_team(self):
        """
        Tests for the football.team function.
        """
        # General tests
        team = self.football.team(450)
        self.assertEqual(team.name, 'Hellas Verona FC')
        self.assertEqual(team.founded, 1903)

    def test_team_matches(self):
        """
        Tests for the football.team_matches function.
        """
        # General tests
        team_matches = self.football.team_matches(450)
        self.assertIsInstance(team_matches, list)
        if len(team_matches) > 0:
            self.assertEqual(team_matches[0].id, 309596)

        team_matches = self.football.team_matches(450, venue='AWAY')
        self.assertEqual(len(team_matches), 19)
        team_matches = self.football.team_matches(450, limit=5)
        self.assertEqual(len(team_matches), 5)

        # Test invalid filters
        team_matches = self.football.team_matches(450, venue='INVALID')
        self.assertEqual(len(team_matches), 0)
        team_matches = self.football.team_matches(450, limit='a')
        self.assertEqual(len(team_matches), 0)

        # TODO test status and dateFrom/dateTo

    def test__build_url(self):
        """
        Tests for the football._build_url function.
        """
        # General tests
        url = self.football._build_url('competitions')
        self.assertEqual(url, 'https://api.football-data.org/v4/competitions')
        url = self.football._build_url('competitions', {'season': 2015})
        self.assertEqual(
            url, 'https://api.football-data.org/v4/competitions/?season=2015')
        url = self.football._build_url(
            'competitions/2015/matches', {'matchday': 1, 'status': 'FINISHED'})
        self.assertEqual(url, ('https://api.football-data.org/v4/competitions/'
                               '2015/matches/?matchday=1&status=FINISHED'))


if __name__ == '__main__':
    unittest.main()
