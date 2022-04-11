from pyspark.sql import SparkSession

spark = SparkSession \
        .builder \
        .master('spark://10.10.28.172:7077') \
        .appName('joining_result_tables') \
        .enableHiveSupport() \
        .getOrCreate()
spark.sql('use twitter_data')

processed_data = spark.sql('select id, created_at from processed_data')
textblob_results = spark.sql('select id, sentiment AS textblob_sentiment from textblob_results')
vader_results = spark.sql('select id, sentiment AS vader_sentiment from vader_results')
wordlist2477_results = spark.sql('select id, sentiment AS wordlist2477_sentiment from wordlist2477_results')

# join all dataframes and write to table
combined_results = processed_data \
.join(
    textblob_results,
    'id',
    how='inner'
).join(
    vader_results,
    on='id',
    how='inner'
).join(
    wordlist2477_results,
    on='id',
    how='inner'
).write.mode("overwrite").saveAsTable("results")