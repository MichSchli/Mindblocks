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

manifest = {'views': ['experiment'], 'languages': ['python', 'theano'], 'name': 'Constant', 'file_path': 'components.basic.constant'}
Constant_3 = Constant(manifest=manifest)
graph.merge(Constant_3.get_graph())
Constant_3.attributes = {'value': '27'}
Constant_3_Output = Constant_3.edges_out[0].destination
subgraph = Graph()
manifest = {'views': ['agent'], 'languages': ['theano'], 'name': 'TensorInput', 'file_path': 'components.agent_io.tensor_input'}
TensorInput_0 = TensorInput(manifest=manifest)
subgraph.merge(TensorInput_0.get_graph())
TensorInput_0.attributes = {'dimension': '1'}
TensorInput_0_Output = TensorInput_0.edges_out[0].destination
manifest = {'views': ['agent'], 'languages': ['theano'], 'name': 'TensorOutput', 'file_path': 'components.agent_io.tensor_output'}
TensorOutput_2 = TensorOutput(manifest=manifest)
subgraph.merge(TensorOutput_2.get_graph())
TensorOutput_2_Input = TensorOutput_2.edges_in[0].origin
subgraph.add_edge(TensorInput_0_Output, TensorOutput_2_Input)
manifest = {'languages': ['python'], 'name': 'SubgraphComponent', 'file_path': 'components.graph.subgraph_component'}
SubgraphComponent_0 = SubgraphComponent(subgraph, manifest=manifest)
graph.merge(SubgraphComponent_0.get_graph())
SubgraphComponent_0_Input_0 = SubgraphComponent_0.edges_in[0].origin
SubgraphComponent_0_Output_0 = SubgraphComponent_0.edges_out[0].destination
graph.add_edge(Constant_3_Output, SubgraphComponent_0_Input_0)
manifest = {'views': ['experiment'], 'languages': ['python'], 'name': 'ConsolePrinter', 'file_path': 'components.experiment_io.console_printer'}
ConsolePrinter_6 = ConsolePrinter(manifest=manifest)
graph.merge(ConsolePrinter_6.get_graph())
ConsolePrinter_6_Input = ConsolePrinter_6.edges_in[0].origin
graph.add_edge(SubgraphComponent_0_Output_0, ConsolePrinter_6_Input)

#=================================
# Run:
#=================================

runner = GraphRunner()
runner.run(graph)
