# CSE495 group D
# Visualize sidewalks, crossings and elevator_paths using networkX

import csv
import networkx as nx
import matplotlib.pyplot as plt

def generate_crs_or_sdwk_network(csv_file, G):
    '''
    Given crossings or sidewalk csv files, generates the network 
    based on coordinates
    '''
    file = open(csv_file)
#    G = nx.Graph()
    pos = {}
    for row in csv.DictReader(file):
        # start node
        v = (str(row["ID"]) + "v")
        coordinates = row["v_coordinates"][1: -1].split(',')
        xv = float(coordinates[0])
        yv = float(coordinates[1])
        G.add_node(v, pos = (xv, yv))
        pos[v] = (xv, yv)
        # end node
        u = (str(row["ID"]) + "u")
        coordinates = row["u_coordinates"][1: -1].split(',')
        xu = float(coordinates[0])
        yu = float(coordinates[1])
        G.add_node(u, pos = (xu, yu))
        pos[u] = (xu, yu)
        # edge
        G.add_edge(v, u)
    
    file.close()
    return G, pos

def generate_elevator_network(csv_file, G):
    '''
    Given the elevator_paths csv file, generates the network 
    based on coordinates
    '''
    file = open("elevator_paths.csv")
#    G = nx.Graph()
    pos = {}
    id = 0
    for row in csv.DictReader(file):
        id += 1
        node_names = []
        coordinates = row["geometry"][12: -1].split(',')
        for i in range(len(coordinates)):
            coordinate = coordinates[i].split(' ')
            if len(coordinate) == 2:
                x = float(coordinate[0])
                y = float(coordinate[1])
            else:
                x = float(coordinate[1])
                y = float(coordinate[2])
            node_name = str(id) + str(i)
            G.add_node(node_name, pos = (x, y))
            pos[node_name] = (x, y)
            node_names.append(node_name)
        for j in range(len(node_names) - 1):
            G.add_edge(node_names[j], node_names[j + 1])

    file.close()
    return G, pos

    
G_crs = nx.Graph()
G_crs, pos_crs = generate_crs_or_sdwk_network("crossings.csv",G_crs)
#plt.figure()
#nx.draw_networkx(G_crs, pos_crs, node_size = 1)
#plt.show()
G_sdw = nx.Graph()
G_sdw, pos_sdw = generate_crs_or_sdwk_network("sidewalks.csv", G_sdw)
#plt.figure()
#nx.draw_networkx(G_sdw, pos_sdw, node_size = 1)
#plt.show()
G_elv = nx.Graph()
G_elv, pos_elv = generate_elevator_network("elevator_paths.csv", G_elv)
#plt.figure()
#nx.draw_networkx(G_elv, pos_elv, node_size = 1)
#plt.show()
