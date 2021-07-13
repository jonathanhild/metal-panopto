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

BASE_URL = 'https://www.metal-archives.com'
HEADER = {'user-agent': 'My-UA'}


def band(url):
    r = requests.get(url, headers=HEADER)

    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    band_dt = soup.find_all('dt')
    band_dd = soup.find_all('dd')
    band_info = dict(zip(band_dt, band_dd))

    print(band_info)


if __name__ == '__main__':
    band('https://www.metal-archives.com/bands/Wolves_in_the_Throne_Room/35741')
