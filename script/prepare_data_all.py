import pandas as pd
import numpy as np
from nltk import ngrams
import pickle
from collections import Counter
import datetime
from nltk.corpus import stopwords
import sklearn.feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


stemmer = nltk.stem.PorterStemmer()
lemmatizer = nltk.stem.WordNetLemmatizer()

def lemmatize(sentence):
    word_list = nltk.word_tokenize(sentence)

    lemmatized_output = ' '.join([lemmatizer.lemmatize(w,pos=get_wordnet_pos(w)) for w in word_list])

    return lemmatized_output


def stemming(text):
    tokens = text.split(' ')
    return ' '.join([stemmer.stem(x) for x in tokens])


# further tidy: remove punctuation, numbers
def further_tidy(x, min_size):
    tkz = nltk.RegexpTokenizer(r"[a-z]+")
    tokens = tkz.tokenize(x)
    return ' '.join([word for word in tokens if not word.isnumeric() and len(word) >= min_size])


def get_timestamp(date, timeFormat='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(date, timeFormat)

def get_time(cur_time, start_time, time_step=1.0):
    return (get_timestamp(cur_time) - get_timestamp(start_time)).total_seconds()/time_step


def display_scores(vectorizer, tfidf_result):
    scores = zip(vectorizer.get_feature_names(),
                 np.asarray(tfidf_result.sum(axis=0)).ravel())
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    word_count = []
    for item in sorted_scores:
        print("{0:50} Score: {1}".format(item[0], item[1]))
        word_count.append([item[0],item[1]])

    wc = pd.DataFrame(word_count,columns=['word','count'])
    return wc


if __name__=='__main__':

    cutoff = 0.01
    df = pd.read_csv('../data/tweets_cutoff%s_sorted.csv' % (cutoff), sep='\t')

    print(df.shape)

    start_time = df['created_at'].values[0]

    time_step = 24*3600.0

    df['text'] = df['text'].apply(lambda x: further_tidy(x,2))
    df['text'] = df['text'].apply(lemmatize)
    #df['text'] = df['text'].apply(stemming)

    tweets = df['text'].values


    enStop = stopwords.words('english')

    # Skip stop words, retweet signs, @ symbols, and URL headers
    stopList = enStop +\
    ['covid','covid-19','covid19','covid_19','covid-2019','covid2019','covid_2019','coronavirus','et','ct','mt','pt','am','pm','rt','http','https']


    vectorizer = CountVectorizer(strip_accents='unicode', tokenizer=None,
                                 token_pattern='(?u)#?\\b\\w+[\'-]?\\w+\\b',
                                 #max_df = 800,
                                 min_df = 30,
                                 stop_words=stopList, binary=True)


    # Create a vectorizer for all our content
    corpus = vectorizer.fit_transform(tweets)

    bow=corpus.toarray()
    X=pd.DataFrame(bow)
    X.columns=vectorizer.get_feature_names()

    wc = display_scores(vectorizer, corpus)

    wc.to_csv('./word_count_all.csv', index=False)

    print(X.shape)


    X.to_csv('../data/all/allwordmatrix_cutoff%s.csv' % (cutoff), index = False)


    # get user id
    users = np.unique(df['handle'].values)

    user_id = {u: i+1 for i, u in enumerate(users)}

    df['time'] = df['created_at'].apply(lambda x: get_time(x,start_time,time_step))
    df['marks'] = df['handle'].apply(lambda x: user_id[x])

    # save
    pickle.dump(user_id, open('../data/all/user_mark_cutoff%s.pickle' % (cutoff), 'wb'))

    df_user_id = pd.DataFrame.from_dict({'user': list(user_id.keys()), 'mark': list(user_id.values())})
    df_user_id.sort_values('mark', inplace=True)
    df_user_id.to_csv('../data/all/user_mark_cutoff%s.csv' % (cutoff), sep='\t', index=False)

    df1 = df[['time','marks']]

    df1.to_csv('../data/all/time_marks_cutoff%s.csv' % (cutoff),index=False)

    df_date = df[['created_at']]
    df_text = df[['text']]

    df_date.to_csv('../data/all/date_cutoff%s.csv' % (cutoff), index=False)
    df_text.to_csv('../data/all/text_cutoff%s.csv' % (cutoff), index=False)

