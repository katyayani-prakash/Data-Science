import os,sys
import argparse
import json
import networkx as nx
import pathlib

def top_three_chars(tp):
    #This function takes as input a tuple list and returns a list of top 3 characters
    top_three_list = []
    for item in tp:
            top_three_list.append(item[0])

    top_three_list = top_three_list[0:3]
    return top_three_list

def main():
    #parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input')
    parser.add_argument('-o','--output')
    args = parser.parse_args()
    
    with open(args.input,'r') as f:
        infile = json.load(f)

    G = nx.Graph(infile)

    for edge in G.edges():
        for key in infile.keys():
            for in_key in infile[key].keys():
                G[key][in_key]['weight'] = infile[key][in_key]
                

    # Best connected character by edges, i.e., highest degree of nodes
    node_degrees = {}
    for v in G.nodes():
        node_degrees[v] = G.degree(v)
    
    # print(node_degrees)

    deg_list = list(node_degrees.items())
    deg_list.sort(key=lambda x: -x[1])

    # print(deg_list)
    
    

    # Best connected character by weight
    node_weights = {}
    for v in G.nodes():
        values = infile[v].values()
        node_weights[v] = sum(values)
    
    # print(node_weights)

    weight_list = list(node_weights.items())
    weight_list.sort(key=lambda x: -x[1])

    # print(weight_list)


    # Best connected character by betweenness
    node_betweenness = {}
    node_betweenness = nx.betweenness_centrality(G)

    # print(node_betweenness)

    betweenness_list = list(node_betweenness.items())
    betweenness_list.sort(key=lambda x: -x[1])

    # print(type(betweenness_list))

    top_three_connected = top_three_chars(deg_list)
    top_three_weight = top_three_chars(weight_list)
    top_three_betness = top_three_chars(betweenness_list)

    out = {}
    out = {
        'most_connected_by_num': top_three_connected,
        'most_connected_by_weight': top_three_weight,
        'most_central_by_betweenness': top_three_betness
    }

    #getting the current working directory
    tgt_path = pathlib.Path.cwd()

    #retrieving the path pointed in -o argument, and splitting the filename and directory name
    output_argument = tgt_path.joinpath(args.output)
    output_fname = output_argument.name
    output_dirname = output_argument.parent

    #creating a directory if it does not exist
    if not output_dirname.exists():
        output_dirname.mkdir()


    with open(args.output,'w+') as outfile:
        json.dump(out,outfile,indent=2)


if __name__ == '__main__':
    main()