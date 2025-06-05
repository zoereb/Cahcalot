import matplotlib.pyplot as plt
import soundfile sf
import numpy as np

data, fs = sf.read('custom_source_acoustic_2d.wav')
t = np.linspace(0, len(data[:,0]), len(data[:,0]))/fs

fig, ax = plt.subplots(3)
ax[0].plot(t, data[:,0])
ax[0].set_title('avant junk')
ax[1].plot(t, data[:,1])
ax[1].set_title('arriere haut')
ax[2].plot(t, data[:,2])
ax[2].set_title(avant haut')

plt.tight_layout
plt.show()
