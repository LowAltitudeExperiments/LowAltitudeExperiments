- overall_plot_belowprob.py for UMAS
- overall_plot.py  for HAHAS

These two scripts have been used to produce the first two plots in the proposal containing the fluxes for Xray and Cherenkov emission for both UMAS and HAHAS.

In case of UMAS the emergence probability is shown as well.

The files can be found in the drive link attached to the general folder of the organization

https://drive.google.com/drive/folders/1B6mTVTx38ynZ05hc_0k4hawXxVFjmxuK?usp=drive_link

## 🧩 Required Python Packages

The scripts in this directory require the following Python packages:

```python
# Core scientific and numerical libraries
import numpy as np
import pandas as pd
import math
import os
from pathlib import Path

# Plotting and visualization
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LogLocator, FuncFormatter