## We have updated to version 2.0! This means the API will return stats from seasons dating all the way back from 19992000

# Seventhman.net API

All endpoints will start with `https://stats.theseventhman.net/stats/api/v2/` an
example link looks like this `https://stats.theseventhman.net/stats/api/v2/players/?&season=2020&player=&toc=&team=&agg=no`

# players/

This endpoint returns the per game stats of players in the database. If you want
to pass more than one parameter than join them with a `+` operator such as
`&season=2018+2019`. `agg` and `toc` only take one parameter.

Arguments:
* player - the player id you want the per game stats of if left blank returns all players.
* season - the season you want if left blank returns all seasons
* toc - the time on court cut off for stats in minutes. If you pass 24 this returns per
game stats of the players in which they play more than 24 minutes in that game
* team - filters results by team id
* agg - denotes whether the results will be aggregated over the time frame or returned
on a season by season basis. Pass either a `yes` or `no` parameter

# players/shots/

This returns the shot descriptions for each player in the database. If you leave player
blank it will default to Stephen Curry to prevent excess strain on the database.

* player - the player id you want the per game stats of if left blank returns all players.
* season - the season you want if left blank returns all seasons
* team - filters results by team id

# players/possession/

Returns player possession stats based on per 100 possessions

* player - the player id you want the per game stats of if left blank returns all players.
* season - the season you want if left blank returns all seasons
* toc - the time on court cut off for stats in minutes. If you pass 24 this returns per
game stats of the players in which they play more than 24 minutes in that game
* team - filters results by team id
* agg - denotes whether the results will be aggregated over the time frame or returned
on a season by season basis. Pass either a `yes` or `no` parameter

# teams/

* season - the season you want if left blank returns all seasons
* team - filters results by team id
* agg - denotes whether the results will be aggregated over the time frame or returned
on a season by season basis. Pass either a `yes` or `no` parameter

# teams/possession/

Returns team possession stats based on per 100 possessions

* season - the season you want if left blank returns all seasons
* team - filters results by team id
* agg - denotes whether the results will be aggregated over the time frame or returned
on a season by season basis. Pass either a `yes` or `no` parameter

# teams/advanced/

Returns team advanced stats only calculated at a season level

* season - the season you want if left blank returns all seasons
* team - filters results by team id

# players/advanced/

Returns player advanced stats only calculated at a season level

* season - the season you want if left blank returns all seasons
* player - filters results by player id

# players/rapm/

* season - the season you want if left blank returns all seasons
* player - filters results by player id

# teams/rapm/

* season - the season you want if left blank returns all seasons
* team - filters results by team id

# players/multirapm/

* player - filters results by player id
* min_season - pass the first season in the three year block you want to pull back.
If you want the RAPM for 2018, 2019, 2020 three year span then pass 2018.

# teams/all/

Returns all team ids along with the team abbreviation associated with each id

# seasons/all/

Returns all seasons included in the database

# multirapmseasons/all/

returns all the multi year rapm seasons in the database

# players/distinct/

returns all the distinct player ids and player names in the database


