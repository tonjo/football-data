### WORK IN PROGRESS

## football_data

A Python wrapper around the [football-data API](https://www.football-data.org) **VERSION 2**

Based on amosbastian [`football`](https://github.com/amosbastian/football)

It takes a different approach, simplified, no models involved, all json responses are converted into objects, thanks to `SimpleNamespace`, so even if `football-data.org` api changes, probably no changes are required in this library.

### Installing

It's in a early stage, install it from github like so

```bash
git clone https://github.com/tonjo/football-data.git
cd football_data
pip install -e .
```

### Usage

Currently the way to use `football-data` is to instantiate a `FootballData` class using your API key by either passing it directly or setting the environment variable `FOOTBALL_DATA_API_KEY`, which can be requested [here](https://www.football-data.org/client/register)

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

## Authors

- **Amos Bastian** - _Initial work_ - [@amosbastian](https://github.com/amosbastian)
- **Antonio Mignolli** - _V2 port and rewrite_ - [@tonjo](https://github.com/tonjo)

See also the list of [contributors](https://github.com/tonjo/football-data/graphs/contributors) who participated in this project.

## License

This project is licensed under the AGPL-3.0 license - see the [LICENSE](https://github.com/tonjo/football-data/blob/master/LICENSE) file for details.

## Acknowledgements

- Daniel Freitag - creator of the [football-data API](https://www.football-data.org/)
