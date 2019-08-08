from flask import Flask, render_template, request, Blueprint, jsonify
from seventhman import db
from seventhman.stats.models import playerbygamestats
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy import literal_column

stats = Blueprint('stats', __name__, url_prefix='/stats')


@stats.route('api/v1/players/all', methods=['GET'])
def api_all():
    #print(request.args['player'].split())
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
                    filter((playerbygamestats.toc > 0) & (playerbygamestats.season == 2019)).all()
    print(jsonify(data))
    return jsonify(data)

@stats.route('api/v1/players/test', methods=['GET'])
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
@stats.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
