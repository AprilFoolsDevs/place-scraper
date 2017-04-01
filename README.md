place-scraper
===

[![PyPI version](https://badge.fury.io/py/placescraper.svg)](https://badge.fury.io/py/placescraper)

A websockets scraper for /r/place on reddit

### Installation
You can download this package on PyPI for Python 3 with pip:

```shell
$ pip3 install placescraper
```

### Requirements

* The `websocket-client` package from PyPI
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
