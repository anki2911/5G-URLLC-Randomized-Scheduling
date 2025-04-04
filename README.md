# 5G-URLLC-Schedule Randomization

This repository contains the source code of 5G URLLC random schedule generation procedure. This schedule generation phase runs at the 5G base station. Given a set of n flows (utilization between 40%-70% and 70%-100%), m frequencies (2,3,4 frequencies), a sub-carrier spacing (SCS = 15KHz and SCS = 30KHz), and '\alpha' (0.1, 0.3, 0.5) fraction of the slots in the frequency, this scheduler runs online and generates random feasible schedules in each hyperperiod. The codes for the EDF based randomization and the period based randomization are given in EDF_Randomization.py and PFair.py respectively. 

More details about the implementation are available in "Online Schedule Randomization to Mitigate Timing Attacks in 5G Periodic URLLC Communications". Link to the paper : https://dl.acm.org/doi/full/10.1145/3600093
