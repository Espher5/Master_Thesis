class MarkovChain:


    def __init__(self):
        self._states = list()
        self._transitions = list()
        self._chain = dict()

    def update_chain(self, el1, el2, prob):
        length = len(self._chain)
        self._chain.update({length : (el1, el2, prob)})

    @property
    def chain(self):
        return self._chain
