from bs4 import BeautifulSoup
from tqdm import tqdm

from app import create_app
from src.database import Band, db
from src.metallum import (find_id, metallum_request, metallum_session,
                          scrape_album, scrape_band)

GENRE = ['black', 'death', 'doom', 'electronic', 'avantgarde', 'folk', 'gothic', 'grind',
         'groove', 'heavy', 'metalcore', 'power', 'prog', 'speed', 'orchestral', 'thrash']


payload = {
    'sEcho': 1,
    'iDisplayStart': 0,
    'iDisplayLength': 500
}

# Initialize Flask app context and database

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all(app=app)


def get_bands_by_genre(g):
    total_records = 999_999_999
    bands = []

    endpoint = f'browse/ajax-genre/g/{g}'
    genre_json_1 = '/json/1'

    while True:
        r = metallum_request(metallum_session, endpoint=endpoint, id='', tail=genre_json_1, params=payload)
        json = r.json()

        # While loop stopping condition, when json['aaData'] == []
        if not json['aaData']:
            break

        total_records = json['iTotalRecords']

        fetching_msg = \
            f"Fetching bands {payload['iDisplayStart']} to {payload['iDisplayStart'] + 499} of {total_records}"

        pbar = tqdm(json['aaData'], desc=fetching_msg, dynamic_ncols=True)

        for i in pbar:
            soup = BeautifulSoup(i[0], 'lxml')
            href = soup.a['href']
            id = find_id(href)
            name = soup.a.text
            band = Band(id=id, name=name)
            bands.append(band)

        # Save to database
        db.session.add_all(bands)
        db.session.commit()

        payload['iDisplayStart'] += payload['iDisplayLength']

    tqdm.write('Crawling bands finished.')
    tqdm.write(f'A total of {len(bands)} bands was inserted into the database from {endpoint}.')

    return bands


def crawl_bands(bands):
    pbar = tqdm(bands, dynamic_ncols=True)
    for band in pbar:
        pbar.set_description(f'Scraping band data for {band.name} (id: {band.id})')
        band = scrape_band(band.id)
        db.session.commit()


def crawl_albums(albums):
    pbar = tqdm(albums, dynamic_ncols=True)
    for album in pbar:
        pbar.set_description(f'Scraping album data for {album.title} (id: {album.id})')
        album = scrape_album(album.id)
        db.session.commit()


def crawl_lyrics(songs):
    pbar = tqdm(songs, dynamic_ncols=True)
    for song in pbar:
        pbar.set_description(f'Scraping song lyrics for {song.title} (id: {song.id})')
        song = crawl_lyrics(song.id)
        db.session.commit()


if __name__ == '__main__':
    bands = get_bands_by_genre('avantgarde')
    crawl_bands(bands)
    db.session.close()
