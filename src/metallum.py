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

import requests
from bs4 import BeautifulSoup

HEADER = {'user-agent': 'My-UA'}


def get_band_info(url):
    """
    Scrape https://www.metal-archives.com/bands/* endpoint.

    Args:
        url (str): A URL query string

    Returns:
        band_info (dict): Dictionary containing band information
    """
    band_info = {}

    band_info['id'] = url.split('/')[-1]

    r = requests.get(url, headers=HEADER)

    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    band_info['name'] = soup.find('h1').text

    dd = soup.find_all('dd')

    band_info['country_of_origin'] = dd[0].text
    band_info['location'] = dd[1].text
    band_info['status'] = dd[2].text
    band_info['formed_in'] = dd[3].text
    band_info['years_active'] = dd[7].text
    band_info['lyrical_theme'] = dd[5].text
    band_info['current_label'] = dd[6].text

    return band_info
