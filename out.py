#=================================
# Imports:
#=================================

from components.basic.constant import Constant
from graph.graph import Graph

#=================================
# Arguments:
#=================================


#=================================
# Code:
#=================================

graph = Graph()

manifest = {'file_path': 'components.basic.constant', 'name': 'Constant', 'languages': ['python', 'theano'], 'views': ['experiment']}
Constant_0 = Constant(manifest=manifest)
graph.merge(Constant_0.get_graph())
Constant_0.attributes = {'value': '0'}
