def iddfs(G,s):
    yielded=set()
    def recurse(G,s,d,S=None):
        if s not in yielded:
            yield s
            yielded.add(s)
        if d==0:return
        if S is None:S=set()
        S.add(s)
        for u in G[s]:
            if u in S:continue
            for v in recurse(G,u,d-1,S):
                yield v
    n=len(G)
for d in range(n):
    if len(yielded)==n:break
    for u in recurse(G,s,d):
        yield u

if __name__=="__main__":
    a, b, c, d, e, f, g, h, i= range(9)
    N = [
         {b, c, d},  # a
         {a, d},     # b
         {a,d},      # c
         {a,b,c},    # d
         {g,f},      # e
         {e,g},      # f
         {e,f},      # g
         {i},        # h
         {h}         # i
         ]
        
         G = [{b,c,d,e,f},#a
              {c,e},      # b
              {d},        # c
              {e},        # d
              {f},        # e
              {c,g,h},    # f
              {f,h},      # g
              {f,g}       # h
              ]
         
         p=list(iddfs(G,0))         # [0, 1, 2, 3, 4, 5, 6, 7]
         m=list(iddfs(N,0))         # [0, 1, 2, 3]
