from deap_tests.core.Config import Config


class Individual:
    def __init__(self, config: Config):
        self._config = config

    def clone(self) -> 'creator.base':
        raise NotImplemented()

    def evaluate(self):
        raise NotImplemented()

    def mutate(self):
        raise NotImplemented()