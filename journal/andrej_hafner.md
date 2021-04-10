# Andrej Hafners's Data Science Project Competition journal

## February 2021 (3h 30m)

* 20\. (1h): Searched for programs to extract images from PDF. Found a Python library PyMuPDF, which works well. Also searched for ways to scrape Google image search results. Tried some open source implementations, most of them don't work since Google actively tries to prevent scraping their results.
* 24\. (2h 30m): Read the article on quality of plots and what makes a good plot. Searched for different ways to scrap images from search engines, since scraping Google is not easy. DuckDuckGo has an open API which returns image links based on the given query (only requires a token which can be acquired with a pre request). There is also an open implementation of a scraper for Bing. We also had a discussion with other teammates about the classificator for plots. We will use neural network for embeddings in which we'll train a classifier. We also discussed what properties of the plot could be gathered using a survey and how would that benefit our research.

## March 2021 [Add!]

* 3\. (1h): Meeting with mentors and discussion about the project course. We decided to continue with scrapping of plots from different browsers on which we will build a classificator for different types (potentially one vs. all SVM). Discussion about the approaches on how to evaluate the quality of graphs.
* 7\. (1h): Tested google image search through their custom search API. Used a library which also downloads all of the images from the search query. There are some problems with the library which i'll try to solve next time (errors when downloading certain images).
