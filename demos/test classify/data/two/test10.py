def DFS(G,v0):
    S = []
    S.append(v0)
    label = set()
    while S:
    v = S.pop()
    if v not in label:
        label.add(v)
        procedure(v)
        for w in G[v]:
        S.append(w)
