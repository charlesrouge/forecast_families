import pandas as pd
import numpy as np
import math


def deterministic_family(hist_file, forecast_folder, variable_names, family_folder, skill_values, begin_date, end_date,
                         mase):

    """ This function creates families of new deterministic forecasts of desired skills from existing forecast.
        It then saves the resulting forecast families in a CSV file for each exisiting forecast

        WARNING: this only works for monthly forecasts. For a different time interval between forecast, modify line 48

        inputs = (hist_file, forecast_folder, variable_name, family_folder, skill_values, begin_date, end_date, mase)

        hist_file           = Full path to file with historical data for which we have the forecasts
        forecast_folder     = Path to the folder where the forecasts are. Enter as string.
        variable_names      = String duplet with the name of the variable both in historical data and forecasts
        family_folder       = Folder where to save outputs. Enter as string.
        skill_values        = 1-D Numpy array with the desired skill values (typically between 0 and 1).
        begin_date          = date at which we start making families from available forecasts. Format 'YYYY/MM/DD'
        end_date            = date after which we stop making families from available forecasts. Format 'YYYY/MM/DD'
        mase                = The performance metric used to compute the skill: string 'MAE' or 'MSE'

        No output variable: output printed to file
    """

    # Read historical data
    hist_all = pd.read_csv(hist_file, index_col=0)
    hist_all.index = pd.to_datetime(np.array(hist_all.index), format='%d/%m/%Y')

    # List dates for forecasts to pull
    date_list = pd.date_range(start=begin_date, end=end_date, freq='MS')

    # Loop on forecast dates
    for t in date_list:

        # Read forecast data
        fore_data = pd.read_csv(forecast_folder + '/' + str(10000*t.year + 100*t.month + t.day) + '_1d_7m_ECMWF_' +
                                variable_names[1] + '.csv', index_col=0)
        fore_data.index = pd.to_datetime(np.array(fore_data.index), format='%d/%m/%Y')

        # Define deterministic forecast using the ensemble average
        fore_det = pd.Series(data=fore_data.mean(axis=1), index=fore_data.index, name='Forecast ' + variable_names[1] +
                             ': average')

        # Get the historical data that corresponds to the forecast period
        hist_data = pd.Series(hist_all.loc[fore_data.index][variable_names[0]])

        # For precipitation and evaporation: historical data needs to be turned into a cumulative sum
        if variable_names[0] == 'Rain' or variable_names[0] == 'PET':
            hist_data = hist_data.cumsum()

        # Define forecast family
        family = pd.DataFrame(data=None, index=fore_det.index)

        # Build forecast family
        for i in range(len(skill_values)):

            skill = skill_values[i]

            # Convert skill to multiplier k
            if mase == 'MAE':
                k = 1 - skill
            elif mase == 'MSE':
                k = math.sqrt(1 - skill)
            else:
                raise ValueError("input variable 'mase' must be a string with values 'MAE' or 'MSE'")

            family.insert(i, column='S=' + str(skill), value=(1-k) * hist_data.values + k * fore_det.values)

        # Save family to CSV
        family.to_csv(path_or_buf=family_folder + '/' + str(10000*t.year + 100*t.month + t.day) + '_1d_7m_ECMWF_' +
                      variable_names[1] + '_' + mase + '_Family.csv')

    return None
