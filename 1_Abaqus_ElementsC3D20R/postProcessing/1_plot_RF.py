import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np
import os
import matplotlib as mpl

cm = 1 / 2.54

plt.rcParams.update({
    "figure.figsize": (14 * cm, 10 * cm),
    
    "text.usetex": True,
    "font.family": "monospace",
    
    "lines.linewidth": 1.5,
    "lines.markersize": 4,
    "errorbar.capsize": 2,
    
    "axes.labelsize": 15,
    "axes.titlesize": 18,
    "axes.linewidth": 0.8,
    
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 10,

    "legend.frameon": True,
    "legend.fontsize": 15,
    
    "grid.linestyle": "-",
    "grid.alpha": 0.3,
})

colors = plt.cm.viridis(np.linspace(0, 1, 6))
uibk_blue = "#003361"
uibk_orange = "#f39200"

figsize_single = (7, 5)
figsize_double = (8, 4)
figsize_doubleVert = (5, 6)

breite_Versuch = 80
breite_Modell = 4
scale = breite_Versuch / breite_Modell

current_dir = os.path.dirname(os.path.abspath(__file__))
last_entry = os.path.basename(current_dir)

data = np.loadtxt("RF.txt", skiprows=1)

ods_path = os.path.join(current_dir, "0_VA1_EBT6cm.ods")
df_exp = pd.read_excel(ods_path, engine="odf", sheet_name=0, header=None, skiprows=2)

fig, ax = plt.subplots()

ax.set_xlabel("Displacement [mm]")
ax.set_ylabel("Reaction Force")

ax.plot(df_exp[0], df_exp[1] * 1000, color="gray", linestyle="--", label="Versuche")
ax.plot(df_exp[2], df_exp[3] * 1000, color="gray", linestyle="--")         
ax.plot(df_exp[4], df_exp[5] * 1000, color="gray", linestyle="--")             

ax.plot(data[:, 0], data[:, 1] * scale, label="Simulation", color=uibk_orange)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x/1000:.2f} kN"))

ax.grid()

max_x_sim = np.max(data[:, 0]) if data.size > 0 else 0
max_x_exp = max(df_exp[0].max(), df_exp[2].max(), df_exp[4].max())
ax.set_xlim(0, max(max_x_sim, max_x_exp))

ax.legend()

plt.title(r"\textbf{ED 6 cm Direct Contact}")

fig.tight_layout()

cwd = os.getcwd()
fn = "RF.pdf"
fig.savefig(os.path.join(cwd, fn), format="pdf", transparent=False)

plt.show()