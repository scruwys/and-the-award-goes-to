# Data Extraction and Preparation

The dataset used in this project was scraped from various publicly available websites. This was done primarily using two Python modules: [Requests](http://docs.python-requests.org/en/master/) to retrieve the webpage content and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse through the underlying HTML elements.

See below for a brief description of the extraction scripts and outputted data sets.

## Nominations <small> ([nominations.py](https://github.com/scruwys/and-the-award-goes-to/blob/master/extract/nominations.py))</small>
The first step when attempting predict Oscar-winning films is to obtain a list of Oscar-nominated films. Wikipedia provides a separate page for each Academy Award category and lists both the nominees and winners in a (more or less) straightforward, tabular format. 

One good indicator of "Oscar success" are the other awards presented in the weeks preceding the Academy Awards. For this project, this includes the Golden Globes, the British Academy Film Awards ("BAFTA"), and the various guild awards, such as the Screen Actors Guild. Part of this project is to test the correlation between winning these awards and an Oscar. Wikipedia provides similar pages for these awards, so we can pull those as well to work them into our model.

The `extract` function in the [nominations.py](https://github.com/scruwys/and-the-award-goes-to/blob/master/extract/nominations.py) script takes these Wikipedia URLs via [inputs.csv](https://github.com/scruwys/and-the-award-goes-to/blob/master/data/inputs.csv) and outputs the following fields:

| Field    | Description          
| -------- |-------------------
| year	   | Nomination year
| award    | Award ceremony (e.g., BAFTA, Oscar, etc.)
| category | Nomination category (e.g., Actress, Picture)
| name | Nominee name
| film | Nominee film name
| href | Nominee film's Wikipedia URL
| winner | Indicates if nominee won award (binary)

This output can be found here: [nominations.csv](https://github.com/scruwys/and-the-award-goes-to/blob/master/data/nominations.csv).

## Films <small> ([films.py](https://github.com/scruwys/and-the-award-goes-to/blob/master/extract/films.py))</small>

Of course, there are other characteristics of a film that can contribute to an Oscar win. One common attribute correlated with a win, for example, is seasonality. More often than not a Oscar winner is released less than 4 months before the award ceremony in February.

I was curious to see what other attributes signal a win. Does critical reception matter more than audience reception? What about how profitable a film is? (fyi - this is covered in the [analysis](https://github.com/scruwys/and-the-award-goes-to/blob/master/notebooks/analysis.ipynb) notebook)
 
The `extract` function in the [films.py](https://github.com/scruwys/and-the-award-goes-to/blob/master/extract/films.py) script takes the Wikipedia URL and film name from [nominations.csv](https://github.com/scruwys/and-the-award-goes-to/blob/master/data/nominations.csv), scrapes various sources, and outputs the following fields:

| Field    | Description       | Source   |   
| -------- |-------------------|----------|
| year | Nomination year | nominations.csv |
| film | Nominee film name | nominations.csv |
| release_date | Release date | IMdb |
| mpaa | Film suitability rating | IMdb |
| imdb_score | IMdb rating | IMdb |
| metacritic_score | Metacritic rating | IMdb |
| rt_audience_score | Audience rating | Rotten Tomatoes |
| rt_critic_score | Critic rating | Rotten Tomatoes |
| bom_domestic | Domestic box office | Box Office Mojo |
| bom_foreign | Foreign box office | Box Office Mojo |
| bom_worldwide | Worldwide box office | Box Office Mojo |
| box_office | Estimated box office | Wikipedia |
| budget | Estimated budget | Wikipedia |
| country | Primary release country | Wikipedia |
| running_time | Length of film (in minutes) | Wikipedia
| stars_count | \# of cast listed in info box | Wikipedia
| writers_count | \# of writers listed in info box | Wikipedia

There are, of course, other attributes that could be considered. Some that come to mind are genre or number of release theaters. Perhaps that can be included in a future iteration...

The results of this extraction can be found here: [films.csv](https://github.com/scruwys/and-the-award-goes-to/blob/master/data/films.csv).

## Prepared <small> ([notebooks/prepare_data.ipynb](https://github.com/scruwys/and-the-award-goes-to/blob/master/notebooks/prepare_data.ipynb))</small>

The film and nomination datasets then needed to be combined and properly formatted to be properly ingested by our decision tree classifier. This is documented in this [Jupyter notebook](https://github.com/scruwys/and-the-award-goes-to/blob/master/notebooks/prepare_data.ipynb).

The results of this process can be found here: [prepared.csv](https://github.com/scruwys/and-the-award-goes-to/blob/master/data/prepared.csv).