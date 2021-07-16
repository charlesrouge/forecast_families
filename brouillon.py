from src.deterministic import deterministic_family
from src.ensemble import ensemble_family
import numpy as np
import os

main_dir = '../../iRONS/iRONS/Notebooks/B - Implementation/Inputs/'
datafile = main_dir + 'hist_clim_data.csv'
forecast_folder = main_dir + 'ECMWF forecasts csv/'
var_name = ['PET', 'Evap']
family_destination = 'families/'
if os.path.exists(family_destination) is False:
    os.mkdir(family_destination)
    os.mkdir(family_destination + 'deterministic/')
skill_values = np.linspace(0, 1, 11)
beg_date = '1981/1/1'
end_date = '2015/05/01'

# Ensembles (skill: CRPSS)
ensemble_family(datafile, forecast_folder, var_name, family_destination, skill_values, beg_date, end_date)

# MAE (deterministic)
deterministic_family(datafile, forecast_folder, var_name, family_destination + '/deterministic/', skill_values, beg_date, end_date, 'MAE')

# MSE (deterministic)
deterministic_family(datafile, forecast_folder, var_name, family_destination + '/deterministic/', skill_values, beg_date, end_date, 'MSE')




