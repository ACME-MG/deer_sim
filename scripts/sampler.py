import sys; sys.path += [".."]
from deer_sim.interface import Interface
import itertools

# Define parameter domains
param_dict = {
    # "tau_s":   [1, 500, 1000, 1500, 2000],
    "tau_s":   [1],
    "b":       [0.1, 1, 10, 100],
    "tau_0":   [100, 200, 300, 400, 500],
    "gamma_0": [round(1e-4/3, 7)],
    "n":       [1, 5, 10, 15, 20],
}

# Get combinations of domains
param_list = list(param_dict.values())
combinations = list(itertools.product(*param_list))
combinations = [list(c) for c in combinations]

# Iterate through the parameters
param_names = list(param_dict.keys())
for i in range(len(combinations)):
    param_dict = dict(zip(param_names, combinations[i]))
    itf = Interface(f"s1_p{i}", input_path="./data/500/16_s1")
    itf.define_mesh("mesh.e", "input_orientations.csv")
    itf.define_material("vshai", param_dict)
    itf.define_simulation("cp_simple", {})
    itf.export_params()
    itf.simulate("~/moose/deer/deer-opt", 8)
    itf.remove_artifacts()
    itf.analyse_results()
