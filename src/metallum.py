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

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

HEADER = {'user-agent': 'My-UA'}


def _metallum_request(endpoint, id, base_url=None):
    if not base_url:
        base_url = 'https://www.metal-archives.com'

    header = {'user-agent': 'My-UA'}

    url = urljoin(base=base_url, url=f'{endpoint}{id}')

    r = requests.get(url, headers=header)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return 'Error' + str(e)

    return r


def find_id(url):
    url_parts = url.split('/')
    for part in url_parts:
        if part.isnumeric():
            return part
    return None


def get_band_info(id):
    """
    Scrape https://www.metal-archives.com/bands/* endpoint.

    Args:
        url (str): A URL query string

    Returns:
        band_info (dict): Dictionary containing band information
    """
    endpoint = 'band/view/id/'
    band_info = {}
    band_info['id'] = id

    response = _metallum_request(endpoint, id)
    soup = BeautifulSoup(response.text, 'lxml')

    band_info['name'] = soup.find('h1', {'class': 'band_name'}).text

    dd = soup.find_all('dd')
    band_info['country_of_origin'] = dd[0].text
    band_info['location'] = dd[1].text
    band_info['status'] = dd[2].text
    band_info['formed_in'] = dd[3].text
    band_info['years_active'] = dd[7].text
    band_info['lyrical_themes'] = dd[5].text
    band_info['current_label'] = dd[6].text

    return band_info
