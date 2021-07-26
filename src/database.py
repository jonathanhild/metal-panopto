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
from sqlalchemy.orm import backref

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
    band_name = db.Column(db.Text)
    country_of_origin = db.Column(db.Text)
    location = db.Column(db.Text)
    status = db.Column(db.Text)
    formed_in = db.Column(db.Integer())
    years_active = db.Column(db.Text)
    lyrical_themes = db.Column(db.Text)
    read_more_text = db.Column(db.Text)
    current_label = db.relationship('Label')
    discography = db.relationship('Album', backref=db.backref('band'))
    members = db.relationship('Artist', )
    reviews = db.relationship('Review', )
    similar = db.relationship('BandSimilar', backref=db.backref('band'))
    links = db.relationship('Link', backref=db.backref('band'))
    timestamp = db.Column(db.DateTime, default=datetime.now())


class Album(db.Model):

    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    type = db.Column(db.Text)
    release_date = db.Column(db.Text)
    catalog_id = db.Column(db.Text)
    version_desc = db.Column(db.Text)
    label = db.relationship('Label', backref=db.backref('album'))
    format = db.Column(db.Text)
    limitation = db.Column(db.Text)
    additional_notes = db.Column(db.Text)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))


class Song(db.Model):

    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer)
    title = db.Column(db.Text)
    length = db.Column(db.Text)
    lyrics = db.Column(db.Text)


class Artist(db.Model):

    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    real_name = db.Column(db.Text)
    age = db.Column(db.Text)
    place_of_origin = db.Column(db.Text)
    gender = db.Column(db.Text)
    links = db.relationship('Link', backref=db.backref('artist'))


class Review(db.Model):

    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    date = db.Column(db.DateTime)
    based_on = db.Column(db.Text)
    rating_pct = db.Column(db.Integer)
    text = db.Column(db.Text)


class BandSimilar(db.Model):

    __tablename__ = 'band_similar'

    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    band_related_id = db.Column(db.Integer, db.ForeignKey('band.id'))


class Link(db.Model):

    __tablename__ = 'link'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text)
    link_url = db.Column(db.Text)


class Label(db.Model):

    __tablename__ = 'label'

    id = db.Column(db.Integer, primary_key=True)
    label_name = db.Column(db.Text)
    address = db.Column(db.Text)
    country = db.Column(db.Text)
    phone_no = db.Column(db.Text)
    status = db.Column(db.Text)
    styles_specialities = db.Column(db.Text)
    founding_date = db.Column(db.Text)
    sub_labels = db.relationship('LabelSublabel')
    online_shopping = db.Column(db.Text)
    website = db.Column(db.Text)
    email = db.Column(db.Text)
    additional_notes = db.Column(db.Text)


class LabelSublabel(db.Model):

    __tablename__ = 'label_sublabel'

    id = db.Column(db.Integer, primary_key=True)
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'))
    sublabel_id = db.Column(db.Integer, db.ForeignKey('label.id'))
