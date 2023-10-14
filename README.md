# 5G-URLLC-Randomized-Scheduling

This repository contains the source code of 5G URLLC random schedule generation procedure. This schedule generation phase runs at the 5G base station. Given a set of n flows (utilization between 40%-70% and 70%-100%), m frequencies (2,3,4 frequencies), a sub-carrier spacing (SCS = 15KHz and SCS = 30KHz), and '\alpha' (0.1, 0.3, 0.5) fraction of the slots in the frequency, this scheduler runs online and generates random feasible schedules in each hyperperiod. The codes for the EDF based randomization and the period based randomization are given in EDF_Randomization.py and PFair.py respectively. 

Details of the implementation are available in the paper. Link to the paper : https://dl.acm.org/doi/full/10.1145/3600093
