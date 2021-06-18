# How good is my plot? #

Statistical plots are an essential tool for visual presentation of information, but their quality is often questionable. In order to determine which plot properties determine its quality, we construct a dataset of statistical plots obtained from student theses. We utilize the crowdsourcing platform Amazon Mechanical Turk for plot quality evaluation through pairwise plot comparisons. And we fine-tune convolutional neural networks and use them to extract image embeddings to predict plot quality. We are unable to achieve good predictive quality, which we suspect is due to poor data quality or insufficient amount of labeled data.

## Dependencies
Reproducing this work requires you to install dependencies from the `src/requirements.txt`. 
You can create an Anaconda environment by running the following command in the root of the repository.
```
conda create --name <env_name> --file src/requirements.txt
```

## Getting the data
Plot quality evaluation first required a good dataset. We decided on using the final theses from three faculties 
from University of Ljubljana. All the images were extracted from the files using the PyMuPDF library. They had 
to be filtered, which is why we first finetuned a CNN for plot type classification (7 main statistical plot types classes and class other).
For initial finetuning we used image search results from three browsers - Google, DuckDuckGo and Bing. Below is a description on how to run each one of them.


### Google images
Setup requires you to create a file named `env.py` in `src/plot_scrapping/google_scrapper` in which you add the following.
```
GOOGLE_API_KEY = "<your-api-key>"
PROJECT_CX = "<your-project-cx>"
```
These can be obtained from the Google Custom Search API console. In the `main` function of `google_image_scrapper.py` 
the query and download folder location is specified, after which the scrapper can be run.

### DuckDuckGo
Specify the query and maximum number of search results in `duckduckgo_image_search.py` and run the scrapper.

### Bing
For downloading plots from Bing, we used the code in ```bing_images_scraper.py```. In ```main``` function you write the plot names in ```queries_to_search``` list and run the code.

### UL Thesis Scrapper
For scrapping the PDF's from [Repository of the Uni-Lj](https://repozitorij.uni-lj.si), use the code at ```ul_thesis_scrapper.py```. In the ```main``` function specify the ```faculty``` parameter for which faculty you want to scrape the PDF's and ```files``` list where you write the types of work you want to download (bachelor's, master's, phd's). 

### PDF image extractor
Run the script `extract_images_pdf.py` in which you have to specify the source directory, where there are folders containing PDF files 
from which you want to extract the images. You also need to specify the target directory, where the images are saved. Images below 
certain dimensions are not saved, since PyMuPDF extractor often returns small bits of images from the PDF, which are not actual figures. 
These dimensions can be changed in the file.

## Plot type classification
The code for plot type classification is gathered in folder ```plot_type_classification```.
Fine-tuning of the network that was used for plot type classification was done on Google Colab. We uploaded all the 
training images to Google Drive, to folder [```how_good_is_my_plot```](https://drive.google.com/drive/u/6/folders/1o9M7LNnwLZyOqnAfHzJeDKrS3x8PIXO1). 
If you want to run the training, you need to copy this folder to your drive, and connect it to Colab.
You should then upload the notebook ```plot_classification.ipynb``` to Colab and run it. 


## Amazon Mechanical Turk

Amazon Mechanical turk was used for crowdsourcing the questionnaires about the plot quality.
Swiss-system tournament was used in which pairwise comparisons between plots were evaluated by workers.
Each worker had to solve 10 plot comparisons. Below is an example of a single comparison, in which the worker 
first selects which plot is visually better and then check the reasons upon which he based the decision.

![Amazon Mechanical Turk questionnaire](https://github.com/AndrejHafner/how-good-is-my-plot/blob/develop/src/figures/questionnaire.png)

Plots used in the tournament system can be found [here](https://drive.google.com/drive/u/6/folders/1o9M7LNnwLZyOqnAfHzJeDKrS3x8PIXO1).


You can calculate how much is certain survey going to cost you with ```price_calculator.py```.
Results can be obtained from the csv files found in ```src/mechanical_turk/batches``` folder.
For generating new pairs for comparisons use ```generate_pairs_based_on_scores.py```. Here you write the paths to csv files with results and call ```generate_pairs_by_scores``` function.
Analysis of the categories selected by MT workers can be seen in ```categories_analysis.ipynb```.


## Models
The code for training and testing the models that were used for quality prediction is gathered in folder ```src/plot_quality_prediction```.

### ELO ratings
Target variable for our models was generated by fitting ELO ratings on the results obtained from Mechanical Turk.
Below you can see the density of the ELO ratings calculated on the dataset that was labeled by MT workers.

![ELO count](https://github.com/AndrejHafner/how-good-is-my-plot/blob/develop/src/figures/elo_count.png)

Below is the image that received the highest ELO score (109):

![109 elo score](https://github.com/AndrejHafner/how-good-is-my-plot/blob/develop/src/figures/9points.jpeg)

This image received median ELO score (5):

![Median elo score](https://github.com/AndrejHafner/how-good-is-my-plot/blob/develop/src/figures/median_elo.jpeg)

This is the image that received the lowest ELO score (-86):

![-86 elo score](https://github.com/AndrejHafner/how-good-is-my-plot/blob/develop/src/figures/0points.jpeg)


### Predicting quality from embeddings
Embeddings can be generated with ```extracting_embeddings.py```. 
For fitting and evaluating the models that use the embeddings for features, use ```quality_predictions.py```.

### Predicting quality by fine-tuning CNNs
Fine-tuning was done on Google Colab. To repeat it you will need to do the same setup as is described in plot type 
classification, then upload and run notebook ```plot_quality_finetuning.ipynb```.
