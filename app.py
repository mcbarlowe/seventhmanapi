import os
from flask import Flask, render_template
from db_models import db, playerbygamestats

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['NBA_CONNECT']
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    data = playerbygamestats.query.filter(playerbygamestats.game_date == '2016-10-25').all()
    return render_template('index.html', value=data)


if __name__ == '__main__':
    app.run(debug=True)
