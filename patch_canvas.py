import json

with open("canvas.json", "r") as f:
    data = json.load(f)

# Update base paths
if "board" in data and "paths" in data["board"]:
    paths = data["board"]["paths"]
    new_paths = []
    for p in paths:
        if p["id"] == "p1_path":
            p["repeatPerPlayer"] = True
            new_paths.append(p)
    data["board"]["paths"] = new_paths

# Update variation paths
if "variations" in data:
    for var in data["variations"]:
        if "board" in var and "paths" in var["board"]:
            paths = var["board"]["paths"]
            new_paths = []
            for p in paths:
                if p["id"] == "p1_path":
                    p["repeatPerPlayer"] = True
                    new_paths.append(p)
            var["board"]["paths"] = new_paths

with open("canvas.json", "w") as f:
    json.dump(data, f, separators=(',', ':'))
