# Establishing connection and authorisation:
import os
import tweepy
import pandas as pd
import json


FETCH_NEW_TWEETS = False

with open(os.path.join('..', 'keys', 'keys.json')) as f:
    twitter_keys = json.load(f)


client = tweepy.Client(bearer_token=twitter_keys['bearer_token'])