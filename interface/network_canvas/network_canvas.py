from components.basic.network.sigmoid import Sigmoid
from components.basic.network.trainable_parameter import TrainableParameter
from components.basic.optimizer.sgd import SGD
from interface.drawable_canvas import DrawableCanvas
from components.basic.network.dot_product import Dot
from components.basic.network.constant import Constant
from components.basic.network.output import Output
from components.basic.network.allgradients import AllGradients


class NetworkCanvas(DrawableCanvas):

    available_components = [Constant(create_graph=False),
                            Output(create_graph=False),
                            Dot(create_graph=False),
                            Sigmoid(create_graph=False),
                            TrainableParameter(create_graph=False),
                            AllGradients(create_graph=False),
                            SGD(create_graph=False)]
