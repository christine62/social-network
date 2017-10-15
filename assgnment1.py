#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 10:28:21 2017

@author: jiahuibi
"""

import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms import bipartite
import re


employees = set(['Pablo',
                 'Lee',
                 'Georgia',
                 'Vincent',
                 'Andy',
                 'Frida',
                 'Joan',
                 'Claude'])

# This is the set of movies
movies = set(['The Shawshank Redemption',
              'Forrest Gump',
              'The Matrix',
              'Anaconda',
              'The Social Network',
              'The Godfather',
              'Monty Python and the Holy Grail',
              'Snakes on a Plane',
              'Kung Fu Panda',
              'The Dark Knight',
              'Mean Girls'])

def plot_graph(G, weight_name=None):
    '''
    G: a networkx G
    weight_name: name of the attribute for plotting edge weights (if G is weighted)
    '''
    
    import matplotlib.pyplot as plt
    
    plt.figure()
    pos = nx.spring_layout(G)
    edges = G.edges()
    weights = None
    
    if weight_name:
        weights = [int(G[u][v][weight_name]) for u,v in edges]
        labels = nx.get_edge_attributes(G,weight_name)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        nx.draw_networkx(G, pos, edges=edges, width=weights);
    else:
        nx.draw_networkx(G, pos, edges=edges);

employee_movie=pd.read_table("Employee_Movie_Choices.txt")
G = nx.Graph()

G = nx.from_pandas_dataframe(employee_movie, '#Employee', 'Movie')
nx.draw_networkx(G)
#nx.number_of_nodes(G)
#plot_graph(G)
#nx.set_node_attributes(G, 'betweenness', bb)
for i in employees:
    G.node[i]['type']='employee'
for x in movies:
    G.node[x]['type']='movie'
#NSet = bipartite.sets(G)
#Act = nx.project(G,NSet[0])    
G1= bipartite.weighted_projected_graph(G, employees)

df1 = pd.DataFrame(G1.edges(data=True), columns=['employees1', 'employee2', 'weight'])
df1['weight'] = df1['weight'].map(lambda x: x['weight'])

employee_rela=pd.read_csv('Employee_Relationships.txt', delim_whitespace=True, 
                   header=None, names=['employee1', 'employee2', 'score'])
G2= nx.from_pandas_dataframe(employee_rela, 'employee1', 'employee2', edge_attr='score')

G3=nx.compose(G1,G2)
for i in employees:
    for u in employees:
        if i<u:
            if 'weight' not in G3.edge[i][u]:
                G3[i][u]['weight']=0
df2 = pd.DataFrame(G3.edges(data=True), columns=['employee1', 'employee2', 'score'])

df2['weight'] = df2['score'].map(lambda x: x['weight'])
df2['score'] = df2['score'].map(lambda x: x['score'])
df2['score'].corr(df2['weight'])
