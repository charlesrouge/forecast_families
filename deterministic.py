import pandas as pd
import numpy as np


def deterministic_family(hist_file, forecast_folder, forecast_file_key, variable_name, family_folder, skill_values, begin_date,
                         end_date, mase):

    # Read data from iRONS
    hist_all = pd.read_csv(hist_file, index_col=0)
    hist_all.index = pd.to_datetime(np.array(hist_all.index), format='%d/%m/%Y')

    for t in range

    return None



def error(data, forecast):
    error = data-forecast
    error.name = 'Deterministic error for ' + data.name
    return error