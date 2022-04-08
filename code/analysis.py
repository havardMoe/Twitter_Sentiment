import csv
from collections import defaultdict

class WordList:
    def __init__(self, path_to_dict=None, delimiter=None):
        if path_to_dict is None:
            path_to_dict = r'/home/ubuntu/twitter_sentiment/wordlist.txt'
        if delimiter is None:
            delimiter = '\t'  # tab
        
        self.dict = defaultdict(int)  # dict returns 0 if key not in dict
        with open(path_to_dict, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=delimiter)
            for [word, score] in reader:
                self.dict[word] = int(score)

    def analyze(self, words):
        '''score is 0 for a word which is not in the dictionary
        * words is a list of words'''
        score = sum(self.dict[word] for word in words)
        return score

    def show_dict(self):
        print(self.dict)

if __name__ == '__main__':
    wl = WordList()
    score = wl.analyze('i really hate politics i wish you were dead'.split(' '))
    print(score)