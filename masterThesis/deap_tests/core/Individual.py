class Individual:
    def clone(self) -> 'creator.base':
        raise NotImplemented()

    def evaluate(self):
        raise NotImplemented()

    def mutate(self):
        raise NotImplemented()