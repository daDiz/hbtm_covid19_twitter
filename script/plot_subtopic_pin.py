import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.style.use('ggplot')
import seaborn as sns
import numpy as np
import datetime
from matplotlib import collections as matcoll

def get_timestamp(date, timeFormat='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(date, timeFormat)


df_all = pd.read_csv('../stats_kl/tweets_cutoff0.01_sorted.csv',sep='\t')

start_time = get_timestamp(df_all['created_at'].values[0])


df_risk = pd.read_csv('../../hbtm_var_mu/all_cluster_cutoff0.01_risk.csv', header=None)
df_vacc = pd.read_csv('../../hbtm_var_mu/all_cluster_cutoff0.01_vaccine.csv', header=None)
df_test = pd.read_csv('../../hbtm_var_mu/all_cluster_cutoff0.01_testing.csv', header=None)


###### risk ################
df1_risk = df_risk[[0,1,12,13]]
df1_risk.columns = ['topic','time','count','mark']

df1_risk['tdiff_sec'] = df1_risk['time'].apply(lambda x: x*24*3600)
df1_risk['date'] = df1_risk['tdiff_sec'].apply(lambda x: start_time + datetime.timedelta(seconds=x))

df1_risk.sort_values(by='date',inplace=True)

thres = 1

data1 = df1_risk.values
data2 = []
r,c = df1_risk.shape

good_topic = []
for i in range(r):
    #if data1[i,0] in topic_selected and data1[i,2] > thres:
    if data1[i,2] > thres:
        data2.append(data1[i])
        good_topic.append(data1[i,0])

df1_risk = pd.DataFrame(data2, columns=df1_risk.columns)

###### vacc ################
df1_vacc = df_vacc[[0,1,12,13]]
df1_vacc.columns = ['topic','time','count','mark']

df1_vacc['tdiff_sec'] = df1_vacc['time'].apply(lambda x: x*24*3600)
df1_vacc['date'] = df1_vacc['tdiff_sec'].apply(lambda x: start_time + datetime.timedelta(seconds=x))

df1_vacc.sort_values(by='date',inplace=True)

thres = 1

data1 = df1_vacc.values
data2 = []
r,c = df1_vacc.shape

good_topic = []
for i in range(r):
    #if data1[i,0] in topic_selected and data1[i,2] > thres:
    if data1[i,2] > thres:
        data2.append(data1[i])
        good_topic.append(data1[i,0])

df1_vacc = pd.DataFrame(data2, columns=df1_vacc.columns)

###### test ################
df1_test = df_test[[0,1,12,13]]
df1_test.columns = ['topic','time','count','mark']

df1_test['tdiff_sec'] = df1_test['time'].apply(lambda x: x*24*3600)
df1_test['date'] = df1_test['tdiff_sec'].apply(lambda x: start_time + datetime.timedelta(seconds=x))

df1_test.sort_values(by='date',inplace=True)

thres = 1

data1 = df1_test.values
data2 = []
r,c = df1_test.shape

good_topic = []
for i in range(r):
    #if data1[i,0] in topic_selected and data1[i,2] > thres:
    if data1[i,2] > thres:
        data2.append(data1[i])
        good_topic.append(data1[i,0])

df1_test = pd.DataFrame(data2, columns=df1_test.columns)



###### plot ###################

fig, (ax1,ax2,ax3) = plt.subplots(3,1,sharex=True)
#ax = fig.add_subplot(111)

left = 0.125  # the left side of the subplots of the figure
right = 0.9   # the right side of the subplots of the figure
bottom = 0.1  # the bottom of the subplots of the figure
top = 0.9     # the top of the subplots of the figure
wspace = 0.2  # the amount of width reserved for space between subplots,
              # expressed as a fraction of the average axis width
hspace = 0.0  # the amount of height reserved for space between subplots,
              # expressed as a fraction of the average axis height


plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=hspace)
### risk ###
r,c = df1_risk.shape
ax1.scatter(df1_risk['date'].values, df1_risk['count'].values, s=20, c='black')
for i in range(r):
    x = df1_risk['date'].values[i]
    y = df1_risk['count'].values[i]
    ax1.plot([x,x],[1,y],color='black',alpha=0.5)

#ax.set_ylim(10,max(df1['count'].values)*2)
ax1.set_yscale('log')

### vacc ###
r,c = df1_vacc.shape
ax2.scatter(df1_vacc['date'].values, df1_vacc['count'].values, s=20, c='black')
for i in range(r):
    x = df1_vacc['date'].values[i]
    y = df1_vacc['count'].values[i]
    ax2.plot([x,x],[1,y],color='black',alpha=0.5)

#ax.set_ylim(10,max(df1['count'].values)*2)
ax2.set_yscale('log')

### risk ###
r,c = df1_test.shape
ax3.scatter(df1_test['date'].values, df1_test['count'].values, s=20, c='black')
for i in range(r):
    x = df1_test['date'].values[i]
    y = df1_test['count'].values[i]
    ax3.plot([x,x],[1,y],color='black',alpha=0.5)

#ax.set_ylim(10,max(df1['count'].values)*2)
ax3.set_yscale('log')

#ax.set_aspect(5)

ax1.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=True,
    labelleft=True) # labels along the bottom edge are off



ax2.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=True,
    labelleft=True) # labels along the bottom edge are off


ax3.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=True,
    labelleft=True) # labels along the bottom edge are off

plt.show()










