import csv
import util
import films
import awards

if __name__ == '__main__':
    # # Step 1: Extract award-nominated films from Wikipedia
    # with open('../data/inputs.csv', 'r') as inputs:
    #     reader = csv.DictReader(inputs)

    #     for row in reader:
    #         util.write_to_csv('../data/awards_raw.csv', awards.extract(row))


    # # Step 2: Extract film-specific information from Wikipedia, Box Office Mojo, Rotten Tomatoes, etc.
    # with open('../data/awards_raw.csv', 'r') as inputs:
    #     reader = csv.DictReader(inputs)

    #     for row in reader:
    #         row['href'] = "".join(['https://en.wikipedia.org', row['href']])
    #         util.write_to_csv('../data/films_raw.csv', films.extract(row))