import json
from TestAttribute import TestAttribute


class CpsTest:
    def __init__(self, filename):
        self._filename = filename

        self._attributes = list()
        self._environments = list()
        self._markov_chain = dict()
        self._test_case = dict()

    @property
    def attributes(self):
        return self._attributes

    @property
    def environments(self):
        return self._environments

    @property
    def test_case(self):
        return self._test_case

    def load_attributes(self):
        with open(self._filename) as f:
            attributes = json.load(f)
            for a in attributes:
                attribute = TestAttribute(a)
                self._attributes.append(attribute)






    def add_attribute(self, attribute):
        self._attributes.append(attribute)

    def add_environment(self, environment):
        self._environments.append(environment)

    def build_test_matrix(self):
        key = 0
        for env in self._environments:
            attr_dict = dict()
            for attr in self._attributes:
                attr_dict.update({attr: 0})

            self._test_case.update({
                key: attr_dict
            })
            key += 1



if __name__ == '__main__':
    test = CpsTest('test.json')
    test.load_attributes()

