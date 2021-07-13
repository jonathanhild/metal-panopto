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

app = Flask(__name__)


@app.route('/')
def index():
    """
    Home page.

    Returns:
        string: Hello, World!
    """
    return '<h1>Hello, World!</h1>'


@app.route('/results')
def results():
    """
    Results from inference pipeline.

    Returns:
        string: Results
    """
    return '<h1>Results</h1>'


@app.route('/about')
def about():
    """
    About page.

    Returns:
        string: About
    """
    return '<h1>About</h1>'


@app.route('/admin')
def admin():
    """
    Admin page.

    Returns:
        string: Admin
    """
    return '<h1>Admin</h1>'


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
