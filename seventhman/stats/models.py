'''
Initialize database ORM models for flask app
'''
#this is initialized in the __init__.py file for the whole website app
from seventhman import db

class Pbp(db.Model):
    '''
    Class to create the play by play table
    '''
    __tablename__ = 'pbp'
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

    __table_args__ = {'schema': 'nba'}


class playerbygamestats(db.Model):
    '''
    Class to create the playerbygamestats table which is each players
    box score for every game they played in.
    '''
    __tablename__ = 'playerbygamestats'
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    season = db.Column(db.Integer)
    game_date = db.Column(db.Date)
    game_id = db.Column(db.Integer)
    player_id = db.Column(db.Integer)
    player_name = db.Column(db.String)
    team_abbrev = db.Column(db.String)
    team_id = db.Column(db.Integer)
    toc = db.Column(db.Integer)
    toc_string = db.Column(db.String)
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
    stl = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    points = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)
    __table_args__ = {'schema': 'nba'}

class team_details(db.Model):
    '''
    Class to create table for team details
    '''
    __tablename__ = 'team_details'
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
    __table_args__ = {'schema': 'nba'}

class teambygamestats(db.Model):
    '''
    Class to create the teambygamestats table which is each teams
    box score for every game they played in.
    '''
    __tablename__ = 'teambygamestats'
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    season = db.Column(db.Integer)
    game_date = db.Column(db.Date)
    game_id = db.Column(db.Integer)
    team_abbrev = db.Column(db.String)
    team_id = db.Column(db.Integer)
    toc = db.Column(db.Integer)
    toc_string = db.Column(db.String)
    points_for = db.Column(db.Integer)
    points_against = db.Column(db.Integer)
    is_win = db.Column(db.Integer)
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
    stl = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    shots_blocked = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    pf_drawn = db.Column(db.Integer)
    points = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)
    is_home = db.Column(db.Integer)
    __table_args__ = {'schema': 'nba'}

class player_details(db.Model):
    '''
    Class to build table with player info
    '''
    __tablename__ = 'player_details'
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
    __table_args__ = {'schema': 'nba'}

class player_possessions(db.Model):
    '''
    creates table for player possesions totals
    '''
    __tablename__ = 'player_possessions'
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    player_id = db.Column(db.Integer)
    player_name = db.Column(db.String)
    game_id = db.Column(db.Integer)
    team_id = db.Column(db.Integer)
    possessions = db.Column(db.Integer)
    __table_args__ = {'schema': 'nba'}

class team_possessions(db.Model):
    '''
    creates table for player possesions totals
    '''
    __tablename__ = 'team_possessions'
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    team_id = db.Column(db.Integer)
    game_id = db.Column(db.Integer)
    team_abbrev = db.Column(db.String)
    possessions = db.Column(db.Integer)
    __table_args__ = {'schema': 'nba'}

class player_advanced(db.Model):
    '''
    creates table for player advanced stats
    '''
    __tablename__ = 'player_advanced_stats'
    __table_args__ = {'schema': 'nba'}
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    player_id = db.Column(db.Integer)
    season = db.Column(db.Integer)
    team_abbrev = db.Column(db.String)
    efg_percentage = db.Column(db.Numeric)
    true_shooting_percentage = db.Column(db.Numeric)
    oreb_percentage = db.Column(db.Numeric)
    dreb_percentage = db.Column(db.Numeric)
    treb_percentage = db.Column(db.Numeric)
    ast_percentage = db.Column(db.Numeric)
    stl_percentage = db.Column(db.Numeric)
    blk_percentage = db.Column(db.Numeric)
    tov_percentage = db.Column(db.Numeric)
    usg_percentage = db.Column(db.Numeric)
    off_rating = db.Column(db.Numeric)
    def_rating = db.Column(db.Numeric)

class team_advanced(db.Model):
    '''
    creates table for team advanced stats
    '''
    __tablename__ = 'team_advanced_stats'
    __table_args__ = {'schema': 'nba'}
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    team_id = db.Column(db.Integer)
    team_abbrev = db.Column(db.String)
    season = db.Column(db.Integer)
    efg_percentage = db.Column(db.Numeric)
    true_shooting_percentage = db.Column(db.Numeric)
    tov_percentage = db.Column(db.Numeric)
    oreb_percentage = db.Column(db.Numeric)
    ft_per_fga = db.Column(db.Numeric)
    opp_efg_percentage = db.Column(db.Numeric)
    opp_tov_percentage = db.Column(db.Numeric)
    dreb_percentage = db.Column(db.Numeric)
    opp_ft_per_fga = db.Column(db.Numeric)
    off_rating = db.Column(db.Numeric)
    def_rating = db.Column(db.Numeric)

class player_single_year_rapm(db.Model):
    '''
    creates table for player single year rapm stats
    '''
    __tablename__ = 'player_single_year_rapm'
    __table_args__ = {'schema': 'nba'}
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    player_id = db.Column(db.Integer)
    season = db.Column(db.Integer)
    rapm_off = db.Column(db.Numeric)
    rapm_def = db.Column(db.Numeric)
    rapm = db.Column(db.Numeric)
    rapm_rank = db.Column(db.Integer)
    rapm_off_rank = db.Column(db.Integer)
    rapm_def_rank = db.Column(db.Integer)
    player_name = db.Column(db.String)

class player_multi_year_rapm(db.Model):
    '''
    creates table for player multi year rapm stats
    '''
    __tablename__ = 'player_multi_year_rapm'
    __table_args__ = {'schema': 'nba'}
    key_col = db.Column(db.String, primary_key=True, nullable=False)
    player_id = db.Column(db.Integer)
    season = db.Column(db.String)
    rapm_off = db.Column(db.Numeric)
    rapm_def = db.Column(db.Numeric)
    rapm = db.Column(db.Numeric)
    rapm_rank = db.Column(db.Integer)
    rapm_off_rank = db.Column(db.Integer)
    rapm_def_rank = db.Column(db.Integer)
    player_name = db.Column(db.String)

def main():
    pass


if __name__ == '__main__':
    main()
