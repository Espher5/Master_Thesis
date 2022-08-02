

class RoadGenerator:

    def __init__(self, map_size, min_len, max_len, min_angle, max_angle):
        self._file = 'roads.json'
        self._init_file = 'init.json'
        self._points_file = 'points.json'
        self._road_points = []
        self._init_states = ['straight', 'left', 'right']

        self._map_size = map_size
        self._min_len = min_len
        self._max_len = max_len
        self._min_angle = min_angle
        self._max_angle = max_angle

        self._transition_names = [
            ['SS', 'SL', 'SR'],
            ['LS', 'LL', 'LR'],
            ['RS', 'RL', 'RR']
        ]

        self._transition_probs = [
            [0.1, 0.45, 0.45],
            [0.2, 0.4, 0.4],
            [0.2, 0.4, 0.4]
        ]


    def generate_test_case(self):
        