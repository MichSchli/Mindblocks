from interface.drawable_canvas import DrawableCanvas
from components.basic.network.dot_product import Dot
from components.basic.network.constant import Constant
from components.basic.network.output import Output


class NetworkCanvas(DrawableCanvas):

    available_components = [Constant(create_graph=False), Output(create_graph=False), Dot(create_graph=False)]
