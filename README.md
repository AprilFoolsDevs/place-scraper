place-scraper
===

[![PyPI version](https://badge.fury.io/py/placescraper.svg)](https://badge.fury.io/py/placescraper)

A websockets scraper for /r/place on reddit

This project will store:

* Every pixel update recieved
* Every activity (player count) update recieved
* The entire 1000x1000 image after every 20,000 pixel changes

Each of the above is placed in its own indexed table in a SQLite file, along with the timestamp of its arrival. Note that due to reddit's issues with server overloading, you will likely miss some pixel updates. Reddit has also been turning off the activity updates at times, so don't worry if you can't see any of those coming in.

### Installation
You can download this package on PyPI for Python 3 with pip:

```shell
$ pip3 install placescraper
```

### Requirements

* The `requests` and `websocket-client` packages from PyPI
* Python 3.X

### Running the scraper

You can either download the file at `placescraper/base.py` and just run it from
the terminal:

```shell
$ python3 base.py # This will create a SQLite file called place.sqlite
```

or you can use the scraper as a class like this:

```python
from placescraper import PlaceScraper

scraper = PlaceScraper()
scraper.scrape_websocket_forever('place.sqlite')
```

If you don't want to utilize PlaceScraper's database functionality, you can
have it just feed you the frames from the websocket through a generator

```python
scraper = PlaceScraper()
for frame in scraper.read_websocket_forever():
    # Do something with the frame
```
