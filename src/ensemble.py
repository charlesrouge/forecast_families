import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


def ecmwf_ensemble_family(history_file, forecast_folder, variable_names, family_folder, skill_values, begin_date,
                          end_date):

    """ This function creates families of new ensemble forecasts of desired skills from existing ensemble forecasts.
        It then saves the resulting forecast families in CSV files: 1 per forecast

        WARNING: this only works for monthly forecasts. For a different time interval between forecast, modify line XX

        inputs = (hist_file, forecast_folder, variable_name, family_folder, skill_values, begin_date, end_date, mase)

        history_file        = Full path to file with historical data for which we have the forecasts
        forecast_folder     = Path to the folder where the forecasts are. Enter as string.
        variable_names      = String duplet with the name of the variable both in historical data and forecasts
        family_folder       = Folder where to save outputs. Enter as string.
        skill_values        = 1-D Numpy array with the desired skill values (typically between 0 and 1).
        begin_date          = date at which we start making families from available forecasts. Format 'YYYY/MM/DD'
        end_date            = date after which we stop making families from available forecasts. Format 'YYYY/MM/DD'

        No output variable: output printed to file
    """

    # Read historical data
    hist_all = pd.read_csv(history_file, index_col=0)
    hist_all.index = pd.to_datetime(np.array(hist_all.index), format='%d/%m/%Y')

    # List dates for forecasts to pull
    date_list = pd.date_range(start=begin_date, end=end_date, freq='MS')

    # Loop on forecast dates
    for t in date_list:

        # Read forecast data
        fore_data = pd.read_csv(forecast_folder + '/' + str(10000*t.year + 100*t.month + t.day) + '_1d_7m_ECMWF_' +
                                variable_names[1] + '.csv', index_col=0)
        fore_data.index = pd.to_datetime(np.array(fore_data.index), format='%d/%m/%Y')

        # Get the historical data that corresponds to the forecast period
        hist_data = pd.Series(hist_all.loc[fore_data.index][variable_names[0]])

        # For precipitation and evaporation: historical data needs to be turned into a cumulative sum
        if variable_names[0] == 'Rain' or variable_names[0] == 'PET':
            hist_data = hist_data.cumsum()

        # Build forecast family
        for i in range(len(skill_values)):

            # Compute multiplier k
            k = 1 - skill_values[i]

            # Member of the forecast family for this skill level
            family_member = pd.DataFrame(data=None, index=fore_data.index)
            for j in range(fore_data.shape[1]):
                family_member.insert(j, column=fore_data.columns[j],
                                     value=(1 - k) * hist_data.values + k * fore_data.values[:, j])

            skill_folder = family_folder + '/ECMWF_Ensemble_skill_CRPSS=' + str("%.2f" % skill_values[i])
            if os.path.exists(skill_folder) is False:
                os.mkdir(skill_folder)

            family_member.to_csv(path_or_buf=skill_folder + '/' + str(10000*t.year + 100*t.month + t.day) +
                                 '_1d_7m_ECMWF_' + variable_names[1] + '.csv')

    return None


def plot_ensemble(hist_file, variable_names, family_folder, skill_values, date):

    # Read historical data
    hist_all = pd.read_csv(hist_file, index_col=0)
    hist_all.index = pd.to_datetime(np.array(hist_all.index), format='%d/%m/%Y')

    num_fig = len(skill_values)

    fig,ax = plt.subplots(ncols=num_fig, nrows=1, figsize=(6*num_fig, 6))

    return None
