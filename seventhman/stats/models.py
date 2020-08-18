"""
Initialize database ORM models for flask app
"""
# this is initialized in the __init__.py file for the whole website app
from seventhman import db
from sqlalchemy.orm import column_property
from sqlalchemy import cast, String


class Pbp(db.Model):
    """
    Class to create the play by play table
    """

    __tablename__ = "pbp"
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    game_id = db.Column(db.Integer, index=True)
    eventnum = db.Column(db.Integer)
    eventmsgtype = db.Column(db.Integer)
    eventmsgactiontype = db.Column(db.Integer)
    period = db.Column(db.Integer)
    wctimestring = db.Column(db.String)
    pctimestring = db.Column(db.String)
    homedescription = db.Column(db.String)
    neutraldescription = db.Column(db.String)
    visitordescription = db.Column(db.String)
    score = db.Column(db.String)
    scoremargin = db.Column(db.String)
    person1type = db.Column(db.Integer)
    player1_id = db.Column(db.Integer)
    player1_name = db.Column(db.String)
    player1_team_id = db.Column(db.Integer)
    player1_team_city = db.Column(db.String)
    player1_team_nickname = db.Column(db.String)
    player1_team_abbreviation = db.Column(db.String)
    person2type = db.Column(db.Integer)
    player2_id = db.Column(db.Integer)
    player2_name = db.Column(db.String)
    player2_team_id = db.Column(db.Integer)
    player2_team_city = db.Column(db.String)
    player2_team_nickname = db.Column(db.String)
    player2_team_abbreviation = db.Column(db.String)
    person3type = db.Column(db.Integer)
    player3_id = db.Column(db.Integer)
    player3_name = db.Column(db.String)
    player3_team_id = db.Column(db.Integer)
    player3_team_city = db.Column(db.String)
    player3_team_nickname = db.Column(db.String)
    player3_team_abbreviation = db.Column(db.String)
    evt = db.Column(db.Integer)
    locx = db.Column(db.Integer)
    locy = db.Column(db.Integer)
    hs = db.Column(db.Integer)
    vs = db.Column(db.Integer)
    de = db.Column(db.String)
    home_team_abbrev = db.Column(db.String)
    away_team_abbrev = db.Column(db.String)
    game_date = db.Column(db.Date)
    season = db.Column(db.Integer)
    home_team_id = db.Column(db.Integer)
    away_team_id = db.Column(db.Integer)
    event_team = db.Column(db.String)
    event_type_de = db.Column(db.String)
    shot_type_de = db.Column(db.String)
    shot_made = db.Column(db.Boolean)
    is_block = db.Column(db.Boolean)
    shot_type = db.Column(db.String)
    seconds_elapsed = db.Column(db.Integer)
    event_length = db.Column(db.Integer)
    is_three = db.Column(db.Boolean)
    points_made = db.Column(db.Integer)
    is_d_rebound = db.Column(db.Boolean)
    is_o_rebound = db.Column(db.Boolean)
    is_turnover = db.Column(db.Boolean)
    is_steal = db.Column(db.Boolean)
    foul_type = db.Column(db.String)
    is_putback = db.Column(db.Boolean)
    home_player_1 = db.Column(db.String)
    home_player_1_id = db.Column(db.Integer)
    home_player_2 = db.Column(db.String)
    home_player_2_id = db.Column(db.Integer)
    home_player_3 = db.Column(db.String)
    home_player_3_id = db.Column(db.Integer)
    home_player_4 = db.Column(db.String)
    home_player_4_id = db.Column(db.Integer)
    home_player_5 = db.Column(db.String)
    home_player_5_id = db.Column(db.Integer)
    away_player_1 = db.Column(db.String)
    away_player_1_id = db.Column(db.Integer)
    away_player_2 = db.Column(db.String)
    away_player_2_id = db.Column(db.Integer)
    away_player_3 = db.Column(db.String)
    away_player_3_id = db.Column(db.Integer)
    away_player_4 = db.Column(db.String)
    away_player_4_id = db.Column(db.Integer)
    away_player_5 = db.Column(db.String)
    away_player_5_id = db.Column(db.Integer)

    __table_args__ = {"schema": "nba"}


class playerbygamestats(db.Model):
    """
    Class to create the playerbygamestats table which is each players
    box score for every game they played in.
    """

    __tablename__ = "playerbygamestats"
    __table_args__ = {"schema": "nba"}
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    team_id = db.Column(db.Integer)
    game_id = db.Column(db.Integer, primary_key=True, nullable=False)
    game_date = db.Column(db.Date)
    toc = db.Column(db.Integer)
    toc_string = db.Column(db.String)
    fgm = db.Column(db.Integer)
    fga = db.Column(db.Integer)
    tpm = db.Column(db.Integer)
    tpa = db.Column(db.Integer)
    ftm = db.Column(db.Integer)
    fta = db.Column(db.Integer)
    points = db.Column(db.Integer)
    ast = db.Column(db.Integer)
    oreb = db.Column(db.Integer)
    dreb = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    tov = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    stl = db.Column(db.Integer)
    plus = db.Column(db.Integer)
    minus = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)
    player_name = db.Column(db.String)
    possessions = db.Column(db.Integer)
    is_home = db.Column(db.Integer)
    team_abbrev = db.Column(db.String)
    opponent = db.Column(db.Integer)
    opponent_abbrev = db.Column(db.String)
    season = db.Column(db.Integer, primary_key=True, nullable=False)


class team_details(db.Model):
    """
    Class to create table for team details
    """

    __tablename__ = "team_details"
    __table_args__ = {"schema": "nba"}
    team_id = db.Column(db.Integer, primary_key=True, nullable=False)
    abbreviation = db.Column(db.String)
    nickname = db.Column(db.String)
    yearfounded = db.Column(db.Integer)
    city = db.Column(db.String)
    arena = db.Column(db.String)
    arena_capacity = db.Column(db.Integer)
    owner = db.Column(db.String)
    generalmanager = db.Column(db.String)
    headcoach = db.Column(db.String)
    dleagueaffiliation = db.Column(db.Integer)


class teambygamestats(db.Model):
    """
    Class to create the teambygamestats table which is each teams
    box score for every game they played in.
    """

    __tablename__ = "teambygamestats"
    __table_args__ = {"schema": "nba"}
    team_id = db.Column(db.Integer, primary_key=True, nullable=False)
    game_id = db.Column(db.Integer, primary_key=True, nullable=False)
    points_for = db.Column(db.Integer)
    tpa = db.Column(db.Integer)
    fga = db.Column(db.Integer)
    fta = db.Column(db.Integer)
    fgm = db.Column(db.Integer)
    tpm = db.Column(db.Integer)
    ftm = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    shots_blocked = db.Column(db.Integer)
    ast = db.Column(db.Integer)
    oreb = db.Column(db.Integer)
    dreb = db.Column(db.Integer)
    tov = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    fouls_drawn = db.Column(db.Integer)
    stl = db.Column(db.Integer)
    points_against = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)
    team_abbrev = db.Column(db.String)
    possessions = db.Column(db.Integer)
    game_date = db.Column(db.Date)
    season = db.Column(db.Integer, primary_key=True, nullable=False)
    toc = db.Column(db.Integer)
    toc_string = db.Column(db.String)
    is_home = db.Column(db.Integer)
    is_win = db.Column(db.Integer)
    opponent = db.Column(db.Integer)
    opponent_abbrev = db.Column(db.String)


class player_details(db.Model):
    """
    Class to build table with player info
    """

    __tablename__ = "player_details"
    __table_args__ = {"schema": "nba"}
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    display_first_last = db.Column(db.String)
    display_last_comma_first = db.Column(db.String)
    display_fi_last = db.Column(db.String)
    birthdate = db.Column(db.Date)
    school = db.Column(db.String)
    country = db.Column(db.String)
    last_affiliation = db.Column(db.String)
    height = db.Column(db.String)
    weight = db.Column(db.String)
    season_experience = db.Column(db.Integer)
    jersey_number = db.Column(db.String)
    position = db.Column(db.String)
    rosterstatus = db.Column(db.String)
    team_id = db.Column(db.Integer)
    team_name = db.Column(db.String)
    team_abbreviation = db.Column(db.String)
    team_code = db.Column(db.String)
    team_city = db.Column(db.String)
    playercode = db.Column(db.String)
    from_year = db.Column(db.Integer)
    to_year = db.Column(db.Integer)
    dleague_flag = db.Column(db.String)
    nba_flag = db.Column(db.String)
    games_played_flag = db.Column(db.String)
    draft_year = db.Column(db.String)
    draft_round = db.Column(db.String)
    draft_number = db.Column(db.String)


class player_advanced(db.Model):
    """
    creates table for player advanced stats
    """

    __tablename__ = "player_advanced_stats"
    __table_args__ = {"schema": "nba"}
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_name = db.Column(db.String)
    team_abbrev = db.Column(db.String)
    gp = db.Column(db.Integer)
    off_rating = db.Column(db.Numeric)
    def_rating = db.Column(db.Numeric)
    efg_percent = db.Column(db.Numeric)
    ts_percent = db.Column(db.Numeric)
    oreb_percent = db.Column(db.Numeric)
    dreb_percent = db.Column(db.Numeric)
    ast_percent = db.Column(db.Numeric)
    blk_percent = db.Column(db.Numeric)
    stl_percent = db.Column(db.Numeric)
    tov_percent = db.Column(db.Numeric)
    usg_percent = db.Column(db.Numeric)
    min_season = db.Column(db.Integer, primary_key=True, nullable=False)
    max_season = db.Column(db.Integer, primary_key=True, nullable=False)


class team_advanced(db.Model):
    """
    creates table for team advanced stats
    """

    __tablename__ = "team_advanced_stats"
    __table_args__ = {"schema": "nba"}
    team_id = db.Column(db.Integer, primary_key=True, nullable=False)
    team_abbrev = db.Column(db.String)
    gp = db.Column(db.Integer)
    efg_percentage = db.Column(db.Numeric)
    true_shooting_percentage = db.Column(db.Numeric)
    oreb_percentage = db.Column(db.Numeric)
    ft_per_fga = db.Column(db.Numeric)
    tov_percentage = db.Column(db.Numeric)
    opp_efg_percentage = db.Column(db.Numeric)
    opp_tov_percentage = db.Column(db.Numeric)
    dreb_percentage = db.Column(db.Numeric)
    opp_ft_per_fga = db.Column(db.Numeric)
    off_rating = db.Column(db.Numeric)
    def_rating = db.Column(db.Numeric)
    min_season = db.Column(db.Integer, primary_key=True, nullable=False)
    max_season = db.Column(db.Integer)


class player_single_year_rapm(db.Model):
    """
    creates table for player single year rapm stats
    """

    __tablename__ = "player_single_year_rapm"
    __table_args__ = {"schema": "nba"}
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    rapm_off = db.Column(db.Numeric)
    rapm_def = db.Column(db.Numeric)
    rapm = db.Column(db.Numeric)
    rapm_rank = db.Column(db.Integer)
    rapm_off_rank = db.Column(db.Integer)
    rapm_def_rank = db.Column(db.Integer)
    player_name = db.Column(db.String)
    min_season = db.Column(db.Integer, primary_key=True, nullable=False)
    max_season = db.Column(db.Integer)


class player_multi_year_rapm(db.Model):
    """
    creates table for player multi year rapm stats
    """

    __tablename__ = "player_three_year_rapm"
    __table_args__ = {"schema": "nba"}
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    rapm_off = db.Column(db.Numeric)
    rapm_def = db.Column(db.Numeric)
    rapm = db.Column(db.Numeric)
    rapm_rank = db.Column(db.Integer)
    rapm_off_rank = db.Column(db.Integer)
    rapm_def_rank = db.Column(db.Integer)
    player_name = db.Column(db.String)
    min_season = db.Column(db.Integer, primary_key=True, nullable=False)
    max_season = db.Column(db.Integer, primary_key=True, nullable=False)
    seasons = column_property(cast(min_season, String) + "-" + cast(max_season, String))


class team_single_year_rapm(db.Model):
    """
    creates table for player single year rapm stats
    """

    __tablename__ = "team_single_year_rapm"
    __table_args__ = {"schema": "nba"}
    team_id = db.Column(db.Integer, primary_key=True, nullable=False)
    rapm_off = db.Column(db.Numeric)
    rapm_def = db.Column(db.Numeric)
    rapm = db.Column(db.Numeric)
    rapm_rank = db.Column(db.Integer)
    rapm_off_rank = db.Column(db.Integer)
    rapm_def_rank = db.Column(db.Integer)
    team_abbrev = db.Column(db.String)
    min_season = db.Column(db.Integer, primary_key=True, nullable=False)
    max_season = db.Column(db.Integer)


class shot_locations(db.Model):
    """
    model for the shot locations table
    """

    __tablename__ = "shot_locations"
    __table_args__ = {"schema": "nba"}
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    grid_type = db.Column(db.String)
    game_id = db.Column(db.Integer)
    game_event_id = db.Column(db.Integer)
    player_id = db.Column(db.Integer)
    player_name = db.Column(db.String)
    team_id = db.Column(db.Integer)
    team_name = db.Column(db.String)
    period = db.Column(db.Integer)
    minutes_remaining = db.Column(db.Integer)
    seconds_remaining = db.Column(db.Integer)
    event_type = db.Column(db.String)
    action_type = db.Column(db.String)
    shot_type = db.Column(db.String)
    shot_zone_basic = db.Column(db.String)
    shot_zone_area = db.Column(db.String)
    shot_zone_range = db.Column(db.String)
    shot_distance = db.Column(db.Integer)
    loc_x = db.Column(db.Integer)
    loc_y = db.Column(db.Integer)
    shot_attempted_flag = db.Column(db.Integer)
    shot_made_flag = db.Column(db.Integer)
    game_date = db.Column(db.Integer)
    htm = db.Column(db.String)
    vtm = db.Column(db.String)


class seasons(db.Model):
    """
    player seasons for multi rapm regressions and gp
    """

    __tablename__ = "player_seasons"
    __table_args__ = {"schema": "nba"}
    player_id = db.Column(db.Integer, primary_key=True)
    gp = db.Column(db.Integer, primary_key=True)
    teams = db.Column(db.String, primary_key=True)
    seasons = db.Column(db.String, primary_key=True)
    min_season = db.Column(db.Integer, primary_key=True)


class pa_stats_view(db.Model):
    """
    materialized view for player advanced stats
    """

    __tablename__ = "pa_stas_view"
    __table_args__ = {"schema": "nba"}
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_name = db.Column(db.String)
    team_abbrev = db.Column(db.String)
    gp = db.Column(db.Integer)
    position = db.Column(db.String)
    off_rating = db.Column(db.Numeric)
    def_rating = db.Column(db.Numeric)
    efg_percent = db.Column(db.Numeric)
    ts_percent = db.Column(db.Numeric)
    oreb_percent = db.Column(db.Numeric)
    dreb_percent = db.Column(db.Numeric)
    ast_percent = db.Column(db.Numeric)
    blk_percent = db.Column(db.Numeric)
    stl_percent = db.Column(db.Numeric)
    tov_percent = db.Column(db.Numeric)
    usg_percent = db.Column(db.Numeric)
    min_season = db.Column(db.Integer, primary_key=True, nullable=False)
    max_season = db.Column(db.Integer, primary_key=True, nullable=False)


class per_game_stats(db.Model):
    __tablename__ = "per_game_stats"
    __table_args__ = {"schema": "nba"}
    player_name = db.Column(db.String, primary_key=True)
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    position = db.Column(db.String, primary_key=True)
    season = db.Column(db.Integer, primary_key=True, nullable=False)
    teams = db.Column(db.String, primary_key=True)
    mins = db.Column(db.Numeric)
    fgm = db.Column(db.Integer)
    fga = db.Column(db.Integer)
    tpm = db.Column(db.Integer)
    tpa = db.Column(db.Integer)
    ftm = db.Column(db.Integer)
    fta = db.Column(db.Integer)
    oreb = db.Column(db.Integer)
    dreb = db.Column(db.Integer)
    ast = db.Column(db.Integer)
    tov = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    stl = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    points = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)


class per_poss_stats(db.Model):
    __tablename__ = "per_poss_stats"
    __table_args__ = {"schema": "nba"}
    player_name = db.Column(db.String, primary_key=True)
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    position = db.Column(db.String, primary_key=True)
    season = db.Column(db.Integer, primary_key=True, nullable=False)
    teams = db.Column(db.String, primary_key=True)
    mins = db.Column(db.Numeric)
    fgm = db.Column(db.Integer)
    fga = db.Column(db.Integer)
    tpm = db.Column(db.Integer)
    tpa = db.Column(db.Integer)
    ftm = db.Column(db.Integer)
    fta = db.Column(db.Integer)
    oreb = db.Column(db.Integer)
    dreb = db.Column(db.Integer)
    ast = db.Column(db.Integer)
    tov = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    stl = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    points = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)


class player_single_rapm_view(db.Model):

    __tablename__ = "player_single_rapm_view"
    __table_args__ = {"schema": "nba"}
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    rapm_off = db.Column(db.Numeric)
    rapm_def = db.Column(db.Numeric)
    rapm = db.Column(db.Numeric)
    rapm_rank = db.Column(db.Integer)
    rapm_off_rank = db.Column(db.Integer)
    rapm_def_rank = db.Column(db.Integer)
    player_name = db.Column(db.String)
    min_season = db.Column(db.Integer, primary_key=True, nullable=False)
    max_season = db.Column(db.Integer)
    gp = db.Column(db.Integer)
    teams = db.Column(db.String)


class player_multi_rapm_view(db.Model):

    __tablename__ = "player_multi_rapm_view"
    __table_args__ = {"schema": "nba"}
    player_id = db.Column(db.Integer, primary_key=True, nullable=False)
    rapm_off = db.Column(db.Numeric)
    rapm_def = db.Column(db.Numeric)
    rapm = db.Column(db.Numeric)
    rapm_rank = db.Column(db.Integer)
    rapm_off_rank = db.Column(db.Integer)
    rapm_def_rank = db.Column(db.Integer)
    player_name = db.Column(db.String)
    min_season = db.Column(db.Integer, primary_key=True, nullable=False)
    max_season = db.Column(db.Integer)
    gp = db.Column(db.Integer)
    teams = db.Column(db.String)


def main():
    pass


if __name__ == "__main__":
    main()
