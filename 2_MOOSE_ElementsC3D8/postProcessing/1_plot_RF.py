import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np
import os

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

uibk_blue = "#003361"
uibk_orange = "#f39200"

breite_Versuch = 80
breite_Modell = 4
scale = breite_Versuch / breite_Modell

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

csv_filename = "POT_Dejori_implicit_dynamic_C3D20R_out.csv"
csv_path = os.path.join(parent_dir, csv_filename)

if not os.path.exists(csv_path):
    print(f"Fehler: Die Datei '{csv_path}' wurde nicht gefunden.")
    exit()

data = np.genfromtxt(csv_path, delimiter=',', names=True)

erwartete_spalten = ['displacement_u_y', 'load_rf_y']
vorhandene_spalten = data.dtype.names

for spalte in erwartete_spalten:
    if spalte not in vorhandene_spalten:
        print(f"Fehler: Die Spalte '{spalte}' fehlt in der CSV. Vorhanden: {vorhandene_spalten}")
        exit()

displacement = data['displacement_u_y']
reaction_force = data['load_rf_y']

txt_fn = "RF.txt"
txt_path = os.path.join(script_dir, txt_fn)

export_data = np.column_stack((displacement, reaction_force))

np.savetxt(txt_path, export_data, 
           header="U2 RF2", 
           fmt="%.6f", 
           comments="", 
           delimiter=" ")

print(f"Daten erfolgreich in '{txt_path}' gespeichert.")

ods_path = os.path.join(script_dir, "0_VA1_EBT6cm.ods")
if os.path.exists(ods_path):
    df_exp = pd.read_excel(ods_path, engine="odf", sheet_name=0, header=None, skiprows=2)
else:
    print(f"Warnung: Die Datei '{ods_path}' wurde nicht gefunden. Versuchsdaten werden nicht geplottet.")
    df_exp = None

fig, ax = plt.subplots()

ax.set_xlabel("Displacement [mm]")
ax.set_ylabel("Reaction Force")

if df_exp is not None:
    ax.plot(df_exp[0], df_exp[1] * 1000, color="gray", linestyle="--", label="Versuche")
    ax.plot(df_exp[2], df_exp[3] * 1000, color="gray", linestyle="--")
    ax.plot(df_exp[4], df_exp[5] * 1000, color="gray", linestyle="--")

ax.plot(displacement, reaction_force * scale, label="Simulation", color=uibk_orange)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x/1000:.2f} kN"))

ax.grid()

max_x_sim = np.max(displacement) if len(displacement) > 0 else 0
if df_exp is not None:
    max_x_exp = max(df_exp[0].max(), df_exp[2].max(), df_exp[4].max())
    ax.set_xlim(0, max(max_x_sim, max_x_exp))
else:
    ax.set_xlim(0, max_x_sim)

ax.legend()
plt.title(r"\textbf{ED 6 cm Direct Contact}")
fig.tight_layout()

fn = "RF.pdf"
fig.savefig(os.path.join(script_dir, fn), format="pdf", transparent=False)

plt.show()