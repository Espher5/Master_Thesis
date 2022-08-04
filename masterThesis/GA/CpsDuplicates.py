from pymoo.core.duplicate import ElementwiseDuplicateElimination


class CpsDuplicates(ElementwiseDuplicateElimination):
    def is_equal(self, a, b):
        return a.X[0].states == b.X[0].states
