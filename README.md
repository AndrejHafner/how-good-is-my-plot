# How good is my plot? #

Statistical plots are an essential tool for visual presentation of information, but their quality is often questionable. In order to determine which plot properties determine its quality, we construct a dataset of statistical plots obtained from student theses. We utilize the crowdsourcing platform Amazon Mechanical Turk for plot quality evaluation through pairwise plot comparisons. And we fine-tune convolutional neural networks and use them to extract image embeddings to predict plot quality. We are unable to achieve good predictive quality, which we suspect is due to poor data quality or insufficient amount of labeled data.

## Dependencies

## Getting the data
### Google images
### DuckDuckGo
### Bing
For downloading plots from Bing, we used the code in ```bing_images_scraper.py```. In ```__main__``` function you write the plot names in ```queries_to_search``` list and run the code.
### UL Thesis Scrapper
For scrapping the PDF's from https://repozitorij.uni-lj.si, use the code at ```ul_thesis_scrapper.py```. In the ```__main__``` function you specify ```faculty``` parameter for which faculty you want to scrapp the PDF's and ```files``` list where you wrote the types of work you want to download (bachelor's, master's, phd's). 

### PDF image extractor

## Classificator


## MT

You can see how did the survey on Amazon's MT look like on picture below.

![primer](link do slike)


You can calculate how much is certain survey going to cost you with ```price_calculator.py```.

Results can be obtained from the csv files found in ```src/mechanical_turk/batches``` folder.

For generating new pairs for comparisons use ```generate_pairs_based_on_scores.py```. Here you write the paths to csv files with results and call ```generate_pairs_by_scores``` function.

Analysis of the categories selected by MT workers can be seen in ```categories_analysis.ipynb```.



## Models

### Embeddings
For fitting and evaluating the models use ```quality_predictions.py```.

### ELO

![ELO count](https://github.com/AndrejHafner/how-good-is-my-plot/blob/develop/src/figures/elo_count.png)
