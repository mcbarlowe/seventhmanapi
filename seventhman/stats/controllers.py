from flask import Flask, render_template, request, Blueprint
from seventhman import db
from seventhman.stats.models import playerbygamestats
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy import literal_column

stats = Blueprint('stats', __name__, url_prefix='/stats')


@stats.route('/', methods=['GET', 'POST'])
def index():
    default_season = '2019'
    default_player = 'LeBron James'
    if request.form:
        player = request.form.get('player')
        season = request.form.get('season')
        players = db.session.query(playerbygamestats.player_name, playerbygamestats.toc)\
                .filter(playerbygamestats.toc > 0).distinct(playerbygamestats.player_name).all()
        players = [row[0] for row in players]
        data = playerbygamestats.query.filter((playerbygamestats.season == season) & (playerbygamestats.player_name == player))
        return render_template('stats/index.html', value=data, default_season=season, default_player=player, auto=players)
    else:
        data = playerbygamestats.query.\
                with_entities(playerbygamestats.player_name,
                              playerbygamestats.season,
                              func.string_agg(playerbygamestats.team_abbrev.distinct(),
                                              aggregate_order_by(literal_column("'/'"), playerbygamestats.team_abbrev.desc())).label('Teams'),
                              func.avg(playerbygamestats.fgm))\
                        .group_by(playerbygamestats.player_name,
                                  playerbygamestats.player_id,
                                  playerbygamestats.season).\
                        filter((playerbygamestats.season == default_season) & (playerbygamestats.toc > 0)).all()
        players = db.session.query(playerbygamestats.player_name, playerbygamestats.toc)\
                .filter(playerbygamestats.toc > 0).distinct(playerbygamestats.player_name).all()
        players = [row[0] for row in players]
        return render_template('stats/index.html', value=data, default_season=default_season, default_player=default_player, auto=players)
