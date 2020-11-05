import matplotlib.pyplot as plt
import networkx as nx


class BipartiteGraph:
    def __init__(self, V1, V2, E=None, W=None):
        """
        Class constructor
        V1 and V2 are iterables containing the vertices in the first and second partitions
        vertices can be any hashable objects
        E is an iterable of edges (edges are iterables of size 2)
        W is an iterable containing the weights of the edges
        """
        if E is None:
            E = []
        self.V1 = set(V1)
        self.V2 = set(V2)
        self.V = self.V1 | self.V2
        self.Adj = {v: set() for v in self.V}
        for (v1, v2) in E:
            self.Adj[v1].add(v2)
            self.Adj[v2].add(v1)

        if W is not None:
            self.W = {tuple(e): W[k] for (k, (u, v)) in enumerate(E) for e in [(u, v), (v, u)]}
        self.E = set(tuple(e) for e in E)


def plot_graph(B, M, Val=None, d=None, t=None):
    G = nx.Graph()
    G.add_nodes_from(B.V)

    G.add_edges_from(M)

    options = {
        "edge_color": 'b',
        "width": 4,
        "label": 'foo',
        "with_labels": True,
    }

    pos = dict()
    pos.update((n, (1, i)) for i, n in enumerate(B.V1))  # put nodes from X at x=1
    pos.update((n, (2, i)) for i, n in enumerate(B.V2))  # put nodes from Y at x=2

    nx.draw(G, pos=pos, **options)

    # Valuation labels
    pos_attrs = {}
    labels = {}
    for node, coords in pos.items():
        pos_attrs[node] = (coords[0], coords[1] + 0.07)
        labels[node] = r"$" + str(Val[node]) + "$"

    nx.draw_networkx_labels(G, pos_attrs, labels, font_size=12)

    # Profit labels
    pos_attrs2 = {}
    labels2 = {}
    for node, coords in pos.items():
        pos_attrs2[node] = (coords[0], coords[1] - 0.07)
        labels2[node] = r"$" " p = " + str(round(d[node])) + "$"

    nx.draw_networkx_labels(G, pos_attrs2, labels2, font_size=12)

    M_not = [(v1, v2) for (v1, v2) in B.E if (v1, v2) not in M and (B.W[(v1, v2)] > 1e-6)]
    G.add_edges_from(M_not)
    nx.draw(G, pos=pos)

    edge_labels = {**{(u, v): (Val[v] + round(d[v])) for (u, v) in G.edges if v in B.V1},
                   **{(v, u): (Val[u] + round(d[u])) for (u, v) in G.edges if u in B.V1},
                   **{(u, v): (Val[v] - round(d[v])) for (u, v) in G.edges if v in B.V2},
                   **{(v, u): (Val[u] - round(d[u])) for (u, v) in G.edges if u in B.V2},
                   }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.15, font_size=14)

    edge_labels_t = {(u, v): "yt = " + str(t[(u, v)]) for (u, v) in M + M_not}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_t, label_pos=0.4, font_size=14)

    plt.show()


def MaximumCardinalityMatching(B, M=[], returnLabeled=False):
    """
    Computes the maximum cardinality matching of the bipartite graph B
    B must be an object of the BipartiteGraph class above
    M is an iterable containing edges (iterables of size 2) in a previously known matching
    """
    mate = {v: None for v in B.V}  # Initializing
    for (v1, v2) in M:
        mate[v1], mate[v2] = v2, v1

    label = {v: None for v in B.V}
    labeledV1, labeledV2 = set(), set()

    L = set(v for v in B.V1 if mate[v] == None)
    for v in L:
        label[v] = '*'

    while L:
        v = L.pop()
        if v in B.V1:
            labeledV1.add(v)
            for u in B.Adj[v]:
                if u != mate[v]:
                    label[u] = v
                    L.add(u)
        else:
            labeledV2.add(v)
            if mate[v] is None:  # Augmenting path found
                while v != '*':
                    u = label[v]
                    mate[u], mate[v] = v, u
                    v = label[u]

                label = {v: None for v in B.V}

                L = set(v for v in B.V1 if mate[v] is None)
                for v in L:
                    label[v] = '*'

            else:
                u = mate[v]
                label[u] = v
                L.add(u)

    M = [(v1, v2) for (v1, v2) in B.E if mate[v1] == v2]

    if returnLabeled:
        return M, labeledV1, labeledV2
    else:
        print("Maximum matching is ", len(M))
        print("Edges in Matching are :", M)
        plot_graph(B, M)


def AssignmentProblem(B, Val):
    """
    Computes the maximum cost assignment of the bipartite graph B
    B is assumed to be complete
    """
    # Feasible Initial Solution
    d = {v: max(B.W[(v, u)] for u in B.Adj[v]) for v in B.V}
    t = {(u, v): 0 for (u, v) in B.E}

    modW = {(u, v): (B.W[(u, v)] - d[u] - d[v]) for (u, v) in B.E}

    M = []
    while True:
        modB = BipartiteGraph(B.V1, B.V2, E=[e for e in B.E if abs(modW[e]) < 1e-6])
        M, lV1, lV2 = MaximumCardinalityMatching(modB, M, returnLabeled=True)
        try:
            delta = min(-modW[(v1, v2)] for v1 in lV1 for v2 in B.V2 - lV2)
        except Exception as e:
            delta = 0
            pass
        if delta > 0:
            # Dual step

            for v1 in lV1:
                d[v1] -= delta / 2
            for v2 in lV2:
                d[v2] += delta / 2

            for v1 in B.V1 - lV1:
                d[v1] += delta / 2
            for v2 in B.V2 - lV2:
                d[v2] -= delta / 2

            modW = {(u, v): (B.W[(u, v)] - d[u] - d[v]) for (u, v) in B.E}

        else:
            break

    # Monopolized Agents have p = 0
    for u in B.V1:
        i = 0
        for v in B.Adj[u]:
            if B.W[(u, v)] > 0:
                i = i + 1
                y = v
        if i == 1:
            t[(u, y)] += d[u]
            d[u] = 0

    for v in B.V2:
        i = 0
        for u in B.Adj[v]:
            if B.W[(u, v)] > 0:
                i = i + 1
                x = u
        if i == 1:
            t[(x, v)] += d[v]
            d[v] = 0

    # # Tightening edges adjacent to M
    # modW = {(u, v): (B.W[(u, v)] - d[u] - d[v]) for (u, v) in B.E}
    # for (u, v) in M:
    #     eps1 = 0
    #     try:
    #         eps1 = min(-modW[(u, y)] for y in (B.Adj[u] - {v}) if (B.W[(u, y)] > 0))
    #     except: pass
    #
    #     if d[u] >= eps1:
    #         d[u] -= eps1
    #         t[(u, v)] += eps1
    #     else:
    #         t[(u, v)] += d[u]
    #         d[u] = 0
    #
    #     modW = {(u, v): (B.W[(u, v)] - d[u] - d[v]) for (u, v) in B.E}
    #
    #     eps2 = 0
    #     try:
    #         eps2 = min(-modW[(x, v)] for x in (B.Adj[v] - {u}) if B.W[(x, v)] > 0)
    #     except: pass
    #
    #     if d[v] >= eps2:
    #         d[v] -= eps2
    #         t[(u, v)] += eps2
    #     else:
    #         t[(u, v)] += d[v]
    #         d[v] = 0
    #
    #     modW = {(u, v): (B.W[(u, v)] - d[u] - d[v]) for (u, v) in B.E}
    W_sum = 0
    M_o = []
    for (u, v) in M:
        W_sum = W_sum + B.W[(u, v)]
        if B.W[(u, v)] > 1e-6:
            M_o.append((u, v))
            print(f"p_{u} = {d[u]} p_{v} = {d[v]} y_t = {t[(u, v)]} and w_uv = {B.W[(u, v)]}")
    print(f"\nEdges in Matching are :{M_o}")
    print("\nMaximum matching is: %d Weight of matching: %d" % (len(M_o), W_sum))
    plot_graph(B, M_o, Val, d, t)
