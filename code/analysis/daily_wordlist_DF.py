from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType
import pyspark.sql.functions as F
from analysis import WordList


spark = SparkSession \
        .builder \
        .master('spark://10.10.28.172:7077') \
        .appName('wordlist_DF_analysis') \
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


df = spark.sql('select to_date(created_at) as date, text from processed_data')

wl = WordList(which_wordlist='2477')
udf_wl_analyze = udf(lambda text: wl.analyze(text), IntegerType())

df.withColumn('sentiment', udf_wl_analyze('text')). \
    groupBy(F.window('date', '1 day')). \
    sum(). \
    select([
        F.to_date(F.col('window.start')).alias('date'), 
        F.col('sum(sentiment)').alias('total_sentiment')]). \
    write.mode('overwrite').saveAsTable('daily_sentiment_DF')