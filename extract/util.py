import re
import os
import csv
import requests
from bs4 import BeautifulSoup

def only_ascii(string):
    """ Returns only ASCII encoded characters """
    return "".join([c for c in string if ord(c) < 127])


def check_headers(filename, fieldnames):
    """ Validates input fields to file fields. """
    with open(filename, 'r') as f:
        header = csv.reader(f).next()
        overlap = set(header).intersection(fieldnames)

        if len(header) != len(overlap):
            raise Exception("Input fields must match file fields.")


def write_to_csv(filename, results, isList = True):
    """ Writes list of dictionaries to CSV file. """
    fieldnames = results[0].keys() if isList else results.keys()
    fieldnames = sorted(fieldnames)

    with open(filename, 'ab+') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if os.path.getsize(filename) == 0:
            writer.writeheader()
        else:
            check_headers(filename, fieldnames)

        if isList:
            writer.writerows(results)
        else:
            writer.writerow(results)


def retrieve_clean_response(href):
    raw_html = requests.get(href)
    raw_html = re.sub(r'\[[0-9A-Z]+\]', '', raw_html.content) # removes footnotes
    dom_tree = BeautifulSoup(raw_html, "lxml")
    # why do we do this?
    for tag in dom_tree.find_all('sup'):
        tag.replaceWith('')
    # why do we do this?
    for tag in dom_tree.find_all('td'):
        if 'rowspan' in tag.attrs.keys():
            tag.name = 'th'
    return dom_tree


def find_first_number(string):
    try:
        return re.findall(r'\b\d+\b', string)[0]
    except:
        return ""


def find_nth(haystack, needle, n):
    """ TBD. """
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start