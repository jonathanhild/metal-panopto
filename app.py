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

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'


class BandURLForm(FlaskForm):
    band_url = StringField('Band',
                           validators=[DataRequired()],
                           render_kw={
                               'placeholder': 'e.g. https://www.metal-archives.com/bands/Froglord/3540467964'
                           }
                           )
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page.

    Returns:
        render_template: Search block.
    """
    form = BandURLForm()
    return render_template('search.html', form=form)


@app.route('/report', methods=['POST'])
def report():
    """
    Report from inference pipeline.

    Returns:
        string: Report
    """
    form = BandURLForm()

    return render_template('report.html', form=form, url=form.band_url.data)


@app.route('/about')
def about():
    """
    About page.

    Returns:
        string: About
    """
    return render_template('about.html')


@app.route('/admin')
def admin():
    """
    Admin page.

    Returns:
        string: Admin
    """
    return render_template('admin.html')


@app.errorhandler(404)
def page_not_found(e):
    """
    Page not found.

    Args:
        e (Error): [description]

    Returns:
        [type]: [description]
    """
    return render_template('404.html'), 404
