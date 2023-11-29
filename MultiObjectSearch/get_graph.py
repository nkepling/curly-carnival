import networkx as nx
import numpy as np
    
def get_graph(size=5):
    G = nx.Graph()
    mat = np.arange(size**2).reshape((size,size))

    for i in range(size):
        for j in range(size):
            node = mat[i,j]

            if i>0: 
                G.add_edge(node,mat[i-1,j])

            if j>0:
                G.add_edge(node,mat[j,j-1])

    return G



if __name__ == "__main__":
    
    import matplotlib.pyplot as plt

    G = get_graph()
    nx.draw(G)
    plt.draw()
    plt.show()    
