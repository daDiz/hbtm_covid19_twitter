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
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import matplotlib.pyplot as plt

np.random.seed(42)

add_stopwords = ['amp','rt']

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


stop_words = set(stopwords.words('english') + ['AT_USER','URL'] + add_stopwords)



# unigram keywords
key_uni = list(set(['covid', 'covid19', 'covid-19', 'covid_19', 'covid2019', 'coronavirus', 'pandemic', 'quarantine', 'socialdistancing', 'social-distancing', 'lockdown', 'symptom', 'symptomatic', 'asymptomatic'] + add_uni)) 

# bigram keywords
key_bi = list(set(['social distancing', 'chinese virus', 'wuhan virus', 'work home', 'working home', 'shelter place'] + add_bi))
 

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


if __name__ == '__main__':

    inpath_list = ['../query_results/trump_and_cabinet', '../query_results/governors']#, '../query_results/congress']
    
    q1 = '|'.join(key_uni)
    q2 = '|'.join(key_bi)

    pos_words = []
    all_words = []
    for inpath in inpath_list:
        onlyfiles = sorted([f for f in listdir(inpath) if isfile(join(inpath, f))])

        for f in onlyfiles:
            df = pd.read_csv(join(inpath,f))
            df['tidy_text'] = df['text'].apply(tidy_text)
            
            words_list = df['tidy_text'].values

            for words in words_list: 
                #unigrams = [word for word in words if word not in omit and len(word)>2]
                unigrams = [word for word in words if len(word)>2]

                bigrams = [' '.join(grams) for grams in ngrams(words,2)]


                # results in unigram and bigram
                ans = [w for w in unigrams if re.search(q1, w)]\
                        + [w for w in bigrams if re.search(q2, w)]


                cur_words = unigrams + bigrams #+ trigrams
                all_words += cur_words
                if len(ans) > 0:
                    #pos_words += [x for x in cur_words if x not in set(key_uni + key_bi)]
                    pos_words += cur_words 
    
    c_pos = Counter(pos_words)
    c_all = Counter(all_words)

    pos_total = sum(c_pos.values())
    all_total = sum(c_all.values())

    freq_pos = {k: v*1.0/pos_total for k,v in c_pos.items()}
    freq_all = {k: v*1.0/all_total for k,v in c_all.items()}

    # get candidate words
    cand = {}
    for k in freq_pos:
        kl = freq_pos[k] * np.log(freq_pos[k]*1.0/freq_all[k])           
        #kl_list.append(kl)
        if kl > cutoff:
            cand[k] = kl


    df = pd.DataFrame.from_dict({'word': list(cand.keys()), 'kl': list(cand.values())})

    df.sort_values('kl',ascending=False, inplace=True)


    df.to_csv('../data/keywords_cutoff%s_trial%d.csv' % (cutoff,trial), header=True, index=False, sep='\t')


