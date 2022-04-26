# With inspiration from https://github.com/jdfoote/Intro-to-Programming-and-Data-Science/blob/fall2021/extra_topics/twitter_v2_example.ipynb
import os
import tweepy
import json
import time
import csv
import argparse
from datetime import datetime, timezone

MAX_TWEETS = 10_000_000
MAX_TWEETS_PER_FILE = 100_000
MAX_TWEETS_PER_PAGE = 500

def write_csv(data, filename, new=False):
    with open(os.path.join('..', 'data', f'{filename}.csv'), 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        if new:  # new file, writing header
            writer.writerow(data)
        else:
            writer.writerows(data)

def fetch_twitter_data(client, query, start_time, end_time):
    tweets_in_file = 0
    total_fetched_tweets = 0

    start_dt = datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    end_dt = datetime.strptime(end_time,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

    total_days = (end_dt - start_dt).days

    filename = ''  # gets set iteratively for each new file
    fields = ['id','text','author_id','created_at','geo']

    for response in tweepy.Paginator(client.search_all_tweets,
                query = query,
                tweet_fields = fields,
                start_time = start_time,
                end_time = end_time,
                max_results=MAX_TWEETS_PER_PAGE               
    ):
        max_date = max([tweet.created_at for tweet in response.data])
        days_fetched = (end_dt - max_date).days
        if days_fetched % 1 == 0:
            print(f'Fetched {days_fetched}/{total_days} | {round(100*days_fetched/total_days, 1)}% of days | {round(100*total_fetched_tweets/MAX_TWEETS, 1)}% of MAX_TWEETS')

        if tweets_in_file > MAX_TWEETS_PER_FILE or tweets_in_file == 0:
            tweets_in_file = 0

            filename = f'{max_date.strftime("%Y%m%d%H%M%S")}'

            write_csv(fields, filename, new=True)  # write headers to file

        tweet_list = [[tweet.id, tweet.text.replace('\n',' '), tweet.author_id, tweet.created_at, tweet.geo] for tweet in response.data]
        write_csv(tweet_list, filename)
        time.sleep(1)
        tweets_in_file += response.meta['result_count']
        total_fetched_tweets += response.meta['result_count']

        if total_fetched_tweets > MAX_TWEETS:
            print('Max_tweets exceeded, exiting')
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--from_time')
    parser.add_argument('--to_time')

    args = parser.parse_args()
    # Find connect to tweepy client with bearer token
    key_path = r'/home/ubuntu/keys/keys.json'
    with open(key_path) as f:
        twitter_keys = json.load(f)
    client = tweepy.Client(bearer_token=twitter_keys['bearer_token'], wait_on_rate_limit=True)

    # Parameters for fetching the data
    ''''
    start_time = '2010-03-16T00:00:00Z'
    end_time = '2010-03-23T00:00:00Z'
    '''

    start_time = args.from_time
    end_time = args.to_time
    query = 'ukraine russia lang:en -is:retweet'

    try:  # check if date is on correct format
        start_dt = datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%SZ')
        end_dt = datetime.strptime(end_time,'%Y-%m-%dT%H:%M:%SZ')
    except:
        raise Exception('Wrong date format, should be: YYYY-mm-ddTHH:MM:SSZ')


    fetch_twitter_data(client, query=query, start_time=start_time, end_time=end_time)
    print('Finished!')
    