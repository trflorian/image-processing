import os

import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# data loading
timing = np.loadtxt("timing.txt")

# plot setup
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 5))

# plot timing
sns.barplot(x=timing[:, 0].astype(int), y=timing[:, 1])

# add cpu core annotation
cpu_cores = os.process_cpu_count()
plt.vlines(cpu_cores - 1, 0, 8, label="CPU cores", linestyles="--", color="r")
plt.text(cpu_cores - 1.9, 5, "CPU cores", color="r", rotation=90)

plt.xlabel("Num workers")
plt.ylabel("Time for 1000 iterations [s]")

plt.tight_layout()
plt.savefig("timing.png")
