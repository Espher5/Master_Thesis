import copy
import numpy as np
import random

import config

from pymoo.model.mutation import Mutation


class CpsMutation(Mutation):
    def __init__(self, mut_rate):
        super().__init__()
        self.mut_rate = mut_rate

    def _do(self, problem, x, **kwargs):
        for i in range(len(x)):
            r = np.random.random()
            s = x[i, 0]
            if s is None:
                print("S i none")
            if (r < self.mut_rate) and (s is not None):  # config.ga["mut_rate"]:
                # For some reason it seems we must do a deep copy
                # and replace the original object
                # pymoo seems to keep a deep copy of the best object if I change it
                # in a mutation it will not change the best pymoo individual, and we end up
                # with an inconsistency in evaluated fitness
                sn = copy.deepcopy(s)

                sn.get_points()
                sn.remove_invalid_cases()

                wr = random.randint(1, 101)
                child = sn.states
                old_states = child

                if wr < 20:
                    candidates = list(np.random.randint(0, high=len(child), size=2))
                    temp = child["st" + str(candidates[0])]
                    child["st" + str(candidates[0])] = child["st" + str(candidates[1])]
                    child["st" + str(candidates[1])] = temp

                elif 20 <= wr <= 40:
                    num = np.random.randint(0, high=len(child))

                    value = "value"
                    if child["st" + str(num)]["state"] == "straight":
                        duration_list = np.arange(
                            config.MODEL["min_len"],
                            config.MODEL["max_len"],
                            config.MODEL["len_step"],
                        )
                    else:
                        duration_list = np.arange(
                            config.MODEL["min_angle"],
                            config.MODEL["max_angle"],
                            config.MODEL["ang_step"],
                        )

                    child["st" + str(num)][value] = int(np.random.choice(duration_list))
                    value = "state"

                    if child["st" + str(num)][value] == "straight":
                        child["st" + str(num)][value] = np.random.choice(
                            ["left", "right"]
                        )
                        duration_list = np.arange(
                            config.MODEL["min_angle"],
                            config.MODEL["max_angle"],
                            config.MODEL["ang_step"],
                        )
                        child["st" + str(num)]["value"] = int(
                            np.random.choice(duration_list)
                        )
                    else:
                        child["st" + str(num)][value] = "straight"
                        duration_list = np.arange(
                            config.MODEL["min_len"],
                            config.MODEL["max_len"],
                            config.MODEL["len_step"],
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
                                    config.MODEL["min_len"],
                                    config.MODEL["max_len"],
                                    config.MODEL["len_step"],
                                )
                            else:
                                duration_list = np.arange(
                                    config.MODEL["min_angle"],
                                    config.MODEL["max_angle"],
                                    config.MODEL["ang_step"],
                                )
                            child["st" + str(c1)]["value"] = int(
                                np.random.choice(duration_list)
                            )

                sn.states = child
                sn.get_points()
                sn.remove_invalid_cases()
                sn.novelty = sn.calc_novelty(old_states, sn.states)
                x[i, 0] = sn

        return x
