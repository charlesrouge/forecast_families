from deterministic import deterministic_family
from ensemble import ensemble_family
import numpy as np
import pandas as pd

main_dir = '../../iRONS/iRONS/Notebooks/B - Implementation/Inputs/'
datafile = main_dir + 'hist_clim_data.csv'
forecast_folder = main_dir + 'ECMWF forecasts csv/'
var_name = ['Rain', 'Rain']
family_destination = 'families/'
skill_values = np.linspace(0, 1, 5)
beg_date = '1981/1/10'
end_date = '1981/4/12'

#deterministic_family(datafile, forecast_folder, var_name, family_destination, skill_values, beg_date, end_date, 'MSE')
ensemble_family(datafile, forecast_folder, var_name, family_destination, skill_values, beg_date, end_date)
