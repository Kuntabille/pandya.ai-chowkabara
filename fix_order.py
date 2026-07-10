import json

# 1. Fix canvas.json
with open('canvas.json', 'r') as f:
    canvas = json.load(f)

# Swap 5x5 p2 and p3
paths_5x5 = canvas['board']['paths']
p2_5x5_idx = next(i for i, p in enumerate(paths_5x5) if p['id'] == 'p2_path')
p3_5x5_idx = next(i for i, p in enumerate(paths_5x5) if p['id'] == 'p3_path')

temp_coords = paths_5x5[p2_5x5_idx]['coordinates']
paths_5x5[p2_5x5_idx]['coordinates'] = paths_5x5[p3_5x5_idx]['coordinates']
paths_5x5[p3_5x5_idx]['coordinates'] = temp_coords

# Swap 7x7 p2 and p3
var_7x7 = next(v for v in canvas['variations'] if v['id'] == '7x7')
paths_7x7 = var_7x7['board']['paths']
p2_7x7_idx = next(i for i, p in enumerate(paths_7x7) if p['id'] == 'p2_path')
p3_7x7_idx = next(i for i, p in enumerate(paths_7x7) if p['id'] == 'p3_path')

temp_coords_7 = paths_7x7[p2_7x7_idx]['coordinates']
paths_7x7[p2_7x7_idx]['coordinates'] = paths_7x7[p3_7x7_idx]['coordinates']
paths_7x7[p3_7x7_idx]['coordinates'] = temp_coords_7

with open('canvas.json', 'w') as f:
    json.dump(canvas, f, separators=(',', ':'))

# 2. Fix logic.lua
with open('logic.lua', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].startswith('local p2_path_5x5'):
        lines[i] = lines[i].replace('p2_path_5x5', 'TEMP_PATH')
    elif lines[i].startswith('local p3_path_5x5'):
        lines[i] = lines[i].replace('p3_path_5x5', 'p2_path_5x5')
        
for i in range(len(lines)):
    if lines[i].startswith('local TEMP_PATH'):
        lines[i] = lines[i].replace('TEMP_PATH', 'p3_path_5x5')

for i in range(len(lines)):
    if lines[i].startswith('local p2_path_7x7'):
        lines[i] = lines[i].replace('p2_path_7x7', 'TEMP_PATH')
    elif lines[i].startswith('local p3_path_7x7'):
        lines[i] = lines[i].replace('p3_path_7x7', 'p2_path_7x7')
        
for i in range(len(lines)):
    if lines[i].startswith('local TEMP_PATH'):
        lines[i] = lines[i].replace('TEMP_PATH', 'p3_path_7x7')

with open('logic.lua', 'w') as f:
    f.writelines(lines)
