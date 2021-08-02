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

from .database import Album, Band, Song

HEADER = {'User-Agent': 'Mozilla/5.0 Gecko/20100101 Firefox/90.0'}


def _metallum_request(endpoint=None, id=None, base_url=None, endpart=None, params=None):
    if not base_url:
        base_url = 'https://www.metal-archives.com'

    url = urljoin(base=base_url, url=f'{endpoint}{id}{endpart}')

    r = requests.get(url, headers=HEADER, params=params)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return 'Error' + str(e)

    return r


def find_id(url):
    url_parts = url.split('/')
    url_parts.reverse()
    for part in url_parts:
        if part.isnumeric():
            return int(part)
        else:
            try:
                raise TypeError
            except TypeError as e:
                print(e)
    return None


def clean_song_no(no):
    return int(no.strip().replace('.', ''))


def scrape_robots_txt():
    robots = {}
    n = 0
    r = _metallum_request('robots.txt', id='', endpart='')
    lines = r.text.splitlines()
    for line in lines:
        line = line.split(': ')
        if line[0] == 'Disallow':
            robots[line[0] + f'_{n}'] = line[1]
            n += 1
        else:
            robots[line[0]] = line[1]
    return robots


def scrape_band(id):
    band_endpoint = 'band/view/id/'
    read_more_endpoint = 'band/read-more/id/'
    albums_endpoint = 'band/discography/id/'
    albums_all_tab = '/tab/all/'
    band = Band()
    band.id = id

    # Band Main Page
    band_response = _metallum_request(band_endpoint, id)

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
    read_more_response = _metallum_request(read_more_endpoint, id)
    soup = BeautifulSoup(read_more_response.text, 'lxml')
    band.read_more_text = soup.text

    # Band Discography
    albums_response = _metallum_request(albums_endpoint, id, endpart=albums_all_tab)

    soup = BeautifulSoup(albums_response.text, 'lxml')
    album_links = soup.find_all('a', {'class': ['album', 'demo', 'other', 'single']})

    # M-A discography class labels are: album, other, demo, single.
    band.discography = []
    for a in album_links:
        album = Album(id=find_id(a['href']), title=a.link, band_id=id)
        band.discography.append(album)

    return band


def scrape_album(id, album=None):
    album_endpoint = 'albums/view/id/'
    lyrics_endpoint = 'release/ajax-view-lyrics/id/'

    album_response = _metallum_request(album_endpoint, id=id)
    soup = BeautifulSoup(album_response.text, 'lxml')

    if album:
        # Update album info from response
        pass
    else:
        # Create new album
        album = Album(id=id)
        album.title = soup.find('h1', {'class': 'album_name'}).text

        album_dd = soup.find_all('dd')
        album.type = album_dd[0].text
        album.release_date = album_dd[1].text
        album.catalog_id = album_dd[2].text
        album.version_desc = album_dd[3].text
        album.label = album_dd[4].text
        album.format = album_dd[5].text
        album.limitation = album_dd[6].text
        album.additional_notes = soup.find('div', {'id': 'album_tabs_notes'}).text
        album.songs = []
        album.band_id = find_id(soup.find('h2').a.attrs['href'])

        songs_tr = soup.find_all('tr', {'class': ['even', 'odd']})
        for tr in songs_tr:
            song = Song(album_id=id)
            song.id = find_id(tr.contents[1].a.attrs['name'][:-1])
            song.no = clean_song_no(tr.contents[1].text)
            song.title = tr.contents[3].text
            song.length = tr.contents[5].text
            lyrics_response = _metallum_request(lyrics_endpoint, id=song.id)
            song.lyrics = lyrics_response.text

            album.songs.append(song)

    return album
