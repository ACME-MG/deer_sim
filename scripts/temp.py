"""
 Title:         617_s3
 Description:   Runs the CPFEM model once
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.interface import Interface
from deer_sim.helper.general import round_sf
from deer_sim.helper.io import csv_to_dict

# Define the mesh and orientations
itf = Interface(input_path="data/617_s3")
itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)

# Defines the material parameters
itf.define_material(
    material_name   = "mat_1to1",
    material_params = {

        # Crystal Plasticity Parameters
        "cp_tau_s":   1250,
        "cp_b":       0.25,
        "cp_tau_0":   107,
        "cp_gamma_0": round_sf(1e-4/3, 5),
        "cp_n":       4.5,

        # Viscoplastic Parameters
        "vp_s0":      93.655,
        "vp_R":       3957.3,
        "vp_d":       0.56507,
        "vp_n":       7.3648,
        "vp_eta":     721.59,
    },
    youngs          = 211000.0,
    poissons        = 0.30,
)

# Defines the simulation parameters
exp_dict = csv_to_dict("data/617_s3/617_s3_exp.csv")
itf.define_simulation(
    simulation_name = "sim_1to1",
    time_intervals  = exp_dict["time_intervals"],
    end_strain      = exp_dict["strain_intervals"][-1] * 2200 * 5/3
)

# Conduct post processing
itf.post_process("/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/results/deer_sim/2024-07-16 (617_s3)")