from basketball_reference_scraper.players import get_stats, get_player_headshot
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def search():
    return render_template('search.html')


@app.route('/player', methods=['POST', 'GET'])
def player():
    if request.method == 'GET':
        return f"The URL /player is accessed directly. Try going to '/' to search for player"

    form_data = request.form
    name = form_data['player']
    year = form_data['year']
    name = name.title()

    try:
        stats = get_stats(name, 'PER_GAME', ask_matches=False)
    except:
        return render_template('error.html')
    pl = stats[['SEASON', 'TEAM', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%']]
    cur_season = pl.loc[pl['SEASON'] == year]

    pic = get_player_headshot(name, ask_matches=False)

    return render_template('base.html',
                           data=cur_season.to_html(classes='table table-striped', index=False, col_space=100,
                                                   justify='match-parent'), name=name, pic=pic, year=year)


if __name__ == '__main__':
    app.run(debug=True, host='localhost')
