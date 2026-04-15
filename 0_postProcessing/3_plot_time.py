import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "Performance_Comparison.txt")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Computation_Time.png")

NAME_MAPPING = {
    "1_Abaqus_Penalty1e5_dt05_ElementsC3D20R": "Abaqus (C3D20R)",
    "1_MOOSE_Penalty1e5_dt05_ElementsC3D20R":  "MOOSE (C3D20R)",
    "2_Abaqus_Penalty1e5_dt05_ElementsC3D8":   "Abaqus (C3D8)",
    "2_MOOSE_Penalty1e5_dt05_ElementsC3D8":    "MOOSE (C3D8)",
    "3_Abaqus_Penalty1e5_dt05_ElementsC3D20":  "Abaqus (C3D20)",
    "3_MOOSE_Penalty1e5_dt05_ElementsC3D20":   "MOOSE (C3D20)",
}

PLOT_TITLE = "Comparison Simulation Time"
X_LABEL = "Wallclock Time"

uibk_blue = "#003361"
uibk_orange = "#f39200"

CM_TO_INCH = 1 / 2.54
PLOT_SETTINGS = {
    "figure.figsize": (20 * CM_TO_INCH, 12 * CM_TO_INCH),
    "text.usetex": False, 
    "font.family": "monospace",
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "legend.frameon": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
}

def format_time(seconds_total):
    minutes = int(seconds_total // 60)
    seconds = int(seconds_total % 60)
    
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds_total:.1f}s"

def time_formatter_axis(x, pos):
    return format_time(x)

def load_data(filepath):
    sim_names = []
    times = []
    
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for line in lines[4:]:
        if not line.strip() or "---" in line:
            continue
            
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            name = parts[0]
            time_str = parts[3]
            
            try:
                time_val = float(time_str)
                sim_names.append(name)
                times.append(time_val)
            except ValueError:
                pass
                
    return sim_names, times

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Fehler: Datei {INPUT_FILE} nicht gefunden.")
        return

    raw_sim_names, times = load_data(INPUT_FILE)
    
    if not raw_sim_names:
        print("Keine validen Daten zum Plotten gefunden.")
        return

    plt.rcParams.update(PLOT_SETTINGS)
    fig, ax = plt.subplots()

    colors = [uibk_blue if "Abaqus" in name else uibk_orange for name in raw_sim_names]

    display_names = []
    for name in raw_sim_names:
        if name in NAME_MAPPING:
            display_names.append(NAME_MAPPING[name])
        else:
            display_names.append(name)

    y_pos = np.arange(len(display_names))
    bars = ax.barh(y_pos, times, color=colors, height=0.6)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(display_names)
    ax.invert_yaxis()
    
    ax.set_xlabel(X_LABEL)
    ax.set_title(PLOT_TITLE, fontweight="bold")
    
    ax.set_xticklabels([]) 
    ax.tick_params(axis='x', length=0)
    ax.grid(axis='x')                  

    max_time = max(times)
    for bar in bars:
        width = bar.get_width()
        
        time_text = format_time(width)
        
        ax.text(width + (max_time * 0.01), bar.get_y() + bar.get_height() / 2,
                time_text, 
                va='center', ha='left', fontsize=10)

    ax.set_xlim(0, max_time * 1.15)

    import matplotlib.patches as mpatches
    patch_abaqus = mpatches.Patch(color=uibk_blue, label='Abaqus')
    patch_moose = mpatches.Patch(color=uibk_orange, label='MOOSE')

    fig.tight_layout()
    fig.savefig(OUTPUT_FILE, format="png", dpi=600)
    print(f"\nBalkendiagramm (in Minuten/Sekunden) gespeichert unter: {OUTPUT_FILE}")
    
    plt.show()

if __name__ == "__main__":
    main()