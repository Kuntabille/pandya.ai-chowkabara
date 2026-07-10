import json

with open("canvas.json", "r") as f:
    data = json.load(f)

def fix_paths(paths):
    for path in paths:
        if "coordinates" in path:
            new_coords = []
            for c in path["coordinates"]:
                if isinstance(c, dict) and "x" in c and "y" in c:
                    new_coords.append(f"{c['x']},{c['y']}")
                else:
                    new_coords.append(c)
            path["coordinates"] = new_coords

if "board" in data and "paths" in data["board"]:
    fix_paths(data["board"]["paths"])

if "variations" in data:
    for v in data["variations"]:
        if "board" in v and "paths" in v["board"]:
            fix_paths(v["board"]["paths"])

with open("canvas.json", "w") as f:
    json.dump(data, f, indent=2)
