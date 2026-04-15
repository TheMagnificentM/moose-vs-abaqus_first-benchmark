import os
import glob
import re
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Performance_Comparison.txt")

MOOSE_COL_ITERATIONS = "sum_nonlinear_iterations"
MOOSE_COL_INCREMENTS = "total_increments" 
MOOSE_COL_TIME       = "simulation_time"

ALLOWED_PREFIXES = ["1_", "2_", "3_"]

def get_abaqus_data(msg_path):
    increments = "N/A"
    iterations = "N/A"
    wallclock_time = "N/A"
    
    with open(msg_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    regex_inc = re.compile(r"TOTAL OF\s+(\d+)\s+INCREMENTS")
    regex_iter = re.compile(r"^\s+(\d+)\s+ITERATIONS\s", re.IGNORECASE)
    regex_time = re.compile(r"WALLCLOCK TIME\s*\(SEC\)\s*=\s*([0-9\.]+)")
    
    for line in reversed(lines):
        if increments == "N/A":
            match_inc = regex_inc.search(line)
            if match_inc:
                increments = match_inc.group(1)
                
        if iterations == "N/A":
            match_iter = regex_iter.search(line)
            if match_iter:
                iterations = match_iter.group(1)
                
        if wallclock_time == "N/A":
            match_time = regex_time.search(line)
            if match_time:
                wallclock_time = match_time.group(1)
                
        if increments != "N/A" and iterations != "N/A" and wallclock_time != "N/A":
            break
            
    return increments, iterations, wallclock_time

def get_moose_data(csv_path):
    increments = "N/A"
    iterations = "N/A"
    wallclock_time = "N/A"
    
    try:
        df = pd.read_csv(csv_path)
        if not df.empty:
            last_row = df.iloc[-1]
            
            if MOOSE_COL_INCREMENTS in df.columns:
                increments = str(int(last_row[MOOSE_COL_INCREMENTS]))
            elif "time_step" in df.columns: 
                increments = str(int(last_row["time_step"]))
                
            if MOOSE_COL_ITERATIONS in df.columns:
                iterations = str(int(last_row[MOOSE_COL_ITERATIONS]))
                
            if MOOSE_COL_TIME in df.columns:
                wallclock_time = f"{float(last_row[MOOSE_COL_TIME]):.2f}"
            elif "wall_time" in df.columns:
                wallclock_time = f"{float(last_row['wall_time']):.2f}"
                
    except Exception as e:
        print(f"Fehler beim Lesen der MOOSE CSV {csv_path}: {e}")
        
    return increments, iterations, wallclock_time

def main():
    results = []
    
    for folder_name in sorted(os.listdir(PARENT_DIR)):
        folder_path = os.path.join(PARENT_DIR, folder_name)
        
        if not os.path.isdir(folder_path) or folder_name == os.path.basename(SCRIPT_DIR):
            continue
            
        if not any(folder_name.startswith(prefix) for prefix in ALLOWED_PREFIXES):
            continue

        data = None
        
        if "Abaqus" in folder_name:
            msg_files = glob.glob(os.path.join(folder_path, "*.msg"))
            if msg_files:
                inc, iter_count, time = get_abaqus_data(msg_files[0])
                data = {"Simulation": folder_name, "Increments": inc, "Iterations": iter_count, "Time_s": time}
            else:
                data = {"Simulation": folder_name, "Increments": "Fehlt", "Iterations": "Fehlt", "Time_s": "Fehlt"}
                print(f"Warnung: Keine .msg Datei in {folder_name} gefunden.")
                
        elif "MOOSE" in folder_name:
            csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
            if csv_files:
                csv_files.sort(key=lambda x: len(x)) 
                inc, iter_count, time = get_moose_data(csv_files[0])
                data = {"Simulation": folder_name, "Increments": inc, "Iterations": iter_count, "Time_s": time}
            else:
                data = {"Simulation": folder_name, "Increments": "Fehlt", "Iterations": "Fehlt", "Time_s": "Fehlt"}
                print(f"Warnung: Keine .csv Datei in {folder_name} gefunden.")
                
        if data:
            results.append(data)

    if not results:
        print("Keine Simulationsdaten für die angegebenen Ordner gefunden.")
        return
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        header = f"{'Simulation Name':<40} | {'Increments':<12} | {'Iterations':<12} | {'Wallclock Time (s)':<20}"
        separator = "-" * len(header)
        
        f.write("SIMULATION PERFORMANCE COMPARISON\n")
        f.write("=" * len(header) + "\n")
        f.write(header + "\n")
        f.write(separator + "\n")
        
        for res in results:
            line = f"{res['Simulation']:<40} | {res['Increments']:<12} | {res['Iterations']:<12} | {res['Time_s']:<20}"
            f.write(line + "\n")
            
    print(f"\nErfolg: Performance-Tabelle wurde erstellt unter:")
    print(OUTPUT_FILE)

if __name__ == "__main__":
    main()