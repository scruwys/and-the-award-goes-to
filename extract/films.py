#
# 
#
import re
import util

def parse_rotten_tomatoes():
	""" Attributes: Audience Score, Critic Score (# of ratings?) """
	return False


def parse_imdb():
	""" TBD. """
	return False


def parse_box_office_mojo():
	""" Attributes: Domestic Gross, Foreign Gross, Worldwide Gross """
	return False


def parse_wikipedia():
	""" Attributes: Running time, """
	return False


def extract(opts):
    response = util.retrieve_clean_response(opts['href'])
    infobox = response.find('table', {'class': 'infobox'})

    # for item in infobox.find_all('th'):
    # 	print item.text.strip()

    for item in response.find_all('a', {'class': 'external'}):
    	print item

if __name__ == '__main__':
    print "These are not the droids you're looking for..."