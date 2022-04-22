CREATE DATABASE IF NOT EXISTS twitter_data;
USE twitter_data;

DROP TABLE IF EXISTS temp_raw_data;
CREATE TABLE IF NOT EXISTS temp_raw_data (
    id STRING, 
    text STRING, 
    author_id STRING, 
    created_at_string STRING, 
    geo STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde';

-- load data form hdfs
LOAD DATA INPATH '/data/*.csv'
INTO TABLE temp_raw_data;

SET hive.support.quoted.identifiers=NONE;

-- cast to proper columntypes
DROP TABLE IF EXISTS raw_data;
CREATE TABLE IF NOT EXISTS raw_data AS
SELECT `(id|author_id|created_at_string)?+.+`
    , cast(id AS BIGINT) AS id
    , cast(author_id AS BIGINT) AS author_id
    , cast(created_at_string AS TIMESTAMP) AS created_at
    FROM temp_raw_data;

-- finished with temp_raw_data
DROP TABLE IF EXISTS temp_raw_data;

-- Create table for processed dat
DROP TABLE IF EXISTS processed_data;
CREATE TABLE IF NOT EXISTS processed_data (
    id BIGINT, 
    text STRING
);

-- Sentiment Analysis Result table
DROP TABLE IF EXISTS sentiment_results;
CREATE TABLE IF NOT EXISTS sentiment_results (
    id BIGINT,
    created_at TIMESTAMP
);

DESCRIBE raw_data;
DESCRIBE processed_data;
DESCRIBE sentiment_results;
