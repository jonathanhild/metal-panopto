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

from database import Album, Band

HEADER = {'user-agent': 'My-UA'}


def _metallum_request(endpoint=None, id=None, base_url=None, endpart=None, params=None):
    if not base_url:
        base_url = 'https://www.metal-archives.com'

    header = {'user-agent': 'My-UA'}

    url = urljoin(base=base_url, url=f'{endpoint}{id}{endpart}')

    r = requests.get(url, headers=header, params=params)

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


def scrape_robots_txt():
    robots = {}
    n = 0
    r = _metallum_request('robots.txt', '')
    lines = r.text.splitlines()
    for line in lines:
        line = line.split(': ')
        if line[0] == 'Disallow':
            robots[line[0] + f'_{n}'] = line[1]
            n += 1
        else:
            robots[line[0]] = line[1]
    return robots


def get_band_list():
    endpoint = 'browse/ajax-letter/l/'
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R' 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'NBR', '~']

    query_params = {'sEcho': '1', 'iDisplayStart': 0, 'iDisplayLength': 500}

    band_list = []

    for letter in letters:
        response = _metallum_request()

    return band_list


def scrape_band(band_id):
    band_endpoint = 'band/view/id/'
    read_more_endpoint = 'band/read-more/id/'
    albums_endpoint = 'band/discography/id/'
    albums_all_tab = '/tab/all/'
    band = Band()
    band.id = band_id

    # Band Main Page
    band_response = _metallum_request(band_endpoint, band_id)

    soup = BeautifulSoup(band_response.text, 'lxml')

    band.name = soup.find('h1', {'class': 'band_name'}).text

    band_dd = soup.find_all('dd')
    band.country_of_origin = band_dd[0].text
    band.location = band_dd[1].text
    band.status = band_dd[2].text
    band.formed_in = band_dd[3].text
    band.years_active = band_dd[7].text
    band.lyrical_themes = band_dd[5].text
    band.current_label = band_dd[6].text

    # Band Read More
    read_more_response = _metallum_request(read_more_endpoint, band_id)
    soup = BeautifulSoup(read_more_response.text, 'lxml')
    band.read_more_text = soup.text

    # Band Discography
    albums_response = _metallum_request(albums_endpoint, band_id, endpart=albums_all_tab)

    soup = BeautifulSoup(albums_response.text, 'lxml')
    album_links = soup.find_all('a', {'class': ['album', 'demo', 'other', 'single']})

    # M-A discography class labels are: album, other, demo, single.
    band.discography = []
    for a in album_links:
        album = Album(id=find_id(a['href']), title=a.link)
        band.discography.append(album)

    return band


if __name__ == '__main__':
    scrape_band(38)
