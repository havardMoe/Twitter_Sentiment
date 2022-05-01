from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType
from analysis import WordList


spark = SparkSession \
        .builder \
        .master('spark://10.10.28.172:7077') \
        .appName('wordlist_analysis') \
        .enableHiveSupport() \
        .config("spark.pyfiles", "analysis.py") \
        .getOrCreate()

# Preventing errors of having too many settings in hive-site.xml
spark.sparkContext.setLogLevel('OFF')
spark.sparkContext.addPyFile("/home/ubuntu/twitter_sentiment/code/analysis/analysis.py")
# name of database
spark.sql('use twitter_data')

query = 'SELECT id, text FROM processed_data'
df = spark.sql(query)

# wl reads the dictionary from the path, and uses this to classify words with a sentiment score
wl = WordList(which_wordlist='2477')
udf_wl_sentiment = udf(lambda text: wl.analyze(text), IntegerType())
df = df.withColumn('sentiment', udf_wl_sentiment('text'))


df.write.mode("overwrite").saveAsTable("wordlist2477_results")
