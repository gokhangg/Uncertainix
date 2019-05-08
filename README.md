This project is intended to be used for image registration uncertainty estimation caused by registration hyper-parameters. 
It comprises of two different approaches for getting the uncertainty estimates: Monte-Carlo (MC) simulation and Polynomial Chaos Expansion (PCE).
The PCE part is predicated upon a Matlab toolbox named as OpenPCE and extended for registration uncertainty estimation. 
The PCE part also requires compilation of Matlab codes to an executable which handles all the issues regarding the PCE uncertainty estimates.
Uncertainix automatically handle this compilation process provided that you have Matlab runtime on your computer and compiler installed.
There are two test files for both MC and PCE approaches, and take them as starting points to understand how the library works.
Currently, the project lacks a nice documentation about the codes, but will soon be uploaded. 
We also plan to give Matlab compiled executables for Windows and Linux and then the project will only require installation of Matlab 
runtime libraries.
