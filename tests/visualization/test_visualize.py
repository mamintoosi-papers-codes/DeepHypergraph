import pytest
import numpy as np
from dhg.random.graphs.graph import graph_Gnp

from dhg.visualization.structure.draw2 import draw_graph, draw_bipartite_graph
from dhg.random import graph_Gnm, graph_Gnp, graph_Gnp_fast, bigraph_Gnm


import matplotlib.pyplot as plt


def test_vis_graph():
    g = graph_Gnp_fast(100, 0.015)
    draw_graph(g, e_style="line")
    plt.show()


def test_vis_bipartite_graph():
    
    g = bigraph_Gnm(40, 80, 100)
    draw_bipartite_graph(g, e_style="line")
    plt.show()
    # try:
    #     g = bigraph_Gnm(40, 80, 100)
    #     draw_bipartite_graph(g, e_style="line")
    #     plt.show()
    # finally:

    #     for i in range(2000):
    #         pos = np.load('./tmp/position_{}.npy'.format(i))
    #         vel = np.load('./tmp/velocity_{}.npy'.format(i))

    #         x=pos[:,0]
    #         y=pos[:,1]
    #         u=vel[:,0]
    #         v=vel[:,1]

    #         plt.quiver(x,y,u,v)
    #         plt.savefig('./tmp/{}.png'.format(i))
    #         plt.clf()