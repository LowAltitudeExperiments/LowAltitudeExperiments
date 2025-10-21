import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from matplotlib.ticker import MultipleLocator

# === Dataset configuration ===
# Each dataset corresponds to a different flight altitude
# and contains precomputed Cherenkov emission distributions.
datasets = {
    "10 km": {
        "folder": "/home/caterina/work/PIRATA/cosmique_proton_generator/cosmic_proton_shower_simulator/TEST_PIRATA/generated_configs_100PeV/output_npz/",
        "optical_axis": 86.79122,
    },
    "20 km": {
        "folder": "/home/caterina/work/PIRATA/cosmique_proton_generator/cosmic_proton_shower_simulator/TEST_PIRATA/generated_configs_20_100PeV/output_npz/",
        "optical_axis": 85.467693,
    },
    "30 km": {
        "folder": "/home/caterina/work/PIRATA/cosmique_proton_generator/cosmic_proton_shower_simulator/TEST_PIRATA/generated_configs_30_100PeV/output_npz/",
        "optical_axis": 84.453558,
    }
}

# === Load all .npz files for each altitude ===
for key, value in datasets.items():
    folder_path = Path(value["folder"])
    files = sorted([f.name for f in folder_path.glob("*.npz")])  # Sorted list of all .npz files
    datasets[key]["files"] = files

# === Assign colors for clarity ===
colors = {
    "10 km": "royalblue",
    "20 km": "darkorange",
    "30 km": "green"
}

# === Create the figure ===
fig, ax = plt.subplots(figsize=(9, 6))

# -------------------------------------------------------------------------
# PLOT 1: Cherenkov photon distributions (from precomputed .npz files)
# -------------------------------------------------------------------------
for label, info in datasets.items():
    folder = info["folder"]
    optical_axis = info["optical_axis"]
    file_list = info["files"]

    counts_list = []
    angles = []

    for filename in file_list:
        path = os.path.join(folder, filename)
        try:
            data = np.load(path)
            counts = data["dist_counts"]
            base_name = os.path.splitext(filename)[0]

            # Extract angle from filename (e.g., "output_86_25" -> 86.25)
            suffix = base_name.split("_")[-2] + "." + base_name.split("_")[-1]
            angle = float(suffix)

            # Select only viewing angles *above* the limb (optical axis)
            if angle > optical_axis:
                angles.append(angle)
                counts_list.append(counts[0])  # Use the first histogram entry

        except Exception as e:
            print(f"❌ Error reading {path}: {e}")

    # Sort data by angle
    if angles:
        sorted_data = sorted(zip(angles, counts_list))
        sorted_angles, sorted_counts = zip(*sorted_data)

        # Plot Cherenkov counts vs. viewing angle
        ax.plot(sorted_angles, sorted_counts,
                label=f"Cherenkov emission {label}",
                color=colors[label],
                linewidth=3)

        # Draw a vertical line for the optical axis
        ax.axvline(optical_axis, color=colors[label],
                   linestyle=':', linewidth=2, alpha=0.7,
                   label=f"Limb-viewing angle {label}")

# -------------------------------------------------------------------------
# PLOT 2: X-ray synchrotron emission (from HDF5 datasets)
# -------------------------------------------------------------------------

# === Load precomputed X-ray fluxes ===
store = pd.HDFStore('eas-xray-synchrotron-altitude-and-angle-scan.h5')
df_30_above = store['above_30km']
df_20_above = store['above_20km']
df_10_above = store['above_10km']
store.close()

# === Function to compute total photon flux per unit area ===
def compute_overall_flux(df):
    """Compute total flux = (band0 + band1 + band2) / area."""
    return (df.band0_rx + df.band1_rx + df.band2_rx) / df.area0_m2

# Compute fluxes for each altitude
flux_30 = compute_overall_flux(df_30_above)
flux_20 = compute_overall_flux(df_20_above)
flux_10 = compute_overall_flux(df_10_above)

# Plot the fluxes with dashed lines
ax.plot(df_10_above.theta_deg, flux_10,
        linestyle='--', color='royalblue', linewidth=3,
        label='X-ray emission 10 km')
ax.plot(df_20_above.theta_deg, flux_20,
        linestyle='--', color='darkorange', linewidth=3,
        label='X-ray emission 20 km')
ax.plot(df_30_above.theta_deg, flux_30,
        linestyle='--', color='green', linewidth=3,
        label='X-ray emission 30 km')

# -------------------------------------------------------------------------
# AXES, LABELS AND STYLE
# -------------------------------------------------------------------------

ax.set_xlabel('Viewing angle θ (degrees)', fontsize=20)
ax.set_ylabel('Flux (photons/m²)', fontsize=20)
ax.set_yscale('log')
ax.set_xlim(84, 140)
ax.set_ylim(1e-1, 1e8)

# Major and minor tick settings
ax.xaxis.set_major_locator(MultipleLocator(5.))
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.tick_params(axis='both', which='major', labelsize=18)
ax.tick_params(axis='both', which='minor', labelsize=12)

# Grid and layout
ax.grid(False)
plt.tight_layout()

# -------------------------------------------------------------------------
# LEGEND
# -------------------------------------------------------------------------

# Combine legends from both Cherenkov and X-ray data
ax.legend(fontsize=14, loc='upper right', frameon=False)

# -------------------------------------------------------------------------
# DISPLAY
# -------------------------------------------------------------------------
plt.show()
