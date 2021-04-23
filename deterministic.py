import pandas as pd


def error(data, forecast):
    error = data-forecast
    error.name = 'Deterministic error for ' + data.name
    return error