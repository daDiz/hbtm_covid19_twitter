import pandas as pd
import matplotlib.pyplot as plt


hbtm = 0.5181071551243962

df = pd.read_csv('./lda_coh.csv')

ntop = df['ntop'].values
lda = df['coh'].values


fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(ntop,lda,color='black',linewidth=3,label='LDA')
ax.plot(ntop,[hbtm]*len(ntop),color='red',linewidth=3,label='HBTM')
#plt.xlabel('LDA number of Topics',fontweight='bold')
#plt.ylabel('UCI Coherence',fontweight='bold')

ax.set_aspect(2)


plt.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False,
    labelleft=False) # labels along the bottom edge are off


plt.grid()
#plt.legend()
plt.show()
#plt.savefig('uci_lda_hbtm.png')
