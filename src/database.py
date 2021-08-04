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

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SearchHistory(db.Model):
    """
    Model for search history.

    Args:
        db.Model (Model): Flask SQLAlchemy object.

    Attrs:
        id (INTEGER): Table primary key.
        search_text (TEXT): Search text from search form.
        timestamp (DATETIME): Timestamp when search was made.

    """
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)
    search_text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now())


class Band(db.Model):

    __tablename__ = 'band'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    country_of_origin = db.Column(db.Text)
    location = db.Column(db.Text)
    status = db.Column(db.Text)
    formed_in = db.Column(db.Integer())
    years_active = db.Column(db.Text)
    lyrical_themes = db.Column(db.Text)
    read_more_text = db.Column(db.Text)
    current_label = db.Column(db.Text)
    discography = db.relationship('Album', backref=db.backref('band'))
    timestamp = db.Column(db.DateTime, default=datetime.now())


class Album(db.Model):

    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    type = db.Column(db.Text)
    release_date = db.Column(db.Text)
    catalog_id = db.Column(db.Text)
    version_desc = db.Column(db.Text)
    label = db.Column(db.Text)
    format = db.Column(db.Text)
    # limitation = db.Column(db.Text)
    additional_notes = db.Column(db.Text)
    songs = db.relationship('Song', backref=db.backref('album'))
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    timestamp = db.Column(db.DateTime, default=datetime.now())


class Song(db.Model):

    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer)
    title = db.Column(db.Text)
    length = db.Column(db.Text)
    lyrics = db.Column(db.Text)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    timestamp = db.Column(db.DateTime, default=datetime.now())
