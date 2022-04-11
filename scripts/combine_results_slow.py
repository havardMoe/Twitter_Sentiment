from pyspark.sql import SparkSession

spark = SparkSession \
        .builder \
        .master('spark://10.10.28.172:7077') \
        .appName('joining_result_tables') \
        .enableHiveSupport() \
        .getOrCreate()

spark.sql('use twitter_data')

join = '''
    SELECT
        processed_data.id
            AS id,
        textblob_results.sentiment 
            AS textblob_sentiment,
        vader_results.sentiment 
            AS vader_sentiment,
        wordlist2477_results.sentiment 
            AS wordlist2477_sentiment,
        processed_data.created_at 
            AS created_at
    FROM
        processed_data,
        textblob_results,
        vader_results,
        wordlist2477_results
    WHERE
        processed_data.id = 
        textblob_results.id = 
        vader_results.id =
        wordlist2477_results.id
'''
# perform join
joined_results = spark.sql(join)

# write to results table
joined_results.write.mode("overwrite").saveAsTable("results")