from odbAccess import *
import sys
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

odb_file = None
for file in os.listdir(parent_dir):
    if file.endswith(".odb"):
        odb_file = os.path.join(parent_dir, file)
        break

if not odb_file:
    print("Fehler: Keine .odb-Datei im übergeordneten Verzeichnis gefunden.")
    sys.exit()

odb = openOdb(odb_file)

stepid = "displacement"
keys = []

keys.append(
    {
        "foutid": "U",
        "foutidx": 1, 
        "partid": "anchor-1".upper(),
        "nsetid": "displacement_anchor".upper(),
        "average": True, 
        "arrayidx": 0,
    }
) 

keys.append(
    {
        "foutid": "RF",
        "foutidx": 1,
        "partid": "anchor-1".upper(),
        "nsetid": "load".upper(),
        "arrayidx": 1,
    }
)

for key in keys:
    if "partid" in key.keys():
        # for Part-Set:
        key.update(
            {"nset": odb.rootAssembly.instances[key["partid"]].nodeSets[key["nsetid"]]}
        )
    else:
        # for Assembly-Set:
        key.update({"nset": odb.rootAssembly.nodeSets[key["nsetid"]]})

output = np.array([])
output.shape = (0, len(keys))
for frame in odb.steps[stepid].frames:
    vals = np.zeros((1, len(keys)))
    for key in keys:
        fieldOutput = frame.fieldOutputs[key["foutid"]].getSubset(region=key["nset"])
        
        if "nidxinset" in key.keys():
            node = fieldOutput.values[key["nidxinset"]]
            vals[0][key["arrayidx"]] = node.data[key["foutidx"]]
            
        elif key.get("average", False):
            sum_val = 0.0
            num_nodes = len(fieldOutput.values)
            for node in fieldOutput.values:
                sum_val += node.data[key["foutidx"]]
            vals[0][key["arrayidx"]] = sum_val / num_nodes if num_nodes > 0 else 0.0
            
        else:
            for node in fieldOutput.values:
                vals[0][key["arrayidx"]] += node.data[key["foutidx"]]
                
    output = np.concatenate((output, vals))

header_list = [None] * len(keys)
for key in keys:
    header_list[key["arrayidx"]] = key["foutid"] + str(key["foutidx"] + 1)

header = " ".join(header_list) + "\n"

output_path = os.path.join(script_dir, "RF.txt")

with open(output_path, "w") as f:
    f.write(header)
    np.savetxt(f, output)