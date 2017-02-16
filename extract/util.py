import os
import csv


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


def write_to_csv(filename, results):
    """ Writes list of dictionaries to CSV file. """
    fieldnames = results[0].keys()

    with open(filename, 'a+') as f:
    	writer = csv.DictWriter(f, fieldnames=fieldnames)
    	
    	if os.path.getsize(filename) == 0:
    		writer.writeheader()
        else:
            check_headers(filename, fieldnames)

        writer.writerows(results)