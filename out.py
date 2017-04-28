#=================================
# Imports:
#=================================

from graph.graph import Graph
from compilation.graph_runner import GraphRunner
from components.basic.constant import Constant
from components.experiment_io.console_printer import ConsolePrinter

#=================================
# Arguments:
#=================================


#=================================
# Code:
#=================================

graph = Graph()

manifest = {'name': 'Constant', 'languages': ['theano', 'python'], 'views': ['agent', 'experiment'], 'file_path': 'components.basic.constant'}
Constant_0 = Constant(manifest=manifest)
graph.merge(Constant_0.get_graph())
