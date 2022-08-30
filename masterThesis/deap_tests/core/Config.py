import time


class Config:
    GA = {
        "population": 100,
        "n_gen": 75,
        "mutation_rate": 0.4,
        "crossover_rate": 1
    }

    MODEL = {
        "speed": 9,         # Parameter for the simplified car model
        "map_size": 200,
        "steer_ang": 12,    # Parameter for the simplified car model
        "min_len": 5,       # Minimal possible distance in meters
        "max_len": 30,      # Maximal possible distance to go straight in meters
        "min_angle": 10,    # Minimal angle of rotation in degrees
        "max_angle": 85,    # Maximal angle of rotation in degrees
    }

    FILES = {
        "ga_archive": ".\\GA_archive\\",
        "tc_img": ".\\TC_img\\",
        "tc_file": ".\\TC_file\\",
    }

    def __init__(self):
        self._fitness_weights = (-1.0, )

    @property
    def fitness_weights(self):
        return self._fitness_weights

    @staticmethod
    def get_seed():
        t = int(time.time() * 1000)
        seed = (
                ((t & 0xFF000000) >> 24)
                + ((t & 0x00FF0000) >> 8)
                + ((t & 0x0000FF00) << 8)
                + ((t & 0x000000FF) << 24)
        )

        return seed
