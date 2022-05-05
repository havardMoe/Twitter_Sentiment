
<a name="toppp"></a>
# Twitter_Sentiment
Sentiment analysis of the Ukraine-Russia war with Hadoop, Hive, and Spark
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
[spark_set_up_raw_data.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/scripts/spark_set_up_raw_data.py)  | Set up raw data table in Hive and write in data.
[set_up_hiveDB.sql](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/scripts/set_up_hiveDB.sql)  | Old file used to set up HiveDB directly in Hive.
[preprocessing.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/preprocessing/preprocessing.py)  | Used to clean the data.
[preproc_functions.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/preprocessing/preproc_functions.py)  | Functions used for preprocessing.
[daily_wordlist_DF.py](https://github.com/havardMoe/Twitter_Sentiment/blob/d57f0d31b3ddcc0d452599b837c01e2d3aa31b5f/code/analysis/daily_wordlist_DF.py)  | Benchmark using MapReduce job on Spark DF.
[daily_wordlist_MR.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/analysis/daily_wordlist_MR.py)  | Benchmark using MapReduce job on Spark RDD.
[analysis.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/analysis/analysis.py)  | Contains functions and classes used for analysis.
[sentiment_analysis_textblob.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/analysis/sentiment_analysis_textblob.py)  | Sentiment Analysis with TextBlob.
[sentiment_analysis_vader.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/analysis/sentiment_analysis_vader.py)  | Sentiment Analysis with VaderSentiment.
[sentiment_analysis_wordlist2477.py](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/analysis/sentiment_analysis_wordlist2477.py)  | Sentiment analysis with wordlist2477.
[visualization_daily.ipynb](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/visualizing/visualization_daily.ipynb)  | Notebook for visualization of results grouped per day.
[visualization_weekly.ipynb](https://github.com/havardMoe/Twitter_Sentiment/blob/c5bbb9a0e545c8305d869071e505ab6a631d7ca3/code/visualizing/visualization_weekly.ipynb)  | Notebook for visualization of results grouped per week.
[plots](https://github.com/havardMoe/Twitter_Sentiment/tree/main/code/visualizing/plots)  | Visualization output from notebooks saved as image files.


<a name="guide"></a>
## Guide:  
Short guide to fetch twitter data, write data to raw table, perfrom preprocessing, and do sentiment analysis.
1. Fetch Twitter data:

    ```bash
    python /scripts/fetch_twitter_data.py --from_time=YYYY-mm-ddTHH:MM:SSZ --to_time=YYYY-mm-ddTHH:MM:SSZ
    ```

2. Load copy data from `/data` folder to hdfs:
    ```bash
    /scripts/load_data_to_hdfs.sh
    ```

3. Set up Hive database, read data from hdfs, and write to Hive table 'raw_data':  
    ```bash
    spark-submit /scripts/spark_set_up_raw_data.py
    ```  

4. Clean data from 'raw_data' save to new table 'preprocessed_data':  
    ```bash
    spark-submit /code/preprocessing/preprocessing.py
    ```

5. Perfrom sentiment analysis for TextBlob:  
    ```bash
    park-submit /code/analysis/sentiment_analysis_textblob.py
    ```

6. Perfrom sentiment analysis for VaderSentiment:  
    ```bash
    spark-submit /code/analysis/sentiment_analysis_vader.py
    ```

7. Perfrom sentiment analysis for WordList 2477:  
    ```bash
    spark-submit /code/analysis/sentiment_analysis_wordlist2477.py
    ```
    
8. Combine the different result tables for the analysers:  
    ```bash
    /scripts/combine_results.py
    ```
    

## Retrieved Data
The Data were retrieved from Twitter with the use of their API and are thus under their [terms of service](https://developer.twitter.com/en/developer-terms/agreement-and-policy).

<br />
<br />

<p align="center">
    <a  href="#toppp">Back to top </a>
</p>
