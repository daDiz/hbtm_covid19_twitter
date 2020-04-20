import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from string import punctuation
import re
import pandas as pd
import numpy as np
import json
import datetime
import sys
from os import listdir
from os.path import isfile, join
from nltk import ngrams
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns


np.random.seed(42)

add_stopwords = ['amp','rt']

stop_words = set(stopwords.words('english') + ['AT_USER','URL'] + add_stopwords)

trial = 0
cutoff = 0.01

add_uni = []
add_bi = []
for i in range(trial):
    df_more_words = pd.read_csv('../data/keywords_cutoff%s_trial%s.csv' % (cutoff,i),sep='\t')

    more_words = df_more_words['word'].values

    for w in more_words:
        elems = w.split(' ')
        if len(elems) == 1:
            add_uni.append(w)
        elif len(elems) == 2:
            add_bi.append(w)
        else:
            raise Exception('only consider upto bigram')


# unigram keywords
key_uni = list(set(['covid', 'covid19', 'covid-19', 'covid_19', 'covid2019', 'coronavirus', 'pandemic', 'quarantine', 'socialdistancing', 'social-distancing', 'lockdown'] + add_uni)) 

# bigram keywords
key_bi = list(set(['social distancing', 'chinese virus', 'wuhan virus', 'work home', 'working home', 'shelter place'] + add_bi))
 
keywords = set(key_uni + key_bi)

def tidy_text(text):
     
    text = text.lower() # convert text to lower-case
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text) # remove URLs
    text = re.sub('@[^\s]+', 'AT_USER', text) # remove usernames
    text = re.sub(r'#([^\s]+)', r'\1', text) # remove the # in #hashtag
    text = re.sub("([^\x00-\x7F])+"," ",text) # remove non-ASCII characters
    #text = word_tokenize(text) # remove repeated characters (helloooooooo into hello)
    tkz = nltk.RegexpTokenizer("\\b[\\w-]+\\b")
    text = tkz.tokenize(text)

    return [word for word in text if word not in stop_words and not word.isnumeric()]


def is_covid(word_list, keywords):
    return any([k in keywords for k in word_list]) 



if __name__ == '__main__':


    inpath_list = {'cabinet':'../query_results/trump_and_cabinet', 
                    'governors':'../query_results/governors'}
    data = []

    for admin in inpath_list:
        inpath = inpath_list[admin]
        onlyfiles = sorted([f for f in listdir(inpath) if isfile(join(inpath, f))])

        for f in onlyfiles:

            elems = np.array(f.split('_'))
            ind = np.argwhere(elems == 'tweets')[0,0]
            name = '_'.join(elems[:ind])

            df = pd.read_csv(join(inpath,f))
            df['tidy_text'] = df['text'].apply(tidy_text)
            
            df['is_covid'] = df['tidy_text'].apply(lambda x: is_covid(x, keywords))

            df['tidy_text'] = df['tidy_text'].apply(lambda x: ' '.join(x))

            df1 = df[df['is_covid'] == True]

            tmp = df1[['created_at','tidy_text']].values

            if len(tmp) == 0:
                print('%s has no covid tweets' % (name))

            for row in tmp:
                line = [name] + list(row)
                data.append(line)

    data = np.array(data)
            
    df = pd.DataFrame(data, columns=['handle','created_at','text'])

    df.to_csv('../data/tweets_cutoff%s.csv' % (cutoff), sep='\t', header=True, index=False)
