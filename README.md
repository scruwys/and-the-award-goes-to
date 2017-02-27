# And the award goes to...

What factors drive success in the movie award circuit? Let's use some supervised classification methods to predict who will win that Oscar gold. 

This project is meant to be a fun way to practice and learn some simple techniques typically used in data analysis and predictive modeling. Constructive commentary and suggestions are appreciated. 

[Click here to skip to the results](https://github.com/scruwys/and-the-award-goes-to#the-results).

## Dataset

The data used for this project was scraped from various publicly available websites. You can find more details on what was pulled and where it came from [here](https://github.com/scruwys/and-the-award-goes-to/tree/master/extract).

The following award categories were considered:

* Best Picture
* Best Director
* Best Actor
* Best Actress
* Best Supporting Actor
* Best Supporting Actress
* Best Original Screenplay
* Best Adapted Screenplay

Prior to building the model, the raw extracted data was transformed into a workable format. For more details on that process, please refer to this [Jupyter notebook](https://github.com/scruwys/and-the-award-goes-to/blob/master/notebooks/prepare_data.ipynb).

## Analysis of Oscar-nominated Films

This [Jupyter notebook](https://github.com/scruwys/and-the-award-goes-to/blob/master/notebooks/analysis.ipynb) contains a preliminary exploratory analysis of the extracted data. Will add more to this over the next few weeks.

## Learning Algorithms Used

Obviously, the goal is to predict whether or not a nominee will win an Academy Award. This is a binary (yes/no) result that can be best predicted using a classification algorithm. 

Keep in mind that we extracted data containing the winner for each award category for previous years. We can use this historical data to train our model so that it makes more accurate categorization. So we can therefore classify (*pun intended*) the overall project as a supervised learning problem.

My hope is to eventually implement several different algorithms and compare the results to determine which would be optimal for this problem. However, due to time constraints, I have only had the chance to implement a [decision tree classifier](https://github.com/scruwys/and-the-award-goes-to/blob/master/predict/decision_tree.py), which is described below.

#### Decisions, Decisions...

This project uses the scikit-learn implementation of a [decision tree classifier](http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html). The scikit-learn [documentation](http://scikit-learn.org/stable/modules/tree.html) provides a decent explanation of decision tree classification.

The extracted nomination data goes as far back as 1960. However, due to inconsistencies in the data and various other constraints, the input data is limited to films released from 1980 to present. This results in roughly 1450 observations across all considered award categories. After splitting the data into training (60%) and test (40%) partitions, the tested "accuracy" of the model hovered around 80% for a leaf size of 1. Not something to bet the farm on, but [I've seen worse](http://money.cnn.com/2016/11/01/news/economy/hillary-clinton-win-forecast-moodys-analytics/). :confounded:

Once the classifier had been implemented, I ran into an interesting obstacle. If I were to just run the model once, it would sometimes label multiple nominees as winners. But, as we all know, [there can be only one](https://www.youtube.com/watch?v=sqcLjcSloXs).

This obstacle was overcome using a technique called [bootstrap aggregation](https://en.wikipedia.org/wiki/Bootstrap_aggregating), or bagging. Bagging is an ensemble technique in which multiple iterations of an algorithm are run against a shuffled version of the training data set. The code for this is included below:
  
    guesses = {}
    
    for idx, film in enumerate(films_CY):      
              guesses[film] += classifier.predict([feats_CY[idx]])[0]

The key of the dictionary is the nominee name. The value of the dictionary represents the number of times that nominee has been predicted to win based on the multiple iterations. Once the cycle has completed, the nominee with the most "wins" is declared the winner.

*Note: This is arguably not the most ideal methodology, but was sufficient for this project. Any alternate methods or suggestions would be very much appreciated!*

The decision tree classifier can be run using the following command:

``` python predict/decision_tree.py --award "Adapted Screenplay" --year 2016 ```

## The Results

Here are my picks for the 89th Academy Awards using the [decision tree classifier](https://github.com/scruwys/and-the-award-goes-to/blob/master/predict/decision_tree.py).

| Award    | Nominee           | Film  | Winner? |
| -------- |-------------------| -----|:-----:|
| Picture  | La La Land        | [La La Land](https://www.rottentomatoes.com/m/la_la_land/) | :x: |
| Director | Damien Chazelle   | [La La Land](https://www.rottentomatoes.com/m/la_la_land/) | :heavy_check_mark: |
| Actor    | Denzel Washington | [Fences](https://www.rottentomatoes.com/m/fences_2016/) | :x: |
| Actress  | Emma Stone        | [La La Land](https://www.rottentomatoes.com/m/la_la_land/) | :heavy_check_mark: |
| Supporting Actor    | Mahershala Ali  | [Moonlight](https://www.rottentomatoes.com/m/moonlight_2016/) | :heavy_check_mark: |
| Supporting Actress  | Viola Davis     | [Fences](https://www.rottentomatoes.com/m/fences_2016/) | :heavy_check_mark: |
| Original Screenplay | Damien Chazelle | [La La Land](https://www.rottentomatoes.com/m/la_la_land/) | :x: |
| Adapted Screenplay  | Allison Schroeder & Theodore Melfi | [Hidden Figures](https://www.rottentomatoes.com/m/hidden_figures/) | :x: |

*UPDATE on February 27*: Hmmm. It looks like the model could use some improvement. Will need to look into adding some more features into the data. Good thing we have a year to improve!

## Future Ideas

This is just a scratchpad for the future. Feel free to contribute or make suggestions.

**Sentiment analysis:** Use the Twitter API to see what movies people are talking about. Inspired in part by [this repository](https://github.com/peacing/OscarsPredictor).

**Additional features:** Critic's Choice Awards, film festival awards, movie genre, theater distribution, past award wins.

**Additional categories:** Documentary Film, Animated Feature Film.
