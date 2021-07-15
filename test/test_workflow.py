import pandas as pd
import numpy as np
import os
import shutil

import sys
sys.path.append('../')
sys.path.append('.')

from src.deterministic import deterministic_family
from src.ensemble import ensemble_family


def test_workflow():

    # Local variables
    mydir = 'workflow_data'
    datafile = mydir + '/clim_data.csv'
    forecast_dir = mydir + '/original_forecasts/'
    family_dir = mydir + '/families/'
    skill_values = np.linspace(0, 1, 3)
    beg_end_date = '1969/1/1'

    # Create directories for test data
    os.mkdir(mydir)
    os.mkdir(forecast_dir)
    os.mkdir(family_dir)

    # Define test data

    # historical data
    hist_data = pd.DataFrame({'Date': ['31/12/1968', '1/1/1969', '2/1/1969', '3/1/1969', '4/1/1969'],
                              'Temp': [1.0, 1.0, 1.0, 1.0, 1.0],
                              'Rain': [2.0, 2.0, 2.0, 2.0, 2.0]})
    hist_data = hist_data.set_index('Date')
    hist_data.to_csv(path_or_buf=datafile)

    # temperature forecast
    temp_forecast = pd.DataFrame({'Date': ['1/1/1969', '2/1/1969', '3/1/1969'],
                                  '1': [1.5, 0.5, -1.0],
                                  '2': [2.0, 1.0, 3.0],
                                  '3': [2.5, 0.0, 1.0]})
    temp_forecast = temp_forecast.set_index('Date')
    temp_forecast.to_csv(path_or_buf=forecast_dir + '19690101_1d_7m_ECMWF_Temp.csv')
    temp_fore_avg = pd.Series(data=temp_forecast.mean(axis=1), index=temp_forecast.index, name='Forecast ' +
                              'Temp: average')

    # rainfall forecast
    rain_forecast = pd.DataFrame({'Date': ['1/1/1969', '2/1/1969', '3/1/1969'],
                                  '1': [2.5, 4.0, 4.0],
                                  '2': [3.0, 5.0, 9.0],
                                  '3': [3.5, 4.5, 6.5]})
    rain_forecast = rain_forecast.set_index('Date')
    rain_forecast.to_csv(path_or_buf=forecast_dir + '19690101_1d_7m_ECMWF_Rain.csv')

    # Create output files
    deterministic_family(datafile, forecast_dir, ['Temp', 'Temp'], family_dir, skill_values, beg_end_date, beg_end_date,
                         'MAE')
    deterministic_family(datafile, forecast_dir, ['Rain', 'Rain'], family_dir, skill_values, beg_end_date, beg_end_date,
                         'MAE')
    deterministic_family(datafile, forecast_dir, ['Temp', 'Temp'], family_dir, skill_values, beg_end_date, beg_end_date,
                         'MSE')
    deterministic_family(datafile, forecast_dir, ['Rain', 'Rain'], family_dir, skill_values, beg_end_date, beg_end_date,
                         'MSE')
    ensemble_family(datafile, forecast_dir, ['Temp', 'Temp'], family_dir, skill_values, beg_end_date, beg_end_date)
    ensemble_family(datafile, forecast_dir, ['Rain', 'Rain'], family_dir, skill_values, beg_end_date, beg_end_date)

    # Testing
    temp_mae_family = pd.read_csv(family_dir + '19690101_1d_7m_ECMWF_Temp_MAE_Family.csv', index_col=0)
    assert np.sum(temp_mae_family.values[:, 0] - temp_fore_avg.values) == 0

    # Cleanup (optional)
    shutil.rmtree('workflow_data')

    return None
