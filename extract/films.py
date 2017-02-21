"""
Extract film information (e.g., box office, critical reception, etc.) from various sources
"""
import re
import util
from bs4 import BeautifulSoup

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

field_names = [
    'bom_domestic',
    'bom_foreign',
    'bom_worldwide',
    'box_office',
    'budget',
    'country',
    'film',
    'imdb_score',
    'metacritic_score',
    'mpaa',
    'release_date',
    'rt_audience_score',
    'rt_critic_score',
    'running_time',
    'stars_count',
    'writers_count']

def parse_rotten_tomatoes(url):
    """ Attributes: Audience Score, Critic Score """
    response = util.retrieve_clean_response(url)

    critics = response.find('div', {'class': 'critic-score'})
    audience = response.find('div', {'class': 'audience-score'})

    c_score = util.find_first_number(critics.text.strip()) if critics else ""
    a_score = util.find_first_number(audience.text.strip()) if audience else ""

    return {'rt_critic_score': c_score, 'rt_audience_score': a_score}


def parse_imdb(url):
    """ Attributes: IMdb score, Metacritic Score, MPAA rating, Release date. """
    response = util.retrieve_clean_response(url)
    output = {}

    title_bar = response.find('div', {'class': 'titleBar'})

    if not title_bar:
        return output

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
    output = {'bom_domestic': '', 'bom_foreign': '', 'bom_worldwide': ''}

    mp_box_content = response.find('div', {'class': 'mp_box_content'})

    if not mp_box_content:
       return output

    for record in mp_box_content.find_all('tr'):
        raw_text = util.only_ascii(record.text).strip().replace('\n', ' ').lower()

        title = re.search(r'[a-z]+', raw_text)
        money = re.search(r'\$[0-9,]+', raw_text)

        if title and money and "bom_{0}".format(title.group(0)) in output.keys():
            output['bom_'+title.group(0)] = util.only_ascii(money.group(0))

    return output


def parse_wikipedia(response):
    """ Attributes: Budget, Running time, Number of cast members, Number of writers. """
    output = {'budget': '', 'running_time': '', 'country': '', 'box_office': ''}

    infobox = response.find('table', {'class': 'infobox'})

    for record in infobox.find_all('tr'):
        th = record.find('th')
        td = record.find('td')

        if th and th.text.strip() in ['Budget', 'Running time', 'Country', 'Box office']:
            field = "_".join(th.text.strip().split()).lower()
            output[field] = util.only_ascii(td.text.strip().split('\n')[0]) if td else ""

        if th and th.text.strip() in ['Written by', 'Screenplay by']:
            count = len(td.find_all('li'))
            output['writers_count'] = count if td and count > 0 else 1 # someone had to write it...

        if th and th.text.strip() == 'Starring':
            count = len(td.find_all('li'))

            if count == 0:
                count = len(td.find_all('a'))

            output['stars_count'] = count if count > 0 else ""

    return output


def extract(opts):
    response = util.retrieve_clean_response(opts['href'])
    infobox = response.find('table', {'class': 'infobox'})
    
    output = {'film': opts['film']}

    attrs = parse_wikipedia(response)
    output.update(attrs)

    elen = str(response).find('<span class="mw-headline" id="External_links">External links</span>')
    response = str(response)[elen:]
    response = response[:find_nth(response, "</ul>", 3)]
    soup = BeautifulSoup(response, "lxml")

    links = set([link['href'].replace('https', 'http') 
                    for link in soup.find_all('a') if link and 'href' in link.attrs])

    for link in links:
        attrs = {}

        if 'archive' in link:
           continue

        if 'www.rottentomatoes.com/m/' in link:
            attrs = parse_rotten_tomatoes(link)

        if 'www.imdb.com' in link:
            attrs = parse_imdb(link)

        if 'http://www.boxofficemojo.com/movies/' in link and 'page' not in link:
            attrs = parse_box_office_mojo(link)

        # merge attrs with output
        output.update(attrs)
    
    for field in field_names:
        if field not in output.keys():
            output[field] = ""

    for key, value in output.items():
        output[key] = util.only_ascii(str(value)).strip().replace('\n', ' ')
    
    return output

if __name__ == '__main__':
    # output = extract({'href': 'https://en.wikipedia.org/wiki/The_Last_King_of_Scotland_(film)', 'film': ''})
    # print output
    print "These are not the droids you are looking for..."