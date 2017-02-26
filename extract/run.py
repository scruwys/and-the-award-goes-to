"""
Script Runner: Executes nominations.py and films.py to extract all relevant information.
"""
import os
import csv
import util
import films
import nominations as noms

if __name__ == '__main__':
    # Step 1: Extract award-nominated films from Wikipedia
    with open('../data/inputs.csv', 'r') as inputs:
        reader = csv.DictReader(inputs)

        for row in reader:
            util.write_to_csv('../data/nominations.csv', noms.extract(row, min_year = 1960, max_year = 2016))

    print("Nominations extracted.")

    # Step 2: Extract film-specific information from Wikipedia, Box Office Mojo, Rotten Tomatoes, etc.
    with open('../data/nominations.csv', 'r') as inputs:
        reader = csv.DictReader(inputs)
        visited = []

        for row in reader:
            row['href'] = "".join(['https://en.wikipedia.org', row['href']])

            if row['film'] in visited:
                continue

            print row['year']

            try:
                util.write_to_csv('../data/films.csv', films.extract(row), isList = False)
            except:
                util.write_to_csv('../data/errors.csv', row, isList = False)

            visited.append(row['film'])