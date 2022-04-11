import csv
from collections import defaultdict
from pyparsing import Word
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_tblob(text):
    return TextBlob(text).sentiment.polarity

# Vader is twice as fast as textblob...
def sentiment_vader(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)['compound']


class WordList:
    def __init__(self, which_wordlist, delimiter=None):   
        wordlists = {
            '2477': [r'/home/ubuntu/twitter_sentiment/code/analysis/wordlists/wl2477.txt', r'\t']
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

if __name__ == '__main__':
    n = 'i really hate politics i wish you were dead'
    p = 'love you'
    wl = WordList(r'/home/ubuntu/twitter_sentiment/code/analysis/wordlists/wl2477.txt')
    an = wl.analyze(n)
    ap = wl.analyze(p)
    print(ap)
   