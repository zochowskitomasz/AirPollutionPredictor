# Project development

The project has been developed over the course of three months. We tried to approach it as an opportunity to get some experience in both managing a project using big data solutions, and a Machine Learning task. Starting with a simple proof of concept ran on our laptops, through an easy API test ran on an old RaspberryPI, all the way to setting up our own cloud server on an old gaming laptop, we've gone through quite a journey with how this project grew. In this segment we will focus on said development.

## Roles
The roles we've assumed at the beginning changed overtime. Even though our skillsets are similar, we ended up diverging based on what seemed easier to each of us. Despite that, we often consulted each other to make sure our solutions made sense and could be integrated in the project structure easily. 
In the end our roles could be described as follows:
- Piotr Jurczyk &ndash; Data Scientist
- Jan Wyrzykowski &ndash; Data Engineer
- Tomasz Żochowski &ndash; Infrastructure Engineer

## Timeline
As mentioned, we started with a simple proof of concept ran on Jupyter notebooks on our laptops. There, we conducted research into the best places to acquire weather and air quality data, both historical and live. We ended up using various sources, especially for historical weather data, which is surprisingly difficult to gather. 

After that aforementioned initial case, we moved on to scaling it up and setting up a live predictor. That was achieved on an old RaspberryPi. Here a baseline was developed, and the workings of the APIs became clearer. We quickly understood that in order to store a larger amount of historical data we would require something with more computing power. Luckily, and old gaming laptop found its way into our hands. There, we set up an ubuntu server `tartaros` and started working on moving the project there.

In order to access the server remotely, we'd tried to set up various forms of port funneling and a VPN. Even though they still are on the `tartaros` server (and work!) we ended up simply using git as an intermediary, with our Infrastructure Engineer being able to perform `git pull` at any time, and any place. It is at this time that the download scripts for the weather and air quality data were perfected. We created `import_historic_data.py`, in their image, and it allowed us to pull the last few years of data onto the server quickly.

After finishing the setup, we let it run for a few days and observed the results, tuning the model if required. Meanwhile we took on the task of documenting our work and making sure it was possible for everyone to reproduce it. This included writing the setup instructions in [README](../README.md) (which included writing a few setup scripts) as well as documentation present here.

## Challenges and solutions

It is worth noting that the development of this project was not the easiest task &ndash; from time to time we hit walls and plateaus which, fortunately, we managed to overcome each time.

The first one was hardware: we had to think of a server on which the project would run. Our own laptops were out of question, since we couldn't have left them on for such a long time. Finally, we settled on solutions described already in the timeline.

Another challenge was finding the source of data. Since one of our goals was to download it on periodical basis, we needed to use an API, or multiple APIs. We also needed a source of historical data from the same location and with the same features. Fortunately, we managed to find one API for weather data and the other one for pollution data &ndash; both providing historical and live data.

The last challenge occurred while training the model. At first, the evaluation on the test set showed nearly perfect predictions, which indicated overfitting or data leakage. It turned out that using `train_test_split`, which randomly picks records for the training and test sets, is not appropriate for dealing with time series data. The model learned how to predict missing values by looking at the closest points in the training set. After switching to `TimeSeriesSplit`, the correct way of training a model on temporal data, the evaluation metrics dropped, but the model remained robust and realistic.