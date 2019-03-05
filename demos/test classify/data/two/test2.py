# 首先定义一个创建图的类，使用邻接矩阵
class Graph(object):
def __init__(self, *args, **kwargs):
self.order = [] # visited order
self.neighbor = {}
def add_node(self, node):
key, val = node
if not isinstance(val, list):
print('节点输入时应该为一个线性表') # 避免不正确的输入
self.neighbor[key] = val

# 深度优先算法的实现
def DFS(self, root):
# 首先判断根节点是否为空节点
if root != None:
search_queue = deque()
search_queue.append(root)
visited = []
else:
print('root is None')
return -1
while search_queue:
person = search_queue.popleft()
self.order.append(person)
if (not person in visited) and (person in self.neighbor.keys()):
tmp = self.neighbor[person]
tmp.reverse()
for index in tmp:
search_queue.appendleft(index)
visited.append(person)


