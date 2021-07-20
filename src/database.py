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
