"""
Extract film information (e.g., box office, critical reception, etc.) from various sources
"""
import re
import util

def parse_rotten_tomatoes(url):
    """ Attributes: Audience Score, Critic Score """
    response = util.retrieve_clean_response(url)

    critics = response.find('div', {'class': 'critic-score'})
    audience = response.find('div', {'class': 'audience-score'})

    c_score = util.find_first_number(critics.text.strip())
    a_score = util.find_first_number(audience.text.strip())

    return {'rt_critic_score': c_score, 'rt_audience_score': a_score}


def parse_imdb(url):
    """ Attributes: IMdb score, Metacritic Score, MPAA rating, Release date. """
    response = util.retrieve_clean_response(url)
    output = {}

    imdb_score = response.find('span', {'itemprop': 'ratingValue'})
    output['imdb_score'] = imdb_score.text.strip() if imdb_score else ""
    
    metacritic_score = response.find('div', {'class': 'metacriticScore'})
    output['metacritic_score'] = metacritic_score.text.strip() if metacritic_score else ""

    mpaa = response.find('meta', {'itemprop': 'contentRating'})
    output['mpaa'] = mpaa.attrs['content'] if mpaa else ""

    release_date = response.find('meta', {'itemprop': 'datePublished'})
    output['release_date'] = release_date.attrs['content'] if release_date else ""

    return output


def parse_box_office_mojo(url):
    """ Attributes: Domestic Gross, Foreign Gross, Worldwide Gross """
    response = util.retrieve_clean_response(url)
    output = {}

    mp_box_content = response.find('div', {'class': 'mp_box_content'})

    for record in mp_box_content.find_all('tr'):
        raw_text = util.only_ascii(record.text).strip().replace('\n', ' ').lower()

        title = re.search(r'[a-z]+', raw_text)
        money = re.search(r'\$[0-9,]+', raw_text)

        if title and money:            
            output[title.group(0)] = money.group(0)

    return output


def parse_wikipedia(response):
    """ Attributes: Budget, Running time, Number of cast members, Number of writers. """
    output = {}

    infobox = response.find('table', {'class': 'infobox'})

    for record in infobox.find_all('tr'):
        th = record.find('th')
        td = record.find('td')

        if th and th.text.strip() in ['Budget', 'Running time', 'Country']:
            field = "_".join(th.text.strip().split()).lower()
            output[field] = td.text.strip().split('\n')[0] if td else ""

        if th and th.text.strip() in ['Written by', 'Screenplay by']:
            count = len(td.find_all('li'))
            output['writers_count'] = count if td and count > 0 else 1 # someone had to write it...

        if th and th.text.strip() == 'Starring':
            output['stars_count'] = len(td.find_all('li')) if td else ""

    return output


def extract(opts):
    response = util.retrieve_clean_response('https://en.wikipedia.org/wiki/The_Revenant_(2015_film)')
    infobox = response.find('table', {'class': 'infobox'})
    output = {'film_id': '', 'film': ''}
    attrs = parse_wikipedia(response)
    output.update(attrs)

    for link in response.find_all('a'): #.find_all('a', {'class': 'external'}):
        attrs = {}

        if 'href' not in link.attrs:
        	continue

        if 'www.rottentomatoes.com' in link['href']:
        	print link
            # attrs = parse_rotten_tomatoes(link['href'])

        if 'www.imdb.com' in link['href']:
        	print link
            # attrs = parse_imdb(link['href'])

        if 'www.boxofficemojo.com' in link['href']:
        	print link
            # attrs = parse_box_office_mojo(link['href'])

        # merge attrs with output
        output.update(attrs)
    
    print output

if __name__ == '__main__':
    extract({})
    # print "These are not the droids you're looking for..."