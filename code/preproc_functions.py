from os.path import abspath
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.feature import StopWordsRemover, Tokenizer
from pyspark.sql.functions import col,isnan, when, count, udf
from pyspark.sql.types import StringType
import emoji
import numpy as np
import re

def emoji_to_word(text):
    changed = emoji.demojize(text, delimiters=(' ', ' '))
    return changed

# https://stackoverflow.com/questions/14081050/remove-all-forms-of-urls-from-a-given-string-in-python
def remove_urls(text):
    url_free_text = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
        '',
        text
    )
    return url_free_text

def _spaces(match):
    '''recieves two strings from a regex match, return a string combining them with space between'''
    return f'{match.group(1).lower()} {match.group(2).lower()}'

def snake_case_to_words(text):
    return re.sub(r'([a-zA-Z]+)_([a-zA-Z]+)', _spaces, text)