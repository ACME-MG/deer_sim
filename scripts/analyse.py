"""
 Title:         Analyse
 Description:   Analyses the simulation results
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.helper.general import transpose, remove_consecutive_duplicates
from deer_sim.helper.io import csv_to_dict

# Constants
EXP_PATH = "data/617_s3/617_s3_exp.csv"
MAP_PATH = "data/617_s3/grain_map.csv"
# SIM_PATH = "results/240718160621_mini/summary.csv"
SIM_PATH = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/results/deer_sim/2024-07-19 (617_s3_compressed)/summary.csv"

def get_grain_ids(exp_path:str, mesh_path:str) -> dict:
    """
    Gets the mappable grain IDs
    
    Parameters:
    * `exp_path`:  Path to the experimental data
    * `mesh_path`: Path to the mesh CSV map

    Returns a dictionary mapping the experimental grain IDs to the mesh grain IDs
    """

    # Read files
    exp_dict  = csv_to_dict(exp_path)  # exp
    mesh_dict = csv_to_dict(mesh_path) # exp : mesh
    exp_grain_ids = [int(key.replace("_phi_1","").replace("g","")) for key in exp_dict.keys() if "_phi_1" in key]
    
    # Map experimental grain IDs to mesh grain IDs
    exp_to_mesh = {}
    for exp_grain_id in exp_grain_ids:
        if exp_grain_id in mesh_dict["ebsd_id"]:
            ebsd_index = mesh_dict["ebsd_id"].index(exp_grain_id)
            exp_to_mesh[exp_grain_id] = int(mesh_dict["mesh_id"][ebsd_index])

    # Return mapping
    return exp_to_mesh

def get_trajectories(data_dict:dict, include:list=None) -> list:
    """
    Gets the reorientation trajectories

    Parameters:
    * `data_dict`: The data dictionary
    * `include`:   List of grain IDs to include;
                   uses all grain IDs if parameter unspecified
    
    Return trajectories as a list of lists of euler angles
    """

    # Read data and specify grain IDs if defined
    grain_ids = [int(key.replace("g","").replace("_phi_1","")) for key in data_dict.keys() if "_phi_1" in key]
    if include != None:
        grain_ids = [grain_id for grain_id in grain_ids if grain_id in include]

    # Get trajectories
    trajectories = []
    for grain_id in grain_ids:
        trajectory = [data_dict[f"g{grain_id}_{phi}"] for phi in ["phi_1", "Phi", "phi_2"]]
        trajectory = transpose(trajectory)
        trajectory = remove_consecutive_duplicates(trajectory)
        trajectories.append(trajectory)

    # Return trajectories
    return trajectories

# Define grain IDs
# GOOD: 16, 21, 37, 46, 76, 82, 87, 99, 101, 110, 137, 141, 147, 152, 154, 159, 166, 167, 173, 180
# OKAY: 23, 27, 36, 38, 40, 49, 56, 64, 66, 97, 108, 109, 112, 114, 120, 128, 130, 139, 148, 176, 178
grain_id_dict = get_grain_ids(EXP_PATH, MAP_PATH)
exp_grain_ids  = [16, 21, 37, 46, 76]
sim_grain_ids  = [grain_id_dict[exp_grain_id] for exp_grain_id in exp_grain_ids]
for exp, sim in zip(exp_grain_ids, sim_grain_ids):
    print(f" exp: {exp}\t sim: {sim}")

# Get experimental data
exp_dict = csv_to_dict(EXP_PATH)
exp_ss   = {"strain": exp_dict["strain"], "stress": exp_dict["stress"]}
exp_traj = get_trajectories(exp_dict, exp_grain_ids)

# Get simulated data
sim_dict     = csv_to_dict(SIM_PATH)
sim_grain_ss = {"strain": exp_dict["strain"], "stress": exp_dict["stress"]}

# # Plot stress-strain curves
# exp_ss = {"strain": exp_dict["strain"], "stress": exp_dict["stress"]}
# sim_ss = {"strain": exp_dict["strain_intervals"], "stress": get_sim_stress(sim_dict_list)}
# plotter_ss = Plotter("strain", "stress")
# plotter_ss.prep_plot()
# plotter_ss.scat_plot(exp_ss, colour="darkgray")
# plotter_ss.line_plot(sim_ss, colour="red")
# plotter_ss.define_legend(["darkgray", "red"], ["Experimental", "CPFEM"], [7, 2], ["scatter", "line"])
# save_plot("plot_ss.png")

# # Plot trajectories on IPF
# exp_trajectories = get_exp_trajectories(exp_dict, exp_grain_ids)
# sim_trajectories = get_sim_trajectories(sim_dict_list, sim_grain_ids)
# quick_ipf(
#     exp_trajectories = exp_trajectories,
#     sim_trajectories = sim_trajectories,
#     file_path        = "plot_phi.png",
#     structure        = "fcc",
#     direction        = [1,0,0],
#     # initial_only     = True,
#     grain_ids        = exp_grain_ids,
# )

