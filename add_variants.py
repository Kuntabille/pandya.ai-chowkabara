import json

with open("canvas.json", "r") as f:
    data = json.load(f)

data["variants"] = [
    {
        "id": "5x5",
        "name": "5x5 (Default)"
    },
    {
        "id": "7x7",
        "name": "7x7 (6 Pieces)"
    }
]

with open("canvas.json", "w") as f:
    json.dump(data, f, indent=2)

