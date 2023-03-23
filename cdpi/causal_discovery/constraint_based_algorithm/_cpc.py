import pandas as pd

from ..._pattern import pattern
from ..util import ( identify_skeleton_from_full_link_graph_in_cpc,
                     identify_skeleton_by_ind,
                     identify_v_structure_with_adjacency_faithfulness,
                     identify_meeks_rule_2_in_cpc,
                     identify_meeks_rule_3,
                     identify_meeks_rule_4_in_cpc )

from ..test import get_test

class cpc:
    def __init__(self):
        self.ptn = pattern()
    
    def identify(self, data:pd.DataFrame = None, test:str = None, ind:dict = None, vertex = None, **test_kwarg) -> pattern: 
        # STEP 0 ~ 1 : Find skeleton
        if ind is not None:
            self.identify_skeleton_by_ind(ind, vertex)
        elif data is not None and test is not None:
            self.test = get_test(test)
            self.identify_skeleton_from_full_link_graph_in_cpc(data, test_kwarg = test_kwarg)
        else:
            print("cpc.identify : both ind and (data, test) are None!")


        # # STEP 2 : Find v-structure and unfaithful triple
        self.identify_v_structure_with_adjacency_faithfulness()

        # STEP 3~5 : use Meek's rules
        cnt = True
        while cnt:
            cnt2 = self.identify_meeks_rule_2_in_cpc()
            # STEP 3 is not related with orient faithfulness assumption.
            # Because it uses only the definition of DAG
            cnt3 = self.identify_meeks_rule_3() 
            cnt4 = self.identify_meeks_rule_4_in_cpc()

            cnt = cnt2 or cnt3 or cnt4 # Check there are vertexs which could be changed

        return self.ptn
    
    def draw(self, **draw_kwarg):
        self.ptn.draw(**draw_kwarg)
        pos = self.ptn.pos
        self.draw_unfaithful_triple(pos)
    
    def draw_by_pos(self, pos):
        self.ptn.draw_by_pos(pos)
        self.draw_unfaithful_triple(pos)
        
    def draw_unfaithful_triple(self, pos):
        for triple in self.unfaithful_triple:
            x, z, y = triple
            
            delta = pos[x] - pos[y]
            l = np.linalg.norm(delta) * 30 / 100
            unit = delta/np.linalg.norm(delta)

            cent = (pos[x] + pos[y]) / 2
            cent = 3 * pos[z]/4 + cent/4
            x, y = cent - unit * l / 2
            dx, dy = unit * l
            plt.arrow(x, y, dx, dy, width = 0.05, color = 'gray', linestyle = '-.')

        
cpc.identify_skeleton_from_full_link_graph_in_cpc = identify_skeleton_from_full_link_graph_in_cpc
cpc.identify_v_structure_with_adjacency_faithfulness = identify_v_structure_with_adjacency_faithfulness
cpc.identify_meeks_rule_2_in_cpc = identify_meeks_rule_2_in_cpc
cpc.identify_meeks_rule_3 = identify_meeks_rule_3
cpc.identify_meeks_rule_4_in_cpc = identify_meeks_rule_4_in_cpc
cpc.identify_skeleton_by_ind = identify_skeleton_by_ind
