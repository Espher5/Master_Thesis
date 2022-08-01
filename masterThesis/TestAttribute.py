class TestAttribute:
    def __init__(self):
        self._name = ''
        self._type = ''
        self._min = 0
        self._max = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def generate_random_value(self):
        pass
