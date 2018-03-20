# Kent-School-Of-Law-Project

##Abstract
The main propose of this project is to work among a huge data set from the Legal project of the Kent School of Law in order to find pattern through this data and analyze potential verdict from cases. The Legal project team of the Kent School of law will try to find a pattern in past judge verdict based on several criteria in order to link a judge to a specific class regarding the profile of the defendant. The Legal project team asked for help from Illinois Institute of technology students in order to bring data science knowledge and practice inside their project in order to understand what can be made for their project and study potentials from this idea.

##I. OVERVIEW

###A - What we seek to address
Through this project, the Advance Data Mining project team will tend to help the Kent School of Law project team to understand what can be made from judgment data in order to find pattern thanks to text processing.


###B - Methodology
The IIT team will tend to understand the data first of all. After an overall understanding of the data set and cleaning the data set, we will find the most representative feature in each observation in the API and the database.
We have, through this project, to improve the process of identifying the opinion (decision of the court) and citations (there can be more than one for each opinion).
We will work on data overview thanks to representation as a graph of opinion and citations.
We will try to find the best model in order find patterns in our dataset based on what we studied during our Data Mining course but also with personal knowledge which we acquired during.

##II. DATA OVERVIEW

###A - Data source
The dataset can be found by calling an API form the Legal Project team. The data is open source and can be found in the GitHub repository: https://github.com/freelawproject/ reporters-db. Each observation is represented as a JSON object and can be obtained by calling the "courtlistener" API
with the judgment ID as a parameter: https:// www.courtlistener.com/api/rest/v3/clusters/107252/


###B - Data structure
The data base is composed of opinions, published documents from the court. Some of those documents may contain more that one opinion. One opinion is an official decision from the court, there can be one or more concurring or dissenting opinions, the most important features for each opinion is the authorship and citations.
There are 4,085,026 opinions on JSON documents representation (from the supreme court dataset) composed of 22 features, some will not be used for data analysis such as resource_uri, absolute_url.