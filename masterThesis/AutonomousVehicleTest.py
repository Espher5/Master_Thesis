import random


class AutonomousVehicleTest:
    def __init__(self):
        self._environment_count = 5
        self._environments = dict()

        self._attributes = {
            'road_segment_type': {
                'values': ['straight', 'turn_left', 'turn_right'],
                'min_value': None,
                'max_value': None,
                'transition_matrix': [
                    [0.1, 0.45, 0.45],
                    [0.2, 0.4, 0.4],
                    [0.2, 0.4, 0.4]
                ]
            },
            'straight_road_length': {
                'values': None,
                'min_value': 5,
                'max_value': 50,
                'transition_matrix': None
            },
            'road_turn_angle': {
                'values': None,
                'min_value': 5,
                'max_value': 50,
                'transition_matrix': None
            }
        }

        self._test_case = None

    @property
    def test_case(self):
        return self._test_case

    def generate_environments(self):
        for i in range(self._environment_count):
            attributes = dict()

            for attribute in self._attributes:
                if self._attributes[attribute]['transition_matrix'] is not None:
                    if len(self._environments) == 0:
                        value = random.choice(self._attributes[attribute]['values'])
                    else:
                        prev_env = self._environments[max(0, i - 1)]
                        prev_value = prev_env[attribute]
                        prev_index = self._attributes[attribute]['values'].index(prev_value)
                        table_line = self._attributes[attribute]['transition_matrix'][prev_index]

                        p = random.uniform(0, 1)
                        if p < table_line[0]:
                            value = self._attributes[attribute]['values'][0]
                        elif table_line[0] <= p < table_line[0] + table_line[1]:
                            value = self._attributes[attribute]['values'][1]
                        else:
                            value = self._attributes[attribute]['values'][2]
                else:
                    value = 0


                attributes.update({
                    attribute: value
                })

            self._environments.update({i: attributes})

        for key in self._environments.keys():
            print(self._environments[key])


if __name__ == '__main__':
    test = AutonomousVehicleTest()
    test.generate_environments()


