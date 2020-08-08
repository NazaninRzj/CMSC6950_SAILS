import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
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

## Plot signal in the time domain
plt.figure(figsize=(10, 4))

ax1 = plt.subplot( 1, 2, 1 )
ax1.plot(time, signal, label='signal')
ax1.set_title('All Time')
ax1.set_ylabel( 'Signal' )
ax1.set_xlabel( 'Time' )
plt.xticks(rotation=90)

N = 24 * 7

ax2 = plt.subplot( 1, 2, 2 )
ax2.plot(time[:N], signal[:N])
ax2.set_title('First Week')
ax2.set_ylabel( 'Signal' )
ax2.set_xlabel( 'Time' )

plt.tight_layout()
plt.xticks(rotation=90)

plt.savefig('data.pdf')
