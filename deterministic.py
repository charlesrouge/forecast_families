import pandas as pd
import numpy as np
import math


def deterministic_family(hist_file, forecast_folder, forecast_file_key, variable_name, family_folder, skill_values,
                         begin_date, end_date, mase):

    # Read data from iRONS

    # Historical data
    hist_all = pd.read_csv(hist_file, index_col=0)
    hist_all.index = pd.to_datetime(np.array(hist_all.index), format='%d/%m/%Y')

    # List dates for forecasts to pull
    date_list = pd.date_range(start=begin_date, end=end_date, freq='MS')

    # Loop on forecast dates
    for t in date_list:

        # Read forecast data
        fore_data = pd.read_csv(forecast_folder + '/' + str(10000*t.year + 100*t.month + t.day) + forecast_file_key +
                                variable_name + '.csv', index_col=0)
        fore_data.index = pd.to_datetime(np.array(fore_data.index), format='%d/%m/%Y')

        # Define deterministic forecast using the ensemble average
        fore_det = pd.Series(data=fore_data.mean(axis=1), index=fore_data.index, name='Forecast ' + variable_name +
                             ': average')

        # Get the historical data that corresponds to the forecast period
        hist_data = pd.Series(hist_all.loc[fore_data.index][variable_name])

        # Build forecast family
        family = pd.DataFrame(data=None, index=fore_det.index)

        for i in range(len(skill_values)):

            skill = skill_values[i]

            if mase == 'MAE':
                k = 1 - skill
            elif mase == 'MSE':
                k = math.sqrt(1 - skill)
            else:
                raise ValueError("input variable 'mase' must be a string with values 'MAE' or 'MSE'")

            family.insert(i, column='S=' + str(skill), value=(1-k) * hist_data.values + k * fore_det.values)

        family.to_csv(path_or_buf=family_folder + '/' + str(10000*t.year + 100*t.month + t.day) + forecast_file_key +
                      variable_name + '_' + mase + '_Family.csv')

    return None
