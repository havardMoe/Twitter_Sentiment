from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

spark = SparkSession \
        .builder \
        .master('spark://10.10.28.172:7077') \
        .appName('vader_analysis') \
        .enableHiveSupport() \
        .getOrCreate()

# Preventing errors of having too many settings in hive-site.xml
spark.sparkContext.setLogLevel('OFF')
# spark.sparkContext.addPyFile("/home/ubuntu/twitter_sentiment/code/analysis/analysis.py")
# name of database
spark.sql('use twitter_data')

query = 'SELECT id, text FROM processed_data'

df = spark.sql(query)

analyzer = SentimentIntensityAnalyzer()
sentiment_vader = lambda text: analyzer.polarity_scores(text)['compound']

udf_vader_sentiment = udf(lambda text: sentiment_vader(text), FloatType())
sentiment_score = df.withColumn('sentiment', udf_vader_sentiment('text'))

sentiment_score.write.mode("overwrite").saveAsTable("vader_results")
