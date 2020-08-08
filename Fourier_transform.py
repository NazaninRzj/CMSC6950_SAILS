import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from sails import FourierMvarMetrics, OLSLinearModel
style.use('ggplot')

# Read & prep data
df = pd.read_csv('911.csv', header=0, index_col=0)

df = df.rename(columns = {k:k.lower() for k in df.columns})
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['timestamp_trunc'] = df['timestamp'].dt.floor('H')
df['N'] = 1

# Count calls per hour
counts = df.groupby(['timestamp_trunc']).sum()
counts = counts[['N']]

# Create time & signal, filling in missing hours with 0 calls
counts_dict = counts['N'].to_dict()
time = pd.date_range(min(counts.index), max(counts.index), freq = 'H').to_series().sort_values()
signal = time.apply(lambda x: counts_dict[x] if x in counts_dict.keys() else 0)

# Set signal to be the difference of call volume from the average
signal = signal - signal.mean()

#convert signal to numpy array
signal_array = signal.to_numpy()
signal_array = np.asarray(signal_array).reshape(1, signal_array.shape[0],1)

delay_vect = np.arange(10)

#use the SAIL package - Fourier transfer
model = OLSLinearModel.fit_model(signal_array, delay_vect)
freq_vect = np.linspace(0,6)
sample_rate = 10
F = FourierMvarMetrics.initialise(model, sample_rate, freq_vect)
F_H = F.H

## Plot signal in the time domain
plt.plot(freq_vect, np.abs(F_H).squeeze())
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.savefig('fourier.pdf')
