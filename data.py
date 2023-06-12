'''
    Este script python manipula e analisa os dados de um dataset de resutados de partidas de futebol 
    da copa do mundo. Nesta modelagem cada seleção representa um nó, e uma aresta é ligada entre os nós
    indicando a quantidade de gols (weight) foi marcado por uma seleção em outra (directed edge) em
    todas as partidas de Copa do mundo. Para efeito de análise, é contabilizado como pontuação (weight) 
    apenas os gols marcados como mandante de campo.

    Obs: este Dataset foi retirado do site Kaggle: https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017

'''


import numpy as np
import pandas as pd 
from pyvis.network import Network
import networkx as nx


'''
    Manipulação do dataset para adequação com os requisitos da rede esperada
'''
#results = pd.read_csv('/kaggle/input/international-football-results-from-1872-to-2017/results.csv', parse_dates=['date'])

#recupera os dados das partidas do arquivo csv e recorta somente as partidas da copa
results = pd.read_csv('results.csv', parse_dates=['date'])
results_fifa = results[results['tournament']== 'FIFA World Cup']

#concatena as partidas entre duas equipes (diferenciando por mandante), soma o saldo de gols das partidas e renomeia as colunas
aggregated_data = results_fifa.groupby(['home_team', 'away_team']).agg({'home_score': 'sum', 'away_score': 'sum'}).reset_index()
aggregated_data = aggregated_data.rename(columns={'home_score': 'total_home_score', 'away_score': 'total_away_score'})

# Remover as linhas repetidas se houver
aggregated_data = aggregated_data.drop_duplicates(subset=['home_team', 'away_team'])

# recupera as seleções e gols do mandante do dataset
home_team = list(aggregated_data['home_team'])
away_team = list(aggregated_data['away_team'])
total_home_score = list(aggregated_data['total_home_score'])
all_team = set(home_team).union(set(away_team))
edge_data = zip(home_team, away_team, total_home_score)

#cria um grafo com NetworkX do dataset
network_nx = nx.DiGraph()
for team in all_team:
    network_nx.add_node(team)
for edge in edge_data:
    network_nx.add_edge(edge[0], edge[1], weight=edge[2])

########################################################


'''
    Análises da rede com o networkX

'''

#calculo de Matriz de Adjascência
MatrizDeAdjascencia = nx.adjacency_matrix(network_nx)
print("**Matriz de adjascencia***")
print(MatrizDeAdjascencia.todense())
print()

print("O grafo é fortemente conectado: " + str(nx.is_strongly_connected(network_nx)))


try:
    # Calcule o diâmetro do grafo
    diametro = nx.diameter(network_nx)

    # Calcule a períferia do grafo
    periferia = nx.periphery(network_nx)
except:
    print("Devido ao fato do grafo não ser fortemente conectado não é possível calcular diametro e periferia com networkX")
print()


# Calcule o coeficiente de clustering global
print("Coeficiente de clustering global: " + str(nx.average_clustering(network_nx)))
print()

componente_fracamente_conectados = nx.weakly_connected_components(network_nx)

print("Quantidade de componentes conectados (fracos): " + str(len(list(componente_fracamente_conectados))))
print()
print("Coeficiente de clustering para Brasil: " + str(nx.clustering(network_nx, "Brazil")))
print("Coeficiente de clustering para Argentina: " + str(nx.clustering(network_nx, "Argentina")))
print()

#Eigenvector centrality 
print("**Centralidade de Eigenvector***")
eigenvector_centrality = nx.eigenvector_centrality(network_nx)
for node, centrality in eigenvector_centrality.items():
    print("Centralidade de Eigenvector para o nó", node, ":", centrality)
print()

# Calcule a centralidade de grau para cada nó do grafo
print("**Centralidade de Grau***")
degree_centrality = nx.degree_centrality(network_nx)
for node, centrality in degree_centrality.items():
    print("Centralidade de Grau para o nó", node, ":", centrality)
print()

# Calcule a centralidade de proximidade para cada nó do grafo
print("**Centralidade de Proximidade***")
closeness_centrality = nx.closeness_centrality(network_nx)
for node, centrality in closeness_centrality.items():
    print("Centralidade de Proximidade para o nó", node, ":", centrality)
print()

# Calcule a centralidade de intermediação para cada nó do grafo
print("**Centralidade de Intermediação**")
betweenness_centrality = nx.betweenness_centrality(network_nx)
for node, centrality in betweenness_centrality.items():
    print("Centralidade de Intermediação para o nó", node, ":", centrality)
print()

# Calcule a assortatividade geral da rede
assortativity = nx.degree_assortativity_coefficient(network_nx)
print("Assortatividade Geral da Rede:", assortativity)

###########################################################################################

'''


    Plotagem do rede visual


'''
#Transforma um grafo NetworkX em um grafo visualizável com o pyvis
network_pyvis = Network(height="750px", width="100%", bgcolor="#222222", font_color="white",notebook=False, directed =True, select_menu=True, heading="Gols como mandante de campo em todas as copas do mundo")
network_pyvis.from_nx(network_nx)
network_pyvis.show_buttons(filter_=['physics'])
network_pyvis.barnes_hut()
network_pyvis.show("teams.html",  notebook=False)
