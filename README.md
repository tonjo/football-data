## football

A Python wrapper around the [football-data API](https://www.football-data.org) **VERSION 2**

Based on amosbastian [`football`](https://github.com/amosbastian/football)

It takes a different approach, simplified, no models involved, all json responses are converted into objects, thanks to `SimpleNamespace`, so even if `football-data.org` api changes, probably no changes are required in this library.

### Installing

It's in a early stage, install it from githubmode like so

```bash
git clone https://github.com/tonjo/football-data.git
cd football_data
pip install -e .
```

### Usage

### WORK IN PROGRESS

Currently the way to use `football-data` is to instantiate a `FootballData` class using your API key by either passing it directly or setting the environment variable `FOOTBALL_API_KEY`, which can be requested [here](https://www.football-data.org/client/register)

```python
from football_data import FootballData
football = FootballData('your_api_key')
```

The following (sub) resources are available

### Get all available competitions

```python
# All
competitions = football.competitions()
# Specific one with id
competition = football.competition(2015)
print(competition.name)
print(competition.area.name)
```

### MORE to come

## Contributing

Please read [CONTRIBUTING.md](https://github.com/tonjo/football-data/blob/master/CONTRIBUTING.md) for details on how to contribute to `football` and what the best way to go about this is!

## Roadmap

- ~~Create classes for each (sub) resource~~
- Add helper functions
- Improve the use of filters
- Add utilities for team/league/competition codes, names etc.
- Create proper documentation
- Include a CLI

## Authors

- **Amos Bastian** - _Initial work_ - [@amosbastian](https://github.com/amosbastian)

See also the list of [contributors](https://github.com/amosbastian/football/graphs/contributors) who participated in this project.

## Changelog

#### 0.1.1 - 2018-05-14

##### Added

- Initial release - contains functions for each (sub) resource of the football-data API, including filtering

#### 0.2.0 - 2018-06-10

##### Updated

- All sub resources are now classes including functions to call retrieve additional information
- Team related functions can now use the name, shortname or code of the team instead of just its ID
- FootballData functions use classes instead
- Unit tests for each function changed to test respective classes

##### Added

- Helper functions for Table and Team classes

## License

This project is licensed under the AGPL-3.0 license - see the [LICENSE](https://github.com/tonjo/football-data/blob/master/LICENSE) file for details.

## Acknowledgements

- Daniel Freitag - creator of the [football-data API](https://www.football-data.org/)
