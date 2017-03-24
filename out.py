#=================================
# Imports:
#=================================

from graph.graph import Graph
from compilation.graph_runner import GraphRunner
from components.basic.constant import Constant
from components.graph.subgraph_component import SubgraphComponent
from graph.graph import Graph
from compilation.graph_runner import GraphRunner
from components.agent_io.tensor_input import TensorInput
from components.agent_io.tensor_output import TensorOutput
from components.experiment_io.console_printer import ConsolePrinter

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
