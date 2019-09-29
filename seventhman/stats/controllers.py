from flask import request, Blueprint, jsonify
from seventhman.stats.models import playerbygamestats, team_details, teambygamestats
from seventhman.stats.models import player_advanced, team_advanced, player_details, player_possessions, team_possessions
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy import literal_column, case, cast, String, and_, Numeric

stats = Blueprint('stats', __name__, url_prefix='/stats')

@stats.route('api/v1/players/', methods=['GET'])
def api_players():
    '''
    this is the main players api endpoint for regular counting stats both
    by season and aggregated
    '''
    #parse players
    if request.args.get('player', '') == '':
        players = playerbygamestats.query.\
                with_entities(playerbygamestats.player_id).\
                filter((playerbygamestats.toc > 0)).distinct().all()
    else:
        players = request.args['player'].split(' ')
    # parse seasons
    if request.args.get('season', '') == '':
        seasons = [playerbygamestats.query.with_entities(func.max(playerbygamestats.season)).all()[0][0]]
        print(seasons)
    else:
        seasons = request.args['season'].split(' ')
    # parse time on court
    if request.args.get('toc', '') == '':
        toc = 1
    else:
        toc = float(request.args['toc']) * 60
    # parse teams
    if request.args.get('team', '') == '':
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
    else:
        teams = request.args['team'].split(' ')
    print(request.args)
    if request.args.get('agg', 'no') == 'no':
        data = playerbygamestats.query.join(player_details, player_details.player_id == playerbygamestats.player_id).\
                with_entities(playerbygamestats.player_name,
                              playerbygamestats.season,
                              playerbygamestats.player_id,
                              player_details.position,
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
                                  player_details.position,
                                  playerbygamestats.player_id,
                                  playerbygamestats.season).\
                        filter((playerbygamestats.toc >= toc) &
                               (playerbygamestats.player_id.in_(players)) &
                               (playerbygamestats.season.in_(seasons)) &
                               (playerbygamestats.team_id.in_(teams))).all()
        return jsonify(data)
    else:
        data = playerbygamestats.query.join(player_details, player_details.player_id == playerbygamestats.player_id).\
                with_entities(playerbygamestats.player_name,
                              case([(func.min(playerbygamestats.season) == func.max(playerbygamestats.season), cast(func.min(playerbygamestats.season), String))],
                                   else_ = func.concat(func.min(playerbygamestats.season),literal_column("'-'"), func.max(playerbygamestats.season))).label('season'),
                              playerbygamestats.player_id,
                              player_details.position,
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
                                  player_details.position,
                                  playerbygamestats.player_id).\
                        filter((playerbygamestats.toc >= toc) &
                               (playerbygamestats.player_id.in_(players)) &
                               (playerbygamestats.season.in_(seasons)) &
                               (playerbygamestats.team_id.in_(teams))).all()

        return jsonify(data)

@stats.route('api/v1/players/possession/', methods=['GET'])
def api_players_possession():
    '''
    api endpoint for possesion rate states
    '''
    #parse players
    if request.args.get('player', '') == '':
        players = playerbygamestats.query.\
                with_entities(playerbygamestats.player_id).\
                filter((playerbygamestats.toc > 0)).distinct().all()
    else:
        players = request.args['player'].split(' ')
    # parse seasons
    if request.args.get('season', '') == '':
        seasons = [playerbygamestats.query.with_entities(func.max(playerbygamestats.season)).all()[0][0]]
        print(seasons)
    else:
        seasons = request.args['season'].split(' ')
    # parse time on court
    if request.args.get('toc', '') == '':
        toc = 1
    else:
        toc = float(request.args['toc']) * 60
    # parse teams
    if request.args.get('team', '') == '':
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
    else:
        teams = request.args['team'].split(' ')
    print(request.args)
    if request.args.get('agg', 'no') == 'no':
        data = playerbygamestats.query.join(player_details, player_details.player_id == playerbygamestats.player_id).\
                join(player_possessions, and_(player_possessions.player_id == playerbygamestats.player_id,
                                             player_possessions.game_id == playerbygamestats.game_id)).\
                with_entities(playerbygamestats.player_name,
                              playerbygamestats.season,
                              playerbygamestats.player_id,
                              player_details.position,
                              func.string_agg(playerbygamestats.team_abbrev.distinct(),
                                              aggregate_order_by(literal_column("'/'"),
                                                                 playerbygamestats.team_abbrev.desc())).label('teams'),
                              func.count(playerbygamestats.player_id).label('gp'),
                              func.round(func.avg(playerbygamestats.toc)/60, 1).label('mins'),
                              func.round((func.sum(cast(playerbygamestats.fgm, Numeric))/
                                          func.sum(cast(player_possessions.possessions, Numeric)) * 100), 1).label('fgm'),
                              func.round((func.sum(cast(playerbygamestats.fga, Numeric))/
                                          func.sum(cast(player_possessions.possessions, Numeric)) * 100), 1).label('fga'),
                              func.round(func.sum(cast(playerbygamestats.tpm, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('tpm'),
                              func.round(func.sum(cast(playerbygamestats.tpa, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('tpa'),
                              func.round(func.sum(cast(playerbygamestats.ftm, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('ftm'),
                              func.round(func.sum(cast(playerbygamestats.fta, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('fta'),
                              func.round(func.sum(cast(playerbygamestats.oreb, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('oreb'),
                              func.round(func.sum(cast(playerbygamestats.dreb, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('dreb'),
                              func.round(func.sum(cast(playerbygamestats.ast, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('ast'),
                              func.round(func.sum(cast(playerbygamestats.tov, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('tov'),
                              func.round(func.sum(cast(playerbygamestats.stl, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('stl'),
                              func.round(func.sum(cast(playerbygamestats.blk, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('blk'),
                              func.round(func.sum(cast(playerbygamestats.pf, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('pf'),
                              func.round(func.sum(cast(playerbygamestats.points, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('points'))\
                        .group_by(playerbygamestats.player_name,
                                  player_details.position,
                                  playerbygamestats.player_id,
                                  playerbygamestats.season).\
                        filter((playerbygamestats.toc >= toc) &
                               (playerbygamestats.player_id.in_(players)) &
                               (playerbygamestats.season.in_(seasons)) &
                               (playerbygamestats.team_id.in_(teams))).all()
        return jsonify(data)
    else:
        data = playerbygamestats.query.join(player_details, player_details.player_id == playerbygamestats.player_id).\
                join(player_possessions, and_(player_possessions.player_id == playerbygamestats.player_id,
                                             player_possessions.game_id == playerbygamestats.game_id)).\
                with_entities(playerbygamestats.player_name,
                              case([(func.min(playerbygamestats.season) == func.max(playerbygamestats.season), cast(func.min(playerbygamestats.season), String))],
                                   else_ = func.concat(func.min(playerbygamestats.season),literal_column("'-'"), func.max(playerbygamestats.season))).label('season'),
                              playerbygamestats.player_id,
                              player_details.position,
                              func.string_agg(playerbygamestats.team_abbrev.distinct(),
                                              aggregate_order_by(literal_column("'/'"),
                                                                 playerbygamestats.team_abbrev.desc())).label('teams'),
                              func.count(playerbygamestats.player_id).label('gp'),
                              func.round(func.avg(playerbygamestats.toc)/60, 1).label('mins'),
                              func.round((func.sum(cast(playerbygamestats.fgm, Numeric))/
                                          func.sum(cast(player_possessions.possessions, Numeric)) * 100), 1).label('fgm'),
                              func.round((func.sum(cast(playerbygamestats.fga, Numeric))/
                                          func.sum(cast(player_possessions.possessions, Numeric)) * 100), 1).label('fga'),
                              func.round(func.sum(cast(playerbygamestats.tpm, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('tpm'),
                              func.round(func.sum(cast(playerbygamestats.tpa, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('tpa'),
                              func.round(func.sum(cast(playerbygamestats.ftm, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('ftm'),
                              func.round(func.sum(cast(playerbygamestats.fta, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('fta'),
                              func.round(func.sum(cast(playerbygamestats.oreb, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('oreb'),
                              func.round(func.sum(cast(playerbygamestats.dreb, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('dreb'),
                              func.round(func.sum(cast(playerbygamestats.ast, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('ast'),
                              func.round(func.sum(cast(playerbygamestats.tov, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('tov'),
                              func.round(func.sum(cast(playerbygamestats.stl, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('stl'),
                              func.round(func.sum(cast(playerbygamestats.blk, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('blk'),
                              func.round(func.sum(cast(playerbygamestats.pf, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('pf'),
                              func.round(func.sum(cast(playerbygamestats.points, Numeric))/
                                         func.sum(cast(player_possessions.possessions, Numeric)) * 100, 1).label('points'),
                              func.round(func.sum(cast(playerbygamestats.fgm, Numeric))/(func.sum(cast(playerbygamestats.fga, Numeric))), 2).label('fg_percentage'))\
                        .group_by(playerbygamestats.player_name,
                                  player_details.position,
                                  playerbygamestats.player_id).\
                        filter((playerbygamestats.toc >= toc) &
                               (playerbygamestats.player_id.in_(players)) &
                               (playerbygamestats.season.in_(seasons)) &
                               (playerbygamestats.team_id.in_(teams))).all()

        return jsonify(data)
@stats.route('api/v1/teams/', methods=['GET'])
def api_teams():
    '''
    this is the api endpoint for the home page of the teams data
    '''

    # parse seasons
    if request.args.get('season', '') == '':
        seasons = [teambygamestats.query.with_entities(func.max(teambygamestats.season)).all()[0][0]]
    else:
        seasons = request.args['season'].split(' ')
    # parse teams
    if request.args.get('team', '') == '':
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
    else:
        teams = request.args['team'].split(' ')
    agg = request.args.get('agg', 'no')
    print(agg)
    if agg == 'no':
        data = teambygamestats.query.\
                with_entities(teambygamestats.team_abbrev.label('team') ,
                              teambygamestats.season,
                              func.count(teambygamestats.team_id).label('gp'),
                              func.round(func.avg(teambygamestats.points_for), 1).label('points'),
                              func.round(func.avg(teambygamestats.points_against), 1).label('points_against'),
                              func.sum(teambygamestats.is_win).label('wins'),
                              func.round(func.avg(teambygamestats.pf_drawn), 1).label('fouls_drawn'),
                              func.round(func.avg(teambygamestats.shots_blocked), 1).label('shots_blocked'),
                              func.round(func.avg(teambygamestats.toc)/60, 1).label('mins'),
                              func.round(func.avg(teambygamestats.fgm), 1).label('fgm'),
                              func.round(func.avg(teambygamestats.fga), 1).label('fga'),
                              func.round(func.avg(teambygamestats.tpm), 1).label('tpm'),
                              func.round(func.avg(teambygamestats.tpa), 1).label('tpa'),
                              func.round(func.avg(teambygamestats.ftm), 1).label('ftm'),
                              func.round(func.avg(teambygamestats.fta), 1).label('fta'),
                              func.round(func.avg(teambygamestats.oreb), 1).label('oreb'),
                              func.round(func.avg(teambygamestats.dreb), 1).label('dreb'),
                              func.round(func.avg(teambygamestats.ast), 1).label('ast'),
                              func.round(func.avg(teambygamestats.tov), 1).label('tov'),
                              func.round(func.avg(teambygamestats.stl), 1).label('stl'),
                              func.round(func.avg(teambygamestats.blk), 1).label('blk'),
                              func.round(func.avg(teambygamestats.pf), 1).label('pf'),
                              func.round(func.avg(teambygamestats.plus_minus), 1).label('plus_minus'))\
                        .group_by(teambygamestats.team_abbrev,
                                  teambygamestats.team_id,
                                  teambygamestats.season).\
                        filter((teambygamestats.season.in_(seasons)) &
                                (teambygamestats.team_id.in_(teams))).all()
    else:
        data = teambygamestats.query.\
                with_entities(teambygamestats.team_abbrev.label('team') ,
                              case([(func.min(teambygamestats.season) == func.max(teambygamestats.season), cast(func.min(teambygamestats.season), String))],
                                   else_ = func.concat(func.min(teambygamestats.season),literal_column("'-'"), func.max(teambygamestats.season))).label('season'),
                              func.count(teambygamestats.team_id).label('gp'),
                              func.round(func.avg(teambygamestats.points_for), 1).label('points'),
                              func.round(func.avg(teambygamestats.points_against), 1).label('points_against'),
                              func.sum(teambygamestats.is_win).label('wins'),
                              func.round(func.avg(teambygamestats.pf_drawn), 1).label('fouls_drawn'),
                              func.round(func.avg(teambygamestats.shots_blocked), 1).label('shots_blocked'),
                              func.round(func.avg(teambygamestats.toc)/60, 1).label('mins'),
                              func.round(func.avg(teambygamestats.fgm), 1).label('fgm'),
                              func.round(func.avg(teambygamestats.fga), 1).label('fga'),
                              func.round(func.avg(teambygamestats.tpm), 1).label('tpm'),
                              func.round(func.avg(teambygamestats.tpa), 1).label('tpa'),
                              func.round(func.avg(teambygamestats.ftm), 1).label('ftm'),
                              func.round(func.avg(teambygamestats.fta), 1).label('fta'),
                              func.round(func.avg(teambygamestats.oreb), 1).label('oreb'),
                              func.round(func.avg(teambygamestats.dreb), 1).label('dreb'),
                              func.round(func.avg(teambygamestats.ast), 1).label('ast'),
                              func.round(func.avg(teambygamestats.tov), 1).label('tov'),
                              func.round(func.avg(teambygamestats.stl), 1).label('stl'),
                              func.round(func.avg(teambygamestats.blk), 1).label('blk'),
                              func.round(func.avg(teambygamestats.pf), 1).label('pf'),
                              func.round(func.avg(teambygamestats.plus_minus), 1).label('plus_minus'))\
                        .group_by(teambygamestats.team_abbrev,
                                  teambygamestats.team_id).\
                        filter((teambygamestats.season.in_(seasons)) &
                                (teambygamestats.team_id.in_(teams))).all()

    return jsonify(data)

@stats.route('api/v1/teams/possession/', methods=['GET'])
def api_teams_possession():
    '''
    api endpoint for possesion rate states
    '''
    # parse seasons
    if request.args.get('season', '') == '':
        seasons = [teambygamestats.query.with_entities(func.max(teambygamestats.season)).all()[0][0]]
    else:
        seasons = request.args['season'].split(' ')
    # parse teams
    if request.args.get('team', '') == '':
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
    else:
        teams = request.args['team'].split(' ')
    if request.args.get('agg', 'no') == 'no':
        data = teambygamestats.query\
                .join(team_possessions, and_(team_possessions.team_id == teambygamestats.team_id,
                                               team_possessions.game_id == teambygamestats.game_id)).\
                with_entities(teambygamestats.team_abbrev,
                              teambygamestats.season,
                              teambygamestats.team_id,
                              func.count(teambygamestats.team_id).label('gp'),
                              func.round(func.avg(teambygamestats.toc)/60, 1).label('mins'),
                              func.round((func.sum(cast(teambygamestats.fgm, Numeric))/
                                          func.sum(cast(team_possessions.possessions, Numeric)) * 100), 1).label('fgm'),
                              func.round((func.sum(cast(teambygamestats.fga, Numeric))/
                                          func.sum(cast(team_possessions.possessions, Numeric)) * 100), 1).label('fga'),
                              func.round(func.sum(cast(teambygamestats.tpm, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('tpm'),
                              func.round(func.sum(cast(teambygamestats.tpa, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('tpa'),
                              func.round(func.sum(cast(teambygamestats.ftm, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('ftm'),
                              func.round(func.sum(cast(teambygamestats.fta, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('fta'),
                              func.round(func.sum(cast(teambygamestats.oreb, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('oreb'),
                              func.round(func.sum(cast(teambygamestats.dreb, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('dreb'),
                              func.round(func.sum(cast(teambygamestats.ast, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('ast'),
                              func.round(func.sum(cast(teambygamestats.tov, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('tov'),
                              func.round(func.sum(cast(teambygamestats.stl, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('stl'),
                              func.round(func.sum(cast(teambygamestats.blk, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('blk'),
                              func.round(func.sum(cast(teambygamestats.pf, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('pf'),
                              func.round(func.sum(cast(teambygamestats.points_for, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('points'))\
                        .group_by(teambygamestats.team_abbrev,
                                  teambygamestats.team_id,
                                  teambygamestats.season).\
                        filter((teambygamestats.season.in_(seasons)) &
                                (teambygamestats.team_id.in_(teams))).all()
        return jsonify(data)
    else:
        data = teambygamestats.query\
                .join(team_possessions, and_(team_possessions.team_id == teambygamestats.team_id,
                                               team_possessions.game_id == teambygamestats.game_id)).\
                with_entities(teambygamestats.team_abbrev,
                              case([(func.min(teambygamestats.season) == func.max(teambygamestats.season), cast(func.min(teambygamestats.season), String))],
                                   else_ = func.concat(func.min(teambygamestats.season),literal_column("'-'"), func.max(teambygamestats.season))).label('season'),
                              teambygamestats.team_id,
                              func.count(teambygamestats.team_id).label('gp'),
                              func.round(func.avg(teambygamestats.toc)/60, 1).label('mins'),
                              func.round((func.sum(cast(teambygamestats.fgm, Numeric))/
                                          func.sum(cast(team_possessions.possessions, Numeric)) * 100), 1).label('fgm'),
                              func.round((func.sum(cast(teambygamestats.fga, Numeric))/
                                          func.sum(cast(team_possessions.possessions, Numeric)) * 100), 1).label('fga'),
                              func.round(func.sum(cast(teambygamestats.tpm, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('tpm'),
                              func.round(func.sum(cast(teambygamestats.tpa, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('tpa'),
                              func.round(func.sum(cast(teambygamestats.ftm, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('ftm'),
                              func.round(func.sum(cast(teambygamestats.fta, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('fta'),
                              func.round(func.sum(cast(teambygamestats.oreb, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('oreb'),
                              func.round(func.sum(cast(teambygamestats.dreb, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('dreb'),
                              func.round(func.sum(cast(teambygamestats.ast, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('ast'),
                              func.round(func.sum(cast(teambygamestats.tov, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('tov'),
                              func.round(func.sum(cast(teambygamestats.stl, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('stl'),
                              func.round(func.sum(cast(teambygamestats.blk, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('blk'),
                              func.round(func.sum(cast(teambygamestats.pf, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('pf'),
                              func.round(func.sum(cast(teambygamestats.points_for, Numeric))/
                                         func.sum(cast(team_possessions.possessions, Numeric)) * 100, 1).label('points'))\
                        .group_by(teambygamestats.team_abbrev,
                                  teambygamestats.team_id).\
                        filter((teambygamestats.season.in_(seasons)) &
                                (teambygamestats.team_id.in_(teams))).all()

        return jsonify(data)

@stats.route('api/v1/teams/advanced/', methods=['GET'])
def teams_advanced():
    '''
    endpoint for the team advanced stats tables
    '''
    # parse seasons
    if request.args.get('season', '') == '':
        seasons = [playerbygamestats.query.with_entities(func.max(playerbygamestats.season)).all()[0][0]]
        print(seasons)
    else:
        seasons = request.args['season'].split(' ')

    # parse teams
    if request.args.get('team', '') == '':
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
    else:
        teams = request.args['team'].split(' ')
    data = team_advanced.query.\
            with_entities(team_advanced.team_abbrev,
                          team_advanced.season,
                          team_advanced.team_id,
                          func.round(team_advanced.efg_percentage * 100, 1).label('efg_percentage'),
                          func.round(team_advanced.true_shooting_percentage * 100, 1).label('true_shooting_percentage'),
                          func.round(team_advanced.tov_percentage, 1).label('tov_percentage'),
                          func.round(team_advanced.oreb_percentage, 1).label('oreb_percentage'),
                          func.round(team_advanced.ft_per_fga, 1).label('ft_per_fga'),
                          func.round(team_advanced.opp_efg_percentage, 1).label('opp_efg_percentage'),
                          func.round(team_advanced.opp_tov_percentage, 1).label('opp_tov_percentage'),
                          func.round(team_advanced.dreb_percentage, 1).label('dreb_percentage'),
                          func.round(team_advanced.opp_ft_per_fga, 1).label('opp_ft_per_fga'),
                          func.round(team_advanced.off_rating, 1).label('off_rating'),
                          func.round(team_advanced.def_rating, 1).label('def_rating')).\
                        filter((team_advanced.team_id.in_(teams)) &
                               (team_advanced.season.in_(seasons))).all()
    return jsonify(data)
@stats.route('api/v1/players/advanced/', methods=['GET'])
def players_advanced():
    '''
    endpoint for the player advanced stats tables
    '''
    #parse players
    if request.args.get('player', '') == '':
        players = playerbygamestats.query.\
                with_entities(playerbygamestats.player_id).\
                filter((playerbygamestats.toc > 0)).distinct().all()
    else:
        players = request.args['player'].split(' ')
    # parse seasons
    if request.args.get('season', '') == '':
        seasons = [playerbygamestats.query.with_entities(func.max(playerbygamestats.season)).all()[0][0]]
        print(seasons)
    else:
        seasons = request.args['season'].split(' ')

    data = player_advanced.query.join(player_details, player_details.player_id == player_advanced.player_id).\
            with_entities(player_details.display_first_last,
                          player_advanced.season,
                          player_advanced.player_id,
                          player_details.position,
                          player_advanced.team_abbrev,
                          func.round(player_advanced.efg_percentage * 100, 1).label('efg_percentage'),
                          func.round(player_advanced.true_shooting_percentage * 100, 1).label('true_shooting_percentage'),
                          func.round(player_advanced.oreb_percentage, 1).label('oreb_percentage'),
                          func.round(player_advanced.dreb_percentage, 1).label('dreb_percentage'),
                          func.round(player_advanced.treb_percentage, 1).label('treb_percentage'),
                          func.round(player_advanced.ast_percentage, 1).label('ast_percentage'),
                          func.round(player_advanced.stl_percentage, 1).label('stl_percentage'),
                          func.round(player_advanced.blk_percentage, 1).label('blk_percentage'),
                          func.round(player_advanced.tov_percentage, 1).label('tov_percentage'),
                          func.round(player_advanced.usg_percentage, 1).label('usg_percentage'),
                          func.round(player_advanced.off_rating, 1).label('off_rating'),
                          func.round(player_advanced.def_rating, 1).label('def_rating')).\
                        filter((player_advanced.player_id.in_(players)) &
                               (player_advanced.season.in_(seasons))).all()
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
    data = playerbygamestats.query.with_entities(playerbygamestats.player_id, playerbygamestats.player_name).filter(playerbygamestats.toc > 0).distinct().all()
    data.sort(key= lambda x: x[1])

    return jsonify(data)
@stats.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
