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

from flask import Flask, render_template, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from src.metallum import get_band_info
from src.preprocessing import lyrical_themes_preprocessing
from src.models import keyword_labeler
from src.postprocessing import lyrical_themes_postprocessing

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'


class SearchForm(FlaskForm):
    """
    Search form by www.metal-archives.com band URL.

    Args:
        FlaskForm (FlaskForm): A form for use in flask.
    """
    band_url = StringField('Band', validators=[DataRequired()],
                           render_kw={'placeholder': 'e.g. https://www.metal-archives.com/bands/Froglord/3540467964'})
    submit = SubmitField('Submit')


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
        session['band_info'] = get_band_info(form.band_url.data)

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
