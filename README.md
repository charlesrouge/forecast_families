This repository presents the source code, along with a Jupyter Notebook demo, for the "forecast families" methodology 
presented in the paper by C. Rougé, A. Peñuela and F. Pianosi:
"Forecast families: a new method to systematically evaluate the benefits of improving the skill of an existing forecast"
published to the Journal of Water Resources Planning and Management at doi:10.1061/JWRMD5.WRENG-5934

Refer to the Jupyter Notebook `Forecast_families_demo.ipynb` to generate and visualize forecast families.

The library is built exclusively using Python code; a list of all the necessary libraries and their versions is 
available in environment file `forecast_families.yml`. To create this environment on your end, you simply need to run:
`conda env create --file forecast_families.yml`

Sub-directories:

=> `src` contains the code for generating forecast families. Ensemble and deterministic families are generated with 
`ensemble.py` and `deterministic.py`, respectively.

=> `test` contains a test function for the forecast family generation workflow(s). Run with 
`pytest test/test_worflow.py` from main directory.

=> `data` contains the bias-corrected forecast ensemble displayed in Figure 3 of the paper, and uses that data to 
demonstrate the method. As you run the Notebook, other data (taken from the iRONS toolbox available at  
`https://github.com/iRONStoolbox/iRONStoolbox`, by Peñuela et al., 2021 at doi:10.1016/j.envsoft.2021.105188)) will
 populate the folder.

=> other directories are created when running the Notebook: 
`example_results` when running Part 1 on the example data.
`ECMWF_families` when running Part 2 on automated generation of forecast families from ECMWF hindcast.
