import numpy as np
import pandas as pd
import pickle
import networkx as nx
import matplotlib.pyplot as plt

np.random.seed(42)

def custom_grid_layout(g,shift=2,step=5):
    pos = {}

    for i,node in enumerate(g.nodes.keys()):
        if handle_party[node] == 'R':
            x,y = i // step + 1, i % step + 1
            b = np.random.normal(0,1)*0.2
            loc = [100*(x+shift),y+b]
            pos[node] = loc
        else:
            x,y = i // step + 1, i % step + 1
            b = np.random.normal(0,1)*0.2
            loc = [100*(-x-shift),y+b]
            pos[node] = loc

    return pos

def custom_grid_layout_test(g,shift=2,step=5,add_noise=True):
    pos = {}
    i, j = 0, 0
    for node in g.nodes.keys():
        if handle_party[node] == 'R':
            x,y = i // step + 1, i % step + 1
            b = np.random.normal(0,1)*0.2
            #loc = [x+shift,y+b]
            if add_noise:
                loc = [x,y+b]
            else:
                loc = [x,y]
            pos[node] = loc
            #print((node,loc))
            i += 1
        else:
            x,y = j // step + 1, j % step + 1
            b = np.random.normal(0,1)*0.2
            #loc = [-x-shift,y+b]
            if add_noise:
                loc = [-x,y+b]
            else:
                loc = [-x,y]
            pos[node] = loc
            #print((node,loc))
            j += 1

    return pos


def custom_layout(g,shift=2,step=1.0,upper=100):
    pos = {}
    right = set()
    left = set()
    for node in g.nodes.keys():
        if handle_party[node] == 'R':
            flag = True
            while flag:
                x,y = np.random.randint(upper,size=2)
                if (x,y) not in right:
                    flag = False
                    right.add((x,y))
                    a,b = np.random.normal(0,1,2)*step
                    loc = [x*step+shift+a,y*step+b]
                    pos[node] = loc
        else:
            flag = True
            while flag:
                x,y = np.random.randint(upper,size=2)
                if (x,y) not in left:
                    flag = False
                    left.add((x,y))
                    a,b = np.random.normal(0,1,2)*step
                    loc = [-x*step-shift+a,y*step+b]
                    pos[node] = loc
    return pos

df_cabinet = pd.read_csv('../name_handle_party/trump_cabinet.csv')
df_governor = pd.read_csv('../name_handle_party/governors_2020.csv')

df_cabinet.dropna(inplace=True)
df_governor.dropna(inplace=True)

df_cabinet['handle']=df_cabinet['handle'].apply(lambda x: x[1:])
df_governor['handle']=df_governor['handle'].apply(lambda x: x[1:])




handle_party =\
dict(zip(list(df_cabinet['handle'].values)+list(df_governor['handle'].values),list(df_cabinet['party'].values)+list(df_governor['party'].values)))

#print(handle_party)

flag = 'testing'

df = pd.read_csv('../hbtm_var_mu/adj_matrix_topic_cutoff0.01_%s.csv' % (flag), header=None)

theta_eff = df.values

user_id = pickle.load(open('../data/%s/user_mark_cutoff0.01.pickle' % (flag),'rb'))

id_user = {v: k for k, v in user_id.items()}

print(np.mean(theta_eff))
print(np.quantile(theta_eff,0.25))
print(np.quantile(theta_eff,0.75))
print(np.max(theta_eff))
print(np.min(theta_eff))

if flag == 'vaccine':
    thres = 0.8
elif flag == 'risk':
    thres = 1
elif flag == 'testing':
    thres = 2

g =nx.DiGraph()

republicans = []
democrats = []

r,c = theta_eff.shape
for i in range(r):
    party=handle_party[id_user[i+1]]
    if party == 'R':
        republicans.append(id_user[i+1])
    elif party == 'D':
        democrats.append(id_user[i+1])
    else:
        raise Exception('no third party')

    g.add_node(id_user[i+1])


    for j in range(c):
        if theta_eff[i,j] > thres:
            g.add_node(id_user[j+1])
            g.add_edge(id_user[i+1],id_user[j+1], weight=theta_eff[i,j])


print('num democrats: %d' % (len(democrats)))
print('num republicans %d' % (len(republicans)))

#pos = custom_grid_layout_test(g, shift=0.5, step=10) # risk
#pos = custom_grid_layout_test(g, shift=0.5, step=5) # vaccine
pos = custom_grid_layout_test(g, shift=0.5, step=13, add_noise=False) # testing




nx.draw_networkx_nodes(g, pos, nodelist=republicans, node_color='r', node_size = 500, alpha=0.5)
nx.draw_networkx_nodes(g, pos, nodelist=democrats, node_color='b', node_size = 500, alpha=0.5)

# risk
#weights = [g[u][v]['weight']*2 for u,v in g.edges()]
# vaccine
#weights = [g[u][v]['weight']*2 for u,v in g.edges()]
# test
weights = [g[u][v]['weight'] for u,v in g.edges()]



nx.draw_networkx_labels(g, pos, font_size=12, font_weight='bold')
nx.drawing.nx_pylab.draw_networkx_edges(g, pos, width=weights, edge_color='black', alpha=0.5,
                       connectionstyle='arc3,rad=0.2',arrows=True)


plt.show()
