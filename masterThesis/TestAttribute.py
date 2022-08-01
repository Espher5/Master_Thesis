import random
from MarkovChain import MarkovChain


class TestAttribute:
    def __init__(self, attribute):
        self._name = attribute['name']
        self._type = attribute['type']

        if attribute['type'] == 'string':
            self._values = list(attribute['values'])
        else:
            self._min = attribute['values']['min']
            self._max = attribute['values']['max']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def generate_random_value(self):
        value = None
        if self._type == 'string':
            i = random.randrange(0, len(self._values))
            value = self._values[i]
        else:
            value = random.randrange(self._min, self._max)

        return value
