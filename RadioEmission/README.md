🛰️ Low-Altitude Emission Experiments

# RASPASS for Aires 19-04-08 — Installation & QuickStart

📘 Project Description  
This repository contains the scripts and procedures used to generate the plots of Radio Emissions included in the proposal, which will serve as the foundation for the upcoming scientific papers.

- 📡 Radio emission — ZHAireS + RASPASS workflows, examples, and post-processing used to produce radio-frequency emission results.

---

This document explains how to install and test the RASPASS extension for ZHAireS built on Aires 19-04-08. This RASPASS package is tailored to Aires 19-04-08 (not 19-04-10). Future RASPASS updates will be integrated into ZHAireS 1.2+. The source file can be found in the Google Drive folder [`https://drive.google.com/drive/folders/1B6mTVTx38ynZ05hc_0k4hawXxVFjmxuK?usp=drive_link`](https://drive.google.com/drive/folders/1B6mTVTx38ynZ05hc_0k4hawXxVFjmxuK?usp=drive_link)

Before starting, check the `19-04-08` configuration directory if you need customizations. See `Install.HowTo` for more details.

---

## Overview / Key Notes
- This RASPASS release is meant for Aires **19-04-08**.
- If you already have Aires installed, change the `AiresRootDir` in the config to avoid overwriting your existing installation. You can keep multiple Aires versions simultaneously if paths are configured correctly.
- After successful installation, you will find Aires binaries in `$HOME/aires/bin`. Consider adding that directory to your `PATH`.

---

## Contents of the distribution
After unpacking, you should see:
- `Aires.19-04-08/` (Aires source tree)
- `Aires.ExtInp.2021Jun.tar.gz` (external input data)
- `ZHAireS-Exten.1-0-30a-Raspass.tar.gz` (ZHAireS + RASPASS extension)

---

## Quick install (step-by-step)

A) Unpack and basic install
1. Unpack the archive:
   ```
   tar -xzf Aires.19-04-08.ZHAireS.1.30.RASPASS.tar.gz
   ```
   This creates the `Aires.19-04-08` directory and the two additional `.tar.gz` files.

2. Change into the `19-04-08` directory and run the installer script:
   ```
   cd Aires.19-04-08
   doinstall 0
   ```
   The script compiles Aires and places binaries under `$HOME/aires/bin`.

3. Add the bin directory to your PATH (optional but recommended):
   ```
   export PATH="$HOME/aires/bin:$PATH"
   ```

4. Successful completion should show:
   ```
   INSTALLATION SUCCESSFULLY COMPLETED.
   ```

B) Add ZHAireS-RASPASS extension
1. After the base installation, compile the extension:
   ```
   addextensions
   ```
   Expected final messages:
   ```
   >>> End of installation process.
   >>> No more extensions to add.

   Installed extension(s):

   ZHAireS version 1.0.30a
   ```

C) Compile the RASPASS primary binary
1. Build the `RASPASSprimary` executable:
   ```
   cd RASPASSPrimary
   gfortran RASPASSprimary.f -o RASPASSprimary -L$HOME/aires/lib -lZHAireSRASPASS
   ```
   - If the linker cannot find `libZHAireSRASPASS.so`, either add `-static` or set `LD_LIBRARY_PATH`:
     ```
     export LD_LIBRARY_PATH="$HOME/aires/lib:$LD_LIBRARY_PATH"
     ```
   - On modern gfortran, you may need to add:
     ```
     -fallow-argument-mismatch
     ```
     to compiler flags if you get argument-mismatch errors (see Troubleshooting).

D) Run the example (quick test)
1. Run a quick example (97° shower example):
   ```
   $HOME/aires/bin/ZHAireSRASPASS < RASPASS_shower_example.inp
   ```
2. For organized outputs, copy `RASPASSprimary` and `.inp` examples to a new working directory before running.

Notes:
- Example inputs are thinned for speed — results will be noisy and are intended only for testing the installation workflow.
- Familiarize with standard Aires and ZHAireS workflows for meaningful simulations.

---

## Important configuration tips
- To avoid overwriting an existing Aires installation, edit the `AiresRootDir` variable in the installer/config.
- If you need different compiler flags, update the config file used by the build scripts (e.g., add `-fallow-argument-mismatch` to `FCFLAGS` or `FFLAGS` if required).

---

## Troubleshooting (common issues)

1. "argument mismatch" compile-time errors
   - Cause: stricter argument checking in newer gfortran versions.
   - Fix: add `-fallow-argument-mismatch` to the Fortran compiler flags in the build config.

2. "FATAL. Internal installation check failed: Main program (Aires) did not give the expected output. Installation aborted"
   - Cause: external input files may be in the wrong location.
   - Fix: move `Aires.ExtInp.2021Jun.tar.gz` (or the extracted input files) into the same parent directory that contains `Aires.19-04-08`, then rerun `doinstall 0`.

3. Linker errors for `libZHAireSRASPASS.so`
   - Fixes:
     - Add the library directory to `LD_LIBRARY_PATH`:
       ```
       export LD_LIBRARY_PATH="$HOME/aires/lib:$LD_LIBRARY_PATH"
       ```
     - Or link statically:
       ```
       gfortran ... -static -lZHAireSRASPASS
       ```

4. If the `RASPASSprimary` binary cannot be found when running `ZHAireSRASPASS`, ensure you copied or referenced it from the working directory where you launch the program.

---

## Best practices
- Keep a separate working directory for your runs; copy input files and executables there to keep the source directories clean.
- Start with un-thinned examples and small debugging runs to verify physics settings before scaling up.
- Read the Aires Manual and ZHAireS Manual — this software is powerful and complex; learning the recommended workflows will save time.

---

## Resources
- Aires Manual — consult for base Aires usage and configuration.
- ZHAireS Manual — consult for radio/emission and ZHAireS-specific settings.

---

## Need help?
If you run into problems, include:
- The exact command you ran
- The full build/install log (or relevant snippet)
- Your OS and gfortran version

I'll help diagnose and propose fixes.
