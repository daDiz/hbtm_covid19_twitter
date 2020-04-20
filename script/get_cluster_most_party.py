import pandas as pd
import pickle

flag = 'testing'

if flag == 'risk':
    topics = [3,1,7,2,10,11,12,4,9,18,20,21,19,24,26,27]
elif flag == 'all':
    topics = [3, 19, 24, 23, 51, 61, 71, 75, 88, 83, 109, 115, 102, 123, 135, 142, 151, 84, 159, 158, 166, 168, 180, 184, 183, 191, 201, 199, 209, 229, 228, 234, 227, 238, 245, 254, 256, 213, 255, 273, 265, 279, 280, 252, 291, 296, 299, 295, 297, 302]
elif flag == 'vaccine':
    topics = [5, 4, 11, 12, 13, 10, 6, 17, 20, 18, 25]
elif flag == 'testing':
    topics = [8, 11, 14, 13, 12, 25, 4, 18, 17, 24, 9, 29, 28, 33, 32, 26, 36, 39, 38]
else:
    raise Exception('unknown data')


df_cabinet = pd.read_csv('../name_handle_party/trump_cabinet.csv',header=None)

df_cabinet.dropna(inplace=True)

cabinet_handle = df_cabinet[2].values

cabinet_handle = [x[1:] for x in cabinet_handle if x[1:] != 'realDonaldTrump']

trump_handle = 'realDonaldTrump'

df_gov = pd.read_csv('../name_handle_party/governors_2020.csv',header=None)

df_gov.dropna(inplace=True)

gov_party = df_gov[2].values
gov_handle = df_gov[3].values

gov_handle = [x[1:] for x in gov_handle]

gov_handle_party = dict(zip(gov_handle,gov_party))

df = pd.read_csv('../hbtm_var_mu/topic_cluster_cutoff0.01_%s.csv' % (flag),header=None)

user_id = pickle.load(open('../data/%s/user_mark_cutoff0.01.pickle' % (flag),'rb'))


id_user = {v: k for k, v in user_id.items()}



data = df.values

topic_party = {}
for x in data:
    if x[0] not in topic_party:
        topic_party[x[0]] = []

    uid = x[2]
    handle = id_user[uid]
    if handle in cabinet_handle:
        topic_party[x[0]].append('cabinet-R')
    elif handle in gov_handle_party:
        topic_party[x[0]].append('governor-' + gov_handle_party[handle])
    elif handle == trump_handle:
        topic_party[x[0]].append('president-R')
    else:
        raise Exception('unknown handle')


from collections import Counter
for topic in topics:
    c = Counter(topic_party[topic])
    mc = c.most_common()
    print('topic %s : %s' % (topic, mc))


