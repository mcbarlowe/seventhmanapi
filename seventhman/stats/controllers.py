from flask import request, Blueprint, jsonify
from seventhman import db
from seventhman.stats.models import playerbygamestats, team_details
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy import literal_column

stats = Blueprint('stats', __name__, url_prefix='/stats')


@stats.route('api/v1/players/all/', methods=['GET'])
def api_all():
    max_season = playerbygamestats.query.with_entities(func.max(playerbygamestats.season)).all()[0][0]
    print(max_season)
    data = playerbygamestats.query.\
            with_entities(playerbygamestats.player_name,
                          playerbygamestats.season,
                          playerbygamestats.player_id,
                          func.string_agg(playerbygamestats.team_abbrev.distinct(),
                                          aggregate_order_by(literal_column("'/'"),
                                                             playerbygamestats.team_abbrev.desc())).label('teams'),
                          func.count(playerbygamestats.player_id).label('gp'),
                          func.round(func.avg(playerbygamestats.toc)/60, 1).label('mins'),
                          func.round(func.avg(playerbygamestats.fgm), 1).label('fgm'),
                          func.round(func.avg(playerbygamestats.fga), 1).label('fga'),
                          func.round(func.avg(playerbygamestats.tpm), 1).label('tpm'),
                          func.round(func.avg(playerbygamestats.tpa), 1).label('tpa'),
                          func.round(func.avg(playerbygamestats.ftm), 1).label('ftm'),
                          func.round(func.avg(playerbygamestats.fta), 1).label('fta'),
                          func.round(func.avg(playerbygamestats.oreb), 1).label('oreb'),
                          func.round(func.avg(playerbygamestats.dreb), 1).label('dreb'),
                          func.round(func.avg(playerbygamestats.ast), 1).label('ast'),
                          func.round(func.avg(playerbygamestats.tov), 1).label('tov'),
                          func.round(func.avg(playerbygamestats.stl), 1).label('stl'),
                          func.round(func.avg(playerbygamestats.blk), 1).label('blk'),
                          func.round(func.avg(playerbygamestats.pf), 1).label('pf'),
                          func.round(func.avg(playerbygamestats.points), 1).label('points'),
                          func.round(func.avg(playerbygamestats.plus_minus), 1).label('plus_minus'))\
                    .group_by(playerbygamestats.player_name,
                              playerbygamestats.player_id,
                              playerbygamestats.season).\
                    filter((playerbygamestats.toc > 0) &
                            (playerbygamestats.season == max_season)).all()
    return jsonify(data)

@stats.route('api/v1/players/submittest/', methods=['GET'])
def api_test():
    #print(request.args['player'].split())
    data = playerbygamestats.query.\
            with_entities(playerbygamestats.player_name,
                          playerbygamestats.season,
                          playerbygamestats.player_id,
                          #func.string_agg(playerbygamestats.player_id.distinct(), playerbygamestats.season).label('row_key'),
                          func.string_agg(playerbygamestats.team_abbrev.distinct(),
                                          aggregate_order_by(literal_column("'/'"),
                                                             playerbygamestats.team_abbrev.desc())).label('teams'),
                          func.count(playerbygamestats.player_id).label('gp'),
                          func.round(func.avg(playerbygamestats.toc)/60, 1).label('mins'),
                          func.round(func.avg(playerbygamestats.fgm), 1).label('fgm'),
                          func.round(func.avg(playerbygamestats.fga), 1).label('fga'),
                          func.round(func.avg(playerbygamestats.tpm), 1).label('tpm'),
                          func.round(func.avg(playerbygamestats.tpa), 1).label('tpa'),
                          func.round(func.avg(playerbygamestats.ftm), 1).label('ftm'),
                          func.round(func.avg(playerbygamestats.fta), 1).label('fta'),
                          func.round(func.avg(playerbygamestats.oreb), 1).label('oreb'),
                          func.round(func.avg(playerbygamestats.dreb), 1).label('dreb'),
                          func.round(func.avg(playerbygamestats.ast), 1).label('ast'),
                          func.round(func.avg(playerbygamestats.tov), 1).label('tov'),
                          func.round(func.avg(playerbygamestats.stl), 1).label('stl'),
                          func.round(func.avg(playerbygamestats.blk), 1).label('blk'),
                          func.round(func.avg(playerbygamestats.pf), 1).label('pf'),
                          func.round(func.avg(playerbygamestats.points), 1).label('points'),
                          func.round(func.avg(playerbygamestats.plus_minus), 1).label('plus_minus'))\
                    .group_by(playerbygamestats.player_name,
                              playerbygamestats.player_id,
                              playerbygamestats.season).\
                    filter((playerbygamestats.toc > 0) & (playerbygamestats.season == 2017)).all()
    return jsonify(data)

@stats.route('api/v1/players/<player>/', methods=['GET'])
def api_player(player):
    season = request.args.get('season', 2019)
    if ' ' in str(season):
        season = season.split()
    else:
        season = [x[0] for x in playerbygamestats.query.with_entities(playerbygamestats.season).distinct().all()]
    team = request.args.get('team', 0)
    if ' ' in str(team):
        team = team.split()
    else:
        team = [x[0] for x in playerbygamestats.query.with_entities(playerbygamestats.team_abbrev).distinct().all() if x[0] != None]
    toc = request.args.get('toc', 0)
    print(team)
    data = playerbygamestats.query.\
            with_entities(playerbygamestats.player_name,
                          playerbygamestats.season,
                          playerbygamestats.player_id,
                          #func.string_agg(playerbygamestats.player_id.distinct(), playerbygamestats.season).label('row_key'),
                          func.string_agg(playerbygamestats.team_abbrev.distinct(),
                                          aggregate_order_by(literal_column("'/'"),
                                                             playerbygamestats.team_abbrev.desc())).label('teams'),
                          func.count(playerbygamestats.player_id).label('gp'),
                          func.round(func.avg(playerbygamestats.toc)/60, 1).label('mins'),
                          func.round(func.avg(playerbygamestats.fgm), 1).label('fgm'),
                          func.round(func.avg(playerbygamestats.fga), 1).label('fga'),
                          func.round(func.avg(playerbygamestats.tpm), 1).label('tpm'),
                          func.round(func.avg(playerbygamestats.tpa), 1).label('tpa'),
                          func.round(func.avg(playerbygamestats.ftm), 1).label('ftm'),
                          func.round(func.avg(playerbygamestats.fta), 1).label('fta'),
                          func.round(func.avg(playerbygamestats.oreb), 1).label('oreb'),
                          func.round(func.avg(playerbygamestats.dreb), 1).label('dreb'),
                          func.round(func.avg(playerbygamestats.ast), 1).label('ast'),
                          func.round(func.avg(playerbygamestats.tov), 1).label('tov'),
                          func.round(func.avg(playerbygamestats.stl), 1).label('stl'),
                          func.round(func.avg(playerbygamestats.blk), 1).label('blk'),
                          func.round(func.avg(playerbygamestats.pf), 1).label('pf'),
                          func.round(func.avg(playerbygamestats.points), 1).label('points'),
                          func.round(func.avg(playerbygamestats.plus_minus), 1).label('plus_minus'))\
                    .group_by(playerbygamestats.player_name,
                              playerbygamestats.player_id,
                              playerbygamestats.season).\
                    filter((playerbygamestats.toc > 0) &
                            (playerbygamestats.season.in_(season)) &
                            (playerbygamestats.player_id == player) &
                            (playerbygamestats.team_abbrev.in_(team))).all()
    return jsonify(data)

@stats.route('api/v1/teams/all/', methods=['GET'])
def api_all_teams():
    '''
    this endpoing returns all the distinct teams for the select boxes
    '''
    data = team_details.query.with_entities(team_details.team_id, team_details.abbreviation).all()

    return jsonify(data)

@stats.route('api/v1/seasons/all/', methods=['GET'])
def api_all_seasons():
    '''
    this endpoing returns all the distinct seasons for the select boxes
    '''
    data = playerbygamestats.query.with_entities(playerbygamestats.season).distinct().all()

    return jsonify(data)

@stats.route('api/v1/players/distinct/', methods=['GET'])
def api_all_players():
    '''
    this endpoing returns all the distinct players for the select boxes
    '''
    data = playerbygamestats.query.with_entities(playerbygamestats.player_id, playerbygamestats.player_name).distinct().all()

    return jsonify(data)
@stats.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
