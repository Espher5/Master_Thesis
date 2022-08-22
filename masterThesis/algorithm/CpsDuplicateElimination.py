from pymoo.model.duplicate import ElementwiseDuplicateElimination


class CpsDuplicateElimination(ElementwiseDuplicateElimination):
    """
    Class for removing identical individuals in the population
    """

    def is_equal(self, a, b):
        return a.X[0].states == b.X[0].states
