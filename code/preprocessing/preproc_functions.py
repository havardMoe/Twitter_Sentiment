import emoji
import re
from textblob import TextBlob


def emoji_to_words(text):
    changed = emoji.demojize(text, delimiters=(' ', ' '))
    return snake_case_to_words(changed)

# https://stackoverflow.com/questions/14081050/remove-all-forms-of-urls-from-a-given-string-in-python
def remove_urls(text):
    url_free_text = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
        '',
        text
    )
    return url_free_text

def remove_special_characters(text):
    return re.sub(r'[^ a-zA-Z]', '', text)

def _spaces(match):
    '''recieves two strings from a regex match, return a string combining them with space between'''
    print(match)
    return f'{match.group(1)} {match.group(2)}'

def snake_case_to_words(text):
    return re.sub(r'([a-zA-Z])_([a-zA-Z])', _spaces, text)

def spell_correction(text):
    txt_blob = TextBlob(text)
    correct = txt_blob.lower().correct()
    return correct.raw

def remove_mentions(text):
    return re.sub(r'@[/w]+', '', text)

def preprocess_all(
    text, 
    translate_emoji=False, 
    del_urls=False,
    del_mentions=False,
    del_non_numeric=False,
    spell_correction=False,
    lower=False,
    ):
    '''functions that combines all the other preprocessing techniques'''
    if translate_emoji:
        text = emoji_to_words(text)  # works alone
    if del_urls:
        text = remove_urls(text)  # does most likely not work (waited like 3 minutes)
    if del_mentions:
        text = remove_mentions(text)
    if del_non_numeric:
        text = remove_special_characters(text)
    if spell_correction:
        # spell correction is taking way too long
        text = spell_correction(text)
    if lower:
        text = text.lower()
    return text

if __name__ == '__main__':
    txt = 'something 🤬'
    res = emoji_to_words(txt)
    print(res)
