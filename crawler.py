import click
from bs4 import BeautifulSoup
from sqlalchemy import exc
from tqdm import tqdm

from app import create_app
from src.database import Album, Band, Song, db
from src.metallum import (find_id, metallum_request, metallum_session,
                          scrape_album, scrape_band, scrape_discography,
                          scrape_lyrics, scrape_read_more)

# Initialize Flask app context and database

app = create_app()
app.app_context().push()

db.create_all(app=app)


@click.group()
def main():
    pass


@main.command()
def band_list():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'NBR', '~']
    for letter in letters:
        total_records = 999_999  # Large default value to allow for request initialization.
        counter = 0
        endpoint = f'browse/ajax-letter/l/{letter}'
        genre_json_1 = '/json/1'
        payload = {
            'sEcho': 1,
            'iDisplayStart': 0,
            'iDisplayLength': 500
        }

        pbar = tqdm(total=total_records, dynamic_ncols=True, position=-1)

        while True:
            r = metallum_request(metallum_session, endpoint=endpoint, id='',
                                 tail=genre_json_1, params=payload, pbar=pbar)
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

                try:
                    db.session.add(band)
                    # Save to database
                    db.session.commit()
                except exc.IntegrityError:
                    db.session.rollback()
                    next
                counter += 1

                pbar.update()

            payload['iDisplayStart'] += payload['iDisplayLength']

        tqdm.write(f'Finished. A total of {counter} bands was inserted into the database from {endpoint}.')


@main.command()
def bands():
    bands = Band.query.filter(Band.status == None).all()
    pbar = tqdm(bands, dynamic_ncols=True, position=-1)
    tqdm.write('Crawling Bands.')
    for band in pbar:
        pbar.set_description(f'Scraping band data for {band.name} (id: {band.id})')
        scrape_band(band)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()


@main.command()
def read_more():
    bands = Band.query.filter(Band.status == None).all()
    pbar = tqdm(bands, dynamic_ncols=True, position=-1)
    tqdm.write('Crawling Bands - Read More Text.')
    for band in pbar:
        pbar.set_description(f'Scraping band data for {band.name} (id: {band.id})')
        scrape_read_more(band)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()


@main.command()
def dicography():
    bands = Band.query.filter(Band.status == None).all()
    pbar = tqdm(bands, dynamic_ncols=True, position=-1)
    tqdm.write('Crawling Bands - Read More Text.')
    for band in pbar:
        pbar.set_description(f'Scraping band data for {band.name} (id: {band.id})')
        scrape_discography(band)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()


@main.command()
def albums():
    albums = Album.query.all()
    pbar = tqdm(albums, dynamic_ncols=True, position=-1)
    tqdm.write('Crawling Albums.')
    for album in pbar:
        pbar.set_description(f'Scraping album data for {album.title} (id: {album.id})')
        scrape_album(album)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()


@main.command()
def lyrics():
    songs = Song.query.all()
    pbar = tqdm(songs, dynamic_ncols=True, position=-1)
    tqdm.write('Crawling Lyrics.')
    for song in pbar:
        pbar.set_description(f'Scraping song lyrics for {song.title} (id: {song.id})')
        scrape_lyrics(song)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()


@main.command()
@click.argument('confirm', type=click.STRING)
def delete_db(confirm):
    if confirm == 'yes':
        db.drop_all()
        click.echo('All data tables deleted.')
    else:
        click.echo("Please confirm database deletion with 'delete-db yes'")


if __name__ == '__main__':
    main()
