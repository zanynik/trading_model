from Bipartite_Matching_Assignment import AssignmentProblem, BipartiteGraph, MaximumCardinalityMatching


def TestMaximumBipartiteMatching():
    V1, V2, E = [], [], []

    m = int(input("Enter the number of Edges in the graph : "))
    for i in range(m):
        v1, v2 = input("Enter Edges as v1 v2 : ").split()
        V1.append(v1)
        V2.append(v2)
        E.append((v1, v2))

    B = BipartiteGraph(V1, V2, E)
    MaximumCardinalityMatching(B, [])


def TestAssignmentProblem():
    V1, V2, E, W, Val = [], [], [], [], {}
    print("s - seller node, val_s - seller valuation,  b - buyer node, val_b - buyer valuation \n ")

    f = open("demofile.txt", "r")
    for x in f:
        v1, val1, v2, val2 = x.split()
        V1.append(v1)
        V2.append(v2)
        E.append((v1, v2))
        w = float(val2) - float(val1)
        W.append(float(w))
        if v1 not in Val.keys():
            Val[v1] = float(val1)
        else:
            if Val[v1] != float(val1):
                print("Valuation is varying for Agent Node ", v1, ". Previous valuation is taken.")

        if v2 not in Val.keys():
            Val[v2] = float(val2)
        else:
            if Val[v2] != float(val2):
                print("Valuation is varying for Agent Node ", v2, ". Previous valuation is taken.")

    # Completing the graph if Incomplete
    for u in V1:
        for v in V2:
            if (u, v) not in E:
                E.append((u, v))
                W.append(float(0))

    B = BipartiteGraph(V1, V2, E, W)
    AssignmentProblem(B, Val)


if __name__ == '__main__':
    # TestMaximumBipartiteMatching()
    TestAssignmentProblem()
