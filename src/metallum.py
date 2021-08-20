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

import time
import random
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from src.database import Album, Song

HEADER = {'User-Agent': 'Mozilla/5.0 Gecko/20100101 Firefox/90.0'}


metallum_session = requests.Session()


def metallum_request(s, endpoint=None, id=None, base_url=None, tail=None, params=None, pbar=None):
    if not base_url:
        base_url = 'https://www.metal-archives.com'
    if not id:
        id = ''
    if not tail:
        tail = ''

    url = urljoin(base=base_url, url=f'{endpoint}{id}{tail}')
    timeout_n = 0

    time.sleep(random.uniform(0.5, 2.0))  # Wait between 0.5 and 2 seconds for initial request

    while timeout_n < 10:  # Loop 10 times before quitting
        try:
            r = s.get(url, headers=HEADER, params=params)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as errh:
            timeout_n += 1
            err_msg = f'{errh}. Retrying attempt {timeout_n} of 10.'
            if pbar:
                pbar.write(err_msg)
            else:
                print(err_msg)
            time.sleep(random.uniform(3.0, 4.0))  # Wait between 3 and 4 seconds before resuming


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
    r = metallum_request(metallum_session, 'robots.txt', id='')
    lines = r.text.splitlines()
    for line in lines:
        line = line.split(': ')
        if line[0] == 'Disallow':
            robots[line[0] + f'_{n}'] = line[1]
            n += 1
        else:
            robots[line[0]] = line[1]
    return robots


def scrape_band(band):
    band_endpoint = 'band/view/id/'
    read_more_endpoint = 'band/read-more/id/'
    albums_endpoint = 'band/discography/id/'
    albums_all_tab = '/tab/all/'
    id = band.id

    # Band Main Page
    band_response = metallum_request(metallum_session, band_endpoint, id)

    soup = BeautifulSoup(band_response.text, 'lxml')

    band.name = soup.find('h1', {'class': 'band_name'}).text

    band_dd = soup.find_all('dd')
    try:
        band.country_of_origin = band_dd[0].text
    except KeyError:
        pass
    try:
        band.location = band_dd[1].text
    except KeyError:
        pass
    try:
        band.status = band_dd[2].text
    except KeyError:
        pass
    try:
        band.formed_in = band_dd[3].text
    except KeyError:
        pass
    try:
        band.years_active = band_dd[7].text
    except KeyError:
        pass
    try:
        band.lyrical_themes = band_dd[5].text
    except KeyError:
        pass
    try:
        band.current_label = band_dd[6].text
    except KeyError:
        pass

    # Band Read More
    read_more_response = metallum_request(metallum_session, read_more_endpoint, id)
    soup = BeautifulSoup(read_more_response.text, 'lxml')
    band.read_more_text = soup.text

    # Band Discography
    albums_response = metallum_request(metallum_session, albums_endpoint, id, tail=albums_all_tab)

    soup = BeautifulSoup(albums_response.text, 'lxml')
    album_links = soup.find_all('a', {'class': ['album', 'demo', 'other', 'single']})

    # M-A discography class labels are: album, other, demo, single.
    for a in album_links:
        album = Album(id=find_id(a['href']), title=a.link, band_id=id)
        band.discography.append(album)

    return band


def scrape_album(album):
    album_endpoint = 'albums/view/id/'

    album_response = metallum_request(metallum_session, album_endpoint, id=id)
    soup = BeautifulSoup(album_response.text, 'lxml')

    album.title = soup.find('h1', {'class': 'album_name'}).text

    album_dd = soup.find_all('dd')
    try:
        album.type = album_dd[0].text
    except IndexError:
        pass
    try:
        album.release_date = album_dd[1].text
    except IndexError:
        pass
    try:
        album.catalog_id = album_dd[2].text
    except IndexError:
        pass
    try:
        album.version_desc = album_dd[3].text
    except IndexError:
        pass
    try:
        album.label = album_dd[4].text
    except IndexError:
        pass
    try:
        album.format = album_dd[5].text
    except IndexError:
        pass
    try:
        album.limitation = album_dd[6].text
    except IndexError:
        pass
    try:
        album.additional_notes = soup.find('div', {'id': 'album_tabs_notes'}).text
    except AttributeError:
        pass
    album.band_id = find_id(soup.find('h2').a.attrs['href'])

    songs_table = soup.find('table', {'class': 'table_lyrics'})
    songs_tr = songs_table.find_all('tr', {'class': ['even', 'odd']})
    for tr in songs_tr:
        song = Song(album_id=id)
        song.id = find_id(tr.contents[1].a.attrs['name'])
        song.no = clean_song_no(tr.contents[1].text)
        song.title = tr.contents[3].text
        song.length = tr.contents[5].text
        album.songs.append(song)

    return album


def scrape_lyrics(song):
    lyrics_endpoint = 'release/ajax-view-lyrics/id/'

    lyrics_response = metallum_request(metallum_session, lyrics_endpoint, id=id)

    song.lyrics = lyrics_response

    return song
