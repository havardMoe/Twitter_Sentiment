from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import TimestampType, IntegerType, LongType

spark = SparkSession \
        .builder \
        .master('spark://10.10.28.172:7077') \
        .appName('DB_setup') \
        .enableHiveSupport() \
        .getOrCreate()

spark.sql('use twitter_data')

# read raw data
raw_data = spark.read.csv('hdfs://namenode:9000/data/*.csv', header=True)

# check if data got read
if raw_data.count() < 10:
    raise ValueError('There are no csv files in hdfs/data/\nPlease run "load_data_to_hdfs" script')

# casting columns to correct format
data = raw_data.\
withColumn('id', col('id').cast(LongType())).\
withColumn('author_id', col('author_id').cast(LongType())).\
withColumn('created_at', col('created_at').cast(TimestampType()))


# write to hive table - twitter_data.raw_data
spark.sql('drop table if exists raw_data')
data.write.format('hive').mode("overwrite").saveAsTable("raw_data")