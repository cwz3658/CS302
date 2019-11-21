# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:56:40 2019

@author: cwz36
"""



#def initialize():
#    global g
#    g=nx.karate_club_graph()
#    g.pos=nx.spring_layout(g)
#    for i in g.nodes_iter():
#        g.nodes[i]['state']= 1 if random() < 0.5 else 0
#        
#def observe():
#    global g
#    cla
#    nx.draw(g, cmap= cm.binary, vmin =0, vmax=1,
#            node_color =[g.node[i]['state'] for i in g.nodes_iter() ], 
#            pos=g.pos)
#    
#def update():
#    global g
#    listener= rd.choice(g.nodes())
#    speaker=rd.choice(g.neighbors(listener))
#    g.node[listener]['state']=g.node[speaker]['state']
#    



import matplotlib.pyplot as plt
import networkx as nx

G=nx.read_edgelist("airport.txt")


options = {
    'node_color': 'black',
    'node_size': 50,
    'line_color': 'grey',
    'linewidths': 0,
    'width': 0.1,
}
nx.draw(G, **options)
plt.show()




