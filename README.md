# C.L.O.B.A.M.A 👨‍🔧

![version](https://img.shields.io/badge/version-1-blue.svg?cacheSeconds=2592000) [![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://clobama.yolasite.com/)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

## [0] Introduction and Index 📄

This is the project Cloud-Based Machine-Learning Analysis of Previous and Hypothetical Armed Conflicts (C.L.O.B.A.M.A.). The main idea behind this project is to process large data-sets of geopolitical information -using Cloud-based techniques- of all the world countries in order to train an Artificial Intelligence model that can predict possible critical regions (hot-points) of possible armed conflicts in the near future. 

Our project was divided in two phases located in two separated pages at this website.

1. A brief discussion over the Cloud techniques employed can be found in the Cloud page ![here](https://clobama.yolasite.com/Cloud.php).

2. All the information regarding the Machine Learning algorithm is located in the Artificial Intelligence page ![here](https://clobama.yolasite.com/Artificial-Intelligence.php). 

## [1] Cloud-based pre-processing ☁️ 

### 1.1 Pre-processing
The first question that should be addressed here is why did we need to pre-process the data. Many of the information we have collected from different websites including Wikipedia did not have sufficient samples or the samples were not in an adequate shape to be directly approached using pyspark or other Machine Learning libraries. Of course, we could have directly pre-processed in Python as part of the Artificial Intelligence phase of this project. Nevertheless, that would have been a mistake as we could make use of the advantages a Cloud-based environment is capable of providing.


We thought long and hard about what features to use for the Datasets and the nature of these. We decided two useful metrics to determine the probability of an armed conflict were the GPD and the inversion in armament as such, among others.


Nevertheless, there has been some periods of time were there was no formal registry about the economical inversion on weapons, soldiers, etc. Therefore, we decided to use a technique known as **INTERPOLATION**. In the aforementioned scenarios, we have assumed that between years X and Y, the increase or decrease in the amount invested could give us a realistic approximation of the value in-between. This technique can be very reliable in cases were there are not many extreme cases (this is, a very low Standard Deviation) as this was the case here.


The same method and formula were applied for the militar inversion. Other dataset that had to be processed was the one containing the wars. The main challenge of this one was related with the cleaning, and the correct display of the dates reported. For this purposes, we have also made use of the Panda's dataframe from Python and some regular expressions. The usage of Spark for this part was discarded due to the nature of the problem, that prevented the process' parallelization. 

### 1.2 Combination

This project has required the managing of several data-sets with fairly different shapes. In order to combine the data-sets the first step was to develop a script to have the same type for the Country feature at all of them. We have used the acronyms registered at the standard ISO 3166-1 for the countries identification ids.


The second step required that the data-set had the years in which each country was involved in an armed conflict starting 1850, as we did not found any premade data-set of this nature. We collected all this information regarding countries in war at a CSV files from several sources including websites such as Wikipedia. We combined all of them into once using Cloud techniques.


The final step to combine everything required doing some processing of the data, cleaning and deleting the fields we were not interested in. For that, we used pyspark . From that code it is worth-mentioning the joining methods applied and the script made to automatize the entire process.

## [2] Machine-Learning 🤖

The goal was being able to **predict future armed conflicts** based on the data collected with the Cloud mechanisms described in the main page.We have used Scikit. The models applied were:


1.   SVM (Support Vector Machine) and LinearSVC, with a number of iterations of 10 million, which is approximately ~54 min of processing. The obtained precision gave us only 38% of correct predictions, which made us choose a second algorithm.


2. Naive Bayes (NB), GaussianNB algorithm. There are no number of iterations, so it is only 0.006 seconds. The result gave us a precision of 65.9%. 

In order to train the Artificial Intelligence and choose the optimal model, we need time as the resources will always be limited at a certain extent, even with Cloud. The algorithms chosen are not -yet- really optimized to take full advantage of the Cloud mechanism. That being said, we conclude that virtually everything related with Big Data and Artificial Intelligence should be carried out in Cloud, even if the classic Machine Learning algorithms are not yet fully optimized for this. The resources of regular computers is not sufficient to have a dynamic workflow of programming/testing as there are big slots of waiting for results, as illustrated at the right.

The estimated time for a computer with i7 3770K + 8GB RAM: Reading CSV ~ 1s and training with Artificial Intelligence a SVC algorithm ~ 1 MB data. Drawing the final Dataset takes approximately ~37 secs. Which lead us to other important highlight of **our conclusions**, which is that we could experiment in first person the elasticity of the Cloud services, that allowed us to process and manage a huge quantity in a few seconds.

## [3] Other interesting conclusions 🔬

Interestingly enough, as you can see in the graph that relates GDP and militar inversion, we can conclude that excluding certain major global powers that rely heavily on their militar actions (such as USA, China or Rusia) most of the countries experience a decrease in their inversion in weapons and such in relation with their GDP, probably because less-wealthy countries are either under a higher risk of being attacked or under direct-militar control (dictatorship) such as North Korea.


Other countries such as Spain benefit from international agreements, as it is member of the European Union, so not only they do not have to worry about adjacent countries invasion but also count with a much higher armed back-up than the one we could achieve on their own without a huge (negative) impact in our economy.

We discovered that **drawing the Confusion Matrix** was of great help to have a better perspective of the real and false positives (and negatives) of the model.Equally relevant was drawing the data and differentiate the obtained results, in this case, if there was or not a war, to have a better understanding on the erroneously generated information.

## [4] Contributors 👦

- ![Diego Isar Muñoz](https://github.com/diegoisar)
- ![Álvaro David Ortiz Marchut](https://github.com/NotAGoodDev)
- ![Ricardo Rodrigo Ruíz](https://github.com/RicardoRodrigoRuiz)
- ![Jin Wang Xu](https://github.com/JwangXu)
- ![Carlos Bilbao Muñoz](https://github.com/Zildj1an)
