import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import ticker

BREITE_VERSUCH = 80
BREITE_MODELL = 4
SCALE_SIM = BREITE_VERSUCH / BREITE_MODELL

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
ODS_FILE = os.path.join(SCRIPT_DIR, "0_VA1_EBT6cm.ods")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "RF_Combined.png")

PLOT_TITLE = "Dejori, ED 6cm"
X_LABEL = "Displacement (mm)"
Y_LABEL = "Reaction Force (kN)"
X_MAX = 1.0

CM_TO_INCH = 1 / 2.54
PLOT_SETTINGS = {
    "figure.figsize": (20 * CM_TO_INCH, 10 * CM_TO_INCH),
    "text.usetex": False,
    "font.family": "monospace",
    "lines.linewidth": 1.5,
    "lines.markersize": 4,
    "axes.labelsize": 15,
    "axes.titlesize": 18,
    "axes.linewidth": 0.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 10,
    "legend.frameon": True,
    "legend.fontsize": 12,
    "grid.linestyle": "-",
    "grid.alpha": 0.3,
}

EXP_COLOR = "gray"
EXP_LINESTYLE = "--"
EXP_LABEL = "Experiments Dejori"

uibk_blue = "#003361"
uibk_orange = "#f39200"

SIM_CONFIG = {
    "1_Abaqus": {"label": "Abaqus (C3D20R)", "color": uibk_blue,   "linestyle": "-"},
    "1_MOOSE":  {"label": "MOOSE (C3D20R)",  "color": uibk_orange, "linestyle": "-"},
    
    "2_Abaqus": {"label": "Abaqus (C3D8)",   "color": uibk_blue,   "linestyle": "--"},
    "2_MOOSE":  {"label": "MOOSE (C3D8)",    "color": uibk_orange, "linestyle": "--"},
    
    "3_Abaqus": {"label": "Abaqus (C3D20)",  "color": uibk_blue,   "linestyle": ":"},
    "3_MOOSE":  {"label": "MOOSE (C3D20)",   "color": uibk_orange, "linestyle": ":"},
}

def main():
    plt.rcParams.update(PLOT_SETTINGS)
    fig, ax = plt.subplots()

    max_x_exp = 0
    max_x_sim = 0

    if os.path.exists(ODS_FILE):
        try:
            df_exp = pd.read_excel(ODS_FILE, engine="odf", sheet_name=0, header=None, skiprows=2)
            
            ax.plot(df_exp[0], df_exp[1] * 1000, color=EXP_COLOR, linestyle=EXP_LINESTYLE, label=EXP_LABEL)
            ax.plot(df_exp[2], df_exp[3] * 1000, color=EXP_COLOR, linestyle=EXP_LINESTYLE)
            ax.plot(df_exp[4], df_exp[5] * 1000, color=EXP_COLOR, linestyle=EXP_LINESTYLE)
            
            max_x_exp = max(df_exp[0].max(), df_exp[2].max(), df_exp[4].max())
            print(f"Erfolg: Versuchsdaten aus {os.path.basename(ODS_FILE)} geladen.")
        except Exception as e:
            print(f"Fehler beim Laden der ODS Datei: {e}")
    else:
        print(f"Warnung: ODS Datei {ODS_FILE} nicht gefunden.")

    for folder_name in sorted(os.listdir(PARENT_DIR)):
        folder_path = os.path.join(PARENT_DIR, folder_name)
        
        if not os.path.isdir(folder_path):
            continue

        for key, config in SIM_CONFIG.items():
            if folder_name.startswith(key):
                rf_path = os.path.join(folder_path, "postProcessing", "RF.txt")
                
                if os.path.exists(rf_path):
                    try:
                        data = np.loadtxt(rf_path, skiprows=1)
                        if data.size > 0:
                            ax.plot(
                                data[:, 0], 
                                data[:, 1] * SCALE_SIM, 
                                label=config["label"], 
                                color=config["color"], 
                                linestyle=config["linestyle"]
                            )
                            current_max_x = np.max(data[:, 0])
                            if current_max_x > max_x_sim:
                                max_x_sim = current_max_x
                            print(f"Erfolg: {key} geladen aus {folder_name}")
                    except Exception as e:
                        print(f"Fehler beim Laden von {rf_path}: {e}")
                else:
                    print(f"Warnung: Keine RF.txt in {folder_name}/postProcessing/ gefunden.")
                
                break 

    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(Y_LABEL)
    ax.set_title(PLOT_TITLE, fontweight="bold")

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x/1000:.2f}"))
    ax.grid()

    ax.set_xlim(0, X_MAX)

    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left') # Setzt die Legende leicht nach außen, falls Platz fehlt

    fig.tight_layout()
    fig.savefig(OUTPUT_FILE, format="png", dpi=600, transparent=False)
    print(f"\nPlot erfolgreich gespeichert unter: {OUTPUT_FILE}")
    
    plt.show()

if __name__ == "__main__":
    main()