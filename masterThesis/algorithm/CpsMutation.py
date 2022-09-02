import numpy as np
from pymoo.model.mutation import Mutation
import copy
import algorithm.config as cf


class CpsMutation(Mutation):
    """
    Class that performs the mutation operation
    """
    def __init__(self, mut_rate):
        super().__init__()
        self.mut_rate = mut_rate

    def _do(self, problem, X, **kwargs):
        for i in range(len(X)):
            r = np.random.random()
            s = X[i, 0]
            # with a probability of 40% - change the order of characters
            if r < self.mut_rate:  # cf.ga["mut_rate"]:
                sn = copy.deepcopy(s)
                sn.get_points()
                sn.remove_invalid_cases()

                wr = np.random.random()
                child = sn.states
                old_states = child
                if wr < 0.2:
                    candidates = list(np.random.randint(0, high=len(child), size=2))
                    temp = child["st" + str(candidates[0])]
                    child["st" + str(candidates[0])] = child["st" + str(candidates[1])]
                    child["st" + str(candidates[1])] = temp
                elif 0.2 <= wr < 0.5:
                    num = np.random.randint(0, high=len(child))
                    value = np.random.choice(["state", "value"])
                    if value == "value":
                        if child["st" + str(num)]["state"] == "straight":
                            duration_list = np.arange(
                                cf.MODEL["min_len"], cf.MODEL["max_len"], 1
                            )
                        else:
                            duration_list = np.arange(
                                cf.MODEL["min_angle"], cf.MODEL["max_angle"], 5
                            )

                        child["st" + str(num)][value] = int(
                            np.random.choice(duration_list)
                        )

                    elif value == "state":

                        if child["st" + str(num)][value] == "straight":
                            child["st" + str(num)][value] = np.random.choice(
                                ["left", "right"]
                            )
                            duration_list = np.arange(
                                cf.MODEL["min_angle"], cf.MODEL["max_angle"], 5
                            )
                            child["st" + str(num)]["value"] = int(
                                np.random.choice(duration_list)
                            )
                        else:
                            child["st" + str(num)][value] = "straight"
                            duration_list = np.arange(
                                cf.MODEL["min_len"], cf.MODEL["max_len"], 1
                            )
                            child["st" + str(num)]["value"] = int(
                                np.random.choice(duration_list)
                            )
                else:
                    cand = list(
                        np.random.randint(0, high=len(child), size=int(len(child) / 2))
                    )
                    while cand:
                        c1 = np.random.choice(cand)
                        cand.remove(c1)
                        if cand:
                            c2 = np.random.choice(cand)
                            cand.remove(c2)
                            temp = child["st" + str(c1)]
                            child["st" + str(c1)] = child["st" + str(c2)]
                            child["st" + str(c2)] = temp
                        else:
                            if child["st" + str(c1)]["state"] == "straight":
                                duration_list = np.arange(
                                    cf.MODEL["min_len"], cf.MODEL["max_len"], 1
                                )
                            else:
                                duration_list = np.arange(
                                    cf.MODEL["min_angle"], cf.MODEL["max_angle"], 5
                                )
                            child["st" + str(c1)]["value"] = int(
                                np.random.choice(duration_list)
                            )

                sn.states = child
                sn.get_points()
                sn.remove_invalid_cases()
                sn.novelty = sn.calc_novelty(old_states, sn.states)

                X[i, 0] = sn

        return X
