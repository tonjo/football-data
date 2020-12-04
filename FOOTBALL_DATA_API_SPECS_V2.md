### WORK IN PROGRESS

# Resources

Taken from [official docs](https://www.football-data.org/documentation/api)

## Competitions

### Available filters:

- competitions

### Available Subresources:

- Matches (shows all matches of that competition. Defaults to the current season; use ?season=YYYY to retrieve former seasons)
- Teams (shows all teams of that competition. Defaults to the current season by default; use ?season=YYYY to retrieve former seasons))
- Standings (shows latest tables (total, home, away) for the current season; not yet available for former seasons)
- Scorers (shows all goal scorers by shot goals descending for the current season)

## Matches

### Available filters:

- competitions
- status
- stage
- group
- dateFrom + dateTo

### Match statuses

From [https://www.football-data.org/assets/v2_status_diagram.png](https://www.football-data.org/assets/v2_status_diagram.png)

![systeMatch statuses](https://www.football-data.org/assets/v2_status_diagram.png)

## Teams

## Standings

## Players

### Available Subresources:

- Matches (shows all matches of that player in all active competitions)

### Available Filters:

### TODO

| Filter | Possible value(s) | Description                    |
| ------ | ----------------- | ------------------------------ |
| id     | Integer /[0-9]+/  | The (unique) id of a resource. |
