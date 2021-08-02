import random
import time

import click
from bs4 import BeautifulSoup

from app import app
from src.database import db
from src.metallum import (_metallum_request, find_id, scrape_album,
                          scrape_band, scrape_robots_txt)

GENRE = ['black', 'death', 'doom', 'electronic', 'avantgarde', 'folk', 'gothic', 'grind',
         'groove', 'heavy', 'metalcore', 'power', 'prog', 'speed', 'orchestral', 'thrash']
robots = scrape_robots_txt()
crawl_delay = int(robots['Crawl-delay'])


payload = {
    'sEcho': 1,
    'iDisplayStart': 0,
    'iDisplayLength': 500
}

db.init_app(app)


# @click.command('genre', help=f'Scrape by genre: {GENRE}')
def fetch_bands_by_genre(g):
    total_records = 999_999_999
    band_ids = []

    if g not in GENRE:
        click.echo(f'Please enter an option of {GENRE}')
    else:
        endpoint = f'browse/ajax-genre/g/{g}'
        endpart = '/json/1'

    while len(band_ids) < total_records:
        print(f"Fetching {payload['iDisplayStart']} to {payload['iDisplayStart'] + 500} of {total_records}")
        r = _metallum_request(endpoint=endpoint, id='', endpart=endpart, params=payload)
        json = r.json()

        total_records = json['iTotalRecords']

        for i in json['aaData']:
            soup = BeautifulSoup(i[0], 'lxml')
            href = soup.a['href']
            band_ids.append(find_id(href))

        payload['iDisplayStart'] += payload['iDisplayLength']

        # Pause crawler to conform to robots.txt crawl delay requirement.
        time.sleep(random.uniform(crawl_delay, crawl_delay + 1))

    return band_ids


def processing(band_ids):
    print('length: ' + len(band_ids))
    print('band 0 id: ' + band_ids[0])
    print('band 499 id: ' + band_ids[499])
    print('band 500 id: ' + band_ids[500])


if __name__ == '__main__':
    bands = fetch_bands_by_genre('black')
    processing(bands)
