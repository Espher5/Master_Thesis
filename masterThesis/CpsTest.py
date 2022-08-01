import json
import random
from TestAttribute import TestAttribute


class CpsTest:
    def __init__(self, filename):
        self._filename = filename
        self._test_case = dict()

        with open(self._filename) as f:
            data = json.load(f)
            self._environments = data['environments']

            self._attributes = list()
            for attr in data['attributes']:
                self._attributes.append(TestAttribute(attr))


    @property
    def attributes(self):
        return self._attributes

    @property
    def environments(self):
        return self._environments

    @property
    def test_case(self):
        return self._test_case


    def generate_attribute_values(self):
        p = random.uniform(0, 1)


    def build_test_matrix(self):
        for i in range(self._environments):
            attr_dict = dict()

            for attr in self._attributes:

                attr_dict.update({attr.name: attr.generate_random_value()})

            self._test_case.update({
                i: attr_dict
            })


if __name__ == '__main__':
    test = CpsTest('test.json')
    test.build_test_matrix()
    res = test.test_case
    for key in res:
        print(res[key])

