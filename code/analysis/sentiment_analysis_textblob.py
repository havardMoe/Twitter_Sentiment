from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType
from textblob import TextBlob


spark = SparkSession \
        .builder \
        .master('spark://10.10.28.172:7077') \
        .appName('textblob_analysis') \
        .enableHiveSupport() \
        .getOrCreate()

# Preventing errors of having too many settings in hive-site.xml
spark.sparkContext.setLogLevel('OFF')

# name of database
spark.sql('use twitter_data')

query = 'SELECT id, text FROM processed_data'
df = spark.sql(query)

# creating udf for analysis with textblob    
sentiment_tblob = lambda text: TextBlob(text).sentiment.polarity
udf_tblob_sentiment = udf(lambda text: sentiment_tblob(text), FloatType())

sentiment_score = df.withColumn('sentiment', udf_tblob_sentiment('text'))
sentiment_score.write.mode("overwrite").saveAsTable("textblob_results")