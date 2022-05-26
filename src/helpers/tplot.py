import os

import matplotlib.pyplot as plt
import pandas as pd

value1 = [10, 20, 30, 40, 50]
value2 = [5, 10, 15, 20, 25]
value3 = [8, 9, 10, 15, 20]

data = pd.read_csv(os.environ.get("BUNDES_CSV_PATH"))
data = data.set_index('Nac').transpose()
data.plot()

plt.legend(loc='upper left')
plt.xlabel("Temporadas")
plt.ylabel("Nro de jugadores")

plt.savefig('presencia_Bundes.png')
