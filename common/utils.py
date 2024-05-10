import os


def get_stopwords(path):
    stopwords = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            stopwords.append(line.strip())
    return stopwords


def is_today(time):
    if time.find(' ') == -1:
        return True
    else:
        return False
