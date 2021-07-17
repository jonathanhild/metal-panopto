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

def lyrical_themes_preprocessing(lyrical_themes):
    """
    Split lyrical themes into individual themes.

    Args:
        lyrical_themes (String): Lyrical themes separated by commas

    Returns:
        List: Themes
    """
    theme_list = lyrical_themes.split(',')
    return [t.strip() for t in theme_list]
