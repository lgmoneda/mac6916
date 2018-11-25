### Reference
### http://www.cs.cmu.edu/~epxing/Class/10708-13/reading/Ch%204.pdf
import itertools
from operator import itemgetter
from functools import reduce
import numpy as np
import sys

def read_uai_file(filename):
    """
    Reads uai file and extract a dictionary describing the network.
    """
    uai_info = {}

    with open(filename, "r") as file_:
        lines = file_.readlines()
        lines = [l.replace("\n", "") for l in lines]
        lines = [l.replace("\t", " ") for l in lines]

        ### Exclude empty lines
        lines = [l for l in lines if l != '']

        uai_info["network_type"] = lines[0]
        uai_info["n_variables"] = int(lines[1])

        ### Variables
        uai_info["variables"] = {}
        for i in range(uai_info["n_variables"]):
            uai_info["variables"][i + 1] = {}

            uai_info["cardinalities"] = [int(c) for c in lines[2].split(" ")]

        ### Cliques
        uai_info["n_cliques"] = int(lines[3])
        uai_info["cliques"] = {}
        for i in range(uai_info["n_cliques"]):
            uai_info["cliques"][i] = {}

            uai_info["cliques"][i]["vars"] = [int(c) for c in lines[3 + (i + 1)].split(" ")][1:]
            uai_info["cliques"][i]["potential"] = [c for c in lines[3 + uai_info["n_cliques"] + (2 * i + 2)].split(" ")]

    return uai_info

def retrieve_potential(evidence, variables, markov_network):
    """
    Retrieve the potential from a certain evidence considering a certain potential table containing variables.
    """

    potential = 0
    for c in range(markov_network["n_cliques"]):
        if variables == markov_network["cliques"][c]["vars"]:
            potential = markov_network["cliques"][c]["potential"]

    all_possibilities = []
    for i in range(len(variables)):
        all_possibilities.append([k for k in range(markov_network["cardinalities"][variables[i]])])

    all_possibilities = itertools.product(*all_possibilities)
    all_possibilities = [a for a in all_possibilities]

    pot = all_possibilities.index(evidence)
    pot = potential[pot]

    return float(pot)

def markov_partition(markov_network):
    """
    CAlculates markov partition given a markov network described by a uai file.
    """
    evidences = []
    for i in range(markov_network["n_variables"]):
        evidences.append([k for k in range(markov_network["cardinalities"][i])])

    evidences = itertools.product(*evidences)
    evidences = [e for e in evidences]

    result = 0
    for evidence in evidences:
        clique_potentials = []
        for c in range(markov_network["n_cliques"]):
            ### Check if the clique is maximal
            ### If not, don't consider it
            ### For now, it only excludes singletons
            # if len(markov_network["cliques"][c]["vars"]) == 1:
            #     continue

            ### Consider only variables present at the considered clique
            reduced_evidence = itemgetter(*markov_network["cliques"][c]["vars"])(evidence)

            ### When there's only one variable the itemgetter does not return a tuple
            if isinstance(reduced_evidence, int): reduced_evidence = (reduced_evidence, )

            ### Get the potential from all the cliques
            clique_potentials.append(retrieve_potential(reduced_evidence, markov_network["cliques"][c]["vars"], markov_network))

        #print(clique_potentials)
        result += reduce(lambda x, y: x * y, clique_potentials)

    return result



filename_ = sys.argv[1]

# markov_network = read_uai_file("grid3x3.uai")
# markov_network = read_uai_file("problem.uai")
# markov_network = read_uai_file("misconception.uai")

markov_network = read_uai_file(filename_)
partition = markov_partition(markov_network)

print("Partition function: {}".format(partition))
print("Log10: {}".format(np.log10(partition)))
