import pandas as pd
import numpy as np
import os
import shutil

import sys
sys.path.append('../')
sys.path.append('.')

from src.deterministic import deterministic_family
from src.ensemble import ensemble_family

"""
Test with pytest from main directory: enter in command line `pytest test/test/workflow.py`
"""


def test_workflow():

    # Local variables
    mydir = 'workflow_data'
    datafile = mydir + '/clim_data.csv'
    forecast_dir = mydir + '/original_forecasts/'
    family_dir = mydir + '/families/'
    skill_values = np.linspace(0, 1, 3)
    skill_values_mse = [0, 0.75, 1]
    beg_end_date = '1969/1/1'

    # Create directories for test data
    if os.path.exists(mydir) is False:
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
    cumulative_rain =[2.0, 4.0, 6.0]

    # temperature forecast
    temp_forecast = pd.DataFrame({'Date': ['1/1/1969', '2/1/1969', '3/1/1969'],
                                  '1': [1.5, 0.5, -1.0],
                                  '2': [2.0, 1.0, 3.0],
                                  '3': [2.5, 0.0, 1.0]})
    temp_forecast = temp_forecast.set_index('Date')
    temp_forecast.to_csv(path_or_buf=forecast_dir + '19690101_1d_7m_ECMWF_Temp.csv')
    temp_fore_avg = pd.Series(data=temp_forecast.mean(axis=1), index=temp_forecast.index, name='Forecast Temp: average')

    # rainfall forecast
    rain_forecast = pd.DataFrame({'Date': ['1/1/1969', '2/1/1969', '3/1/1969'],
                                  '1': [2.5, 4.0, 4.0],
                                  '2': [3.0, 5.0, 9.0],
                                  '3': [3.5, 4.5, 6.5]})
    rain_forecast = rain_forecast.set_index('Date')
    rain_forecast.to_csv(path_or_buf=forecast_dir + '19690101_1d_7m_ECMWF_Rain.csv')
    rain_fore_avg = pd.Series(data=rain_forecast.mean(axis=1), index=rain_forecast.index, name='Forecast Rain: average')

    # Create output files
    deterministic_family(datafile, forecast_dir, ['Temp', 'Temp'], family_dir, skill_values, beg_end_date, beg_end_date,
                         'MAE')
    deterministic_family(datafile, forecast_dir, ['Rain', 'Rain'], family_dir, skill_values, beg_end_date, beg_end_date,
                         'MAE')
    deterministic_family(datafile, forecast_dir, ['Temp', 'Temp'], family_dir, skill_values_mse, beg_end_date,
                         beg_end_date, 'MSE')
    deterministic_family(datafile, forecast_dir, ['Rain', 'Rain'], family_dir, skill_values_mse, beg_end_date,
                         beg_end_date, 'MSE')
    ensemble_family(datafile, forecast_dir, ['Temp', 'Temp'], family_dir, skill_values, beg_end_date, beg_end_date)
    ensemble_family(datafile, forecast_dir, ['Rain', 'Rain'], family_dir, skill_values, beg_end_date, beg_end_date)

    # Test MAE temp
    family_to_test = pd.read_csv(family_dir + '19690101_1d_7m_ECMWF_Temp_MAE_Family.csv', index_col=0)
    deterministic_family_testing(family_to_test, hist_data['Temp'].values[1:4], temp_fore_avg)

    # Test MAE rain
    family_to_test = pd.read_csv(family_dir + '19690101_1d_7m_ECMWF_Rain_MAE_Family.csv', index_col=0)
    deterministic_family_testing(family_to_test, cumulative_rain, rain_fore_avg)

    # Test MSE Temp
    family_to_test = pd.read_csv(family_dir + '19690101_1d_7m_ECMWF_Temp_MSE_Family.csv', index_col=0)
    deterministic_family_testing(family_to_test, hist_data['Temp'].values[1:4], temp_fore_avg)

    # Test MSE rain
    family_to_test = pd.read_csv(family_dir + '19690101_1d_7m_ECMWF_Rain_MSE_Family.csv', index_col=0)
    deterministic_family_testing(family_to_test, cumulative_rain, rain_fore_avg)

    # Test CRPSS, skill = 0
    family_to_test = pd.read_csv(family_dir + 'ECMWF_Ensemble_Skill_CRPSS=0.0/19690101_1d_7m_ECMWF_Temp.csv',
                                 index_col=0)
    np.testing.assert_array_almost_equal(family_to_test.values, temp_forecast.values, decimal=6)
    family_to_test = pd.read_csv(family_dir + 'ECMWF_Ensemble_Skill_CRPSS=0.0/19690101_1d_7m_ECMWF_Rain.csv',
                                 index_col=0)
    np.testing.assert_array_almost_equal(family_to_test.values, rain_forecast.values, decimal=6)

    # Test CRPSS, skill = 0.5
    family_to_test = pd.read_csv(family_dir + 'ECMWF_Ensemble_Skill_CRPSS=0.5/19690101_1d_7m_ECMWF_Temp.csv',
                                 index_col=0)
    for i in range(family_to_test.shape[1]):
        np.testing.assert_array_almost_equal(family_to_test.values[:, i], (hist_data['Temp'].values[1:4] +
                                                                           temp_forecast.values[:, i]) / 2, decimal=6)
    family_to_test = pd.read_csv(family_dir + 'ECMWF_Ensemble_Skill_CRPSS=0.5/19690101_1d_7m_ECMWF_Rain.csv',
                                 index_col=0)
    for i in range(family_to_test.shape[1]):
        np.testing.assert_array_almost_equal(family_to_test.values[:, i], (cumulative_rain +
                                                                           rain_forecast.values[:, i]) / 2, decimal=6)

    # Test CRPSS, skill = 1
    family_to_test = pd.read_csv(family_dir + 'ECMWF_Ensemble_Skill_CRPSS=1.0/19690101_1d_7m_ECMWF_Temp.csv',
                                 index_col=0)
    for i in range(family_to_test.shape[1]):
        np.testing.assert_array_almost_equal(family_to_test.values[:, i], hist_data['Temp'].values[1:4], decimal=6)
    family_to_test = pd.read_csv(family_dir + 'ECMWF_Ensemble_Skill_CRPSS=1.0/19690101_1d_7m_ECMWF_Rain.csv',
                                 index_col=0)
    for i in range(family_to_test.shape[1]):
        np.testing.assert_array_almost_equal(family_to_test.values[:, i], cumulative_rain, decimal=6)

    # Cleanup (optional)
    shutil.rmtree('workflow_data')

    return None

def deterministic_family_testing(family, data_nparray, forecast):
    np.testing.assert_array_almost_equal(family.values[:, 0], forecast.values, decimal=6)
    np.testing.assert_array_almost_equal(family.values[:, 2], data_nparray, decimal=6)
    np.testing.assert_array_almost_equal(family.values[:, 1], (forecast.values + data_nparray) / 2, decimal=6)
    return None
