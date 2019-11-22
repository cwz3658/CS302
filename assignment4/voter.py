import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def initialize():
    global G
    G=nx.read_edgelist("airport.txt")

def observe(ini):
    global G,ones    
    for i in G:
        G.nodes[i]['state']= 1 if np.random.random() < ini else 0
    ones=0
    for i in G:
        ones=ones+G.node[i]['state']

def update():
    global G, ones
    listener= np.random.choice(G.nodes())
    speaker=np.random.choice(list(G.neighbors(listener)))
    if not G.node[listener]['state']==G.node[speaker]['state']:
        if G.node[speaker]['state']==1:
            ones=ones+1
        else:
            ones=ones-1
    G.node[listener]['state']=G.node[speaker]['state']

    
initialize()
observe(0.5)
ones_list=[]
while not (ones==500 or ones==0):
    ones_list.append(ones)
    update()
plt.figure()
plt.plot(ones_list)
plt.title('Network Voter-model')
plt.xlabel ('Step')
plt.ylabel ('number of red nodes')

#repeat 100 times 50/50
result=[]
k_list=[]
for i in range(100):
    observe(0.5)
    k=0
    while not (ones==500 or ones==0):
        k=k+1
        update()
    if ones==500:
        result.append(1)
    else:
        result.append(0)
    k_list.append(k)

#repeat 100 times 20/80
result2=[]
for i in range(100):
    observe(0.2)
    while not (ones==500 or ones==0):
        update()
    if ones==500:
        result2.append(1)
    else:
        result2.append(0)
plt.figure()
plt.hist([result,result2], bins=2,label=['50/50','20/80'])
plt.legend()
plt.title('majority nodes color at consensus with different initials')
plt.xlabel('blue red')

# generate configuration model
initialize()
degree_sequence = [d for n, d in G.degree()]
G=nx.configuration_model(degree_sequence)
k_list3=[]
for i in range(100):
    observe(0.5)
    k=0
    while not (ones==500 or ones==0):
        k=k+1
        update()
    k_list3.append(k)
plt.figure()
plt.hist(k_list)
plt.title('real network')
plt.xlabel ('number of steps reachs consensus')
plt.figure()
plt.hist(k_list3)
plt.title('configuration model network')
plt.xlabel ('number of steps reachs consensus')

