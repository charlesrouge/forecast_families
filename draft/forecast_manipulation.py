import pandas as pd


def deterministic_improve(data, forecast, k):

    """ This function creates new deterministic forecast as linear combination of data and its existing forecast

    inputs = (data, forecast, k)

    data        = the time series being forecast
    forecast    = the deterministic forecast for that data
    k           = scaling factor of the error (forecast - data) between 0 and 1. 0 corresponds to a perfect forecast
                    whereas 1 is identical to the original forecast with no improvement
    """

    return (1-k)*data + k*forecast


def ensemble_improve(data, forecast, k):

    """ This function creates new ensemble forecast as linear combination of data and its existing forecast

    inputs = (data, forecast, k)

    data        = a Pandas Series object of the time series being forecast (a Serie
    forecast    = a Pandas DataFrame object of the ensemble forecast for that data
    k           = scaling factor of the error (forecast - data) between 0 and 1. 0 corresponds to a perfect forecast
                        whereas 1 is identical to the original forecast with no improvement
    """

    new_ensemble = pd.DataFrame(data=None, index=forecast.index)
    for i in range(forecast.shape[1]):
        new_ensemble.insert(i, column=forecast.columns[i], value=(1-k)*data.values+k*forecast.values[:,i])
    return new_ensemble


def ensemble_average(forecast_ensemble, variable_name):

    """ This function creates a new deterministic forecast as the average of an ensemble

    inputs = (forecast_ensemble, variable_name)

    forecast_ensemble   = a Pandas DataFrame with the ensemble forecast of interest
    variable_name       = the name of the variable being forecast
    """

    return pd.Series(data=forecast_ensemble.mean(axis=1), index=forecast_ensemble.index, name='Forecast ' +
                     variable_name + ': average')
