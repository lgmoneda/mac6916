### Reference: http://ai.stanford.edu/~paskin/gm-short-course/lec2.pdf
### Results compared with http://pgmlearning.herokuapp.com/dSepApp

class node():
    """
    Nodes class
    """
    def __init__(self, name):
        self.name = name
        self.nodes_in = []
        self.nodes_out = []
        self.gray = False

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def set_gray(self, value):
        self.gray = value

    def set_nodes_in(self, nodes_list):
        self.nodes_in += nodes_list

    def set_nodes_out(self, nodes_list):
        self.nodes_out += nodes_list

        for node in nodes_list:
            node.set_nodes_in([self])

    def is_blocked(self):
        return self.gray

    def print_connections(self):
        print("Node {} connections: ".format(self.name))
        print("In: {}".format([node.name for node in self.nodes_in]))
        print("Out: {}".format([node.name for node in self.nodes_out]))

def reset_gray(nodes):
    """
    Unblock all nodes from a network.
    """
    for node in nodes:
        node.set_gray(False)

def control_for(nodes):
    """
    Turn controlled nodes gray.
    """
    for node in nodes:
        node.set_gray(True)

def roll_bayes_ball(node):
    """
    It rolls bayes ball to reveal the adjacencies of its current position.
    It's going to identify the paths we should check considering their topology
    and controlled nodes if the ball will be able to continue rolling on it.
    """
    adjacent_nodes = []

    pairs = []
    triples = []
    paths = []

    for adj in node.nodes_in + node.nodes_out:
        pairs.append([node, adj])

    for pair in pairs:
        neighbors = pair[1].nodes_in + pair[1].nodes_out
        if len(neighbors) == 0:
            paths.append(pair)
        else:
            for adj2 in pair[1].nodes_in + pair[1].nodes_out:
                if adj2 != pair[0]:
                    triples.append(pair + [adj2])
                    paths.append(pair + [adj2])

    return paths

def chain(path):
    """
    Return True if a path is a chain.
    """
    return path[2] in path[1].nodes_out and path[1] in path[0].nodes_out

def collision(path):
    """
    Return True if a path is a collision.
    """
    return all(node in path[1].nodes_in for node in [path[0], path[2]])

def fork(path):
    """
    Return True if a path is a fork.
    """
    return all(node in path[1].nodes_out for node in [path[0], path[2]])

def which_topology(path):
    """
    Classify a path in respect to its topology.
    """
    if len(path) == 2: return "pair"
    if chain(path): return "chain"
    if fork(path): return "fork"
    if collision(path): return "collision"

def apply_rules(paths):
    """
    Take paths and classify their topologies and apply
    Bayes' ball rules accordingly to each one revealing the nodes reached
    and the ones to be explored in the next iteration.
    """
    nodes_to_explore = []
    reachable = []
    rules = []

    for path in paths:
        rules.append({"path": path,
                      "topology": which_topology(path)})

    for rule in rules:
        topology = rule["topology"]
        path = rule["path"]

        ### pairs
        if topology == "pair":
            ### always reached
            if not path[1].is_blocked():
                reachable.append(path[1])
            ### towards arrow
            if path[1] in path[0].nodes_out:
                if path[1].is_blocked():
                    nodes_to_explore.append(path[1])
            ### against arrow
            else:
                if not path[1].is_blocked():
                    nodes_to_explore.append(path[1])

        if topology == "fork":
            if not path[1].is_blocked():
                reachable += [path[1], path[2]]
                nodes_to_explore.append(path[1])

        if topology == "collision":
            if path[1].is_blocked():
                reachable += [path[1], path[2]]
                nodes_to_explore.append(path[1])

        if topology == "chain":
            if not path[1].is_blocked():
                reachable += [path[1], path[2]]
                nodes_to_explore.append(path[1])

    return nodes_to_explore, reachable

def check_dseparation(node1, node2, controlled, network):
    """
    Checks if node1 and node2 are d-separated given a set of controlled
    variables (it can be empty) from a network.
    """

    ### Clean from previous test
    reset_gray(network)

    ### Block controlled nodes
    control_for(controlled)

    reachable_nodes = []
    nodes_to_explore = [node1]

    next_node = node1
    while node2 not in reachable_nodes and len(nodes_to_explore) > 0:
        paths = roll_bayes_ball(next_node)

        # print("Reachable: {}".format(reachable_nodes))
        # print("To explore: {}".format(nodes_to_explore))

        new_nodes_to_explore, new_reachable = apply_rules(paths)

        nodes_to_explore += new_nodes_to_explore
        reachable_nodes += new_reachable
        reachable_nodes = list(set(reachable_nodes))

        nodes_to_explore.pop(0)
        if len(nodes_to_explore) > 0:
            next_node = nodes_to_explore[0]

    msg = node1.name + " and " + node2.name
    if len(controlled) > 0:
        msg += " given " + ", ".join([node.name for node in controlled])
    if node2 in reachable_nodes:
        print(msg + " are not d-separated")
    else:
        print(msg + " are d-separated")
    return network

### Declare the nodes
A = node("Visit to (A)sia")
T = node("(T)uberculosis")
E = node("(E)ither")
X = node("(X)-ray")
D = node("(D)yspnoea")
L = node("(L)ung cancer")
S = node("(S)moking")
B = node("(B)ronchitis")

### Declare the connections
A.set_nodes_out([T])
T.set_nodes_out([E])
E.set_nodes_out([X, D])

S.set_nodes_out([L, B])
L.set_nodes_out([E])
B.set_nodes_out([D])

network = [A, T, E, X, D, L, S, B]

### Not d-separated
check_dseparation(A, B, [E, D], network)

### D-separated
check_dseparation(A, X, [E], network)

### D-separated
check_dseparation(A, L, [], network)

### not d-separated
check_dseparation(A, L, [E], network)
