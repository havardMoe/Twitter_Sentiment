from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, TimestampType, IntegerType
import pyspark.sql.functions as F
from preproc_functions import emoji_to_words, preprocess_all, remove_special_characters, remove_urls, remove_mentions

# Warning:
# If you have fetched tweets later than 01042022, change last line of 'query'
# Warning

spark = SparkSession \
        .builder \
        .master('spark://10.10.28.172:7077') \
        .appName('pre_processing') \
        .enableHiveSupport() \
        .config("spark.pyfiles", "preproc_functions.py") \
        .getOrCreate()

# Change to 'OFF' if it produces too much output
spark.sparkContext.setLogLevel('WARN')  
# files used for preprocessing
spark.sparkContext.addPyFile("/home/ubuntu/twitter_sentiment/code/preprocessing/preproc_functions.py")
# name of database
spark.sql('use twitter_data')

# load raw data
query = '''
    SELECT *
    FROM raw_data
    WHERE text IS NOT NULL
    AND created_at IS NOT NULL
    AND id IS NOT NULL
    AND created_at >= date"2012-01-01"
    AND created_at <= date"2022-04-01"
'''

raw_data = spark.sql(query)

# regexes and udfs
    # 1. translates emojies
    # 2. removes user mentions
    # 3. removes urls
    # 4. removes all non-numerical characters
    # 5. change multiple spaces to a single space (may be doubled due to the emoji translator)
    # 6. remove space in start of a text (may happen due to the emoji translator)
    # 7. all text to lowercase

udf_translate_emojies = udf(lambda text: emoji_to_words(text))
user_regex = r'(@\w{1,15})'
url_regex = r'(https?:\/\/)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
neg_alphanumeric_regex = r'([^ a-zA-Z])'
double_spaces_regex = r'(  +)'
start_spaces_regex = r'(^ )'

data = raw_data.\
    withColumn('text', udf_translate_emojies(col('text'))). \
    withColumn('text', F.regexp_replace(col('text'), url_regex, '')). \
    withColumn('text', F.regexp_replace(col('text'), user_regex, '')). \
    withColumn('text', F.regexp_replace(col('text'), neg_alphanumeric_regex, '')). \
    withColumn('text', F.regexp_replace(col('text'), double_spaces_regex, ' ')). \
    withColumn('text', F.regexp_replace(col('text'), start_spaces_regex, '')). \
    withColumn('text', F.lower(col('text'))
)

# write to hive table - twitter_data.proccesed_data
spark.sql('drop table if exists processed_data')
data.write.format('hive').mode("overwrite").saveAsTable("processed_data")

spark.sql('select count(*) from processed_data').show()