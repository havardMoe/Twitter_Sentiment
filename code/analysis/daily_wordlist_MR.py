from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from analysis import WordList
from operator import add

spark = SparkSession \
        .builder \
        .master('spark://10.10.28.172:7077') \
        .appName('wordlist_MR_analysis') \
        .enableHiveSupport() \
        .config("spark.pyfiles", "analysis.py") \
        .getOrCreate()

# name of database
spark.sql('use twitter_data')

# Preventing errors of having too many settings in hive-site.xml
spark.sparkContext.setLogLevel('OFF')
spark.sparkContext.addPyFile("/home/ubuntu/twitter_sentiment/code/analysis/analysis.py")

wl = WordList('2477')
wordlist = wl.dict
df = spark.sql('select to_date(created_at) as date, split(text, " ") as word from processed_data')

rdd = df.rdd
# creates a table 'daily_sentiment_MR' containing
# columns 'date' and 'total_sentiment'
# where total_sentiment is the sum of sentiment scores for that day
rdd.flatMapValues(lambda x: x) \
    .mapValues(lambda x: wordlist[x]) \
    .reduceByKey(add) \
    .toDF(['date', 'total_sentiment']) \
    .write.mode("overwrite").saveAsTable('daily_sentiment_MR')