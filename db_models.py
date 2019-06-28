'''
Initialize database ORM models for flask app
'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


# pylint: disable=too-many-statements
def main():
    pass


if __name__ == '__main__':
    main()
