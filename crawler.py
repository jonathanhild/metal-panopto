from bs4 import BeautifulSoup
from tqdm import tqdm

from app import create_app
from src.database import Band, db
from src.metallum import (find_id, metallum_request, metallum_session,
                          scrape_album, scrape_band)

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'NBR', '~']


# Initialize Flask app context and database

app = create_app()
app.app_context().push()

db.create_all(app=app)


def get_bands_by_letter(letter):
    total_records = 999_999
    counter = 0
    endpoint = f'browse/ajax-letter/l/{letter}'
    genre_json_1 = '/json/1'
    payload = {
        'sEcho': 1,
        'iDisplayStart': 0,
        'iDisplayLength': 500
    }

    pbar = tqdm(total=total_records, dynamic_ncols=True)

    while True:
        r = metallum_request(metallum_session, endpoint=endpoint, id='', tail=genre_json_1, params=payload, pbar=pbar)
        json = r.json()

        # While loop stopping condition, when json['aaData'] == []
        if not json['aaData']:
            break

        total_records = json['iTotalRecords']

        pbar.total = total_records
        bands_from = payload['iDisplayStart'] + 1
        if (payload['iDisplayStart'] + 500) > total_records:
            bands_to = total_records
        else:
            bands_to = payload['iDisplayStart'] + 500
        pbar.desc = f"Fetching bands {bands_from} to {bands_to} for letter '{letter}'."

        for i in json['aaData']:
            soup = BeautifulSoup(i[0], 'lxml')
            href = soup.a['href']
            id = find_id(href)
            name = soup.a.text
            band = Band(id=id, name=name)
            db.session.add(band)
            counter += 1

            pbar.update()

            # Save to database
            db.session.commit()

        payload['iDisplayStart'] += payload['iDisplayLength']

    tqdm.write('Crawling bands finished.')
    tqdm.write(f'A total of {counter} bands was inserted into the database from {endpoint}.')
    pbar.clear()


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
    for letter in letters:
        get_bands_by_letter(letter)
