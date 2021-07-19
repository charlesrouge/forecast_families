from src.deterministic import deterministic_family
from src.ensemble import ensemble_family
import numpy as np
import os

"""
The below defines all input variables needed by the forecast family generation functions (see their meaning in 
`src/ensemble.py` and `src/determinisic.py`) and calls them.

NOTE: you need to call the function different times for different variables

The ensemble implementation creates a family of directories that are organised 

In the deterministic implementation, families are put in the same file instead, but this can be modified to be 
identical to the ensemble implementation.
"""

main_dir = '../../iRONS/iRONS/Notebooks/B - Implementation/Inputs/'
datafile = main_dir + 'hist_clim_data.csv'
forecast_folder = main_dir + 'ECMWF forecasts csv/'
var_name = ['PET', 'Evap']
family_destination = 'families/'
if os.path.exists(family_destination) is False:
    os.mkdir(family_destination)
if os.path.exists(family_destination + 'deterministic/') is False:
    os.mkdir(family_destination + 'deterministic/')
skill_values = np.linspace(0, 1, 11)
beg_date = '1981/1/1'
end_date = '2015/05/01'

# Ensembles (skill: CRPSS)
ensemble_family(datafile, forecast_folder, var_name, family_destination, skill_values, beg_date, end_date)

# MAE (deterministic)
deterministic_family(datafile, forecast_folder, var_name, family_destination + '/deterministic/', skill_values,
                     beg_date, end_date, 'MAE')

# MSE (deterministic)
deterministic_family(datafile, forecast_folder, var_name, family_destination + '/deterministic/', skill_values,
                     beg_date, end_date, 'MSE')
