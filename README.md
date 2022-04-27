
<a name="toppp"></a>
# Twitter_Sentiment
Sentiment analysis of the Ukraine-Russia war.
#### Table of Contents:  
- [Tech/Framework Used](#tech)  
- [Short Description](#desc)  





<a name="tech"></a>
## Tech/Framework Used
- [Apache Hadoop](https://hadoop.apache.org/)
- [Apache Hive](https://hive.apache.org/)
- [Apache Spark](https://spark.apache.org/)
- [Tweepy](https://www.tweepy.org/)

<a name="desc"></a>
## Short Description:

Script  | Description
------------- | ------------- 
[fetch_twitter_data.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/scripts/fetch_twitter_data.py)  | Fetches data from the Twitter API with tweepy
[load_data_to_hdfs.sh](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/scripts/load_data_to_hdfs.sh)  | Used to load data from namenode into HDFS.
[preprocessing.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/preprocessing/preprocessing.py)  | Used to clean the data.
[preproc_functions.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/preprocessing/preproc_functions.py)  | Functions used for preprocessing.
[analysis.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/analysis/analysis.py)  | Contains functions and classes used for analysis.
[sentiment_analysis_textblob.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/analysis/sentiment_analysis_textblob.py)  | Sentiment Analysis with TextBlob.
[sentiment_analysis_vader.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/analysis/sentiment_analysis_vader.py)  | Sentiment Analysis with VaderSentiment.
[sentiment_analysis_wordlist2477.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/analysis/sentiment_analysis_wordlist2477.py)  | Sentiment analysis with wordlist2477.
[visualization.ipynb](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/visualizing/visualization.ipynb)  | Notebook for visualization of results.
[visualization_output_24hr_vertical](https://github.com/havardMoe/Twitter_Sentiment/tree/main/code/visualizing/visualization_output_24hr_vertical)  | Visualization output from notebook with sentiment scores with average every 24 hour.


## Retrieved Data
The Data were retrieved from Twitter with the use of their API and are thus under their [terms of service](https://developer.twitter.com/en/developer-terms/agreement-and-policy).

<br />
<br />

<p align="center">
    <a  href="#toppp">Back to top </a>
</p>
