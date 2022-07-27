import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import os


def generate_family(observations, fore_det, skill_values, skill_name):

    # Define forecast family
    family = pd.DataFrame(data=None, index=fore_det.index)

    # Build forecast family
    for i in range(len(skill_values)):

        skill = skill_values[i]

        # Convert skill to multiplier k
        if skill_name == 'MAE':
            k = 1 - skill
        elif skill_name == 'MSE':
            k = math.sqrt(1 - skill)
        else:
            raise ValueError("input variable 'mase' must be a string with values 'MAE' or 'MSE'")

        family.insert(i, column='S=' + str(skill), value=(1 - k) * observations.values + k * fore_det.values)

    return family


def plot_det_family(history_file, benchmark_path, var_names, skill_name, skill_specs, destination):

    """
        This function plots the difference between observations and ensemble average (taken as deterministic forecasts)
        for different values of the skill, with forecasts generated from a benchmark using the forecast family method.

        NOTE: this function only supports skill of a deterministic forecast based on MAE (mean absolute error) or
        MSE (mean squared error)

        :param history_file: string, the path to observations
        :param benchmark_path: string, the path to the benchmark forecast
        :param var_names: string vector length 2, the names of the forecast quantity, both in observations and forecast data
        :param skill_name: string, the name of the metric upon which skill is based ('MAE' or 'MSE')
        :param skill_specs: Pandas DataFrame that contains the list of skills but also info to plot them
        :param destination: string, destination folder of the figures
        :return: the function saves the resulting figure in PNG format
        """

    # Read original forecast (which is also the zero-skill family member)
    benchmark_ensemble = pd.read_csv(benchmark_path, index_col=0)
    benchmark_ensemble.index = pd.to_datetime(np.array(benchmark_ensemble.index), format='%Y/%m/%d')
    benchmark_forecast = pd.Series(benchmark_ensemble.mean(axis=1))

    # Read historical data
    hist_all = pd.read_csv(history_file, index_col=0)
    hist_all.index = pd.to_datetime(np.array(hist_all.index), format='%d/%m/%Y')
    # Get the historical data that corresponds to the forecast period
    hist_data = pd.Series(hist_all.loc[benchmark_forecast.index][var_names[0]])

    # For precipitation and evaporation: historical data needs to be turned into a cumulative sum
    if var_names[0] == 'Rain' or var_names[0] == 'PET':
        hist_data = hist_data.cumsum()

    print(skill_specs['value'].values)

    # Compute the forecast family
    family = generate_family(hist_data, benchmark_forecast, skill_specs.loc[:, 'value'], skill_name)

    # Rename the columns
    family.columns = skill_specs.loc[:, 'stringvalue']

    # Plot the figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    h, = ax.plot(family.index, hist_data, c='gold', linewidth=2, label='Observations')
    first_legend = ax.legend(handles=[h], loc=2)
    ax.add_artist(first_legend)
    handles = []
    for i in skill_specs.index:
        h, = ax.plot(family.index, family.iloc[:, i], c=skill_specs.loc[i, 'color'],
                     linestyle=skill_specs.loc[i, 'linestyle'], label=skill_specs.loc[i, 'stringvalue'])
        handles.append(h)

    # X-axis labels
    date_list = pd.date_range(start=benchmark_forecast.index[0], periods=8, freq='MS')
    all_date_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', 'J', 'F', 'M', 'A', 'M', 'J', 'J']
    date_label = all_date_labels[date_list[0].month - 1: date_list.month + 7]
    print(date_label)
    ax.xaxis.set_ticks(date_list)
    ax.xaxis.set_ticklabels(date_label)

    # Figure title
    if skill_name == 'MAE':
        title_figure = '(a) Skill based on MAE'
    elif skill_name == 'MSE':
        title_figure = '(b) Skill based on MSE'
    ax.set_title(title_figure, size=16)

    # Other figure specs
    ax.set_xlabel('Date', size=14)
    ax.set_xlim(family.index[0], family.index[-1])
    ax.set_ylabel('Cumulative rainfall error (mm)', size=14)
    ax.legend(handles=handles, title='Forecasts by skill value', loc=4)

    # Figure save
    if os.path.exists(destination + '/deterministic_family') is False:
        os.mkdir(destination + '/deterministic_family')
    fig.savefig(destination + '/deterministic_family/family_errors_' + skill_name + '.png')
    fig.clf()

    return None


def ecmwf_deterministic_family(history_file, forecast_folder, variable_names, family_folder, skill_val, begin_date,
                               end_date, mase):

    """ For the specified range of dates, this function creates deterministic forecast families from existing
        ECMWF forecasts.
        It then saves the resulting forecast families in a CSV file for each exisiting forecast

        WARNING 1: only works for monthly forecasts. For a different time interval between forecast, modify first line

        WARNING 2: produces deterministic forecast as ensemble average only.
        This needs modifying if you want something else.

        inputs = (history_file, forecast_folder, variable_name, family_folder, skill_val, begin_date, end_date, mase)

        history_file        = Full path to file with historical data for which we have the forecasts
        forecast_folder     = Path to the folder where the forecasts are. Enter as string.
        variable_names      = String duplet with the name of the variable both in historical data and forecasts
        family_folder       = Folder where to save outputs. Enter as string.
        skill_val           = 1-D Numpy array with the desired skill values (typically between 0 and 1).
        begin_date          = date at which we start making families from available forecasts. Format 'YYYY/MM/DD'
        end_date            = date after which we stop making families from available forecasts. Format 'YYYY/MM/DD'
        mase                = The performance metric used to compute the skill: string 'MAE' or 'MSE'

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

        # Define deterministic forecast using the ensemble average
        deterministic_forecast = pd.Series(data=fore_data.mean(axis=1), index=fore_data.index, name='Forecast ' +
                                           variable_names[1] + ': average')

        # Get the historical data that corresponds to the forecast period
        hist_data = pd.Series(hist_all.loc[fore_data.index][variable_names[0]])

        # For precipitation and evaporation: historical data needs to be turned into a cumulative sum
        if variable_names[0] == 'Rain' or variable_names[0] == 'PET':
            hist_data = hist_data.cumsum()

        # Generate the desired deterministic forecast family
        family = generate_family(hist_data, deterministic_forecast, skill_val, mase)

        # Save family to CSV
        family.to_csv(path_or_buf=family_folder + '/' + str(10000*t.year + 100*t.month + t.day) + '_1d_7m_ECMWF_' +
                      variable_names[1] + '_' + mase + '_Family.csv')

    return None
