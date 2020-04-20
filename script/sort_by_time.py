import pandas as pd

df = pd.read_csv('../data/tweets_cutoff0.01.csv',sep='\t')


df.sort_values(by='created_at',inplace=True)

print(df.head())


df.to_csv('../data/tweets_cutoff0.01_sorted.csv', sep='\t', header=True, index=False)

