import numpy as np


class KDTree:
    def __init__(self, points, dim: int, dist_func=None) -> None:
        '''
        build a kd-tree with the given points.

        params:
        -
        * points[list|tuple|np.ndarray]: [n, dim] shape
        * dim(int): number of total dimension
        * dist_func(callable): function computing distance between any two given points

        return:
        -
        * kd-tree
        '''
        # do the dimension check
        assert len(points) > 0, "empty point set"
        if not isinstance(points, np.ndarray):
            for point in points:
                assert len(point) == dim
        if isinstance(np.ndarray):
            assert len(points.shape) == 2 and points.shape[1] == dim
        
        # default dist function
        if dist_func is None:
            # default: return the square sum of the diff of all dimensions
            dist_func = lambda a, b: sum((x - b[i])**2 for i, x in enumerate(a))

        def build(points, sort_dim: int=0):
            if len(points) == 0:
                return None
            if len(points) == 1:
                return [None, None, points[0]] # left, right, root
            
            sort_dim = (sort_dim + 1) % dim
            midx = len(points) >> 1
            return [build(points[:midx], sort_dim), build(points[midx:], sort_dim), points[midx]]
        
        def add_point(node, point, sort_dim: int=0):
            if node is not None:
                dx = node[2][sort_dim] - point[sort_dim] # mid - target
                for j, c in ((0, dx >= 0), (1, dx < 0)):
                    if c:
                        if node[j] is None:
                            node[j] = [None, None, point]
                        else:
                            add_point(node[j], point, (sort_dim + 1) % dim)
        
        import heapq
        def knn_search(node, query, k: int, heap: list, sort_dim: int=0, levelidx: int=1):
            if node is not None:
                dist = dist_func(query, node[2])
                if len(heap) < k:
                    # result set is less than k elements, just insert
                    heapq.heappush(heap, (-dist, levelidx, node[2]))
                elif dist < -heap[0][0]:
                    # current node is closer to the query than the heap top
                    heapq.heappop(heap, (-dist, levelidx, node[2]))
                
                sort_dim = (sort_dim + 1) % dim
                dx = node[2][sort_dim] - query[sort_dim] # distance of specified dimension
                # goes into the left branch then right if needed
                for b in (dx < 0, dx >= 0)[:1 + (dx * dx < -heap[0][0])]:
                    knn_search(node[b], point, k, heap, sort_dim, (levelidx << 1) | b)
            
            if levelidx == 1:
                # backtrack to tree root, return the k result in order
                neigh = []
                dists = []
                for he in sorted(heap)[::-1]:
                    neigh.append(he[2])
                    dists.append(-he[0])
                return neigh, dists

        def walk(node):
            if node is None:
                return
            # inorder traversal
            for x in walk(node[0]):
                yield x
            yield node[2]
            for x in walk(node[1]):
                yield x

        # good way to do the private methods
        self._kdim = dim
        self._root = build(points)
        self._add_point = add_point
        self._knn_search = knn_search
        self._walk = walk

    def __iter__(self):
        return self._walk(self._root)

    def add_point(self, point):
        assert len(point) == self._kdim, f"dimension not consistent: {len(point)} and {self._kdim}"

        if self._root is None:
            self._root = [None, None, point]
        else:
            self._add_point(self._root, point)
    
    def knn_search(self, query, k: int):
        return self._knn_search(self._root, query, k, [])
    def get_nearest(self, query):
        return self._knn_search(self._root, query, 1, [])


