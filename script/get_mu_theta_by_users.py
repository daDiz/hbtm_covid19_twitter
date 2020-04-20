import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_mu = pd.read_csv('../hbtm_var_mu/mu_topic_cutoff0.01_all.csv', header=None)
df_theta = pd.read_csv('../hbtm_var_mu/theta_topic_cutoff0.01_all.csv',header=None)
df_theta_eff = pd.read_csv('../hbtm_var_mu/adj_matrix_topic_cutoff0.01_all.csv',header=None)

df = pd.read_csv('../data/user_mark_cutoff0.01.csv',sep='\t')


print(df_mu.shape)
print(df_theta.shape)
print(df_theta_eff.shape)

mu = df_mu.values.T
theta = df_theta.values
theta_eff = df_theta_eff.values

np.fill_diagonal(theta, 0)
np.fill_diagonal(theta_eff, 0)

mu_mean = np.mean(mu,axis=1)


df['mu'] = mu_mean
df['theta'] = np.sum(theta, axis=1)
df['theta_eff'] = np.sum(theta_eff, axis=1)
print(df.head())

df['mu'] = df['mu'].values / df['mu'].sum()
df['theta'] = df['theta'].values / df['theta'].sum()
df['theta_eff'] = df['theta_eff'].values / df['theta_eff'].sum()

df.to_csv('user_influence_scores.csv', index=False)


