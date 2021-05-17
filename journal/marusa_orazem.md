# Maruša Oražem's Data Science Project Competition journal

## February 2021 (3h 30min)

*20. (2h): Read the article 'Testing Statistical Charts: What Makes a Good Graph?' and looked for some libraries for scraping the pictures from Google search result. Found 'google-images-download' and tried to download some images.
*24. (1h 30min): Had a discussion with teammates about article and also about what we have found about scrapping and downloading graphs.

## March 2021 (6h)

* 3\. (1h): Had a meeting with teammates and mentors. Discussed about what we have found out and how to pursue further. We decided to download plots from different browsers and also from Bachelor's and Master's degrees and Doctoral thesis.
* 8\. (3h): Started with scrapping PDF's of Bachelor degrees from Repozitorij of Ljubljana. For now I have scrapped all Bachelor degrees from FRI.
* 9\. (2h): Scrapped most of PDF's from FRI.

## April 2021 (36h)

* 2\. (4h): Scraper of RUL had several bugs, it missed almost 1/3 of all files. Fixed it. Also changed the way it downloads files, so now it's quicker.
* 10\. (2h): Looked at Bing image scraper. Original one we found was not good. Looked for others. Problem is that Bing only searches for about 150 images. Found some library and change it a bit. Tested it and downloaded images for some plots.
* 18.4\. (1h): Discussion with teammates.
* 19.4\. (5h): Started scrapping figures from journals from PLOS.
* 20.4\. (8h): Had discussion with teammates and later also with menthors. We have presented what we have done so far and discussed what we are planning to do next. Continued with scrapping PLOS. Started writing interim report.
* 21.4\. (5h): Scrapped few journals from PLOS. Registered to Amazon's Mechanical Turk, looked at how it works, how much workers are paid ...
* 22.4\. (4h): Finished interim report, talked to team mates. Also made questionaries and send them to professors and some colleagues. 
* 23.4\. (1h): Made a few changes to the code to make it more readable, added some comments.
* 27.4\. (2h): Had a discussion with team members, created 3 more questionarries and send them to friends. Also solved one.
* 28.4\. (4h): Had a discussion with teammates. Went to the beggining and looked at all bar plots and histograms and sort them again in the right group. Also went through all other plots to check for some outliers. We have decided to put only the most obvious plots in train set. We have started to check at the results of the questionarries.

## May 2021 (?)

* 1\. (4h): Looked at Amazon Mechanical Turk and tried to make a test survey. Had some troubles with understanding the procedure to do that. Found a different site names Qualttrics where you can make your survey and then export it to Amazon Mechanical Turk.
* 2\. (4h): Had a discussion with teammates about a structure of a survey we will put on Amazon Mechanical Turk. Looked at various tutorials how to make a survey. Had some problems with how to put different plots in survey for different people. Made a test survey.
* 3\. (4h): Test a test survey - I have answered various questions to see how much time does it take to answer them, so we will know how much to pay for workers. Had a meeting with teammates and menthors. After that I have changed a survey as we have discussed. Then tried to integrate it to MT, but I wasn't successful (yet).
* 9\. (2h): Correct and add some things for ul_thesis_scrapper so it worked also for FMF and EF.
* 12\. (3h): Had a discussion with team mater about our future work. We have also discussed on how we will generate pairs of plots for amazon mechanical workers. Started with implementation of our idea (ring graph connected to n nearest neighbours).
* 13\. (2h): Finished with generating pairs.
* 14\. (5h): Removed duplicates of plots, and went through all of the plots and checked each one if it is right classified.
* 15\. (2h): Wrote price calculator, so we could easily check how much we have to pay for a survey, depending on number of plots, questioner sizes ...
* 17\. (4h): Had a meeting with teammates. We have finaly made a questioner on Amazon Mechanical Turk and we have take some time to polish it, write an introduction, decide on layering, colors, ... We have put together a test sample of plots, creates csv, ... to put everithing on test survey on MT. Had a debate on pricing, calculated some final prices depending on parameters, number of plots, how many times each plot is shown, workers price ,....