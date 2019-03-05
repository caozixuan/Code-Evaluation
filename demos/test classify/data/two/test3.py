def rec_dfs(G,s,S=None):
    if S is None:S = set()
    S.add(s)
    for u in G[s]:
        if u in S:coontinue
        rec_dfs(G,u,S)
