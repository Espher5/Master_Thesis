from pymoo.model.duplicate import ElementwiseDuplicateElimination


class CpsDuplicatesElimination(ElementwiseDuplicateElimination):
    """
    Class that removes identical individuals in the population
    """
    def is_equal(self, a, b):
        return a.X[0].states == b.X[0].states
