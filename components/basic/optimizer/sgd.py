import numpy as np

import theano

from components.component import Component


class SGD(Component):

    name='SGD'
    links_in = [{'name': 'Gradient'}]

    def copy(self, identifier=None):
        return SGD(identifier=identifier)