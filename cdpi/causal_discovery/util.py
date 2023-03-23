from .._pattern import pattern

from collections import deque
from itertools import combinations, chain
from collections import defaultdict

def identify_skeleton_from_empty_graph(self, data, test_kwarg):
    self.ptn = pattern()
    self.ptn.add_vertex(list(data.columns))

    self.p_independence_set = defaultdict(lambda: defaultdict(set))
    
    pairs = combinations(self.ptn.vertex, 2)
    for x, y in pairs:
        v_not_x_y = list(self.ptn.vertex - {x, y})
        power_set_of_v_not_x_y = chain(*[combinations(v_not_x_y, n) for n in range(len(v_not_x_y) + 1)])
        for subset in power_set_of_v_not_x_y:
            if self.test(data, {x}, {y}, set(subset), **test_kwarg):
                self.p_independence_set[x][y]
                self.p_independence_set[y][x] = self.p_independence_set[x][y]
                self.p_independence_set[x][y].add(subset)
                break

    self.identify_skeleton_by_ind(self.p_independence_set)

def identify_skeleton_by_ind(self, ind, vertex:set = None):
    self.ptn.add_vertex(list(ind.keys()))
    if vertex is not None: self.ptn.add_vertex(vertex)
    
    self.p_independence_set = ind
    pairs = combinations(self.ptn.vertex, 2)

    for x, y in pairs:
        if len(self.p_independence_set[x][y]) == 0:
            self.ptn.add_link(x, y)
    

def identify_v_structure_with_adjacency_orient_faithfulness(self):
    uncoupled_triple = deque()
    for x in self.ptn.link.keys():
        for z in self.ptn.link[x].keys():
            for y in self.ptn.link[z].keys():
                # Test x-z-y is uncoulped meeting
                if x != y and not self.ptn.is_adjacent(x, y): 
                    if all(z not in subset for subset in self.p_independence_set[x][y]) : uncoupled_triple.append((x, y, z))
    
    while uncoupled_triple:
        x, y, z = uncoupled_triple.popleft()
        #if Z not in every S in S[(X, Y)]:
        # orient X - Z - Y as X -> Z <- Y
        self.ptn.remove_links([(x,z), (y,z)])
        self.ptn.add_edges([(x,z), (y,z)])


def identify_meeks_rule_2(self):
    uncoupled_triple = deque()
    for x in self.ptn.child.keys():
        for z in self.ptn.child[x].keys():
            for y in self.ptn.link[z].keys():
                # Test x-z-y is uncoulped meeting
                if x != y and not self.ptn.is_adjacent(x, y): uncoupled_triple.append((x, y, z))

    if len(uncoupled_triple) == 0: return False

    while uncoupled_triple:
        x, y, z = uncoupled_triple.popleft()
        # X -> Z - Y is not v-structure, therefore 
        # orient Z - Y  as Z -> Y
        self.ptn.remove_links([(y,z)])
        self.ptn.add_edges([(z,y)])

    return True


def identify_meeks_rule_3(self):
    pairs = deque()
    for x in self.ptn.link.keys():
        for y in self.ptn.link[x].keys(): 
            if len(self.ptn.get_path(x, y, directed=True)) > 0: pairs.append((x, y))
    
    if len(pairs) == 0: return False

    while pairs:
        x, y = pairs.popleft()
        #Given graph G is DAG, therefore there is not cyclic path between X and Y
        # However, if Y -> X, then there is cyclic path : X -> ... -> Y -> X
            # thus orient X - Y as X -> Y
        self.ptn.remove_links([(x,y)])
        self.ptn.add_edges([(x,y)])
    
    return True


def identify_meeks_rule_4(self):
    pairs = deque()
    for w in self.ptn.parent.keys():
        # Find W which has more than two parents and vertex Z linked with
        if len(self.ptn.parent[w].keys()) >= 2 and w in self.ptn.link.keys():
            linked_with_w = set(self.ptn.link[w].keys())

            # Find pair of parents of W (x, y) such that x is not adjacent with y
            # X   Y
            #  \ /
            #   ><
            #   W
            parent_of_w = list(self.ptn.parent[w].keys())
            xy = combinations(parent_of_w, 2)

            for x, y in xy:
                if not self.ptn.is_adjacent(x, y):

                    # Find Z such that X - Z, Y - Z, and W - Z
                    linked_with_x = set(self.ptn.link[x].keys())
                    linked_with_y = set(self.ptn.link[y].keys())
                    linked_with_x_y_w = linked_with_w & linked_with_x & linked_with_y

                    for z in linked_with_x_y_w: pairs.append((z, w))
    
    if len(pairs) == 0: return False
    while pairs:
        z, w = pairs.popleft()
        # Now, we know that 
        # X - Z - Y
        #  \  |  /
        #   > W <
        # X - Z - Y is not v-structure -> Z is parent of X or Y
        # if Z <- W, there is cyclic path through X or Y 
        # thus orient Z - W as Z -> W

        self.ptn.remove_links([(z,w)])
        self.ptn.add_edges([(z,w)])

    return True


def identify_skeleton_from_full_link_graph(self, data, test_kwarg):
    self.ptn = pattern()
    self.ptn.add_vertex(list(data.columns))

    self.p_independence_set = defaultdict(lambda: defaultdict(set))

    # Lemma 1, Verma and Pearl, 1991, On the Equivalence of Causal Models
	# X and Y are adjacent 
	# <-> X and Y are not d-separated by any subset of PA_X or PA_Y

	# => X and Y are not adjacent 
	# <-> X and Y are d-separated by some subset of PA_X or PA_Y

	# therefore, we do not have to check d-separation for every possible subset S, 
    # only have to do for subsets of PA_X or PA_Y

    self.ptn.full_link()

    adj = {x : self.ptn.adjacent(x) for x in self.ptn.vertex}
    
    i = 0
    while any(i < len(adj[x]) for x in adj.keys()):
        for x in self.ptn.vertex:
            adj_x = adj[x]

            for y in adj_x:
                adj_x_not_y = list(adj_x - {y})
                power_set = combinations(adj_x_not_y, i)
                for subset in power_set:
                    if self.test(data, {x}, {y}, set(subset), **test_kwarg):
                        self.p_independence_set[x][y]
                        self.p_independence_set[y][x] = self.p_independence_set[x][y]
                        self.p_independence_set[x][y].add(subset)

                        self.ptn.remove_links([(x, y)])
                        break
            
            adj[x] = self.ptn.adjacent(x)

        i += 1

def identify_skeleton_from_full_link_graph_in_cpc(self, data, test_kwarg):
    self.ptn = pattern()
    self.ptn.add_vertex(list(data.columns))

    self.p_independence_set = defaultdict(lambda: defaultdict(set))

    # Lemma 1, Verma and Pearl, 1991, On the Equivalence of Causal Models
	# X and Y are adjacent 
	# <-> X and Y are not d-separated by any subset of PA_X or PA_Y

	# => X and Y are not adjacent 
	# <-> X and Y are d-separated by some subset of PA_X or PA_Y

	# therefore, we do not have to check d-separation for every possible subset S, 
    # only have to do for subsets of PA_X or PA_Y

    self.ptn.full_link()

    adj = {x : self.ptn.adjacent(x) for x in self.ptn.vertex}
    
    i = 0
    while any(i < len(adj[x]) for x in adj.keys()):
        for x in self.ptn.vertex:
            adj_x = adj[x]

            for y in adj_x:
                adj_x_not_y = list(adj_x - {y})
                power_set = combinations(adj_x_not_y, i)
                for subset in power_set:
                    if self.test(data, {x}, {y}, set(subset), **test_kwarg):
                        self.p_independence_set[x][y]
                        self.p_independence_set[y][x] = self.p_independence_set[x][y]
                        self.p_independence_set[x][y].add(subset)

                        self.ptn.remove_links([(x, y)])
            
            adj[x] = self.ptn.adjacent(x)

        i += 1

def identify_v_structure_with_adjacency_faithfulness(self):
    uncoupled_triple = deque()
    self.unfaithful_triple = set()
    for x in self.ptn.link.keys():
        for z in self.ptn.link[x].keys():
            for y in self.ptn.link[z].keys():
                # Test x-z-y is uncoulped meeting
                if x != y and not self.ptn.is_adjacent(x, y): 
                    if all(z not in subset for subset in self.p_independence_set[x][y]) : uncoupled_triple.append((x, y, z))
                    elif all(z in subset for subset in self.p_independence_set[x][y]) : continue
                    else: self.unfaithful_triple.add((x,z,y))
                    
    while uncoupled_triple:
        x, y, z = uncoupled_triple.popleft()
        #if Z not in every S in S[(X, Y)]:
        # orient X - Z - Y as X -> Z <- Y
        self.ptn.remove_links([(x,z), (y,z)])
        self.ptn.add_edges([(x,z), (y,z)])

def identify_meeks_rule_2_in_cpc(self):
    uncoupled_triple = deque()
    for x in self.ptn.child.keys():
        for z in self.ptn.child[x].keys():
            for y in self.ptn.link[z].keys():
                # Check whether the triple x->z-y is unfaithful or not
                # If unfaithful, pass
                if (x,z,y) in self.unfaithful_triple : continue
                
                # Test x->z-y is uncoulped meeting
                if x != y and not self.ptn.is_adjacent(x, y): uncoupled_triple.append((x, y, z))

    if len(uncoupled_triple) == 0: return False

    while uncoupled_triple:
        x, y, z = uncoupled_triple.popleft()
        # X -> Z - Y is not v-structure, therefore 
        # orient Z - Y  as Z -> Y
        self.ptn.remove_links([(y,z)])
        self.ptn.add_edges([(z,y)])

    return True

def identify_meeks_rule_4_in_cpc(self):
    pairs = deque()
    for w in self.ptn.parent.keys():
        # Find W which has more than two parents and vertex Z linked with
        if len(self.ptn.parent[w].keys()) >= 2 and w in self.ptn.link.keys():
            linked_with_w = set(self.ptn.link[w].keys())

            # Find pair of parents of W (x, y) such that x is not adjacent with y
            # X   Y
            #  \ /
            #   ><
            #   W
            parent_of_w = list(self.ptn.parent[w].keys())
            xy = combinations(parent_of_w, 2)

            for x, y in xy:
                if not self.ptn.is_adjacent(x, y):

                    # Find Z such that X - Z, Y - Z, and W - Z
                    linked_with_x = set(self.ptn.link[x].keys())
                    linked_with_y = set(self.ptn.link[y].keys())
                    linked_with_x_y_w = linked_with_w & linked_with_x & linked_with_y
                    
                    for z in linked_with_x_y_w: 
                        # Check whether the triple x-z-y is unfaithful or not
                        # If unfaithful, pass
                        if (x,z,y) in self.unfaithful_triple : continue
                        pairs.append((z, w))
    
    if len(pairs) == 0: return False
    while pairs:
        z, w = pairs.popleft()
        # Now, we know that 
        # X - Z - Y
        #  \  |  /
        #   > W <
        # X - Z - Y is not v-structure -> Z is parent of X or Y
        # if Z <- W, there is cyclic path through X or Y 
        # thus orient Z - W as Z -> W

        self.ptn.remove_links([(z,w)])
        self.ptn.add_edges([(z,w)])

    return True