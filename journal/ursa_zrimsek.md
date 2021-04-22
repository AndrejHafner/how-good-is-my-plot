# Urša Zrimšek's Data Science Project Competition journal

## February 2021 (3h 30min)

* 20\. (2h): Studied the article "What makes a good graph?" and tried to find how we could use it.
* 24\. (1h 30m): Discussion with team mates.

## March 2021 (1h 30min)

* 3\. (1h 30min): Had a meeting with teammates and mentors. Discussed about what we have found out and how to pursue 
further. Before the meeting I prepared the talking points and our questions.

## April 2021 (?)

* 6\. (2h): Studied options for plot type classification. Decided to use pytorch pretrained CNNs, which we can use for 
embeddings of the plot images, to then further classify them based on cosine distance or with SVM. If that won't work well, 
we can finetune the CNNs and classify directly with them.
* 7\. (5h): Made embeddings of images scraped from Google. I used ResNet101 trained on ImageNet.
Prepared code for fine-tuning ResNet101 to classify between the types of plots. For fine-tuning we first need more data,
then we can try to classify the plots directly with the trained net, or we can take the embeddings from it and train 
another classifier.
* 14\. (3h): Downloaded and cleaned images from Google and DuckDuckGo.
* 15\. (3h): Brainstorming for questionnaire. Extracting images from FRI bachelor thesis. Enabled fine 
tuning on Google Colab. On 7 classes of plots we achieved 93% accuracy on validation set with ResNet101.
* 16\. (1h): Discarded small images. Filtered extracted images to build a dataset for 8th class - not a plot. With it we
will try to classify all the extracted images directly with CNN.
* 18\. (2h): Selected random images for train and validation set for the not_plot class. Fine tuned ResNet101 and 
achieved the same accuracy as with 7 classes - we could also try taking a bigger dataset for non-plots. Meeting with 
teammates about questionnaires.
* 19\. (5h 30min): Implemented classification with CNN trained as described above. There is an option of showing the 
images together with predicted probabilities. Copied first 1000 images into predicted classes, depending on how sure the
algorithm was in the predictions (>99% / >90% / not sure). For better learning we should filter them again by hand and 
add more training images on which it was wrong or not sure.
* 20\. (4h): Discussion with teammates, meeting with mentors. Filtering first 2000 images and adding wrongly classified
to correct categories in training set. Extracted images from masters and phd thesis.
* 21\. (1h 30min): Discussion with teammates about the first questionnaire. Further training of the CNN. Observing the
predictions on the first 2000 images - it worked almost perfectly (because the hard images were already in the training 
set). Run the filtering on the whole batchelor thesis dataset.
* 22\. (5h): Observing predictions on the whole dataset. Writing report. Corrected the training to select the model with
the best loss, not the best accuracy. Overviewing report and discussing questionnaires.

