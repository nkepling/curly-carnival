import networkx as nx
import numpy as np
    
def get_graph(desc,size):
    """
    INPUTS:

    numpy.array[String] desc : numpy array of map description


    int size : size length of input map
    """
    G = nx.Graph()
    # mat = np.arange(size**2).reshape((size,size))

    for i in range(size):
        for j in range(size):
            # node = mat[i,j]
            
            if i>0: 
                if desc[i,j] ==  "W" or desc[i-1,j] == "W":
                    G.add_edge((i,j),(i-1,j),weight = np.inf)
                else:
                    G.add_edge((i,j),(i-1,j),weight = 1)

            if j>0:
                if desc[i,j] == "W" or desc[i,j-1] == "W":
                    G.add_edge((i,j),(i,j-1),weight = np.inf)
                else:
                    G.add_edge((i,j),(i,j-1),weight = 1)
    return G



if __name__ == "__main__":
    
    import matplotlib.pyplot as plt
    import yaml
    
    with open("MultiObjectSearch/MAPS.yaml","r") as f:
        MAPS = yaml.load(f, Loader=yaml.FullLoader)

    map_name = "9x9"
    size = 9
    
    desc = np.array([list(i) for i in MAPS[map_name]])
    print(desc)

    G = get_graph(desc=desc,size=size)
    print(G)
    nx.draw(G)
    plt.draw()
    plt.show()    
