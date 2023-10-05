# 5G-URLLC-Randomized-Scheduling

This repository contains the source code of 5G URLLC random schedule generation procedure. This schedule generation phase runs at the 5G base station. Given a set of n flows, m frequencies, a sub-carrier spacing, and '\alpha' fraction of the slots in the frequency, this scheduler runs online and generates random feasible schedules in each hyperperiod. The codes for the EDF based randomization and the period based randomization are given in EDF_Randomization.py and PFair.py respectively. 
Details of the implementation are given in the paper. Link to the paper : https://dl.acm.org/doi/full/10.1145/3600093
