import os
from flask import Flask, render_template, request
from db_models import db, playerbygamestats

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['NBA_CONNECT']
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    default_season = '2019'
    default_player = 'LeBron James'
    if request.form:
        print(request.form)
        player = request.form.get('player')
        season = request.form.get('season')
        data = playerbygamestats.query.filter((playerbygamestats.season == season) & (playerbygamestats.player_name == player))
        return render_template('index.html', value=data, default_season=season, default_player=player)
    else:
        data = playerbygamestats.query.filter(playerbygamestats.game_date == '2016-10-25').all()
        return render_template('index.html', value=data, default_season=default_season, default_player=default_player)


if __name__ == '__main__':
    app.run(debug=True)
