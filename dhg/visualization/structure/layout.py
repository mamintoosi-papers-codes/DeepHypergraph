import numpy as np
from scipy.spatial import ConvexHull

from .simulator import Simulator
from .geometry import radian_from_atan, vlen, common_tangent_radian, polar_position


def _force_directed_layout(n_v, H, max_iter=100, epsilon=0.01):
    """
    Force-directed layout algorithm.
    """
    pos = np.random.rand(n_v, 2)
    sim = Simulator({
        Simulator.NODE_ATTRACTION: 1.0,
        Simulator.NODE_REPULSION: 1.5,
        Simulator.EDGE_REPULSION: 1.5})
    pos = sim.simulate(pos, H, max_iter, epsilon)

    # transform to (0.1, 0.9)
    pos = (pos - pos.min(axis=0)) / (pos.max(axis=0) - pos.min(axis=0)) * 0.8 + 0.1
    return pos

def _hull_layout(n_v, e_list, pos, init_radius=0.015, radius_increment=0.005):

    paths = []
    polygons_vertices_index = []
    vertices_radius = np.zeros(n_v) + init_radius

    for edge in e_list:
        pos_in_edge = pos[edge]
        if len(edge) == 2:
            vertices_index = np.array((0, 1), dtype=np.int64)
        else:
            hull = ConvexHull(pos_in_edge)
            vertices_index = hull.vertices

        n_vertices = vertices_index.shape[0]

        vertices_index = np.append(vertices_index, vertices_index[0]) # close the loop

        thetas = []

        for i in range(n_vertices):
            # line
            i1 = edge[vertices_index[i]]
            i2 = edge[vertices_index[i + 1]]

            r1 = vertices_radius[i1]
            r2 = vertices_radius[i2]

            p1 = pos[i1]
            p2 = pos[i2]

            dp = p2 - p1
            dp_len = vlen(dp)

            beta = radian_from_atan(dp[0], dp[1])
            alpha = common_tangent_radian(r1, r2, dp_len)

            theta = beta - alpha
            start_point = polar_position(r1, theta, p1)
            end_point = polar_position(r2, theta, p2)

            paths.append((start_point, end_point))
            thetas.append(theta)

        thetas.append(thetas[0])

        for i in range(n_vertices + 1):
            # arcs
            theta_1 = thetas[i - 1]
            theta_2 = thetas[i]

            arc_center = pos[edge[vertices_index[i]]]
            radius = vertices_radius[edge[vertices_index[i]]]

            paths.append((arc_center, theta_1, theta_2, radius))

        vertices_radius[edge] += radius_increment

        polygons_vertices_index.append(vertices_index.copy())

        paths.append('END')

    return paths, polygons_vertices_index

def _check_cover(points, polygons_vertices_index, e_list):
    """
    Check if the point is covered by any of the polygons.
    """
    n = points.shape[0]

    cover = np.zeros(n, dtype=np.bool)

    for edge in e_list:
        polygons_vertices_index_set = map(lambda x: set(x.tolist()), polygons_vertices_index)

    return False
