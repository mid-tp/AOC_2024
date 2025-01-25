import networkx as nx
from time import time as time
start = time()
G = nx.Graph()

data = open("day_23/data_23.txt")

for line in data:
    c1, c2 = line.strip().split("-")
    # Add the computer as nodes, then add an 
    # edge between them
    G.add_node(c1)
    G.add_node(c2)
    G.add_edge(c1, c2)

# Now find the largest connectec component
lcc = ",".join(sorted(max(nx.find_cliques(G), key=len)))
print(lcc)
print(f"{time()-start:.4f}")