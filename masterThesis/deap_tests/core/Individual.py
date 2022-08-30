from deap_tests.core.Config import Config


class Individual:
    def __init__(self, config: Config):
        self._config = config

    def clone(self) -> 'creator.base':
        raise NotImplemented()

    def evaluate(self):
        raise NotImplemented()

    def penalty_function(self):
        raise NotImplemented()

    def mate(self, other: 'Individual'):
        raise NotImplemented()

    def mutate(self, prob=0.4):
        raise NotImplemented()

    @staticmethod
    def calc_novelty(old, new):
        raise NotImplemented()
