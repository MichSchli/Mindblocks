import numpy as np

from model.component.component_model import ComponentModel


class SGD(ComponentModel):

    name='SGD'
    default_in_sockets = [{'position': [0, 20],
                 'name': 'Gradient'}]
    attributes = {'learning rate': '0.1'}

    def parse_float(self, string):
        return np.fromstring(string, sep=' ', dtype=np.float32)

    def parse_attributes(self):
        d = {'learning_rate': self.parse_float(self.attributes['learning rate'])}

        for k in d:
            if d[k] is None:
                return False

        self.parsed_attributes = d

        return True

    def theano_updates(self):
        trainables = self.get_upstream_trainables()
        gradients = self.pull_by_index(0)

        updates = [None]*len(trainables)

        for i in range(len(trainables)):
            updates[i] = (trainables[i], trainables[i]-self.parsed_attributes['learning_rate']*gradients[i])

        return updates

