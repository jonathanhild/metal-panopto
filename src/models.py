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


SKETCH_WORDS = (
    'nationalism',
    'national socialism',
    'anti-communism',
    'white power',
    'aryanism',
    'fascism',
    'hate',
    'hatred',
    'pride',
    'racism',
    'anti-zionism',
    'antisemitism'
)


def keyword_labeler(themes_list, keywords=SKETCH_WORDS):
    """
    Deterministic model to label lyrical themes from collection of labels.

    Args:
        themes_list (List): A list of lyrical themes.
        keywords (Collection, optional): Keywords. Defaults to SKETCH_WORDS.

    Returns:
        List: Labeled keywords.
    """
    labeled_themes = []
    for theme in themes_list:
        if theme.lower() in keywords:
            theme = '<span class="sketch">' + theme + '</span>'
            labeled_themes.append(theme)
        else:
            labeled_themes.append(theme)
    return labeled_themes
