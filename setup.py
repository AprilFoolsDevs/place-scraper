from os import path
from re import search
from setuptools import setup

PACKAGE_NAME = 'placescraper'
HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, PACKAGE_NAME, 'version.py'), 'r') as fp:
    VERSION = search('__version__ = \'([^\']+)\'', fp.read()).group(1)

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description='A websockets scraper for /r/place on reddit',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    url='https://github.com/PlaceDevs/place-scraper',
    author='teaearlgraycold',
    license='MIT',
    packages=[PACKAGE_NAME],
    install_requires=[
        'websocket-client',
    ],
    test_suite='nose.collector',
    zip_safe=False
)
