#! /usr/bin/python3
import json
import sys
import networkx as nx
import numpy as np
import pennylane as qml
from pennylane import qaoa


# DO NOT MODIFY any of these parameters
NODES = 6
N_LAYERS = 10


def find_max_independent_set(graph, params):
    """Find the maximum independent set of an input graph given some optimized QAOA parameters.
    The code you write for this challenge should be completely contained within this function
    between the # QHACK # comment markers. You should create a device, set up the QAOA ansatz circuit
    and measure the probabilities of that circuit using the given optimized parameters. Your next
    step will be to analyze the probabilities and determine the maximum independent set of the
    graph. Return the maximum independent set as an ordered list of nodes.
    Args:
        graph (nx.Graph): A NetworkX graph
        params (np.ndarray): Optimized QAOA parameters of shape (2, 10)
    Returns:
        list[int]: the maximum independent set, specified as a list of nodes in ascending order
    """

    max_ind_set = []

    # QHACK #

    # function that takes in a graph and outputs the hamiltonians
    cost_h, mixer_h = qaoa.max_independent_set(graph, constrained=True) # Assume the graph they give me is good

    def qaoa_layer(gamma, alpha):
        qaoa.cost_layer(gamma, cost_h)
        qaoa.mixer_layer(alpha, mixer_h)

    dev = qml.device("default.qubit", wires=range(NODES))

    def circuit(params, **kwargs): 
        qml.layer(qaoa_layer, N_LAYERS, params[0], params[1]) 

    @qml.qnode(dev)
    def probability_circuit(gamma, alpha):
        circuit([gamma, alpha])
        return qml.probs(wires=range(NODES))

    answer = probability_circuit(params[0], params[1])

    maxn = 0
    maxn = max(answer)

    for i in range(len(answer)):
        if maxn == answer[i]:
            decimal = i
    
    binary_num = []
    def DecimalToBinary(decimal):
        if decimal >= 1:
            DecimalToBinary(decimal // 2)
            binary_num.append(decimal % 2)
       
    DecimalToBinary(decimal)

    if len(binary_num) < 6:
        if len(binary_num) < 5:
            if len(binary_num) < 4:
                if len(binary_num) < 3:
                    if len(binary_num) < 2:
                        binary_num.insert(0, 0) # At beginning append 0
                    binary_num.insert(0, 0)
                binary_num.insert(0, 0)
            binary_num.insert(0, 0)
        binary_num.insert(0, 0)

    for i in range(6):
        if binary_num[i] == 1:
            max_ind_set.append(i)

    # QHACK #

    return max_ind_set


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block

    # Load and process input
    graph_string = sys.stdin.read()
    graph_data = json.loads(graph_string)

    params = np.array(graph_data.pop("params"))
    graph = nx.json_graph.adjacency_graph(graph_data)

    max_independent_set = find_max_independent_set(graph, params)

    print(max_independent_set)