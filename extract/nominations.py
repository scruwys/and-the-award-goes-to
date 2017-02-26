"""
Extracts award-nominated films from Wikipedia
"""
import re
import util

def check_for_winner(record, colors=['b0c4de', 'faeb86', 'd3d3d3', 'ccc']):
    record = record if 'style' in record.attrs else record.find('td')

    if record and 'style' in record.attrs:
        for color in colors:
            if color in record['style'].lower():
                return 1
    return 0


def determine_film_year(content):
    match = re.search(r'[0-9]{4}', content)
    return match.group(0) if match else ""


def extract(opts, min_year = 1960, max_year = 2016):
    response = util.retrieve_clean_response(opts['href'])
    wikitables = response.find_all('table', {'class': 'wikitable'})

    cache = []

    for table in wikitables:
        records = table.find_all('tr')
        film_year = determine_film_year(table.text[0:25]) # for Oscar best picture year

        for num, record in enumerate(records):
            if num == 0: continue; # skip headers
        	
            ### Determine film year ###
            check_for_year = determine_film_year(record.text[0:25])

            if check_for_year: # failing for space odyssey
                film_year = check_for_year

            if not film_year.isdigit():
                continue

            if film_year.isdigit() and (min_year > int(film_year) or int(film_year) > max_year):
                continue

            ### Assign film information to dictionary ###
            output = {'year': film_year, 'category': opts['category'].strip(), 'award': opts['award'].strip()}            
            output['winner'] = check_for_winner(record)

            fields = record.find_all('td')
            header = record.find('th')

            if 'British Academy Film Awards' in str(record):
                continue

            try:
                name_obj = fields[int(opts['name_col'])]
                name = name_obj.find('a')
                film = fields[int(opts['film_col'])].find('a')

                output['name'] = name.text.encode('utf-8') if name else name_obj.text.encode('utf-8')
                output['film'] = film.text.encode('utf-8').replace('&', 'and')
                output['href'] = film['href']
            except:
                # STILL HAVE ISSUE WITH ROWSPAN
            	continue
 
            ### Get rid of some rogue records ###
            if str(film_year) == output['name']:
                continue

            ### Clean the output ###
            for key, value in output.items():
                output[key] = util.only_ascii(str(value)).strip().replace('\n', ' ')

            cache.append(output)
            
    return cache

if __name__ == '__main__':
    print "These aren't the droids your looking for..."