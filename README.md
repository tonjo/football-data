
# ⚰️ DEPRECATED
### included directly in other projects

## football_data

A Python wrapper around the [football-data API](https://www.football-data.org) **VERSION 2**

Based on amosbastian [`football`](https://github.com/amosbastian/football)

It takes a different approach, simplified, _schema-less_ (no models involved), all json responses are converted into objects, thanks to `SimpleNamespace`, so even if `football-data.org` API changes, hopefully no changes are required in this package (endpoints excluded).

## Install

It's in a early stage, install it from github:

```bash
git clone https://github.com/tonjo/football-data.git
cd football_data
pip install -e .
```

## Usage

Currently the way to use `football-data` is to instantiate a `FootballData` class using your API key by either passing it directly or setting the environment variable `FOOTBALL_DATA_API_KEY`, which can be requested [here](https://www.football-data.org/client/register)

```python
from football_data import FootballData
football = FootballData('your_api_key')
```

The following (sub) resources are available

## Competitions

```python
# All
competitions = football.competitions()

# Specific one with id
competition = football.competition(2000)
print(f'{competition.code}, {competition.name}, {competition.area.name}')

# ... or code (WC = World Cup)
competition = football.competition('WC)
print(f'{competition.code}, {competition.name}, {competition.area.name}')

```

#### For all competition codes look into

- [API Reference](https://www.football-data.org/documentation/api)
  (search for Appendix Table of League-Codes)

## Competition matches

List all matches for a particular competition.

```python

matches = football.competition_matches(2019)
# OR
matches = football.competition_matches('CL')

# Filter for a particular status
matches = football.competition_matches('CL', status='FINISHED')

```

### Available arguments (filters):

- dateFrom
- dateTo
- stage
- status
- matchday
- group
- season

## Competition teams

List all teams for a particular competition.

```python
teams = football.competition_teams(2019)
# OR
teams = football.competition_teams('SA')
for team in teams:
  print(team.name)

```

### Available arguments (filters):

- season
- stage

## Matches

List matches across (a set of) competitions.

```python

# Today's matches, any competition available
matches = football.matches()

# Today's matches, premier league only (code or id)
matches = football.matches(competitions='PL')

# Specific time frame matches, premier league and Champions League
matches = football.matches(competitions='PL,CL', dateFrom='2020-03-03', dateTo='2020-03-04')


# Single match
match = football.match(200063)
```

### Available arguments (filters):

- competitions
- dateFrom
- dateTo
- status

## Team

Show one particular team.

```python
team = self.football.team(450)

```

## Team Matches

Show all matches for a particular team.

```python
matches = self.football.matches('SA')
print(f'found {len(matches)} matches for competition "SA"')
```

# TODO

- Standings
- Scorers
- Areas
- Players
- Player matches

---

# Football-Api official resources list

Please consult official docs:

- [Quick start](https://www.football-data.org/documentation/quickstart)
- [API Reference](https://www.football-data.org/documentation/api)

### Match statuses

From [https://www.football-data.org/assets/v2_status_diagram.png](https://www.football-data.org/assets/v2_status_diagram.png)

![Match statuses](https://www.football-data.org/assets/v2_status_diagram.png)

## Contributing

Please read [CONTRIBUTING.md](https://github.com/tonjo/football-data/blob/master/CONTRIBUTING.md) for details on how to contribute to `football-data` and what the best way to go about this is!

## Authors

- **Amos Bastian** - _Initial work_ - [@amosbastian](https://github.com/amosbastian)
- **Antonio Mignolli** - _V2 port and rewrite_ - [@tonjo](https://github.com/tonjo)

See also the list of [contributors](https://github.com/tonjo/football-data/graphs/contributors) who participated in this project.

## License

This project is licensed under the AGPL-3.0 license - see the [LICENSE](https://github.com/tonjo/football-data/blob/master/LICENSE) file for details.

## Acknowledgements

- Daniel Freitag - creator of the [football-data API](https://www.football-data.org/)
