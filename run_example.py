import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

main_dir = '../../iRONS/iRONS/Notebooks/B - Implementation/Inputs/'

# Read data from iRONS
hist_all = pd.read_csv(main_dir + 'hist_clim_data.csv', index_col=0)
hist_all.index = pd.to_datetime(np.array(hist_all.index), format = '%d/%m/%Y')

# Read forecast data
variable_name = 'Temp'
fore_data = pd.read_csv(main_dir + 'ECMWF forecasts csv/20141101_1d_7m_ECMWF_' + variable_name + '.csv', index_col=0)
fore_data.index = pd.to_datetime(np.array(fore_data.index), format = '%d/%m/%Y')

# Get data that corresponds to the forecast
hist_data = pd.Series(hist_all.loc[fore_data.index][variable_name])
# hist_data = hist_data.cumsum()

# Get average forecast (non bias corrected)
fore_avg = pd.Series(data=fore_data.mean(axis=1), index=fore_data.index, name='Forecast ' + variable_name + ': average')

# Compute errors
det_error = hist_data-fore_avg
det_error.name = 'Deterministic error for ' + variable_name
ens_error = -fore_data.sub(hist_data.values, axis=0)
ens_error.name = 'Ensemble error for ' + variable_name

# Change the ensembles
def deterministic_improve(data, forecast, k):
    return (1-k)*data + k*forecast
def ensemble_improve(data, forecast, k):
    new_ensemble = pd.DataFrame(data=None, index=forecast.index)
    for i in range(forecast.shape[1]):
        new_ensemble.insert(i, column=forecast.columns[i], value=(1-k)*hist_data.values+k*forecast.values[:,i])
    return new_ensemble

# Get forecast family (by 0.25), MAE, and PLOT
mae_family = pd.DataFrame(data=None, index=fore_avg.index)
for i in range(5):
    S = float(i)/4
    k = 1 - S
    mae_family.insert(i, column=str(S), value=deterministic_improve(hist_data, fore_avg, k).values)
fig = plt.figure(figsize=(16,6))
ax = fig.add_subplot(1,1,1)
ax.plot(hist_data,c='blue', linewidth=2, label='Historical data')
ax.plot(fore_avg,c='black', linewidth=2, label='Forecast data')
ax.plot(mae_family.index, mae_family.values[:, 1], linewidth=1, linestyle='dashed', c='red', label='Skill 0.25')
ax.plot(mae_family.index, mae_family.values[:, 2], linewidth=1, linestyle='dashdot', c='red', label='Skill 0.5')
ax.plot(mae_family.index, mae_family.values[:, 3], linewidth=1, linestyle='dotted', c='red', label='Skill 0.75')
#for i in np.arange(2,4):
#    ax.plot(mae_family.index, mae_family.values[:, 1], linewidth=1, c='red')
ax.set_xlim(mae_family.index[0], mae_family.index[31]) #[-1])
ax.set_xlabel('Date', size=18)
ax.set_ylabel('Temperature', size=18)
ax.set_title('Skill based on MAE', size=20)
ax.tick_params(labelsize=16)
ax.legend(prop={'size': 16})
fig.savefig('MAE.png')
fig.clf()

# Get forecast family (by 0.25) MSE

# Get forecast family (only for 0.5) CRPS
crps_family = pd.DataFrame(data=None, index=fore_avg.index)
S = 0.5
k = 1 - S
crps_family = ensemble_improve(hist_data, fore_data, k)
fig = plt.figure(figsize=(16,6))
ax = fig.add_subplot(1,1,1)
handles = []
h, = ax.plot(hist_data ,c='blue', linewidth=2, label='Historical data')
handles.append(h)
f, = ax.plot(fore_data.index, fore_data.values[:,0] ,c='black', linewidth=2, label='Forecast data')
handles.append(f)
s, = ax.plot(crps_family.index, crps_family.values[:,0], linewidth=1, c='red', label='Mixed ensemble, skill = 0.5')
handles.append(s)
ax.legend(handles=handles, prop={'size': 16})
ax.plot(fore_data,c='black', linewidth=2, label='Forecast data')
ax.plot(crps_family, linewidth=1, c='red', label='Mixed ensemble, skill = 0.5')
ax.plot(hist_data,c='blue', linewidth=2, label='Historical data')
ax.set_xlim(crps_family.index[0], crps_family.index[31]) #[-1])
ax.set_xlabel('Date', size=18)
ax.set_ylabel('Temperature', size=18)
ax.set_title('Skill based on CRPS', size=20)
ax.tick_params(labelsize=16)
#plt.show()
fig.savefig('CRPS.png')
fig.clf()