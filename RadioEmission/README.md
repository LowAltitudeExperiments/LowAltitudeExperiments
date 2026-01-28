**Installation Guide for RASPASS with Aires 19-04-08**

**Getting Started:**

Before diving into the installation, make sure to check the config file in the 19.04.08 directory if you need any customizations. For more detailed instructions, refer to the Install.HowTo file.

If you already have Aires installed, consider changing the AiresRootDir variable to prevent overwriting. You can run both versions simultaneously with the right setup.

**Important Note:**

This RASPASS version is tailored for Aires 19-04-08, not the latest 19-04-10. No major changes are needed, and future RASPASS updates will be integrated directly into ZHAireS 1.2 and above, simplifying your updates.

**Step-by-Step Instructions:**

**A) Unpack and Set Up:**

1. Unzip the Aires.19-04-08.ZHAireS.1.30.RASPASS.tar.gz file. This will create a directory named Aires.19-04-08 with a subdirectory, along with two additional files: Aires.ExtInp.2021Jun.tar.gz and ZHAireS-Exten.1-0-30a-Raspass.tar.gz.

1. Open a terminal, navigate to the 19-04-08 directory, and run `doinstall 0`.

1. The script will compile the Aires source code, generating binary files in $HOME/aires/bin. Consider adding this directory to your system PATH for easy access.

1. Completion is marked by the message: “INSTALLATION SUCCESSFULLY COMPLETED.”

**B) Install ZHAireS-RASPASS Extension:**

1. After installation, run `addextensions` to compile the ZHAireS binaries with RASPASS modifications. The process should conclude with:

   >>> End of installation process.
   >>> No more extensions to add.

   Installed extension(s):

   ZHAireS version 1.0.30a

**C) Compile the RASPASS Binary:**

1. Navigate to the RASPASSPrimary directory and execute:

   gfortran RASPASSprimary.f -o RASPASSprimary -L(your home directory)/aires/lib -lZHAireSRASPASS

1. If you encounter issues finding libZHAiresRASPASS.so, add `-static` or include the lib directory in your LD_LIBRARY_PATH environment variable.

1. This will create a RASPASSprimary binary for processing primary particles in ZHAireS.

**D) Test the Examples:**

1. Run a quick simulation of a 97-degree shower using:

   /(your home directory)/aires/bin/ZHAireSRASPASS <RASPASS_shower_example.inp

1. Feel free to explore other examples, but it’s best to copy the RASPASSprimary and .inp files to a new directory for organized output.

**Note:** These examples are designed for speed, resulting in noisy and less meaningful outputs due to aggressive thinning. Familiarize yourself with standard Aires and ZHAireS first. The Aires Manual and ZHAireS Manual are invaluable resources. This software is complex and powerful—mastery takes time!

**Troubleshooting Tips:**

1. If you encounter “argument mismatch” errors, it’s a change in the gnu compiler’s behavior. Add `-fallow-argument-mismatch` to the compiler options in the config file.

1. If you see the error: “FATAL. Internal installation check failed: Main program (Aires) did not give expected output. Installation aborted,” it might be due to the external input file being misplaced. Move it to the directory containing 19-04-08 and rerun `doinstall 0`.

For more assistance, don’t hesitate to ask!
