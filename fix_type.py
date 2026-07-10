import json

with open("canvas.json", "r") as f:
    data = json.load(f)

for v in data.get("variations", []):
    if "board" in v:
        v["board"]["type"] = "BOARD_TYPE_GRID"
        
with open("canvas.json", "w") as f:
    json.dump(data, f, separators=(',', ':'))

with open("logic.lua", "r") as f:
    logic = f.read()

import sys
sys.stdout.write("Fix done")
