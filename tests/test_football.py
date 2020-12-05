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
        competition_teams = self.football.competition_teams(2019)
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

#     def test_fixture(self):
#         """
#         Tests for the football.fixture function.
#         """
#         fixture = self.football.fixture(159321)
#         self.assertIsInstance(fixture, Fixture)
#         self.assertEqual(fixture.home_team, "Manchester United FC")

#     def test_team_matches(self):
#         """
#         Tests for the football.team_matches function.
#         """
#         # General tests
#         team_matches = self.football.team_matches(66)
#         self.assertIsInstance(team_matches, list)
#         if len(team_matches) > 0:
#             self.assertIsInstance(team_matches[0], Fixture)

#         # Test with query parameters
#         self.assertRaises(
#             ValueError, self.football.team_matches, 66, time_frame="abc")
#         self.assertRaises(
#             ValueError, self.football.team_matches, 66, season="abc")
#         self.assertRaises(
#             ValueError, self.football.team_matches, 66, venue="abc")

#         # Test with team name, shortname and code
#         code_matches = self.football.team_matches("MUFC")
#         shortname_matches = self.football.team_matches("ManU")
#         name_matches = self.football.team_matches("Manchester United FC")

#         self.assertEqual(team_matches[0].winner, code_matches[0].winner)
#         self.assertEqual(team_matches[0].winner, shortname_matches[0].winner)
#         self.assertEqual(team_matches[0].winner, name_matches[0].winner)

#     def test_team(self):
#         """
#         Tests for the football.team function.
#         """
#         # General tests
#         team = self.football.team(66)
#         self.assertIsInstance(team, Team)
#         self.assertEqual(team.name, "Manchester United FC")
#         self.assertEqual(team.code, "MUFC")
#         self.assertEqual(team.shortname, "ManU")

#         # Test with team name, shortname and code
#         code_team = self.football.team("MUFC")
#         shortname_team = self.football.team("ManU")
#         name_team = self.football.team("Manchester United FC")

#         self.assertEqual(team.name, code_team.name)
#         self.assertEqual(team.name, shortname_team.name)
#         self.assertEqual(team.name, name_team.name)

#     def test_players(self):
#         """
#         Tests for the football.players function.
#         """
#         # General tests
#         players = self.football.players(66)
#         self.assertIsInstance(players, list)
#         player_names = [player.name for player in players]
#         self.assertIn("Eric Bailly", player_names)

#         # Test with team name, shortname and code
#         code_players = self.football.players("MUFC")
#         shortname_players = self.football.players("ManU")
#         name_players = self.football.players("Manchester United FC")

#         self.assertEqual(players[0].name, code_players[0].name)
#         self.assertEqual(players[0].name, shortname_players[0].name)
#         self.assertEqual(players[0].name, name_players[0].name)

    def test__build_url(self):
        """
        Tests for the football._build_url function.
        """
        # General tests
        url = self.football._build_url('competitions')
        self.assertEqual(url, 'https://api.football-data.org/v2/competitions')
        url = self.football._build_url('competitions', {'season': 2015})
        self.assertEqual(
            url, 'https://api.football-data.org/v2/competitions/?season=2015')
        url = self.football._build_url(
            'competitions/2015/matches', {'matchday': 1, 'status': 'FINISHED'})
        self.assertEqual(url, ('https://api.football-data.org/v2/competitions/'
                               '2015/matches/?matchday=1&status=FINISHED'))


if __name__ == '__main__':
    unittest.main()
