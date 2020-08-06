
'''We will be using some data from a single MEG Virtual Electrode reconstruction.
   We start with some necessary libraries and finding the location of the data'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from os.path import join
from sails import find_example_path, VieiraMorfLinearModel, FourierMvarMetrics, ModalMvarMetrics
import h5py

style.use('bmh')


sample_rate = 2034.51 / 24

'''Nyquist frequency is half of the sampeling rate of a discrete signal processing system'''
nyq = sample_rate / 2.
freq_vect = np.linspace(0, nyq, 64)

'''If the git repository is in your home directory, this function
will then find the path.  If you wish to store the data in another
location, set the SAILS_EXAMPLE_DATA environment variable to
the location of the git checkout'''

# path = ('.../sails-example-data')

data_directory = find_example_path()

'''The data is stored as the dataset x
    (nsignals, nsamples, ntrials)
    (1, 30517, 1)
    We are performing a univariate analysis so we have one signal
    We have 30517 data points
    One trial'''

data = h5py.File(join(data_directory,'meg_occipital_ve.hdf5'), 'r')['X'][...]

'''Now we are going to set up a model by learning the parameters from data.
    Vieira-Morf algorithm is used to fit the model.
    And fit a model of order 19 using the delay_vect argument.'''

delay_vect = np.arange(20)
model = VieiraMorfLinearModel.fit_model(data, delay_vect)

diag = model.compute_diagnostics(data)

F = FourierMvarMetrics.initialise(model, sample_rate, freq_vect)
F_H = F.H

M = ModalMvarMetrics.initialise(model, sample_rate, freq_vect)
M_H  = M.modes.per_mode_transfer_function(sample_rate, freq_vect)

R_squares = []
orders = []

fig, ax1 = plt.subplots()

ax1.plot(freq_vect, np.abs(F_H).squeeze(), '*', color = 'r')
ax1.plot(freq_vect, np.abs(M_H).squeeze())
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Frequency Response')
ax1.legend(['Fourier H', 'Modal H'])

plt.savefig('F_M.pdf')

ss = M.modes.pole_plot()
plt.savefig('Real_Imag.pdf')
