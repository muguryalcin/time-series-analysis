import torch
from dataloader import DataLoader
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def classical_decomposition(data, seasonal_period, style = 'add', show = True):
    
    data = DataLoader(data).to_tensor()#torch.clone(data).numpy()

    if data.ndim >= 1:

        data = np.squeeze(data)

    number_of_cycles = len(data) // seasonal_period

    # Computing the trend-cycle component using moving averages
    trend = pd.Series(data).rolling(seasonal_period,center=True).mean()

    if seasonal_period % 2 == 0:
        trend = trend.shift(-1).rolling(2).mean()
    
    # Detrending
    if style == 'add':
        detrended = data - trend.values
    elif style == 'mul':
        detrended = data / trend.values

    # Calculating the seasonal component
    seasonal = np.nanmean(data.reshape(number_of_cycles, seasonal_period).T, axis=1)

    # Normalizing seasonal averages
    seasonal -= np.mean(seasonal)
    # Putting seasonality component in a numpy array same length as the original data
    seasonal = np.array([seasonal[i%seasonal_period] 
                         for i in range(seasonal_period * number_of_cycles)])
    
    # Deseasoning (Calculating remainder)
    if style == 'add' :
        remainder = detrended - seasonal
    elif style == 'mul':
        remainder = detrended / seasonal

    if show:
        # Here plots of data, trend, seasonal and remainder will be drawn

        mpl.rcParams["figure.figsize"] = (12,8)
        fig, axes = plt.subplots(3, 1)
        ax1, ax2, ax3 = axes
            
        ax1.plot(range(len(trend)), trend)
        ax1.set_ylabel("Trend")

        ax2.plot(range(len(seasonal)), seasonal)
        ax2.set_ylabel("Seasonal")

        ax3.scatter(range(len(remainder)), remainder)
        ax3.set_ylabel("Remainder")

        plt.show()

    
    return trend, seasonal, remainder

