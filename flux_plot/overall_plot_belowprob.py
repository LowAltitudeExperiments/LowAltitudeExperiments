import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from pathlib import Path
import matplotlib.ticker as ticker

# ======================================
# CONSTANTS
# ======================================
RE = 6378  # Earth radius in km

# ======================================
# DATASET DEFINITIONS
# ======================================
datasets = {
    "10 km": {
        "folder": "/home/caterina/work/PIRATA/cosmique_proton_generator/cosmic_proton_shower_simulator/TEST_PIRATA/below_limb/below_generated_configs_100PeV/output_npz/",
        "optical_axis": 86.79122,
    },
    "20 km": {
        "folder": "/home/caterina/work/PIRATA/cosmique_proton_generator/cosmic_proton_shower_simulator/TEST_PIRATA/below_limb/below_generated_configs_20_100PeV/output_npz/",
        "optical_axis": 85.467693,
    },
    "30 km": {
        "folder": "/home/caterina/work/PIRATA/cosmique_proton_generator/cosmic_proton_shower_simulator/TEST_PIRATA/below_limb/below_generated_configs_30_100PeV/output_npz/",
        "optical_axis": 84.453558,
    }
}

# ======================================
# EMERGENCE ANGLES (precomputed) by using generalized Austin's script available in the folder CherFly
# ======================================
emer_angles = np.array([
    2.02169133e-03, 1.80986219e-03, 1.64989844e-03, 1.23674768e-03,
    1.02298836e-03, 8.38838978e-04, 6.50581475e-04, 5.07186554e-04,
    3.92577600e-04, 3.18449487e-04, 2.45138649e-04, 1.98058350e-04,
    1.69064517e-04, 1.45671753e-04, 1.16596352e-04, 1.03982740e-04,
    8.69033411e-05, 7.52353981e-05, 6.46191114e-05, 5.49691906e-05,
    4.71997205e-05, 3.99570455e-05, 3.66770393e-05, 3.02926141e-05,
    2.56558095e-05, 2.20945082e-05, 1.90275537e-05, 1.66590946e-05,
    1.46538173e-05, 1.28899179e-05, 1.11854525e-05, 9.68366193e-06,
    8.38350604e-06, 7.59581015e-06, 6.90704198e-06, 6.28072949e-06,
    6.00000000e-06, 5.00000000e-06, 4.00000000e-06, 3.00000000e-06,
    0.000000000, 0.00000000e-10, 0.00000000e-10, 0.00000000e-10,
    0.00000000e-10, 0.00000000e-10, 0.00000000e-10, 0.00000000e-10,
    0.00000000e-10, 0.00000000e-10, 0.00000000e-10, 0.00000000e-10,
    0.00000000e-10, 0.00000000e-10, 0.00000000e-10, 0.00000000e-10,
    0.00000000e-10,
])

# Add altitude to dataset info
for key in datasets:
    datasets[key]["altitude"] = int(key.split()[0])

# Get all .npz files in each folder
for key, value in datasets.items():
    folder_path = Path(value["folder"])
    files = sorted([f.name for f in folder_path.glob("*.npz")])
    datasets[key]["files"] = files

# Define colors
colors = {
    "10 km": "royalblue",
    "20 km": "darkorange",
    "30 km": "green"
}

# ======================================
# FIGURE INITIALIZATION
# ======================================
fig, ax = plt.subplots(figsize=(10, 6))

# ======================================
# LOOP OVER CHERENKOV DATASETS
# ======================================
for label, info in datasets.items():
    folder = info["folder"]
    optical_axis = info["optical_axis"]
    h = info["altitude"]

    file_list = info["files"]
    counts_list = []
    angles = []

    for filename in file_list:
        path = os.path.join(folder, filename)
        try:
            data = np.load(path)
            counts = data["dist_counts"]
            base_name = os.path.splitext(filename)[0]
            suffix = base_name.split("_")[-2] + "." + base_name.split("_")[-1]
            angle = float(suffix)

            # Only below limb region
            if angle < 100.:
                angles.append(angle)
                counts_list.append(counts[0])
        except Exception as e:
            print(f"❌ Error reading file {path}: {e}")

    # Sort by angle
    if angles:
        sorted_data = sorted(zip(angles, counts_list))
        sorted_angles, sorted_counts = zip(*sorted_data)
        sorted_counts = np.array(sorted_counts)
        theta_sh_rad = np.radians(sorted_angles)

        # Compute observation angle from spherical geometry
        value = (RE / (RE + h)) * np.cos(theta_sh_rad)
        value = np.clip(value, -1, 1)
        theta_d_rad = np.arcsin(value)
        theta_d_deg = np.degrees(theta_d_rad)
        sorted_angles = np.array(theta_d_deg)

        # Plot Cherenkov distribution
        ax.plot(
            sorted_angles,
            sorted_counts,
            label=f'Cherenkov emission ({label})',
            color=colors[label],
            linewidth=3
        )

        # Draw optical axis line
        ax.axvline(
            optical_axis,
            color=colors[label],
            linestyle=':',
            linewidth=2,
            alpha=0.7,
            label=f'Limb-viewing angle ({label})'
        )

# ======================================
# LOAD X-RAY FLUX DATA FROM HDF5
# ======================================
store = pd.HDFStore('altitude-and-angle-scan-extended.h5')
df_30 = store['below_30km']
df_20 = store['below_20km']
df_10 = store['below_10km']
store.close()

# Compute total X-ray flux
def compute_overall_flux(df):
    return (df.band0_rx + df.band1_rx + df.band2_rx) / df.area0_m2

# Plot X-ray flux curves
ax.plot(df_30.theta_deg, compute_overall_flux(df_30),
        linestyle='--', color='green', linewidth=2, label='X-ray flux (30 km)')
ax.plot(df_20.theta_deg, compute_overall_flux(df_20),
        linestyle='--', color='darkorange', linewidth=2, label='X-ray flux (20 km)')
ax.plot(df_10.theta_deg, compute_overall_flux(df_10),
        linestyle='--', color='royalblue', linewidth=2, label='X-ray flux (10 km)')

# ======================================
# PLOT SETTINGS (LEFT AXIS)
# ======================================
ax.set_xlabel('Viewing angle θ (degrees)', fontsize=20)
ax.set_ylabel('Flux / Counts (a.u.)', fontsize=20)
ax.set_yscale('log')
ax.set_xlim(40, 88)
ax.set_ylim(1e-1, 1e9)
ax.tick_params(axis='both', labelsize=18)
ax.grid(False)

# ======================================
# SECOND Y-AXIS FOR EMERGENCE PROBABILITY
# ======================================
ax2 = ax.twinx()
emer_angles_cut = emer_angles[:len(sorted_angles)]
ax2.plot(
    sorted_angles, emer_angles_cut,
    linestyle='-', color='gray',
    linewidth=3, label='Emergence probability'
)
ax2.set_yscale('log')
ax2.set_ylabel('Emergence probability', fontsize=20, color='black')
ax2.tick_params(axis='y', labelcolor='black', labelsize=18)

# Use scientific notation on right axis
def sci_notation(x, _):
    if x == 0:
        return "0"
    exp = int(np.floor(np.log10(x)))
    return f"$10^{{{exp}}}$"

ax2.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation))

# ======================================
# LEGEND AND FINAL TOUCHES
# ======================================
fig.tight_layout(rect=[0, 0, 0.9, 1.])
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=14, loc='upper left')

plt.show()
