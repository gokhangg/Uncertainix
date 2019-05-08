This project is intended to be used for image registration uncertainty estimation caused by registration hyper-parameters. 
It comprises of two different approaches for getting the uncertainty estimates: Monte-Carlo (MC) simulation and Polynomial Chaos Expansion (PCE).
The PCE part is predicated upon a Matlab toolbox named as OpenPCE [1,2] and extended for registration uncertainty estimation. 
The PCE part also requires compilation of Matlab codes to an executable which handles all the issues regarding the PCE uncertainty estimates.
Uncertainix automatically handle this compilation process provided that you have Matlab runtime on your computer and compiler installed.
There are two test files for both MC and PCE approaches, and take them as starting points to understand how the library works.
Currently, the project lacks a nice documentation about the codes, but it will soon be uploaded. 
We also plan to give Matlab compiled executables for Windows and Linux and then the project will only require installation of Matlab runtime libraries.
In the repository, we also added 30 simulated images and using them you can run your experiments and inspect how the codes work.

[1] Perkó, Zoltán, et al. "Fast and accurate sensitivity analysis of IMPT treatment plans using Polynomial Chaos Expansion." Physics in medicine and biology 61.12 (2016): 4646.
[2] Van Der Voort, Sebastian, et al. "Robustness recipes for minimax robust optimization in intensity modulated proton therapy for oropharyngeal cancer patients." International Journal of Radiation Oncology* Biology* Physics 95.1 (2016): 163-170.
