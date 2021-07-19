This is a draft implementation of the generation of forecast families. It is tailored to the forecast file format from 
ECMWF, as presented in the iRONS toolbox by Andrés Peñuela and Francesca Pianosi (2020) at 
https://github.com/AndresPenuela/iRONS

Files and sub-directories:

=> `src` contains the code for generating forecast families, along with all the necessary information on input variables

=> `test` contains a test function for the forecast family generation workflow(s). Run with 
`pytest test/test_worflow.py` from main directories

=> `draft` contains old files used for a draft implementation (not relevant any more, will clean up later)

=> `example_implementation.py` contains basic code for the generation of forecast families.
