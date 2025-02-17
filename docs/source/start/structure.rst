Structures in DHG
===================================

Introduction
----------------
The core motivation of **DHG** is to attach those spectral-based and spatial-based operations to each specified structure. 
When a structure is created, those related Laplacian Matrices and message passing operations with different aggregation functions can be called and combined to manipulate any input features. 
Currently, the **DHG** has implemented the following structures and attached operations. More structures and operations will be added in the future. **Welcome to contribute!**


.. csv-table:: Summary of Supported Structures and Attached Operations
    :header: "Structure", "Class Name", "Type", "Spectral-Based Operations", "Spatial-Based Operations", "Aggregations"
    :widths: 2 2 2 3 3 2

    "| Simple
    | Graphs", ":ref:`dhg.Graph <dhg_graph_class>`", "Low-Order", "| :math:`\mathcal{L}_{sym}` , :math:`\mathcal{L}_{rw}` 
    | :math:`\mathcal{L}_{GCN}`", ":math:`v \rightarrow v`", "| ``mean``,
    | ``sum``,
    | ``softmax_then_sum``"
    "| Directed
    | Graphs", ":ref:`dhg.Digraph <dhg_digraph_class>`", "Low-Order", *To Be Added*, "| :math:`v_{src} \rightarrow v_{dst}`
    | :math:`v_{dst} \rightarrow v_{src}`", "| ``mean``,
    | ``sum``,
    | ``softmax_then_sum``"
    "| Bipartite
    | Graphs", ":ref:`dhg.Bigraph <dhg_bigraph_class>`", "Low-Order", ":math:`\mathcal{L}_{GCN}`", "| :math:`u \rightarrow v` 
    | :math:`v \rightarrow u`", "| ``mean``,
    | ``sum``,
    | ``softmax_then_sum``"
    "| Simple
    | Hypergraphs", ":ref:`dhg.Hypergraph <dhg_hypergraph_class>`", "High-Order", "| :math:`\mathcal{L}_{sym}` , :math:`\mathcal{L}_{rw}` 
    | :math:`\mathcal{L}_{HGNN}`", "| :math:`v \rightarrow e`
    | :math:`v \rightarrow e` (specified group)
    | :math:`e \rightarrow v`
    | :math:`e \rightarrow v` (specified group)", "| ``mean``,
    | ``sum``,
    | ``softmax_then_sum``"


Applications
-----------------

.. csv-table:: Summary of Applications of Differnet Structures
    :header: Structure, "Applications", "Example Code"
    :widths: 2, 6, 4

    "Simple Graphs", "Paper Classification of Citation Networks, *etc.*", "aaaaaaaaaa"
    "Directed Graphs", "Point Clouds Classification, *etc.*", "aaaaaaaaa"
    "Bipartite Graphs", "| Item Recommender of User-Item Graphs,
    | Correlation Prediction of Potein-Drug Graphs, *etc.*", "aaaaaaaaaaa"
    "Simple Hypergraphs", "| Vertex Classification of Social Networks, 
    | Visual Object Classification on Multi-Modal Visual Object Graphs, *etc.*", "aaaaaaaaaa"
    

Two Core Operations
----------------------------
The most learning on structures (graphs, hypergraphs, etc.) can be divided into two categories: spectral-based convolution and spatial-based message passing.
The spectral-based convolution methods, like typical GCN and HGNN, learn a Laplacian Matrix for a given structure, and perform ``vertex feature smoothing`` with the generated 
Laplacian Matrix to embed to low-order and high-order structures to vertex features. The spatial-based message passing methods, like typical GraphSAGE, GAT, and HGNN :sup:`+`, perform ``vertex to vertex``, ``vertex to hyperedge``, ``hyperedge to vertex``, 
and ``vertex set to vertex set`` message passing to embedd the low-order and high-order structures to vertex features. The learned vertex features can also be pooled to generate the unified structure feature.
Finally, the learned vertex features or structure features can be fed into many down-stream tasks like classification, retrieval, regression, and link prediction, 
and applications like paper classification, movie recommender, drug exploition, *etc.*

The Spectral-Based Operations
+++++++++++++++++++++++++++++++
The core of spectral-based convolution is the smoothing matrix like Laplacian Matrix. Some common smoothing matrices are provided in each structure. 
For example, the Laplacian Matrix proposed in `GCN <_blank>`_ can be called in the simple graph structure and the bipartite graph structure, and the Laplacian Matrix proposed in 
`HGNN <_blank>`_ can be called in the simple hypergraph structure.

In the following example, we randomly generate a **simple graph** structure with 5 vertices and 8 edges. 
We can fetch the Laplacian Matrix of the specified simple graph structure with the ``g.L_GCN`` inside attribute.
The size of the generated Laplacian Matrix is :math:`5 \times 5`. 
Then, for any input vertex features you can smoothing these with the specified simple graph ``g`` with function ``g.smoothing_with_GCN()``.

    .. code:: python

        >>> import torch
        >>> import dhg
        >>> dhg.random.set_seed(2022)
        >>> g = dhg.random.graph_Gnm(5, 8)
        >>> # Generate a vertex feature matrix with size 5x2
        >>> X = torch.rand(5, 2)
        >>> # Print information about the graph and feature
        >>> g 
        Simple Graph(num_v=5, num_e=8)
        >>> # Print edges in the graph
        >>> g.e[0]
        [(0, 1), (2, 4), (0, 4), (3, 4), (0, 3), (2, 3), (0, 2), (1, 3)]
        >>> # Print vertex features
        >>> X
        tensor([[0.3958, 0.9219],
                [0.7588, 0.3811],
                [0.0262, 0.3594],
                [0.7933, 0.7811],
                [0.4643, 0.6329]])
        >>> # Print the inside Laplacian Matrix by GCN on the simple graph structure
        >>> g.L_GCN.to_dense()
        tensor([[0.2000, 0.2582, 0.2236, 0.2000, 0.2236],
                [0.2582, 0.3333, 0.0000, 0.2582, 0.0000],
                [0.2236, 0.0000, 0.2500, 0.2236, 0.2500],
                [0.2000, 0.2582, 0.2236, 0.2000, 0.2236],
                [0.2236, 0.0000, 0.2500, 0.2236, 0.2500]])
        >>> X_ = g.smoothing_with_GCN(X)
        >>> # Print the vertex features after GCN-based smoothing
        >>> X_
        tensor([[0.5434, 0.6609],
                [0.5600, 0.5668],
                [0.3885, 0.6289],
                [0.5434, 0.6609],
                [0.3885, 0.6289]])

In the following example, we randomly generate a **bipartite graph** structure with 3 vertices in set :math:`\mathcal{U}`, 5 vertices in set :math:`\mathcal{V}`, and 8 edges.
We can fetch the Laplacian Matrix of the specified bipartite graph structure with ``g.L_GCN`` inside attribute. 
The size of the generated Laplacian Matrix is :math:`8 \times 8`. 
Then, for any input vertex features you can smoothing these with the specified bipartite graph ``g`` with function ``g.smoothing_with_GCN()``. More details can refer to :ref:`here <start_learning_on_bipartite_graph>`.

    .. note:: 

        The GCN's Laplacian Matrix of bipartite graphs is achieve by concate the bipartite adjacency matrix :math:`\mathbf{B}` with size :math:`|\mathcal{U}| \times |\mathcal{V}|` to 
        the big adjacency matrix :math:`\mathbf{A}` with size :math:`||\mathcal{U}| + |\mathcal{V}|| \times ||\mathcal{U}| + |\mathcal{V}||`.

    .. code:: python

        >>> import torch
        >>> import dhg
        >>> dhg.random.set_seed(2022)
        >>> g = dhg.random.bigraph_Gnm(3, 5, 8)
        >>> # Print edges in the bipartite graph structure 
        >>> g.e[0]
        [(2, 4), (0, 4), (0, 3), (2, 0), (1, 4), (2, 3), (2, 2), (1, 3)]
        >>> # Print the inside Laplacian Matrix by GCN on the bipartite graph structure
        >>> g.L_GCN.to_dense()
        tensor([[0.3333, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.2887, 0.2887],
                [0.0000, 0.3333, 0.0000, 0.0000, 0.0000, 0.0000, 0.2887, 0.2887],
                [0.0000, 0.0000, 0.2000, 0.3162, 0.0000, 0.3162, 0.2236, 0.2236],
                [0.0000, 0.0000, 0.3162, 0.5000, 0.0000, 0.0000, 0.0000, 0.0000],
                [0.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000, 0.0000],
                [0.0000, 0.0000, 0.3162, 0.0000, 0.0000, 0.5000, 0.0000, 0.0000],
                [0.2887, 0.2887, 0.2236, 0.0000, 0.0000, 0.0000, 0.2500, 0.0000],
                [0.2887, 0.2887, 0.2236, 0.0000, 0.0000, 0.0000, 0.0000, 0.2500]])

In the following example, we randomly generate a **simple hypergraph** structure with 5 vertices and 4 hyperedges. 
We can fetch the Laplacian Matrix of the specified simple hypergraph structure with ``hg.L_HGNN`` inside attribute. 
The size of the generated Laplacian Matrix is :math:`5 \times 5`.
Then, for any input vertex features you can smoothing these with the specified simple hypergraph ``hg`` with function ``hg.smoothing_with_HGNN()``. More details can refer to :ref:`here <start_learning_on_simple_hypergraph>`.

    .. code:: python

        >>> import torch
        >>> import dhg
        >>> dhg.random.set_seed(2022)
        >>> hg = dhg.random.hypergraph_Gnm(5, 4)
        >>> # Print hyperedges in the simple hypergraph structure 
        >>> hg.e[0]
        [(2, 3), (0, 2, 4), (2, 3, 4), (1, 2, 3, 4)]
        >>> # Print the inside Laplacian Matrix by HGNN on the simple hypergraph structure
        >>> hg.L_HGNN.to_dense()
        tensor([[0.3333, 0.0000, 0.1667, 0.0000, 0.1925],
                [0.0000, 0.2500, 0.1250, 0.1443, 0.1443],
                [0.1667, 0.1250, 0.3542, 0.3127, 0.2646],
                [0.0000, 0.1443, 0.3127, 0.3611, 0.1944],
                [0.1925, 0.1443, 0.2646, 0.1944, 0.3056]])


The Spatial-Based Operations 
+++++++++++++++++++++++++++++++
The core of the spatial-based operation is message passing from ``source domain`` to ``target domain`` and message aggregation with different aggregation function. 
In **DHG**, the ``soure domain`` and ``target domain`` can be anyone of ``a vertex``, ``a vertex in specified vertex set``, ``a hyperedge``, and ``a vertex set``. 
The message aggregation function can be ``mean``, ``softmax``, and ``softmax_then_sum``. 
Thus, unlike `PyG <https://www.pyg.org/>`_ and `DGL <https://www.dgl.ai/>`_ that can only pass messages from ``a vertex`` to ``another vertex or edge``, 
the **DHG** provides more types of message passing functions on both low-order structure and high-order structure. 

In the following example, we randomly generate a **simple graph** structure with 5 vertices and 8 edges. 
The simple graph structure provides propagate message from ``a vertex`` to ``another vertex``, and the supported message aggregation function includes ``mean``, ``softmax``, and ``softmax_then_sum``.

    .. code:: python

        >>> import torch
        >>> import dhg
        >>> dhg.random.set_seed(2022)
        >>> g = dhg.random.graph_Gnm(5, 8)
        >>> # Generate a vertex feature matrix with size 5x2
        >>> X = torch.rand(5, 2)
        >>> # Print information about the graph and feature
        >>> g 
        Simple Graph(num_v=5, num_e=8)
        >>> # Print edges in the graph
        >>> g.e[0]
        [(0, 1), (2, 4), (0, 4), (3, 4), (0, 3), (2, 3), (0, 2), (1, 3)]
        >>> # Print vertex messages
        >>> X
        tensor([[0.3958, 0.9219],
                [0.7588, 0.3811],
                [0.0262, 0.3594],
                [0.7933, 0.7811],
                [0.4643, 0.6329]])
        >>> # Propagate messages from a vertex to another vertex with mean aggregation function
        >>> X_ = g.v2v(X, aggr="mean")
        >>> # Print new vertex messages
        >>> X_
        tensor([[0.5107, 0.5386],
                [0.5946, 0.8515],
                [0.5512, 0.7786],
                [0.4113, 0.5738],
                [0.4051, 0.6875]])
        >>> # Propagate messages from a vertex to another vertex with sum aggregation function
        >>> X_ = g.v2v(X, aggr="sum")
        >>> # Print new vertex messages
        >>> X_
        tensor([[2.0427, 2.1545],
                [1.1892, 1.7030],
                [1.6535, 2.3359],
                [1.6452, 2.2954],
                [1.2154, 2.0624]])
        >>> # Set the weight of each edge for softmax in neighbor aggregation
        >>> e_weight = g.e_weight
        >>> # Propagate messages from a vertex to another vertex with softmax_then_sum aggregation function
        >>> X_ = g.v2v(X, e_weight=e_weight, aggr="softmax_then_sum")
        >>> # Print new vertex messages
        >>> X_
        tensor([[0.5107, 0.5386],
                [0.5946, 0.8515],
                [0.5512, 0.7786],
                [0.4113, 0.5738],
                [0.4051, 0.6875]])


In the following example, we randomly generate a **bipartite graph** structure with 3 vertices in set :math:`\mathcal{U}`, 5 vertices in set :math:`\mathcal{V}`, and 8 edges.
The bipartite graph structure provides message passing from ``a vertex in a specified vertex set`` to ``another vertex in another specified vertex set``, and 
the supported message aggregation function includes ``mean``, ``softmax``, and ``softmax_then_sum``.
The detailed spatial-based operation on bipartite graph can refer to :ref:`here <start_learning_on_bipartite_graph>`.


    .. code:: python

        >>> import torch
        >>> import dhg
        >>> # Generate a random bipartite graph with 3 vertices in set U, 5 vertices in set V, and 8 edges
        >>> g = dhg.random.bigraph_Gnm(3, 5, 8)
        >>> # Generate feature matrix for vertices in set U and set V, respectively.
        >>> X_u, X_v = torch.rand(3, 2), torch.rand(5, 2)
        >>> g 
        Bipartite Graph(num_u=3, num_v=5, num_e=8)
        >>> # Print edges in the graph
        >>> g.e[0]
        [(2, 4), (0, 4), (0, 3), (2, 0), (1, 4), (2, 3), (2, 2), (1, 3)]
        >>> # Print vertex features
        >>> X_u
        tensor([[0.3958, 0.9219],
                [0.7588, 0.3811],
                [0.0262, 0.3594]])
        >>> X_v
        tensor([[0.7933, 0.7811],
                [0.4643, 0.6329],
                [0.6689, 0.2302],
                [0.8003, 0.7353],
                [0.7477, 0.5585]])
        >>> # Propagate messages from vertices in set V to vertices in set U with mean aggregation
        >>> X_u_ = g.v2u(X_v, aggr="mean")
        >>> X_u_
        tensor([[0.7740, 0.6469],
                [0.7740, 0.6469],
                [0.7526, 0.5763]])
        >>> # Propagate messages from vertices in set U to vertices in set V with mean aggregation
        >>> X_v_ = g.u2v(X_u, aggr="mean")
        >>> X_v_
        tensor([[0.0262, 0.3594],
                [0.0000, 0.0000],
                [0.0262, 0.3594],
                [0.3936, 0.5542],
                [0.3936, 0.5542]])


In the following example, we randomly generate a **simple hypergraph** structure with 5 vertices and 4 hyperedges. 
The simple hypergraph structure provides message passing from ``a vertex`` to ``another vertex``, from ``a vertex set`` to ``a hyperedge``, 
from ``a hyperedge`` to ``a vertex set``, and from ``a vertex set`` to ``another vertex set``. 
The supported message aggregation function includes ``mean``, ``softmax``, and ``softmax_then_sum``.
The detailed spatial-based operation on simple hypergraph can refer to :ref:`here <start_learning_on_simple_hypergraph>`.
 
    .. code:: python
    
        >>> import torch
        >>> import dhg
        >>> dhg.random.set_seed(2022)
        >>> g = dhg.random.hypergraph_Gnm(5, 4)
        >>> # Generate a vertex feature matrix with size 5x2
        >>> X = torch.rand(5, 2)
        >>> # Print information about the hypergraph and feature
        >>> g 
        Simple Hypergraph(num_v=5, num_e=4)
        >>> # Print edges in the graph
        >>> g.e[0]
        [(2, 3), (0, 2, 4), (2, 3, 4), (1, 2, 3, 4)]
        >>> # Print vertex messages
        >>> X
        tensor([[0.3958, 0.9219],
                [0.7588, 0.3811],
                [0.0262, 0.3594],
                [0.7933, 0.7811],
                [0.4643, 0.6329]])
        >>> # Propagate messages from vertex sets to hyperedges with mean aggregation function
        >>> Y_ = g.v2e(X, aggr="mean")
        >>> # Print new hyperedge messages
        >>> Y_
        tensor([[0.4098, 0.5702],
                [0.2955, 0.6381],
                [0.4280, 0.5911],
                [0.5107, 0.5386]])
        >>> # Propagate messages from hyperedges to vertex sets with mean aggregation function
        >>> X_ = g.e2v(Y_, aggr="mean")
        >>> # Print new vertex messages
        >>> X_
        tensor([[0.2955, 0.6381],
                [0.5107, 0.5386],
                [0.4110, 0.5845],
                [0.4495, 0.5667],
                [0.4114, 0.5893]])


What Can be Done with the Two Operations?
-------------------------------------------


Add Eary Self-loop and Late Self-Loop
++++++++++++++++++++++++++++++++++++++++++

Self-loop is a important structure for feature learning especially for the simple graph structure. 
In the following examples, we introduce how to add early self-loop and late self-loop for spatial-based learning on the simple graph structure.

Add mathematical definition aaaaaaaaaaaaaaaaaaaaaaaaa

    .. code:: python

        >>> import torch
        >>> import dhg
        >>> dhg.random.set_seed(2022)
        >>> g = dhg.random.graph_Gnm(5, 8)
        >>> # Generate a vertex feature matrix with size 5x2
        >>> X = torch.rand(5, 2)
        >>> # Print information about the graph and feature
        >>> g 
        Simple Graph(num_v=5, num_e=8)
        >>> # Print edges in the graph
        >>> g.e[0]
        [(0, 1), (2, 4), (0, 4), (3, 4), (0, 3), (2, 3), (0, 2), (1, 3)]
        >>> # Print vertex features
        >>> X
        tensor([[0.3958, 0.9219],
                [0.7588, 0.3811],
                [0.0262, 0.3594],
                [0.7933, 0.7811],
                [0.4643, 0.6329]])

Message Passing with Early Self-Loop 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    .. code:: python
        
        >>> # Print edges in the graph
        >>> g.e[0]
        [(0, 1), (2, 4), (0, 4), (3, 4), (0, 3), (2, 3), (0, 2), (1, 3)]
        >>> # Print vertex features
        >>> X
        tensor([[0.3958, 0.9219],
                [0.7588, 0.3811],
                [0.0262, 0.3594],
                [0.7933, 0.7811],
                [0.4643, 0.6329]])
        >>> # Add self-loop before message passing
        >>> g.add_extra_selfloop()
        >>> g.e[0]
        [(0, 1), (2, 4), (0, 4), (3, 4), (0, 3), (2, 3), (0, 2), (1, 3), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
        >>> X_ = g.v2v(X, aggr="mean")
        >>> X_
        tensor([[0.4877, 0.6153],
                [0.6493, 0.6947],
                [0.4199, 0.6738],
                [0.4877, 0.6153],
                [0.4199, 0.6738]])


Message Passing with Late Self-Loop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. code:: python
        
        >>> # Print edges in the graph
        >>> g.e[0]
        [(0, 1), (2, 4), (0, 4), (3, 4), (0, 3), (2, 3), (0, 2), (1, 3)]
        >>> # Print vertex features
        >>> X
        tensor([[0.3958, 0.9219],
                [0.7588, 0.3811],
                [0.0262, 0.3594],
                [0.7933, 0.7811],
                [0.4643, 0.6329]])
        >>> # Add self-loop after message passing
        >>> X_ = X + g.v2v(X, aggr="mean")
        >>> X_
        tensor([[0.9065, 1.4606],
                [1.3534, 1.2326],
                [0.5774, 1.1380],
                [1.2046, 1.3549],
                [0.8695, 1.3204]])


Fuse Features Learned from the Spectral and Spatial Domain
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In the following example, we randomly generate a **simple graph** structure with 5 vertices and 8 edges. 
Then, we attemp to fuse the features that learned from the different methods but the same structure ``g``.

    .. code:: python

        >>> import torch
        >>> import dhg
        >>> dhg.random.set_seed(2022)
        >>> g = dhg.random.graph_Gnm(5, 8)
        >>> # Generate a vertex feature matrix with size 5x2
        >>> X = torch.rand(5, 2)
        >>> # Print information about the graph and feature
        >>> g 
        Simple Graph(num_v=5, num_e=8)
        >>> # Print edges in the graph
        >>> g.e[0]
        [(0, 1), (2, 4), (0, 4), (3, 4), (0, 3), (2, 3), (0, 2), (1, 3)]
        >>> # Print vertex features
        >>> X
        tensor([[0.3958, 0.9219],
                [0.7588, 0.3811],
                [0.0262, 0.3594],
                [0.7933, 0.7811],
                [0.4643, 0.6329]])
        >>> # Fuse features learned from different domains
        >>> X_ = (g.smoothing_with_GCN(X) + g.v2v(X, aggr="mean"))/2
        >>> X_
        tensor([[0.5271, 0.5998],
                [0.5773, 0.7091],
                [0.4699, 0.7038],
                [0.4774, 0.6174],
                [0.3968, 0.6582]])


Fuse Features Learned from different Structures
++++++++++++++++++++++++++++++++++++++++++++++++++

In the following example, we construct two different structures including simple graph structure and simple hypergraph structure on the same vertex set. 
Then, two structures' message passing functions are adopted to generate vertex features learned from different structure, 
and the final hybrid vertex features can be generated by the combination of them.

    .. code:: python

        >>> import torch
        >>> import dhg
        >>> dhg.random.set_seed(2022)
        >>> # Generate the vertex features
        >>> X = torch.rand(5, 2)
        >>> # Generate the low-order structure on the vertex set
        >>> g = dhg.random.graph_Gnm(5, 8)
        >>> # Generate the high-order structure on the vertex set
        >>> hg = dhg.random.hypergraph_Gnm(5, 4)
        >>> # Print information before message passing
        >>> X
        tensor([[0.3958, 0.9219],
                [0.7588, 0.3811],
                [0.0262, 0.3594],
                [0.7933, 0.7811],
                [0.4643, 0.6329]])
        >>> g.e[0]
        [(0, 1), (2, 4), (0, 4), (3, 4), (0, 3), (2, 3), (0, 2), (1, 3)]
        >>> hg.e[0]
        [(0, 1), (0, 3, 4), (1, 2, 3), (1, 3)]
        >>> X_low = g.v2v(X, aggr="mean")
        >>> X_high = hg.v2v(X, aggr="mean")
        >>> X_ = torch.cat([X_low, X_high], dim=1)
        >>> # Print new vertex features
        >>> X_
        tensor([[0.5107, 0.5386, 0.5642, 0.7151],
                [0.5946, 0.8515, 0.6265, 0.5799],
                [0.5512, 0.7786, 0.5261, 0.5072],
                [0.4113, 0.5738, 0.6178, 0.6223],
                [0.4051, 0.6875, 0.5512, 0.7786]])
