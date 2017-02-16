import re
import csv
import util
import requests
from bs4 import BeautifulSoup

def extract(opts):
    response = util.retrieve_clean_response(opts['href'])

    print response


if __name__ == '__main__':
    inputs = {'category': 'Supporting Actor', 'name': 'Edward Norton', 'winner': '0', 'award': 'Guild', 'href': 'https://en.wikipedia.org/wiki/Birdman_(film)', 'year': '2014', 'film': 'Birdman'}
    extract(inputs)