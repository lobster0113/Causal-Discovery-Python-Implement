from collections import deque
from itertools import combinations, chain
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

class pattern:
    def __init__(self, vertex = None, edges = None, links = None):
        self.vertex = set()
        self.parent = dict()
        self.child = dict()
        self.link = dict()

        self.link_count = 0

        self.add_vertex(vertex)
        self.add_edges(edges)
        self.add_links(links)

        self.d_separation_set = defaultdict(lambda: defaultdict(set))
    
    def add_vertex(self, vertex) -> None:
        if vertex: 
            for v in vertex:
                if v not in self.vertex:
                    self.vertex.add(v)
                    self.parent[v] = dict()
                    self.child[v] = dict()
                    self.link[v] = dict()


    def remove_vertex(self, vertex) -> None:
        for v in vertex:
            self.vertex.remove(v)

            for p in self.parent[v].keys():
                self.child[p].pop(v, None)
            
            for c in self.child[v].keys():
                self.parent[c].pop(v, None)
            
            for l in self.link[v].keys():
                self.remove_links((l,v))
            
            self.parent.pop(v, None)
            self.child.pop(v, None)
            self.link.pop(v, None)

    def add_edge(self, v1,  v2, **attribute)->None:
        self.add_vertex([v1, v2])

        self.parent[v2][v1] = attribute
        self.child[v1][v2] = attribute


    def add_edges(self, edges) -> None:
        if edges:
            for e in edges:
                if isinstance(e, dict):
                    v1 = e['v1']; v2 = e['v2']
                    del e['v1']; del e['v2']
                    self.add_edge(v1, v2, **e)
                elif len(e) == 2:
                    self.add_edge(*e)
                else:
                    arg = dict()
                    i = 0
                    for attr in e[2:]:
                        arg[f'A{i}'] = attr
                        i += 1
                    self.add_edge(e[0], e[1], **arg)


    def remove_edges(self, edges) -> None:
        for e in edges:
            pa, ch = e
            del self.parent[ch][pa]
            del self.child[pa][ch]

            exist1 = self.parent[ch].pop(pa, None)
            exist2 = self.child[pa].pop(ch, None)

            if exist1 is not None and exist2 is not None: continue
            elif not (exist1 is None and exist2 is None):
                print(f'remove_edges : the edge between {pa} and {ch} is not matched with self.parent and self.child!')

    def add_link(self, v1, v2, **attribute) -> None:
        self.add_vertex([v1, v2])

        self.link[v1][v2] = attribute
        self.link[v2][v1] = attribute
        
        self.link_count += 1

    def add_links(self, links) -> None:
        if links:
            for l in links:
                if isinstance(l, dict):
                    v1 = l['v1']; v2 = l['v2']
                    del l['v1']; del l['v2']
                    self.add_link(v1, v2, **l)
                elif len(l) == 2:
                    self.add_link(*l)
                else:
                    arg = dict()
                    i = 0
                    for attr in l[2:]:
                        arg[f'A{i}'] = attr
                        i += 1
                    self.add_link(l[0], l[1], **arg)

    def remove_links(self, links) -> None:
        for l in links:
            v1, v2 = l

            exist1 = self.link[v1].pop(v2, None)
            exist2 = self.link[v2].pop(v1, None)

            if exist1 is not None and exist2 is not None:
                self.link_count -= 1
            elif not (exist1 is None and exist2 is None):
                print(f'remove_links : there are unsymmetric links between {v1} and {v2}!')
            
    def is_adjacent(self, v1, v2):
        return v1 in self.link[v2].keys() or v1 in self.child[v2].keys() or v1 in self.parent[v2].keys() 

    def adjacent(self, v1):
        return {v2 for v2 in (self.vertex - {v1}) if self.is_adjacent(v1, v2)}

    def get_ancestor(self, vertex) -> set:
        visited = {v:0 for v in self.vertex}
        visited[vertex] = 1
        result = set()

        queue = deque([vertex])

        while queue:
            v = queue.popleft()
            for v1 in self.parent[v].keys():
                if not visited[v1]:
                    visited[v1] = 1
                    result.add(v1)
                    queue.append(v1)
        
        return result

    def get_descendant(self, vertex) -> set:
        visited = {v:0 for v in self.vertex}
        visited[vertex] = 1
        result = set()

        queue = deque([vertex])

        while queue:
            v = queue.popleft()
            for v1 in self.child[v].keys():
                if not visited[v1]:
                    visited[v1] = 1
                    result.add(v1)
                    queue.append(v1)
        
        return result

    def get_path(self, source, target, directed = True):
        return self.get_path_(source, target, directed=directed)
    
    def get_path_(self, v1, v2, trace = None, initial = True, directed = True):
        if initial:
            self.visited = {v:0 for v in self.vertex}
            self.visited[v1] = 1
            self.result = []
            trace = [v1]
        
        for v in self.child[v1].keys():
            if v == v2:
                self.result.append(trace + [v2])
            else:
                if not self.visited[v]:
                    new_trace = trace + [v]
                    self.visited[v] = 1
                    self.get_path_(v, v2, new_trace, False, directed)
                    self.visited[v] = 0
        
        if not directed:
            for v in self.parent[v1].keys():
                if v == v2:
                    self.result.append(trace + [v2])
                else:
                    if not self.visited[v]:
                        new_trace = trace + [v]
                        self.visited[v] = 1
                        self.get_path_(v, v2, new_trace, False, directed)
                        self.visited[v] = 0

            for v in self.link[v1].keys():
                if v == v2:
                    self.result.append(trace + [v2])
                else:
                    if not self.visited[v]:
                        new_trace = trace + [v]
                        self.visited[v] = 1
                        self.get_path_(v, v2, new_trace, False, directed)
                        self.visited[v] = 0
        
        return self.result #2d list  
    
    def is_cyclic(self) -> bool:
        # Code Resource : https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
        visited = {v:0 for v in self.vertex}
        recStack =  {v:0 for v in self.vertex}

        for v in self.vertex:
            if not visited[v]:
                if self.is_cyclic_util(v, visited, recStack): return True
        
        return False
        
    
    def is_cyclic_util(self, v, visited, recStack) -> bool:
        visited[v] = 1
        recStack[v] = 1

        for ch in self.child[v].keys():
            if not visited[ch]:
                if self.is_cyclic_util(ch, visited, recStack):
                    return True
            elif recStack[ch]:
                return True
        
        recStack[v] = 0
        return False

    def get_d_separation(self, X, Z) -> set:
        # Test X and Z are disjoint
        if X & Z:
            print('get_d_separation : given two vertex sets are not disjoint!')
            return

        # 1) make descendent list 
        descendent = {v:0 for v in self.vertex}
        for i in self.vertex:
            descendent_of_i = self.get_descendant(i)
            if descendent_of_i&Z or i in Z:
                descendent[i] = 1
        
        # 2) make undirected version of this DAG
        sym_graph = {v: [] for v in self.vertex}
        for pa in list(self.child.keys()) + list(self.link.keys()):
            for ch in self.child[pa].keys():
                sym_graph[pa].append([ch, 0]) # [vertex, label]
                sym_graph[ch].append([pa, 0])

            for ch in self.link[pa].keys():
                sym_graph[pa].append([ch, 0])
        
        # 3) for each x in X, find vertex v such that v and x are d-separated by Z 
        # ez explanation  1) do BFS from 's' in undirected graph we create above
        #                 2) whenever you meet another vertex v in V/X, 
        #                    check the trail 'previous-current-v' is 'active' or not
        #                 3) If the trail is active, v and x are not d-separated by Z.
        #                    Save this fact and append edges v ->its neiborhood to queue
        #                 4) If the trail is not active, stop searching along the trail
        reachable = set()
        queue = deque()
        for v in X:
            queue.append(('', v))
        
        while queue:
            #v1 -> v2
            v1, v2 = queue.popleft()

            for i, v3 in enumerate(sym_graph[v2]):
                v3, label = v3
                if not label and v1 != v3:
                    # test whether the trail 'v1-v2-v3' is active
                    # first, check : given triple (v1, v2, v3) are v-structure & descendent[v2] = 1
                    if v1 in self.parent[v2].keys() and v3 in self.parent[v2].keys(): 
                        if descendent[v2]:
                            reachable.add(v3)
                            sym_graph[v2][i][1] = 1 # labeling
                            queue.append((v2, v3))

                    # second, check : given triple (v1, v2, v3) are NOT v-structure & v2 NOT in Z
                    elif v2 not in Z:
                        reachable.add(v3)
                        sym_graph[v2][i][1] = 1 # labeling
                        queue.append((v2, v3))

        Ys = self.vertex - (reachable|X|Z)

        return (X, Ys, Z)

    def d_separated(self, X, Y, Z) -> bool:
        # Warning : This method is terribly inefficient
        return Y <= self.get_d_separation(X, Z)[1]
    
    def full_link(self):
        temp_vertex = list(self.vertex)
        for i, v1 in enumerate(temp_vertex[:-1]):
            for v2 in temp_vertex[i + 1 :]:
                self.add_link(v1, v2)

    def add_d_separations(self, d_separation_set):
        for ds in d_separation_set:
            x, y, z = ds
            x, y= x.pop(), y.pop()
            z = tuple(z)

            self.d_separation_set[x][y]
            self.d_separation_set[y][x] = self.d_separation_set[x][y]
            self.d_separation_set[x][y].add(z)
    
    def get_all_d_separation(self) -> dict:
        pairs = combinations(self.vertex, 2)
        for x, _ in pairs:
            v_not_x_and_some_v = list(self.vertex - {x, _})
            power_set = chain(*[combinations(v_not_x_and_some_v, n) for n in range(len(v_not_x_and_some_v))])

            for z in power_set:
                z = set(z)
                ys = self.get_d_separation({x}, z)[1]
                if len(ys) > 0:
                    for y in ys:
                        self.add_d_separations([({x}, {y}, z)])

        return self.d_separation_set.copy()
    
    
    def draw(self, **draw_kwarg):
        max_int =  int(np.sqrt(2 * len(self.vertex))) + 1
        loc = list(combinations(list(range(max_int + 1)), 2))
        vertices = list(self.vertex)

        pos = dict()
        for i, v in enumerate(vertices):
          pos[v] = np.array(loc[i]).astype('float64')

        pos = self.force_directed_algorithm(pos, **draw_kwarg)
        self.draw_by_pos(pos)

    def force_directed_algorithm(self, pos, iterations:int = 100, t = 1, ideal_length = 1, c_rep = 2, c_spr = 1):
        # The formula is from https://www.youtube.com/watch?v=WWm-g2nLHds
        
        for i in range(iterations):
            # Calculate repulsion force
            repulsion = {vertex: np.zeros(2) for vertex in self.vertex}
            for u, v in combinations(self.vertex, 2):
                delta = pos[u] - pos[v]
                dist = np.sqrt(delta.dot(delta))
                if dist > 0:
                    rep = delta * c_rep / dist**3
                    repulsion[u] += rep
                    repulsion[v] -= rep
            
            # Calculate attraction force
            attraction = {vertex: np.zeros(2) for vertex in self.vertex}
            for u in self.vertex:
                for v in list(self.child[u].keys()) + list(self.link[u].keys()):
                    delta = pos[u] - pos[v]
                    dist = np.sqrt(delta.dot(delta))
                    if dist > 0:
                        attr = c_spr * delta * np.log(dist/ideal_length)/dist - delta * c_rep / dist**3
                        attraction[u] -= attr
                        attraction[v] += attr
                    
            
            # Calculate total force
            force = {vertex: attraction[vertex] + repulsion[vertex] for vertex in self.vertex}
            
            # Update vertex pos
            for vertex in self.vertex:
                delta = force[vertex]
                dist = np.sqrt(delta.dot(delta))
                pos[vertex] += delta * min(dist, t) / dist
            
            t *= (1 - i / iterations)
        
        return pos
    
    def draw_by_pos(self, pos):
        fig, ax = plt.subplots()

        for pa in self.child.keys():
            for ch in self.child[pa].keys():
                x, y = pos[pa]
                dx, dy = (pos[ch] - pos[pa])/10 * 8
                plt.arrow(x, y, dx, dy, length_includes_head = True, width = 0.1, color = 'black')
        
        pairs = combinations(list(self.link.keys()), 2)
        for v1 in self.link.keys():
            for v2 in self.link[v1].keys():
                x, y = pos[v1]
                dx, dy = pos[v2] - pos[v1]
                plt.arrow(x, y, dx, dy, width = 0.1, color = 'black')
        
        for v, p in pos.items():
            ax.add_patch(plt.Circle(p, 0.5, color = 'lightsteelblue'))
            if len(v) == 1:plt.text(p[0], p[1], v, fontsize = 16, ha='center', va='center')
            else : plt.text(p[0], p[1], v, fontsize = 12, ha='center', va='center')

        self.pos = pos
