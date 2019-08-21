EPICPY is a toolbox for the creation and evaluation of Polynomial Chaos Expansions

QUICK START
----------------

To use EPICPY to make the PCE of a problem two things need to be provided: A settings file and a matlab function to interface with the 'blackbox'

The settings file is .json file, an example is provided in the settings folder. 

the corresponding matlab inteface can be found in Blackbox/Functions/example_problem.m

An example on how to run this problem is found in ExampleRun.m

NOTATION
----------------

The code has some notation specifications:
- functions, variables start with a lower case letter, structures start with a upper case letter.
- There are a few shorthands used for easier reading:
	- N: Number of
	- u: unique
	- I: index of
	- LI: logical index of
	- i: i-th element of (used in iterations)
  For example the variable N_dims means: Number of dimensions. 
  These shorthands can also be combined, e.g. N_u_pol_types means the number of unique polynomial types.




