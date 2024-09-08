"""
 Title:         Sample 617_s3
 Description:   Runs the CPFEM model using CCD
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
from deer_sim.interface import Interface
from deer_sim.helper.sampler import get_ccd
from deer_sim.helper.general import round_sf
from deer_sim.helper.io import csv_to_dict

# Constants
NUM_PARALLEL   = 4
NUM_PROCESSORS = 48

# Define VP material parameters
vp_param_dict = {
    "vp_s0":  93.655,
    "vp_R":   3957.3,
    "vp_d":   0.5651,
    "vp_n":   7.3648,
    "vp_eta": 721.59,
}

# Get CP parameter combinations
bounds_dict = {
    "cp_tau_s": (2, 4), # 2**Nx50
    "cp_b":     (1, 3), # 2**Nx0.5
    "cp_tau_0": (2, 4), # 2**Nx25
    "cp_n":     (2, 4), # 0.5*2**N
}
param_dict_list = get_ccd(bounds_dict)

# Transform CP parameters
for param_dict in param_dict_list:
    param_dict["cp_tau_s"]   = 50*2**param_dict["cp_tau_s"]
    param_dict["cp_b"]       = 0.5*2**param_dict["cp_b"]
    param_dict["cp_tau_0"]   = 25*2**param_dict["cp_tau_0"]
    param_dict["cp_n"]       = 0.5*2**param_dict["cp_n"]
    param_dict["cp_gamma_0"] = round_sf(1e-4/3, 4)

# # Print out domains of parameters
# from deer_sim.helper.sampler import get_domains
# print(get_domains(param_dict_list))
# {
#    'cp_tau_s':   [100.0, 200.0, 400.0, 800.0, 1600.0],
#    'cp_b':       [0.5, 1.0, 2.0, 4.0, 8.0],
#    'cp_tau_0':   [50.0, 100.0, 200.0, 400.0, 800.0],
#    'cp_n':       [1.0, 2.0, 4.0, 8.0, 16.0],
#    'cp_gamma_0': [3.333e-05]
# }

# Section CP parameter list for script
sim_id     = int(sys.argv[1])
num_sims   = int(len(param_dict_list)/NUM_PARALLEL)
index_list = list(range(32))[sim_id*num_sims:(sim_id+1)*num_sims]
param_dict_list = [param_dict_list[i] for i in index_list]

# Iterate through CP parameter list
for i, param_dict in enumerate(param_dict_list):

    # Initialise
    index_str = str(i+1).zfill(2)
    itf = Interface(
        title       = f"{sim_id}_{index_str}",
        input_path  = "../data/617_s3",
        output_path = "../results/",
    )

    # Define the mesh
    itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)

    # Defines the material parameters
    itf.define_material(
        material_name   = "cvp_ae",
        material_params = {**param_dict, **vp_param_dict},
        c_11            = 250000,
        c_12            = 151000,
        c_44            = 123000,
        youngs          = 211000.0,
        poissons        = 0.30,
    )

    # Defines the simulation parameters
    exp_dict = csv_to_dict("../data/617_s3/617_s3_exp.csv")
    itf.define_simulation(
        simulation_name = "1to1_ui",
        end_time        = exp_dict["time_intervals"][-1],
        end_strain      = exp_dict["strain_intervals"][-1] * 2200 * 5/3
    )

    # Runs the model and saves results
    itf.export_params()
    itf.simulate("~/moose/deer/deer-opt", NUM_PROCESSORS, 100000)

    # Conduct post processing
    itf.compress_csv(sf=5, exclude=["x", "y", "z"])
    itf.post_process()
    itf.remove_files(["mesh.e", "element_stats.csv", "results", "simulation_out_cp"])