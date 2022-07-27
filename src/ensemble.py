import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


def generate_family(observations, forecast_ensemble, skill_values, family_folder, different_folders, output_filename):

    # Loop on skill values
    for i in range(len(skill_values)):

        # Compute multiplier k
        k = 1 - skill_values[i]

        # Member of the forecast family for this skill level
        family_member = pd.DataFrame(data=None, index=forecast_ensemble.index)
        for j in range(forecast_ensemble.shape[1]):
            family_member.insert(j, column=forecast_ensemble.columns[j],
                                 value=(1 - k) * observations.values + k * forecast_ensemble.values[:, j])

        if different_folders is True:
            skill_folder = family_folder + str("%.2f" % skill_values[i])
            if os.path.exists(skill_folder) is False:
                os.mkdir(skill_folder)
            family_member.to_csv(path_or_buf=skill_folder + '/' + output_filename + '.csv')
        else:
            if os.path.exists(family_folder) is False:
                os.mkdir(family_folder)
            family_member.to_csv(path_or_buf=family_folder + '/' + output_filename + '_' +
                                 str("%03d" % int(100*skill_values[i])) + '.csv')

    return None


def plot_ensemble_family(hist_file, forecast_path, family_path, var_names, destination):

    """
    This function plots the difference between observations and  forecast ensemble for different values of the skill,
    with forecasts generated from a benchmark using the forecast family method.
    NOTE: this function only supports skill of an ensemble forecast based on CRPSS (continuous rank probability
    skill score)
    :param hist_file: string, the path to observations
    :param forecast_path: string, the path to the benchmark forecast
    :param var_names: string vector length 2, the names of the forecast quantity, both in observations and forecast data
    :param destination: string, destination folder of the figures
    :return: the function saves the resulting figures in PNG format
    """

    # Read original forecast (which is also the zero-skill family member)
    benchmark_forecast = pd.read_csv(forecast_path + '.csv', index_col=0)
    benchmark_forecast.index = pd.to_datetime(np.array(benchmark_forecast.index), format='%Y/%m/%d')
    benchmark_stats = pd.DataFrame({'min': benchmark_forecast.min(axis=1),
                                    'mean': benchmark_forecast.mean(axis=1),
                                    'max': benchmark_forecast.max(axis=1)}, index=benchmark_forecast.index)

    # Get first day of months
    date_list = pd.date_range(start=benchmark_forecast.index[0], periods=8, freq='MS')
    date_label = ['N', 'D', 'J', 'F', 'M', 'A', 'M', 'J']

    # Read historical data
    hist_all = pd.read_csv(hist_file, index_col=0)
    hist_all.index = pd.to_datetime(np.array(hist_all.index), format='%d/%m/%Y')
    # Get the historical data that corresponds to the forecast period
    hist_data = pd.Series(hist_all.loc[benchmark_forecast.index][var_names[0]])
    # For precipitation and evaporation: historical data needs to be turned into a cumulative sum
    if var_names[0] == 'Rain' or var_names[0] == 'PET':
        hist_data = hist_data.cumsum()

    # Figures
    for i in np.arange(0, 12, 2):

        # Initialise figure
        fig = plt.figure(figsize=(6.7, 5))
        ax = fig.add_subplot(1, 1, 1)
        handles = []

        hb, = ax.plot(benchmark_forecast.index, benchmark_stats.loc[:, 'mean'], alpha=.2, color='black',
                      label='Benchmark')
        ax.fill_between(benchmark_forecast.index, benchmark_stats.loc[:, 'mean'], benchmark_stats.loc[:, 'max'],
                        alpha=.2, color='black')
        ax.fill_between(benchmark_forecast.index, benchmark_stats.loc[:, 'min'], benchmark_stats.loc[:, 'mean'],
                        alpha=.2, color='black')

        # Read current forecast
        if i == 10:
            modified_forecast = hist_data
        else:
            modified_forecast = pd.read_csv(family_path + str(i) + '.csv', index_col=0)
            modified_forecast.index = pd.to_datetime(np.array(benchmark_forecast.index), format='%Y/%m/%d')

        # Plot current forecast vs. observed data
        if i != 10:
            hf, = ax.plot(modified_forecast.index, modified_forecast.iloc[:, 0], c='red', linewidth=0.5,
                          label='Forecast')
            ax.plot(modified_forecast, c='red', linewidth=0.5)
        h, = ax.plot(benchmark_forecast.index, hist_data, c='blue', label='Observations', linewidth=2)
        handles.append(h)
        handles.append(hb)
        handles.append(hf)

        # Wrap up
        ax.set_xlabel('Date', size=14)
        ax.xaxis.set_ticks(date_list)
        ax.xaxis.set_ticklabels(date_label)
        ax.tick_params(labelsize=14)
        ax.set_xlim(benchmark_forecast.index[0], benchmark_forecast.index[-1])
        ax.set_ylabel('Cumulative rainfall (mm)', size=14)
        if i == 0:
            ax.legend(handles=handles, loc=2, prop={'size': 16})
        ax.set_title('(' + chr(ord('`')+int(float(i)/2.0+1)) + ') CRPSS=' + str(float(i) / 10), size=18)

        # Figure save
        if os.path.exists(destination + '/ensemble_family') is False:
            os.mkdir(destination + '/ensemble_family')
        fig.savefig(destination + '/ensemble_family/family_CRPSS=' + str(float(i) / 10) + '.png')
        fig.clf()

    return None


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

    # List dates for forecasts to pull
    date_list = pd.date_range(start=begin_date, end=end_date, freq='MS')

    # Read historical data
    hist_all = pd.read_csv(history_file, index_col=0)
    hist_all.index = pd.to_datetime(np.array(hist_all.index), format='%d/%m/%Y')

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

        # Generate forecast family after specifying outputs (True for different folders)
        full_family_folder = family_folder + '/ECMWF_Ensemble_skill_CRPSS='
        output_name = str(10000*t.year + 100*t.month + t.day) + '_1d_7m_ECMWF_' + variable_names[1]
        generate_family(hist_data, fore_data, skill_values, full_family_folder, True, output_name)

    return None


def plot_ensemble(hist_file, variable_names, family_folder, skill_values, date):

    # Read historical data
    hist_all = pd.read_csv(hist_file, index_col=0)
    hist_all.index = pd.to_datetime(np.array(hist_all.index), format='%d/%m/%Y')

    num_fig = len(skill_values)

    fig,ax = plt.subplots(ncols=num_fig, nrows=1, figsize=(6*num_fig, 6))

    return None
