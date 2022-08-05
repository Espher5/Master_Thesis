import json
import os
import shutil
import time
import numpy as np
import matplotlib.pyplot as plt

from zipfile import ZipFile
from itertools import combinations

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_performance_indicator
from pymoo.optimize import minimize
from pymoo.termination.ftol import MultiObjectiveSpaceTermination
from pymoo.termination.robust import RobustTermination

import config as cf
from CpsProblem import CpsProblem
from CpsSampling import CpsSampling
from CpsCrossover import CpsCrossover
from CpsMutation import CpsMutation
from CpsDuplicates import CpsDuplicates


algorithm = NSGA2(
    pop_size=cf.GENETIC_ALGORITHM["population"],
    sampling=CpsSampling(),
    crossover=CpsCrossover(cf.GENETIC_ALGORITHM["crossover_rate"]),
    mutation=CpsMutation(cf.GENETIC_ALGORITHM["mutation_rate"]),
    eliminate_duplicates=CpsDuplicates(),
)


termination = MultiObjectiveSpaceTermination(
    tol=0.0025,
    #n_last=cf.GENETIC_ALGORITHM["generations"],
    #nth_gen=5,
    #n_max_gen=cf.GENETIC_ALGORITHM["generations"],
    #n_max_evals=None,
)


def plot_convergence(res):
    n_evals = np.arange(0, len(res.history), 1)
    opt = np.array([e.opt[0].F for e in res.history])

    fig, ax1 = plt.subplots(figsize=(12, 4))
    plt.title("Convergence")
    plt.plot(n_evals, opt, "o--")
    plt.xlabel("Number of generations")
    plt.ylabel("Fitness function value")

    fig.savefig(cf.FILES["ga_conv"] + "conv.png")
    plt.close(fig)


def plot_car_path(road_points, car_path, fitness, novelty, generation, i):
    fig, ax = plt.subplots(figsize=(12, 12))
    road_x = []
    road_y = []
    for p in road_points:
        road_x.append(p[0])
        road_y.append(p[1])

    if len(car_path):
        ax.plot(car_path[0], car_path[1], "bo", label="Car path")

    ax.plot(road_x, road_y, "yo--", label="Road")

    top = cf.MODEL["map_size"]
    bottom = 0

    ax.set_title(
        "Test case fitness " + str(fitness) + " novelty " + str(novelty), fontsize=17
    )

    ax.set_xlim(bottom, top)
    ax.set_ylim(bottom, top)
    ax.legend()

    save_path = os.path.join(cf.FILES["tc_img"], "generation_" + str(generation))

    fig.savefig(save_path + "\\" + "tc_" + str(i) + ".jpg")
    plt.close(fig)


def save_results(res):
    plot_convergence(res)

    if os.listdir(cf.FILES["tc_file"]):
        dt_string = str(int(time.time()))

        #  Create directory and prepare files
        shutil.make_archive(dt_string + "_tc_img", "zip", cf.FILES["tc_img"])
        shutil.make_archive(dt_string + "_tc_file", "zip", cf.FILES["tc_file"])
        shutil.copyfile(".\\config.py", ".\\" + dt_string + "_config.py")
        shutil.copyfile(".\\conv.png", ".\\" + dt_string + "_conv.png")
        shutil.copyfile(".\\vehicle.py", ".\\" + dt_string + "_vehicle.py")

        zip_obj = ZipFile(dt_string + "_results.zip", "w")

        # Add multiple files to the zip
        zip_obj.write(dt_string + "_tc_img.zip")
        zip_obj.write(dt_string + "_tc_file.zip")
        zip_obj.write(dt_string + "_conv.png")
        zip_obj.write(dt_string + "_config.py")
        zip_obj.write(dt_string + "_vehicle.py")
        zip_obj.close()

        #  Move the archive to the destination folder
        shutil.move(
            dt_string + "_results.zip",
            cf.FILES["ga_archive"] + dt_string + "_results.zip",
        )

        #  Remove files
        os.remove(".\\" + dt_string + "_config.py")
        os.remove(".\\" + dt_string + "_vehicle.py")
        os.remove(".\\" + dt_string + "_conv.png")
        os.remove(".\\" + "conv.png")
        os.remove(".\\" + dt_string + "_tc_img.zip")
        os.remove(".\\" + dt_string + "_tc_file.zip")

        for folder in os.listdir(cf.FILES["tc_img"]):
            shutil.rmtree(cf.FILES["tc_img"] + folder)

        for file in os.listdir(cf.FILES["tc_file"]):
            os.remove(cf.FILES["tc_file"] + file)

    #  Create new folders
    for gen in [0, len(res.history) - 1]:
        os.mkdir(cf.FILES["tc_img"] + "generation_" + str(gen))

    #  Build images and write tc to file
    for gen in [0, len(res.history) - 1]:
        test_cases = {}
        states_tc = {}

        for i, x in enumerate(res.history[gen].pop.get("X")):
            road_points = x[0].intp_points
            car_path = x[0].car_path
            fitness = x[0].fitness
            states = x[0].states
            novelty = x[0].novelty

            plot_car_path(road_points, car_path, fitness, novelty, gen, i)

            test_cases["tc" + str(i)] = road_points
            states_tc["tc" + str(i)] = states

            if i > 20:
                break
            i += 1

        save_path = os.path.join(
            cf.FILES["tc_file"], "generation_" + str(gen) + ".json"
        )
        save_path2 = os.path.join(cf.FILES["tc_file"], "states_" + str(gen) + ".json")
        with open(save_path, "w") as outfile:
            json.dump(test_cases, outfile, indent=4)
        with open(save_path2, "w") as outfile:
            json.dump(states_tc, outfile, indent=4)


def calc_novelty(old, new):
    novelty = 0

    difference = abs(len(new) - len(old)) / 2
    novelty += difference
    if len(new) <= len(old):
        shorter = new
    else:
        shorter = old
    for tc in shorter:
        if old[tc]["state"] == new[tc]["state"]:
            value_list = [old[tc]["value"], new[tc]["value"]]
            ratio = max(value_list) / min(value_list)
            if ratio >= 2:
                novelty += 0.5
        else:
            novelty += 1
    return -novelty


if __name__ == "__main__":

    res_dict = {}

    time_list = []
    m = 0

    for m in range(30):
        fit_list = []

        print("Evaluation", m)

        t = int(time.time() * 1000)
        seed = (
            ((t & 0xFF000000) >> 24)
            + ((t & 0x00FF0000) >> 8)
            + ((t & 0x0000FF00) << 8)
            + ((t & 0x000000FF) << 24)
        )
        print("Seed ", seed)

        res = minimize(
            CpsProblem(),
            algorithm,
            ("n_gen", cf.GENETIC_ALGORITHM["generations"]),
            seed=seed,
            verbose=True,
            save_history=True,
            eliminate_duplicates=True,
        )

        print("time", res.exec_time)
        print("time, sec ", res.exec_time)

        time_list.append(res.exec_time)
        res_dict["run" + str(m)] = {}
        res_dict["run" + str(m)]["time"] = res.exec_time

        hv_values = []

        hv = get_performance_indicator("hv", ref_point=np.array([0, 0]))

        for gen in range(0, len(res.history)):

            i = 0
            minim = 0
            hv_list = []
            while i < len(res.history[gen].opt):
                result = res.history[gen].pop.get("X")[i]
                hv_item = res.history[gen].pop.get("F")[i]
                hv_list.append(hv_item)

                fit = result[0].fitness
                if fit < minim:
                    minim = fit

                i += 1
            fit_list.append(minim)
            hv_values.append(hv.calc(np.array(hv_list)))

        gen = len(res.history) - 1
        reference = res.history[gen].pop.get("X")[0]
        novelty_list_old = []
        for i in range(1, len(res.history[gen].opt)):
            current = res.history[gen].pop.get("X")[i]
            nov = calc_novelty(reference[0].states, current[0].states)
            novelty_list_old.append(nov)

        res_dict["run" + str(m)]["fitness"] = fit_list
        print(min(fit_list))
        res_dict["run" + str(m)]["hv"] = hv_values

        gen = len(res.history) - 1
        novelty_list = []
        for i in combinations(range(0, 20), 2):
            current1 = res.history[gen].pop.get("X")[i[0]]
            current2 = res.history[gen].pop.get("X")[i[1]]
            nov = calc_novelty(current1[0].states, current2[0].states)
            novelty_list.append(nov)

        novelty_list2 = []
        for i in combinations(range(0, 10), 2):
            current1 = res.history[gen].pop.get("X")[i[0]]
            current2 = res.history[gen].pop.get("X")[i[1]]
            nov = calc_novelty(current1[0].states, current2[0].states)
            novelty_list2.append(nov)

        # res_dict["run" + str(m)]["fitness"] = fit_list
        res_dict["run" + str(m)]["novelty_20"] = sum(novelty_list) / len(novelty_list)
        res_dict["run" + str(m)]["novelty_10"] = sum(novelty_list2) / len(novelty_list2)
        res_dict["run" + str(m)]["novelty"] = sum(novelty_list_old) / len(
            novelty_list_old
        )

        with open("Results_vehicle(2).json", "w") as f:
            json.dump(res_dict, f, indent=4)

        save_results(res)
