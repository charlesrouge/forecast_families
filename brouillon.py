from src.deterministic import deterministic_family
from src.ensemble import ensemble_family
import numpy as np
import pandas as pd

main_dir = '../../iRONS/iRONS/Notebooks/B - Implementation/Inputs/'
datafile = main_dir + 'hist_clim_data.csv'
forecast_folder = main_dir + 'ECMWF forecasts csv/'
var_name = ['Rain', 'Rain']
family_destination = 'families/'
skill_values = np.linspace(0, 1, 11)
beg_date = '1981/1/1'
end_date = '1981/1/1'

deterministic_family(datafile, forecast_folder, var_name, family_destination, skill_values, beg_date, end_date, 'MSE')
#ensemble_family(datafile, forecast_folder, var_name, family_destination, skill_values, beg_date, end_date)

temp_forecast = pd.DataFrame({'Date': ['1/1/1969', '2/1/1969', '3/1/1969'],
                                  '1': [1.5, 0.5, -1.0],
                                  '2': [2.0, 1.0, 3.0],
                                  '3': [2.5, 0.0, 1.0]})

rain_forecast = pd.DataFrame({'Date': ['1/1/1969', '2/1/1969', '3/1/1969'],
                                  '1': [2.5, 4.0, 4.0],
                                  '2': [3.0, 5.0, 9.0],
                                  '3': [3.5, 4.5, 6.5]})

print(temp_forecast.values[:, 0])
#print(np.allclose(temp_forecast.values[:, 0], rain_forecast.values[:, 0]))

