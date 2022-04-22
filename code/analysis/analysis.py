import csv
from collections import defaultdict
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import random

def sentiment_tblob(text):
    return TextBlob(text).sentiment.polarity

# todo: remove
def old_sentiment_vader(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)['compound']


class WordList:
    def __init__(self, which_wordlist, delimiter=None):   
        wordlists = {
            '2477': [r'/home/ubuntu/twitter_sentiment/code/analysis/wordlists/wl2477.txt', '\t']
        }
        if which_wordlist not in wordlists:
            raise ValueError('specified wordlist is not in the dictionary\nadd it or try another one')

        path, delimiter = wordlists[which_wordlist]

        self.dict = defaultdict(int)  # dict returns 0 if key not in dict
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=delimiter)
            for [word, score] in reader:
                self.dict[word] = int(score)

    def analyze(self, text):
        '''Score is 0 for a word which is not in the dictionary
        * words is a list of words'''
        score = sum(self.dict[word] for word in text.split(' '))
        return score

def analyze_random_sentence(n, analyzer, n_print=0):
    names = ['ola', 'anna', 'jack', 'daniel', 'adam', 'eva']
    verbs = ['cycles', 'rides', 'watches', 'shoots', 'paints', 'slams', 'jams']
    sentiment = ['hates', 'love', 'likes', 'dislikes', 'rages', 'kills', 'kisses']
    nouns = ['a bike', 'a machine', 'a person', 'a painting', 'a plane', 'a ball']
    printed = 0
    start = time.time()
    for _ in range(n):
        sentence = ' '.join([random.choice(names), random.choice(verbs), random.choice(sentiment), random.choice(nouns)])
        sent_score = analyzer(sentence)
        if printed < n_print:
            print(sentence, sent_score, sep=' score:')
            printed += 1

    return time.time() - start


if __name__ == '__main__':
    pass
    n = 10000

    wl = WordList('2477')
    t = analyze_random_sentence(n, wl.analyze)
    print(f'wordlist: {t}')
   
    t = analyze_random_sentence(n, old_sentiment_vader)
    print(f'vader: {t}')

    t = analyze_random_sentence(n, sentiment_tblob)
    print(f'blob: {t}')

    vad = SentimentIntensityAnalyzer()
    new_vad = lambda text: vad.polarity_scores(text)['compound']
    t = analyze_random_sentence(n, new_vad)
    print(f'new_vad: {t}')
    