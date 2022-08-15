GA = {
    "population": 500,
    "n_gen": 100,
    "mut_rate": 0.4,
    "cross_rate": 1
}

MODEL = {
    "speed": 9,
    "map_size": 200,
    "steer_ang": 12,
    "min_len": 5,       # Minimal possible distance to go straight in meters
    "max_len": 50,      # Maximal possible distance to go straight in meters
    "min_angle": 10,    # Minimal angle of rotation in degrees
    "max_angle": 85,    # Maximal angle of rotation in degrees
    "ang_step": 5,
    "len_step": 1,
}

FILES = {
    "ga_archive": ".\\GA_archive\\",
    "ga_conv": ".\\",
    "schedules": "roads.json",
    "models": "models.csv",
    "tc_img": ".\\TC_img\\",
    "tc_file": ".\\TC_file\\",
}
