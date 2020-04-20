import gensim
import numpy
import gensim
import pandas as pd
import numpy as np
from nltk.corpus import stopwords


stopList = stopwords.words('english')


df = pd.read_csv('../hbtm_var_mu/topic_cluster_cutoff0.01_all.csv',header=None)


topics = np.unique(df[0].values)

texts = []
words = []
topic_word_dict = []
topic_count = {}

for t in topics:
    topic_word_dict.append({})

data = df.values

for row in data:
    text_split = row[3].split()
    min_index = int(row[0])-1
    ww = []
    if min_index in topic_count:
        topic_count[min_index] +=1
    else:
        topic_count[min_index]=1

    for w in text_split:
        if w not in stopList:
            if w in topic_word_dict[min_index]:
                topic_word_dict[min_index][w]+=1
            else:
                topic_word_dict[min_index][w]=1

            ww.append(w)

    texts.append(' '.join(ww))
    words.append(ww)

topic_words = []
Nstop = 10
for i in range(len(topics)):
    d = topic_word_dict[i]
    counts = 0
    tw = []
    print(('Topic:', i))
    for w in sorted(d, key=d.get, reverse=True):
        counts+=1
        tw.append(w)
        print(w)
        if counts == Nstop:
            break
    topic_words.append(tw)




text_dict = gensim.corpora.Dictionary(words)

cm = gensim.models.CoherenceModel(topics=topic_words, texts=words, dictionary=text_dict, coherence='c_uci')
print('coherence uci: %s' % (cm.get_coherence()))
