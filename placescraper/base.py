import requests
import re
import time
import json
import sqlite3
from websocket import create_connection


class PlaceScraper(object):
    def __init__(self):
        self.insert_queue_size = 0
        self.place_count = 0
        self.max_queue_size = 100  # A count of database transactions
        self.save_frame_per = 20000  # A count of 'place' events

    def scrape_websocket_forever(self, db_name):
        self.db_init(db_name)
        url = self.get_place_url()
        self.ws = create_connection(url)
        self.save_bitmap()  # Store the initial board

        while True:
            try:
                raw_frame = self.ws.recv_frame()
                frame = json.loads(raw_frame.data.decode('utf-8'))
                print(frame)

                if frame['type'] == 'place':
                    self.handle_place(frame)
                elif frame['type'] == 'activity':
                    self.handle_activity(frame)
                elif frame['type'] == 'batch-place':
                    self.handle_batch_place(frame)
                else:
                    print('Unknown frame type: {}'.format(frame['type']))

            except KeyboardInterrupt:
                print('Exiting safely...')
                self.conn.commit()
                self.conn.close()
                self.ws.close()
                return
            except Exception as e:
                print('Error occured: {} {}'.format(str(type(e)), str(e)))

    def read_websocket_forever(self):
        url = self.get_place_url()
        self.ws = create_connection(url)

        while True:
            try:
                raw_frame = self.ws.recv_frame()
                frame = json.loads(raw_frame.data.decode('utf-8'))
                yield frame
            except KeyboardInterrupt:
                print('Exiting safely...')
                self.ws.close()
                raise StopIteration
            except Exception as e:
                print('Error occured: {} {}'.format(str(type(e)), str(e)))

    def db_init(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.c.execute(
        '''CREATE TABLE IF NOT EXISTS placements (
            recieved_on INTEGER,
            y INTEGER,
            x INTEGER,
            color INTEGER,
            author TEXT
        )''')
        self.c.execute(
        '''CREATE TABLE IF NOT EXISTS activity (
            recieved_on INTEGER,
            count INTEGER
        )''')
        self.c.execute(
        '''CREATE TABLE IF NOT EXISTS starting_bitmaps (
            recieved_on INTEGER,
            data BLOB
        )''')
        self.c.execute('CREATE INDEX IF NOT EXISTS placements_recieved_on_idx ON placements (recieved_on)')
        self.c.execute('CREATE INDEX IF NOT EXISTS placements_author_idx ON placements (author)')
        self.c.execute('CREATE INDEX IF NOT EXISTS placements_color_idx ON placements (color)')
        self.c.execute('CREATE INDEX IF NOT EXISTS activity_recieved_on_idx ON activity (recieved_on)')
        self.c.execute('CREATE INDEX IF NOT EXISTS bitmaps_recieved_on_idx ON starting_bitmaps (recieved_on)')
        self.conn.commit()

    def save_bitmap(self):
        resp = requests.get('https://www.reddit.com/api/place/board-bitmap')
        self.c.execute('INSERT INTO starting_bitmaps VALUES (?, ?)', [
            int(time.time()),
            resp.content
        ])
        self.conn.commit()

    def get_place_url(self):
        match = None

        while match is None:
            # Forgive me, for I am a sinner
            resp = requests.get('https://reddit.com/r/place')
            url_re = re.compile(r'"place_websocket_url": "([^"]+)"')
            matches = re.findall(url_re, resp.content.decode('utf-8'))

            if len(matches) > 0:
                match = matches[0]

        return match

    def commit_queue_check(self):
        if self.insert_queue_size >= self.max_queue_size:
            self.conn.commit()
            self.insert_queue_size = 0
        if self.place_count >= self.save_frame_per:
            self.save_bitmap()
            self.place_count = 0

    # Frame type handlers
    def handle_place(self, frame):
        self.c.execute('INSERT INTO placements VALUES (?, ?, ?, ?, ?)', [
            int(time.time()),
            frame['payload'].get('x'),
            frame['payload'].get('y'),
            frame['payload'].get('color'),
            frame['payload'].get('author')
        ])

        self.place_count += 1
        self.insert_queue_size += 1
        self.commit_queue_check()

    def handle_activity(self, frame):
        self.c.execute('INSERT INTO activity VALUES (?, ?)', [
            int(time.time()),
            frame['payload'].get('count')
        ])

        self.insert_queue_size += 1
        self.commit_queue_check()

    def handle_batch_place(self, frame):
        for x in frame['payload']:
            self.handle_place(frame)


def main():
    scraper = PlaceScraper()
    scraper.scrape_websocket_forever('place.sqlite')


if __name__ == '__main__':
    main()
