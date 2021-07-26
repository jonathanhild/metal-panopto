# Copyright (C) 2021 Jonathan Hildenbrand
#
# This file is part of VargScore.
#
# VargScore is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# VargScore is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with VargScore.  If not, see <http://www.gnu.org/licenses/>.

import os

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, session, url_for

from src.forms import SearchForm
from src.metallum import find_id, get_band_info
from src.preprocessing import lyrical_themes_preprocessing
from src.models import keyword_labeler
from src.postprocessing import lyrical_themes_postprocessing
from src.database import db, SearchHistory

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(basedir, '.env')

# Flask App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Flask SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'vargdb.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page.

    Returns:
        search.html (Response): Search block.
    """
    form = SearchForm()
    if form.validate_on_submit():
        session['band_url'] = form.band_url.data
        session['id'] = find_id(session['band_url'])
        session['band_info'] = get_band_info(session['id'])

        search_history = SearchHistory()
        search_history.search_text = form.band_url.data
        db.session.add(search_history)
        db.session.commit()

        # INFERENCE
        lyrical_themes = session['band_info']['lyrical_themes']
        lyrical_themes = lyrical_themes_preprocessing(lyrical_themes)
        lyrical_themes = keyword_labeler(lyrical_themes)
        session['band_info']['lyrical_themes'] = lyrical_themes_postprocessing(lyrical_themes)

        return redirect(url_for('report'))

    return render_template('search.html', form=form)


@app.route('/report')
def report():
    """
    Report from inference pipeline.

    Returns:
        report.html (Response): Report block.
    """
    return render_template('report.html')


@app.route('/about')
def about():
    """
    About page.

    Returns:
        about.html (Response): About block.
    """
    return render_template('about.html')


@app.route('/admin')
def admin():
    """
    Admin page.

    Returns:
        admin.html (Response): Admin block.
    """
    return render_template('admin.html')


@app.errorhandler(404)
def page_not_found(e):
    """
    Page not found.

    Args:
        e (Error): 404 Page Not Found.

    Returns:
        404.html (Response): 404 block.
    """
    return render_template('404.html'), 404
