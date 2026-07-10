import json

with open("canvas.json", "r") as f:
    data = json.load(f)

def unfix_paths(paths):
    for path in paths:
        if "coordinates" in path:
            new_coords = []
            for c in path["coordinates"]:
                if isinstance(c, str):
                    parts = c.split(',')
                    if len(parts) == 2:
                        new_coords.append({"x": int(parts[0]), "y": int(parts[1])})
                    else:
                        new_coords.append(c)
                else:
                    new_coords.append(c)
            path["coordinates"] = new_coords

if "board" in data and "paths" in data["board"]:
    unfix_paths(data["board"]["paths"])

if "variations" in data:
    for v in data["variations"]:
        if "board" in v and "paths" in v["board"]:
            unfix_paths(v["board"]["paths"])

with open("canvas.json", "w") as f:
    json.dump(data, f, separators=(',', ':'))
